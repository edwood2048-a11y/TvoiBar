import React, { useState } from 'react';
import { useFetchEvents } from '../../features/fetch-events/useFetchEvents';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Typography, Box, CircularProgress, Card, CardContent, Button, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import LocationOnIcon from '@mui/icons-material/LocationOn';

// Fix for default markers in react-leaflet
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

// Cluster icon
const createClusterCustomIcon = (cluster: any) => {
  return L.divIcon({
    html: `<span>${cluster.getChildCount()}</span>`,
    className: 'marker-cluster-custom',
    iconSize: L.point(40, 40, true),
  });
};

export const EventMap: React.FC = () => {
  const { events, loading, error, refetch } = useFetchEvents();
  const [selectedEvent, setSelectedEvent] = useState<any>(null);

  if (loading) return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <CircularProgress />
      <Typography variant="body1" sx={{ marginLeft: 2 }}>Загрузка событий...</Typography>
    </Box>
  );
  if (error) return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h6" color="error">Ошибка: {error}</Typography>
    </Box>
  );

  const center: [number, number] = events.length > 0 ? [events[0].latitude, events[0].longitude] : [50.4501, 30.5234]; // Default to Kyiv

  return (
    <Box sx={{ height: '100%', width: '100%', position: 'relative' }}>
      <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {events.map(event => (
          <Marker
            key={event.id}
            position={[event.latitude, event.longitude]}
            icon={beerIcon}
            eventHandlers={{
              click: () => setSelectedEvent(event),
            }}
          />
        ))}
      </MapContainer>
      {selectedEvent && (
        <Card
          sx={{
            position: 'absolute',
            bottom: 80,
            left: 10,
            right: 10,
            height: '60%',
            zIndex: 1000,
            overflow: 'hidden',
          }}
        >
          <CardContent sx={{ height: '100%', overflowY: 'auto' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h2">{selectedEvent.title}</Typography>
              <IconButton onClick={() => setSelectedEvent(null)}>
                <CloseIcon />
              </IconButton>
            </Box>
            <Typography variant="body1" sx={{ marginY: 2 }}>{selectedEvent.description}</Typography>
            <Typography variant="body2" color="textSecondary" sx={{ marginY: 1 }}>
              Участники: {selectedEvent.current_participants || 0}/{selectedEvent.max_participants || 10}
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', marginY: 1 }}>
              <CalendarTodayIcon sx={{ marginRight: 1 }} />
              <Typography variant="body1">
                {selectedEvent.date_time ? `Начало: ${new Date(selectedEvent.date_time).toLocaleString()}` : `Создано: ${new Date(selectedEvent.created_at).toLocaleString()}`}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', marginY: 1 }}>
              <LocationOnIcon sx={{ marginRight: 1 }} />
              <Typography variant="body1">Адрес: {selectedEvent.latitude.toFixed(4)}, {selectedEvent.longitude.toFixed(4)}</Typography>
            </Box>
            <Button variant="contained" color="primary" fullWidth>
              Присоединиться
            </Button>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};