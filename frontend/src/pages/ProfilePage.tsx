import React, { useState, useEffect, useMemo } from 'react';
import { useTelegram } from '../shared/lib/useTelegram';
import { Paper, Typography, Avatar, Box, List, ListItem, ListItemText, Button, Divider, Card, CardContent, IconButton, TextField, Snackbar, Alert } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import { useFetchEvents } from '../features/fetch-events/useFetchEvents';
import apiClient from '../shared/api/client';
import { useNavigate } from 'react-router-dom';

export const ProfilePage: React.FC = () => {
  const { user } = useTelegram();
  const { events, loading, error, refetch } = useFetchEvents();
  const navigate = useNavigate();
  const [participants, setParticipants] = useState<any[]>([]);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [userParticipations, setUserParticipations] = useState<any[]>([]);
  const [editingProfile, setEditingProfile] = useState(false);
  const [trustedContact, setTrustedContact] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [activeCheckIn, setActiveCheckIn] = useState<any>(null);
  const [photoFile, setPhotoFile] = useState<File | null>(null);

  const userEvents = useMemo(() => events.filter(event => event.creator_id === user?.id), [events.length, user?.id]);

  useEffect(() => {
    const fetchUser = async () => {
      if (user?.id) {
        try {
          const response = await apiClient.get(`/users/${user.id}`);
          setCurrentUser(response.data);
          setTrustedContact(response.data.trusted_contact || '');
        } catch (error: any) {
          if (error.response?.status === 404) {
            // User not found, create
            try {
              const createData = {
                telegram_id: user.id,
                username: user.username,
                first_name: user.first_name,
                last_name: user.last_name,
              };
              const createResponse = await apiClient.post('/users/', createData);
              setCurrentUser(createResponse.data);
            } catch (createError) {
              console.error('Error creating user');
            }
          } else {
            console.error('Error fetching user');
          }
        }
      }
    };
    fetchUser();

    const fetchParticipants = async () => {
      const userEvents = events.filter(event => event.creator_id === user?.id);
      if (!userEvents.length) return;
      const allParts: any[] = [];
      for (const event of userEvents) {
        try {
          const response = await apiClient.get(`/events/${event.id}/participants`);
          allParts.push(...response.data.map((p: any) => ({ ...p, eventTitle: event.title })));
        } catch (error) {
          console.error('Error fetching participants for event', event.id);
        }
      }
      setParticipants(allParts);
    };
    fetchParticipants();

    const fetchUserParticipations = async () => {
      if (user?.id) {
        try {
          const response = await apiClient.get(`/users/${user.id}/participants`);
          setUserParticipations(response.data);
        } catch (error) {
          console.error('Error fetching user participations');
        }
      }
    };
    fetchUserParticipations();
  }, [events, user?.id]);

  useEffect(() => {
    const fetchActiveCheckIn = async () => {
      if (user?.id) {
        try {
          const response = await apiClient.get(`/users/${user.id}/participants`);
          const active = response.data.find((p: any) => p.meeting_status === 'in_progress');
          setActiveCheckIn(active || null);
        } catch (error) {
          console.error('Error fetching participants:', error);
        }
      }
    };
    fetchActiveCheckIn();
  }, [user?.id]);

  const handleDelete = async (eventId: number) => {
    if (!confirm('Удалить событие?')) return;
    try {
      await apiClient.delete(`/events/${eventId}`);
      refetch();
    } catch (error) {
      alert('Ошибка удаления');
    }
  };

  const handleEdit = (eventId: number) => {
    navigate(`/create?edit=${eventId}`);
  };

  const handleAccept = async (participantId: number) => {
    try {
      await apiClient.put(`/participants/${participantId}/accept`);
      setParticipants(prev => prev.map(p => p.id === participantId ? { ...p, status: 'accepted' } : p));
    } catch (error) {
      alert('Ошибка принятия');
    }
  };

  const handleReject = async (participantId: number) => {
    try {
      await apiClient.put(`/participants/${participantId}/reject`);
      setParticipants(prev => prev.map(p => p.id === participantId ? { ...p, status: 'rejected' } : p));
    } catch (error) {
      alert('Ошибка отклонения');
    }
  };

  const handleStartMeeting = async (participantId: number) => {
    try {
      await apiClient.put(`/participants/${participantId}/meeting_status?meeting_status=in_progress`);
      setParticipants(prev => prev.map(p => p.id === participantId ? { ...p, meeting_status: 'in_progress' } : p));
    } catch (error) {
      alert('Ошибка запуска встречи');
    }
  };

  const handleEndMeeting = async (participantId: number) => {
    try {
      await apiClient.put(`/participants/${participantId}/meeting_status?meeting_status=completed`);
      setParticipants(prev => prev.map(p => p.id === participantId ? { ...p, meeting_status: 'completed' } : p));
    } catch (error) {
      alert('Ошибка завершения встречи');
    }
  };

  const handleSaveProfile = async () => {
    try {
      await apiClient.put(`/users/${user.id}`, { trusted_contact: trustedContact });
      setCurrentUser({ ...currentUser, trusted_contact: trustedContact });
      setEditingProfile(false);
      setSnackbarMessage('Профиль обновлен');
      setSnackbarOpen(true);
    } catch (error) {
      console.error('Error updating profile:', error);
      setSnackbarMessage('Ошибка обновления профиля');
      setSnackbarOpen(true);
    }
  };

  const handleTestAlert = async () => {
    try {
      // Get geolocation
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;
          await apiClient.post('/test-safety-alert', { telegram_id: user.id, lat, lng });
          setSnackbarMessage('Тестовое уведомление отправлено');
          setSnackbarOpen(true);
        }, (error) => {
          console.error('Geolocation error:', error);
          // Send without geolocation
          apiClient.post('/test-safety-alert', { telegram_id: user.id });
          setSnackbarMessage('Тестовое уведомление отправлено (без геолокации)');
          setSnackbarOpen(true);
        });
      } else {
        await apiClient.post('/test-safety-alert', { telegram_id: user.id });
        setSnackbarMessage('Тестовое уведомление отправлено');
        setSnackbarOpen(true);
      }
    } catch (error) {
      console.error('Error sending test alert:', error);
      setSnackbarMessage('Ошибка отправки уведомления');
      setSnackbarOpen(true);
    }
  };

  const handleCheckInResponse = async (response: string) => {
    if (!activeCheckIn) return;
    try {
      await apiClient.post('/check-in-response', { participant_id: activeCheckIn.id, response });
      setSnackbarMessage(`Ответ "${response}" отправлен`);
      setSnackbarOpen(true);
      setActiveCheckIn(null);
    } catch (error) {
      console.error('Error sending check-in response:', error);
      setSnackbarMessage('Ошибка отправки ответа');
      setSnackbarOpen(true);
    }
  };

  const handlePhotoUpload = async () => {
    if (!photoFile || !user?.id) return;
    try {
      const formData = new FormData();
      formData.append('file', photoFile);
      const response = await apiClient.post(`/users/${user.id}/upload-photo`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setCurrentUser({ ...currentUser, photo_url: response.data.photo_url });
      setSnackbarMessage('Фото загружено');
      setSnackbarOpen(true);
      setPhotoFile(null);
    } catch (error) {
      console.error('Error uploading photo:', error);
      setSnackbarMessage('Ошибка загрузки фото');
      setSnackbarOpen(true);
    }
  };

  const handleReport = async (reason: string) => {
    // For demo, report self
    try {
      await apiClient.post('/complaints/', {
        complainant_id: user.id,
        accused_id: user.id, // change to actual accused
        reason,
        description: 'Test complaint'
      });
      setSnackbarMessage('Жалоба отправлена');
      setSnackbarOpen(true);
    } catch (error) {
      console.error('Error sending complaint:', error);
      setSnackbarMessage('Ошибка отправки жалобы');
      setSnackbarOpen(true);
    }
  };

  if (!user) {
    return (
      <Box sx={{ padding: 2 }}>
        <Typography variant="h6">Пользователь не найден</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ padding: 2, maxWidth: 600, margin: '0 auto' }} className="page-container cozy-bg">
      <Box sx={{ textAlign: 'center', marginBottom: 2 }}>
        <Avatar
          src={currentUser?.photo_url ? `http://localhost:8001${currentUser.photo_url}` : undefined}
          sx={{ width: 100, height: 100, margin: '0 auto 1rem' }}
        >
          {user.first_name?.[0]}{user.last_name?.[0]}
        </Avatar>
        <div className="icon-large">🏠</div>
        <Typography variant="h1" gutterBottom>
          {user.first_name} {user.last_name}
        </Typography>
        <Typography variant="body1" color="textSecondary" className="welcome-text">
          Добро пожаловать в твой профиль! Здесь твои события и друзья.
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ marginTop: 1 }}>
          Создано событий: {userEvents.length} | Присоединяйся к новым встречам!
        </Typography>
        <Button variant="outlined" onClick={() => setEditingProfile(!editingProfile)} sx={{ marginTop: 1 }}>
          {editingProfile ? 'Отмена' : 'Редактировать профиль'}
        </Button>
        <Typography variant="body1" sx={{ marginTop: 1 }}>
          Доверенный контакт: {currentUser?.trusted_contact || 'Не указан'}
        </Typography>
        {currentUser?.trusted_contact && (
          <Button variant="outlined" color="warning" onClick={handleTestAlert} sx={{ marginTop: 1 }}>
            Отправить тестовое уведомление
          </Button>
        )}
        {editingProfile && (
          <Card sx={{ marginTop: 2, padding: 2 }}>
            <Typography variant="h6">Доверенный контакт</Typography>
            <TextField
              fullWidth
              label="Доверенный контакт"
              value={trustedContact}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTrustedContact(e.target.value)}
              placeholder="Введите Telegram username (@username) или ID вручную"
              sx={{ marginTop: 1 }}
            />
            <Typography variant="h6" sx={{ marginTop: 2 }}>Фото профиля</Typography>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setPhotoFile(e.target.files?.[0] || null)}
              style={{ marginTop: 8 }}
            />
            {photoFile && (
              <Button variant="contained" onClick={handlePhotoUpload} sx={{ marginTop: 1 }}>
                Загрузить фото
              </Button>
            )}
            <Button variant="contained" onClick={handleSaveProfile} sx={{ marginTop: 1 }}>
              Сохранить
            </Button>
          </Card>
        )}
        <Typography variant="caption" color="textSecondary" sx={{ marginTop: 1 }}>
          Telegram ID: {user.id}
        </Typography>
        <Button variant="contained" color="secondary" onClick={handleTestAlert} sx={{ marginTop: 1 }}>
          Отправить тестовое уведомление
        </Button>
        <Button variant="outlined" color="error" onClick={() => handleReport('fake_photo')} sx={{ marginTop: 1 }}>
          Пожаловаться (ненастоящее фото)
        </Button>
      </Box>

      {activeCheckIn && (
        <Card sx={{ marginTop: 2, padding: 2 }}>
          <Typography variant="h6">Проверка безопасности</Typography>
          <Typography>Вы в безопасности?</Typography>
          <Box sx={{ display: 'flex', gap: 1, marginTop: 1 }}>
            <Button variant="contained" color="success" onClick={() => handleCheckInResponse('safe')}>
              Я в безопасности
            </Button>
            <Button variant="contained" color="error" onClick={() => handleCheckInResponse('unsafe')}>
              Помогите!
            </Button>
            <Button variant="outlined" onClick={() => handleCheckInResponse('completed')}>
              Встреча завершена
            </Button>
          </Box>
        </Card>
      )}

      <Box>
        <Typography variant="h2" gutterBottom color="primary">
          Мои события
        </Typography>
        {loading ? (
          <Typography>Загрузка...</Typography>
        ) : error ? (
          <Typography color="error">{error}</Typography>
        ) : userEvents.length === 0 ? (
          <Typography>У вас нет созданных событий</Typography>
        ) : (
          <Box>
            {userEvents.map(event => (
              <Card key={event.id} sx={{ marginBottom: 2 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="h2">{event.title}</Typography>
                      <Typography variant="body1">Дата: {new Date(event.created_at).toLocaleDateString()}</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton color="secondary" onClick={() => handleEdit(event.id)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton color="error" onClick={() => handleDelete(event.id)}>
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        )}
      </Box>

      <Box sx={{ marginTop: 4 }}>
        <Typography variant="h2" gutterBottom color="primary">
          Заявки на участие
        </Typography>
        {participants.filter(p => p.status === 'pending').length === 0 ? (
          <Typography>Нет новых заявок</Typography>
        ) : (
          <Box>
            {participants.filter(p => p.status === 'pending').map(participant => (
              <Card key={participant.id} sx={{ marginBottom: 2 }}>
                <CardContent>
                  <Typography variant="h3">{participant.eventTitle}</Typography>
                  <Typography variant="body1">Пользователь ID: {participant.user_id}</Typography>
                  {participant.message && <Typography variant="body2">Сообщение: {participant.message}</Typography>}
                  <Box sx={{ display: 'flex', gap: 1, marginTop: 1 }}>
                    <Button variant="contained" color="success" startIcon={<CheckIcon />} onClick={() => handleAccept(participant.id)}>
                      Принять
                    </Button>
                    <Button variant="contained" color="error" startIcon={<CloseIcon />} onClick={() => handleReject(participant.id)}>
                      Отклонить
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        )}
      </Box>

      {userParticipations.length > 0 && (
        <Box sx={{ marginTop: 4 }}>
          <Typography variant="h2" gutterBottom color="primary">
            Мои участия
          </Typography>
          <Box>
            {userParticipations.map(participation => (
              <Card key={participation.id} sx={{ marginBottom: 2 }}>
                <CardContent>
                  <Typography variant="h3">Участие в событии ID: {participation.event_id}</Typography>
                  <Typography variant="body1">Статус: {participation.status}</Typography>
                  <Typography variant="body1">Статус встречи: {participation.meeting_status}</Typography>
                  <Box sx={{ display: 'flex', gap: 1, marginTop: 1 }}>
                    {participation.meeting_status === 'not_started' && (
                      <Button variant="contained" color="primary" onClick={() => handleStartMeeting(participation.id)}>
                        Начать встречу
                      </Button>
                    )}
                    {participation.meeting_status === 'in_progress' && (
                      <Button variant="contained" color="secondary" onClick={() => handleEndMeeting(participation.id)}>
                        Завершить встречу
                      </Button>
                    )}
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        </Box>
      )}

      <Button variant="text" color="primary" sx={{ marginTop: 2 }}>
        Выйти
      </Button>
      <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={() => setSnackbarOpen(false)}>
        <Alert onClose={() => setSnackbarOpen(false)} severity={snackbarMessage.includes('Ошибка') ? 'error' : 'success'} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};