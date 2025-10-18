import React from 'react';
import { EventMap } from '../widgets/event-map/EventMap';
import { Box, Typography } from '@mui/material';
import { useFetchEvents } from '../features/fetch-events/useFetchEvents';

export const MapPage: React.FC = () => {
  const { events } = useFetchEvents();

  return (
    <Box sx={{ padding: 2, maxWidth: 1200, margin: '0 auto' }} className="page-container cozy-bg">
      <Box sx={{ textAlign: 'center', marginBottom: 3 }}>
        <div className="icon-large">🗺️</div>
        <Typography variant="h1" component="h1" gutterBottom align="center" color="primary">
          Карта событий
        </Typography>
        <Typography variant="body1" className="welcome-text">
          Найди ближайшие встречи и присоединяйся к компании! {events.length > 0 ? `Найдено ${events.length} событий.` : 'Пока нет событий, создай первое!'}
        </Typography>
      </Box>
      <Box sx={{ height: '50vh', width: '100%', borderRadius: 2, border: '1px solid rgba(255, 107, 53, 0.4)', overflow: 'hidden', boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)', marginBottom: 2 }} className="fade-in">
        <EventMap />
      </Box>
    </Box>
  );
};