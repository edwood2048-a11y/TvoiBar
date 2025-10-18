import React, { useState } from 'react';
import { useTelegram } from '../../shared/lib/useTelegram';
import apiClient from '../../shared/api/client';
import { Card, CardContent, Typography, Button, Chip, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import EventIcon from '@mui/icons-material/Event';

interface Event {
  id: number;
  title: string;
  description?: string;
  latitude: number;
  longitude: number;
  creator_id: number;
  created_at: string;
  current_participants: number;
  max_participants: number;
}

interface EventCardProps {
  event: Event;
}

export const EventCard: React.FC<EventCardProps> = ({ event }) => {
  const { user } = useTelegram();
  const [joined, setJoined] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [message, setMessage] = useState('');

  console.log('EventCard event:', event); // Для отладки

  const handleJoin = () => {
    setDialogOpen(true);
  };

  const handleConfirmJoin = async () => {
    if (!user) return;
    try {
      await apiClient.post(`/events/${event.id}/join`, null, {
        params: { user_id: user.id, message }
      });
      setJoined(true);
      setDialogOpen(false);
      setMessage('');
    } catch (error) {
      alert('Ошибка присоединения');
    }
  };

  return (
    <Card className="event-card fade-in" sx={{ margin: 2, borderRadius: 3 }}>
      <CardContent>
        <Typography variant="h5" component="h3" gutterBottom color="primary">
          <EventIcon sx={{ marginRight: 1, verticalAlign: 'middle' }} />
          {event.title}
        </Typography>
        <Typography variant="body1" paragraph>
          {event.description}
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ marginBottom: 2 }}>
          Участники: {event.current_participants || 0}/{event.max_participants || 10}
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ display: 'flex', alignItems: 'center', marginBottom: 2 }}>
          <LocationOnIcon sx={{ marginRight: 0.5 }} />
          Координаты: {event.latitude.toFixed(4)}, {event.longitude.toFixed(4)}
        </Typography>
        {!joined ? (
          event.current_participants >= event.max_participants ? (
            <Button variant="contained" color="secondary" disabled fullWidth>
              Места заняты
            </Button>
          ) : (
            <Button variant="contained" color="primary" onClick={handleJoin} fullWidth sx={{ '&:hover': { backgroundColor: 'primary.dark' } }}>
              Присоединиться
            </Button>
          )
        ) : (
          <Chip label="Вы присоединились!" color="success" variant="outlined" />
        )}
      </CardContent>
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>Присоединиться к событию</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Сообщение (опционально)"
            fullWidth
            variant="outlined"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Расскажите, почему хотите присоединиться..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Отмена</Button>
          <Button onClick={handleConfirmJoin} variant="contained">Присоединиться</Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};