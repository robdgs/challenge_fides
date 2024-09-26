import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './index.css';
import Button from '../Button/Button';
import Input from '../Input/Input';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
	
  const onHandleSubmit = (e) => {
    e.preventDefault();
		if (username && password) {
			console.log('Username:', username);
			console.log('Password:', password);
		} else {
			console.log('Per favore, inserisci sia username che password.');
		}
  };

  const onRegisterClick = () => {
    navigate('/register');
  };

  return (
    <div className="global">
			{/* <div class="background">
        <div class="shape"></div>
        <div class="shape"></div>
			</div> */}
      <div className="login_box">
        <h1>Login</h1>
        <div className="login_form">
          <form className="login_form" onSubmit={(e)=> onHandleSubmit(e)}>
            <Input
              type="text"
              name="username"
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              type="password"
              name="password"
              placeholder="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div>
              <Button text={"Login"} type={"submit"}/>
              <Button onclick={onRegisterClick} text={"Register"} type={"submit"}/>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
