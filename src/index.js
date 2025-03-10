import React from 'react';
import ReactDOM from 'react-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles'; // Importiere das Theme
import App from './App';
import './index.css'; // Falls du eine eigene CSS-Datei verwendest

// Definiere das Theme mit einer dunklen Palette
const theme = createTheme({
  palette: {
    mode: 'dark', // Wähle entweder 'light' oder 'dark'
    primary: {
      main: '#1976d2', // Primärfarbe, kann nach Wunsch angepasst werden
    },
    secondary: {
      main: '#9c27b0', // Sekundärfarbe, kann nach Wunsch angepasst werden
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif', // Standard-Schriftart
  },
});

ReactDOM.render(
  <ThemeProvider theme={theme}> {/* Hier wird das Theme angewendet */}
    <App />
  </ThemeProvider>,
  document.getElementById('root')
);
