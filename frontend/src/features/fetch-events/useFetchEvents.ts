import { useState, useEffect, useCallback } from 'react';
import apiClient from '../../shared/api/client';

interface Event {
  id: number;
  title: string;
  description?: string;
  latitude: number;
  longitude: number;
  creator_id: number;
  created_at: string;
}

export const useFetchEvents = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEvents = useCallback(async () => {
    setLoading(true);
    try {
      const response = await apiClient.get('/events/');
      setEvents(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch events');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEvents();
    // Temporarily disabled polling to reduce server load
    // const interval = setInterval(fetchEvents, 30000); // Poll every 30 seconds
    // return () => clearInterval(interval);
  }, [fetchEvents]);

  return { events, loading, error, refetch: fetchEvents };
};