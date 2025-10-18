import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#FF6B35', // Теплый оранжевый для уюта
    },
    secondary: {
      main: '#F7931E', // Золотой для акцентов
    },
    error: {
      main: '#E63946', // Мягкий красный
    },
    background: {
      default: '#1A1A1A', // Темный теплый фон
      paper: 'rgba(50, 30, 10, 0.8)', // Полупрозрачный теплый фон
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#D4A574', // Теплый бежевый
    },
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    h1: {
      fontSize: '24px',
      fontWeight: 700,
    },
    h2: {
      fontSize: '18px',
      fontWeight: 600,
    },
    body1: {
      fontSize: '16px',
      fontWeight: 400,
    },
    caption: {
      fontSize: '14px',
      fontWeight: 400,
      color: '#B0B0B0',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#1A1A1A',
          backgroundImage: 'radial-gradient(circle at 20% 50%, rgba(255, 107, 53, 0.1) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(247, 147, 30, 0.1) 0%, transparent 50%)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: 'rgba(50, 30, 10, 0.8)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 107, 53, 0.4)',
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0 4px 12px rgba(255, 107, 53, 0.3)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 6px 20px rgba(255, 107, 53, 0.5)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(50, 30, 10, 0.8)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 107, 53, 0.4)',
          borderRadius: '16px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
          transition: 'all 0.3s ease',
          '&:hover': {
            border: '2px solid rgba(255, 107, 53, 0.7)',
            boxShadow: '0 12px 40px rgba(0, 0, 0, 0.4)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: 'rgba(50, 30, 10, 0.8)',
            borderRadius: '12px',
            outline: 'none',
            '& fieldset': {
              borderWidth: '2px',
              borderColor: '#D4A574',
            },
            '&:hover fieldset': {
              borderColor: '#FF6B35',
            },
            '&.Mui-focused': {
              outline: 'none',
              boxShadow: 'none',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#FF6B35',
            },
            '& textarea': {
              border: 'none',
            },
            '& input, & textarea': {
              backgroundColor: 'transparent',
              color: '#FFFFFF',
              '&:-webkit-autofill, &:-webkit-autofill:hover, &:-webkit-autofill:focus, &:-webkit-autofill:active': {
                WebkitBoxShadow: '0 0 0 30px rgba(50, 30, 10, 0.8) inset !important',
                WebkitTextFillColor: '#FFFFFF !important',
              },
            },
          },
          '& .MuiInputLabel-root': {
            color: '#D4A574',
            '&.Mui-focused': {
              color: '#FF6B35',
            },
          },
        },
      },
    },
    MuiBottomNavigation: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(50, 30, 10, 0.8)',
          backdropFilter: 'blur(10px)',
          borderTop: '1px solid rgba(255, 107, 53, 0.4)',
          borderRadius: '16px 16px 0 0',
        },
      },
    },
  },
});

export default theme;