import "./Chat.css";
import React, { useState } from "react";
import Message from "./Message/Message";
import Input from "../Input/Input";
import Button from "../Button/Button";

export default function Chat() {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={`chat separated ${isExpanded ? "expanded" : ""}`}>
      <div className="chat-button">
        <button className="clickable-div" onClick={handleExpand}>
          <div className="chat-header">
            <h1>Chat</h1>
          </div>
        </button>
      </div>
      {isExpanded && (
        <div className="scrollable-content">
          <Message message={{ text: "Ciao", sender_name: "Anna" }} />
          <Message message={{ text: "Come state?", sender_name: "Anna" }} />
          <Message message={{ text: "Così così?", personal_message: true }} />
          <Message message={{ text: "Bene, tu?", sender_name: "Luca" }} />
          <Message message={{ text: "Anch'io", sender_name: "Anna" }} />
          <Message message={{ text: "cosa hai?", sender_name: "Anna" }} />
          <Message
            message={{
              text: "Sto facendo una chat web",
              personal_message: true,
            }}
          />
          <Message message={{ text: "Che schifo", sender_name: "Luca" }} />
          <Message
            message={{
              text: "volevo dirvi: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
              sender_name: "Anna",
            }}
          />
        </div>
      )}
      {isExpanded && (
        <div className="fixed-footer">
          <Input type="text" placeholder="Scrivi un messaggio..." />
          <Button text="Invia" />
        </div>
      )}
    </div>
  );
}
