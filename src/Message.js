import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

function Message({ message }) {
  return (
    <Box my={2} display="flex" flexDirection={message.sender === 'user' ? 'row-reverse' : 'row'}>
      <Paper
        elevation={3}
        style={{
          padding: '10px',
          backgroundColor: message.sender === 'user' ? '#1976d2' : '#f1f1f1',
          color: message.sender === 'user' ? '#fff' : '#000',
        }}
      >
        <Typography variant="body1">{message.text}</Typography>
      </Paper>
    </Box>
  );
}

export default Message;
