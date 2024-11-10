// src/App.js

import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import LegalAid from './components/legalAid';
import HomePage from './components/home'


function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* <LegalAid /> */}
      <HomePage />
    </ThemeProvider>
  );
}

export default App;