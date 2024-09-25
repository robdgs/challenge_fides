import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './index.css';
import Button from '../Button/Button';
import Input from '../Input/Input';

export default function Login()
{
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const navigate = useNavigate();

    const onHandleClick = (e) => { 
        console.log("sono stato cliccato");
    };

    const onHandleSubmit = (e) => {
        e.preventDefault();
        console.log("sono stato submittato");
      };

	  const onRegisterClick = () => {
		navigate('/register');
	  };

    return(
    <div className="global">
        <div className="login_box">
                <h1>Login</h1>
        <div className="login_form">
            <form className="login_form" onSubmit={onHandleSubmit}>
                    <Input type="text" name="username" placeholder='username' value={username} onChange={(e) => setUsername(e.target.value)}/>
                    <Input type="password" name="password" placeholder='password' value={password} onChange={(e) => setPassword(e.target.value)}/>
					<div>
						<Button onclick={onHandleClick} text={"Login"} />
						<Button onclick={onRegisterClick} text={"Register"} />
					</div>
            </form>
        </div>
        </div>
    </div>
    )
}