import React, { useState, useEffect } from 'react';
import useWebSocket from 'react-use-websocket';

// http request con la room e cr

const WebSocketComponent = () => {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const roomId = 'room1';
  const token = localStorage.getItem('token');
  const wsUrl = `ws://localhost:8001/ws/chat/${roomId}/?token=${token}`;

  const { sendMessage, lastMessage, readyState, getWebSocket } = useWebSocket(wsUrl, {
    onOpen: () => {
      console.log('WebSocket connection opened');
      alert('Connessione WebSocket stabilita');
    },
    onClose: () => console.log('WebSocket connection closed'),
    onError: (e) => console.error('WebSocket error:', e),
  });

  useEffect(() => {
    if (lastMessage !== null) {
      const data = JSON.parse(lastMessage.data);
      setChat((prevChat) => [...prevChat, data.message]);
    }

    // Funzione di pulizia per chiudere la connessione WebSocket
    return () => {
      const socket = getWebSocket();
      if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
        console.log('Chiudendo la connessione WebSocket');
        socket.close();
      }
    };
  }, [lastMessage, getWebSocket]);

  const handleSendMessage = () => {
    const socket = getWebSocket();
    console.log('Stato della connessione WebSocket:', socket.readyState);
    if (socket && socket.readyState === WebSocket.OPEN) {
      const messageData = {
        message: message,
        room_id: roomId,
        sender: 'your_username'  // Replace with the actual sender's username
      };
      sendMessage(JSON.stringify(messageData));
      setChat((prevChat) => [...prevChat, message]); // Aggiungi il messaggio inviato alla chat
      setMessage('');
      alert('Messaggio inviato con successo');
    } else {
      alert('Connessione WebSocket non attiva');
    }
  };

  return (
    <div>
      <div>Ready state: {readyState}</div>
      <div>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message"
        />
        <button onClick={handleSendMessage}>Send Message</button>
      </div>
      <div>
        <h2>Chat</h2>
        <div>
          {chat.map((msg, index) => (
            <div key={index}>{msg}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WebSocketComponent;