import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useTelegram } from '../shared/lib/useTelegram';
import apiClient from '../shared/api/client';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { TextField, Button, Paper, Typography, Box } from '@mui/material';

// Fix for default markers
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom beer icon
const beerIcon = L.divIcon({
  html: '🍺',
  className: 'beer-marker',
  iconSize: [30, 30],
  iconAnchor: [15, 30],
});

interface EventData {
  title: string;
  description: string;
  latitude: number;
  longitude: number;
  date_time: string | null;
  max_participants: string;
}

function LocationMarker({ position, setPosition }: { position: [number, number] | null; setPosition: (pos: [number, number]) => void }) {
  const map = useMapEvents({
    click(e) {
      setPosition([e.latlng.lat, e.latlng.lng]);
    },
  });

  return position === null ? null : (
    <Marker position={position} icon={beerIcon}>
      <Popup>Вы выбрали это место</Popup>
    </Marker>
  );
}

export const CreateEventPage: React.FC = () => {
  const { user } = useTelegram();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const editId = searchParams.get('edit');
  const isEditing = !!editId;

  const [eventData, setEventData] = useState<EventData>({
    title: '',
    description: '',
    latitude: 50.4501,
    longitude: 30.5234,
    date_time: null,
    max_participants: '',
  });
  const [position, setPosition] = useState<[number, number] | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<Array<{lat: number, lon: number, name: string}>>([]);

  const center: [number, number] = position ? position : [50.4501, 30.5234];

  useEffect(() => {
    if (isEditing && editId) {
      const loadEvent = async () => {
        try {
          console.log('Loading event with id:', editId);
          const response = await apiClient.get(`/events/${editId}`);
          const event = response.data;
          console.log('Loaded event:', event);
          setEventData({
            title: event.title,
            description: event.description,
            latitude: event.latitude,
            longitude: event.longitude,
            date_time: event.date_time,
            max_participants: event.max_participants.toString(),
          });
          setPosition([event.latitude, event.longitude]);
        } catch (error) {
          console.error('Error loading event:', error);
          alert('Ошибка загрузки события');
          navigate('/profile');
        }
      };
      loadEvent();
    }
  }, [isEditing, editId, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !position) {
      console.log('No user or position', { user, position });
      return;
    }

    setLoading(true);
    try {
      const data = { ...eventData, latitude: position[0], longitude: position[1], max_participants: parseInt(eventData.max_participants) || 1 };
      if (isEditing && editId) {
        console.log('Updating event', data);
        await apiClient.put(`/events/${editId}`, data);
        alert('Событие обновлено!');
        navigate('/profile');
      } else {
        console.log('Creating event', data);
        await apiClient.post('/events/', data, {
          params: { creator_id: user.id }
        });
        alert(`Событие создано! Максимум участников: ${parseInt(eventData.max_participants) || 1}`);
        setEventData({ title: '', description: '', latitude: 50.4501, longitude: 30.5234, date_time: null, max_participants: '' });
        setPosition(null);
        navigate('/');
      }
    } catch (error) {
      console.error('Error saving event', error);
      alert('Ошибка сохранения события');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery) return;
    const currentPos = position || [50.4501, 30.5234];
    const bbox = [currentPos[1] - 0.1, currentPos[0] - 0.1, currentPos[1] + 0.1, currentPos[0] + 0.1]; // lon min, lat min, lon max, lat max
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&viewbox=${bbox.join(',')}&bounded=1&limit=10`);
      const data = await response.json();
      console.log('Search results:', data);
      setSearchResults(data.map((item: any) => ({ lat: parseFloat(item.lat), lon: parseFloat(item.lon), name: item.display_name })));
      if (data.length > 0) {
        setPosition([parseFloat(data[0].lat), parseFloat(data[0].lon)]);
        setEventData({ ...eventData, latitude: parseFloat(data[0].lat), longitude: parseFloat(data[0].lon) });
      } else {
        alert('Место не найдено');
      }
    } catch (error) {
      console.error('Ошибка поиска:', error);
      alert('Ошибка поиска');
    }
  };

  return (
    <Box sx={{ padding: 2, maxWidth: 800, margin: '0 auto' }} className="page-container cozy-bg">
      <Box sx={{ textAlign: 'center', marginBottom: 3 }}>
        <div className="icon-large">🍻</div>
        <Typography variant="h1" component="h1" gutterBottom align="center" color="primary">
          {isEditing ? 'Редактировать событие' : 'Создать событие'}
        </Typography>
        <Typography variant="body1" className="welcome-text">
          {isEditing ? 'Обнови детали и собери больше друзей!' : 'Собери друзей, выбери место и создай незабываемую встречу!'}
        </Typography>
      </Box>
      <Box sx={{ padding: 3, borderRadius: 3, backgroundColor: 'rgba(50, 30, 10, 0.8)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255, 107, 53, 0.4)' }} className="fade-in">
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Название события"
            value={eventData.title}
            onChange={(e) => setEventData({ ...eventData, title: e.target.value })}
            required
            margin="normal"
            variant="outlined"
          />
          <TextField
            fullWidth
            label="Описание"
            value={eventData.description}
            onChange={(e) => setEventData({ ...eventData, description: e.target.value })}
            multiline
            minRows={3}
            maxRows={6}
            margin="normal"
            variant="outlined"
            placeholder="Расскажи о встрече: что будем делать, сколько человек, атмосфера... Например: 'Вечер пива и настолок в уютном баре!'"
          />
          <TextField
            fullWidth
            label="Дата и время начала"
            type="datetime-local"
            value={eventData.date_time || ''}
            onChange={(e) => setEventData({ ...eventData, date_time: e.target.value })}
            margin="normal"
            variant="outlined"
            InputLabelProps={{
              shrink: true,
            }}
          />
          <TextField
            fullWidth
            label="Максимум участников"
            type="number"
            value={eventData.max_participants}
            onChange={(e) => setEventData({ ...eventData, max_participants: e.target.value })}
            margin="normal"
            variant="outlined"
            inputProps={{ min: 1, max: 20 }}
            helperText="От 1 до 20 человек"
          />
          <Box sx={{ display: 'flex', alignItems: 'center', marginY: 2 }}>
            <TextField
              fullWidth
              label="Поиск места"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              variant="outlined"
              sx={{ marginRight: 1 }}
            />
            <Button variant="contained" color="secondary" onClick={handleSearch} sx={{ padding: '14px 16px', borderRadius: 2 }}>
              Найти
            </Button>
          </Box>
          <Typography variant="body1" gutterBottom>
            Выберите место на карте
          </Typography>
          <Box sx={{ height: 300, width: '100%', marginY: 2, borderRadius: 2, overflow: 'hidden' }}>
            <MapContainer center={center} zoom={10} style={{ height: '100%', width: '100%' }}>
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />
              <LocationMarker position={position} setPosition={setPosition} />
              {searchResults.map((result, index) => (
                <Marker key={index} position={[result.lat, result.lon]} icon={beerIcon} eventHandlers={{
                  click: () => {
                    setPosition([result.lat, result.lon]);
                    setEventData({ ...eventData, latitude: result.lat, longitude: result.lon });
                    setSearchResults([]);
                  }
                }}>
                  <Popup>{result.name}</Popup>
                </Marker>
              ))}
            </MapContainer>
          </Box>
          {position && (
            <Box sx={{ marginY: 2 }}>
              <Typography variant="body2">Широта: {position[0].toFixed(4)}</Typography>
              <Typography variant="body2">Долгота: {position[1].toFixed(4)}</Typography>
            </Box>
          )}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            disabled={loading || !position}
            sx={{ marginTop: 2, padding: 1.5, borderRadius: 2 }}
          >
            {loading ? (isEditing ? 'Обновление...' : 'Создание...') : (isEditing ? 'Обновить событие' : 'Создать событие')}
          </Button>
        </form>
      </Box>
    </Box>
  );
};