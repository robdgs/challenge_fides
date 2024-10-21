import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <div className="navbar">
      <ul>
        <li><a href="/home">Home</a></li>
        <li><a href="/tasks">Tasks</a></li>
        <li><a href="/profile">Profile</a></li>
        <li><a href="/settings">Settings</a></li>
		<li><a href="/chat">Chat</a></li>
      </ul>
    </div>
  );
};

export default Navbar;
