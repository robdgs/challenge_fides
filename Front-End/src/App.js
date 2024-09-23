import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
	const [UsernameValue, setUsernameValue] = useState('');
	const handleUsernameChange = (event) => {
		setUsernameValue(event.target.value);
	  };

	const [PasswordValue, setPasswordValue] = useState('');
	const handlePasswordChange = (event) => {
		setPasswordValue(event.target.value);
	  }
	
	

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Login
        </p>
		<input
          type="username"
          value={UsernameValue}
          onChange={handleUsernameChange}
          placeholder="Username"
        />
		<input
          type="password"
          value={PasswordValue}
          onChange={handlePasswordChange}
          placeholder="Password"
        />
		<MyButton />
      </header>
    </div>
  );
}

function MyButton() {
	function handleClick() {
	  alert('You clicked me!');
	}
  
	return (
	  <button onClick={handleClick}>
		login with google
	  </button>
	);
  }

export default App;
