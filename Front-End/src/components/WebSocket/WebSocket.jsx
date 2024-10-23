import React, { useState, useEffect } from 'react';
import useWebSocket from 'react-use-websocket';
/* // ChatComponent.js
import React, { useContext, useState } from 'react';
import { WebSocketContext } from './WebSocketProvider';

const ChatComponent = () => {
    const { messages, sendMessage } = useContext(WebSocketContext);
    const [input, setInput] = useState('');

    const handleSend = () => {
        const message = {
            message: input,
            room_id: 1, // Replace with actual room ID
            sender: 'testuser', // Replace with actual sender
            timestamp: new Date().toISOString(),
        };
        sendMessage(message);
        setInput('');
    };

    return (
        <div>
            <div>
                {messages.map((msg, index) => (
                    <div key={index}>
                        <strong>{msg.sender}</strong>: {msg.message}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
            />
            <button onClick={handleSend}>Send</button>
        </div>
    );
};

export default ChatComponent; // WebSocketProvider.js
import React, { createContext, useEffect, useRef, useState } from 'react';

export const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
    const [messages, setMessages] = useState([]);
    const ws = useRef(null);

    useEffect(() => {
        // Replace 'room_name' with the actual room name
        const roomName = 'room_name';
        ws.current = new WebSocket(`ws://localhost:8002/ws/chat/${roomName}/`);

        ws.current.onopen = () => {
            console.log('WebSocket connected');
        };

        ws.current.onmessage = (event) => {
            const message = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, message]);
        };

        ws.current.onclose = () => {
            console.log('WebSocket disconnected');
        };

        return () => {
            ws.current.close();
        };
    }, []);

    const sendMessage = (message) => {
        if (ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify(message));
        }
    };

    return (
        <WebSocketContext.Provider value={{ messages, sendMessage }}>
            {children}
        </WebSocketContext.Provider>
    );
};*/
const WebSocketComponent = () => {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const roomId = 'room1';
  const token = localStorage.getItem('token');
  const wsUrl = `ws://${window.location.host}/ws/chat/${roomId}/?token=${token}`;

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