import React, { useState, useEffect } from 'react';
import useWebSocket from 'react-use-websocket';

const WebSocketComponent = () => {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const roomId = 'room1';
  const token = 'your_access_token';
  const wsUrl = `ws://${window.location.host}/ws/chat/${roomId}/?token=${token}`;

  const { sendMessage, lastMessage, readyState } = useWebSocket(wsUrl, {
    onOpen: () => console.log('WebSocket connection opened'),
    onClose: () => console.log('WebSocket connection closed'),
    onError: (e) => console.error('WebSocket error:', e),
  });

  useEffect(() => {
    if (lastMessage !== null) {
      const data = JSON.parse(lastMessage.data);
      setChat((prevChat) => [...prevChat, data.message]);
    }
  }, [lastMessage]);

  const handleSendMessage = () => {
    const messageData = {
      message: message,
      room_id: roomId,
      sender: 'your_username'  // Replace with the actual sender's username
    };
    sendMessage(JSON.stringify(messageData));
    setChat((prevChat) => [...prevChat, message]); // Aggiungi il messaggio inviato alla chat
    setMessage('');
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