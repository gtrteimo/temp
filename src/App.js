import React, { useState, useRef, useEffect } from 'react';
import { Container, Box, Typography, TextField, Button, Paper } from '@mui/material';
import Message from './Message';
import SendIcon from '@mui/icons-material/Send';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  // Feste Werte für User ID und Session ID (diese können alternativ über Input-Felder eingegeben werden)
  const userId = '123';     // Beispiel: feste User ID
  const sessionId = 'abc';  // Beispiel: feste Session ID

  // Automatisches Scrollen zum Ende der Nachrichtenliste
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSendMessage = async () => {
    if (input.trim() !== '') {
      const messageText = input;
      // Zeige die vom Benutzer eingegebene Nachricht
      const userMessage = { text: messageText, sender: 'user' };
      setMessages(prevMessages => [...prevMessages, userMessage]);
      setInput('');

      // Sende die Nachricht an den API-Endpunkt /api/message
      try {
        const payload = {
          user_id: userId,
          session_id: sessionId,
          message: messageText,
        };

        const response = await fetch('http://192.168.141.175:5000/api/message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.response) {
          setMessages(prevMessages => [
            ...prevMessages,
            { text: data.response, sender: 'bot' },
          ]);
        } else {
          setMessages(prevMessages => [
            ...prevMessages,
            { text: "Bot response not available", sender: 'bot' },
          ]);
        }
      } catch (error) {
        console.error('Error sending message:', error);
        setMessages(prevMessages => [
          ...prevMessages,
          { text: "Error sending message", sender: 'bot' },
        ]);
      }
    }
  };

  // Scrollt automatisch nach unten, wenn sich die Nachrichten ändern
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handler für die Enter-Taste
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Container
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        width: '100vw',
        padding: 0,
        margin: 0,
      }}
    >
      <Paper
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          width: '100%',
          padding: '20px',
          boxSizing: 'border-box',
        }}
      >
        <Typography variant="h4" gutterBottom align="center">
          SüdtirolKI
        </Typography>

        <Box
          style={{
            flex: 1,
            overflowY: 'auto',
            marginBottom: '16px',
          }}
        >
          {messages.map((msg, index) => (
            <Message key={index} message={msg} />
          ))}
          <div ref={messagesEndRef} />
        </Box>

        <Box display="flex" alignItems="center" justifyContent="space-between">
          <TextField
            fullWidth
            variant="outlined"
            label="Type a message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            style={{ marginRight: '10px' }}
          />
          <Button
            variant="contained"
            color="primary"
            startIcon={<SendIcon />}
            style={{ padding: '14px 24px', fontSize: '16px' }}
            onClick={handleSendMessage}
          >
            Send
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}

export default App;
