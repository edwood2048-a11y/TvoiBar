import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { MapPage } from './pages/MapPage';
import { ProfilePage } from './pages/ProfilePage';
import { CreateEventPage } from './pages/CreateEventPage';
import { useTelegram } from './shared/lib/useTelegram';
import apiClient from './shared/api/client';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BottomNavigation, BottomNavigationAction, Paper, Box } from '@mui/material';
import MapIcon from '@mui/icons-material/Map';
import PersonIcon from '@mui/icons-material/Person';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import theme from './shared/theme';

function Navigation() {
  const location = useLocation();
  const [value, setValue] = React.useState(location.pathname);

  React.useEffect(() => {
    setValue(location.pathname);
  }, [location.pathname]);

  return (
    <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 100 }} elevation={3}>
      <BottomNavigation
        value={value}
        onChange={(event, newValue) => {
          setValue(newValue);
        }}
        showLabels
      >
        <BottomNavigationAction label="Карта" value="/" icon={<MapIcon />} component={Link} to="/" />
        <BottomNavigationAction
          label="Создать"
          value="/create"
          icon={
            <AddCircleIcon
              sx={{
                fontSize: 48,
                color: 'primary.main',
                transform: 'translateY(-10px)',
              }}
            />
          }
          component={Link}
          to="/create"
          showLabel={false}
        />
        <BottomNavigationAction label="Профиль" value="/profile" icon={<PersonIcon />} component={Link} to="/profile" />
      </BottomNavigation>
    </Paper>
  );
}

function App() {
  const { user } = useTelegram();

  useEffect(() => {
    if (user) {
      apiClient.post('/users/', {
        telegram_id: user.id,
        username: user.username,
        first_name: user.first_name,
        last_name: user.last_name,
      });
    }
  }, [user]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ paddingBottom: 10 }}>
          <Routes>
            <Route path="/" element={<MapPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/create" element={<CreateEventPage />} />
          </Routes>
          <Navigation />
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;