import React, { useState } from 'react';
import './index.css';
import SideChats from '../Chat/SideChats';
import WebSocketComponent from '../WebSocket/WebSocket';
// import { Nav, navbar } from 'react-bootstrap';
// import 'bootstrap/dist/css/bootstrap.min.css';

const Home = () => {
	const [isDivVisible, setIsDivVisible] = useState(false);

	const toggleDiv = () => {
    setIsDivVisible(!isDivVisible);
  };

  return (
    <div className="home">
			<div className="navbar">
				<h1>logo</h1>
				<p>panino</p>
				{/* Aggiungi il contenuto della tua home page qui */}
			</div>
			<div className="undernavbar">
        <div className="sidebar">
					<button onClick={toggleDiv}>Toggle Div</button>
				</div>
        {/* {isDivVisible && <SideChats />} */}
				{/* nome del canale e il resto in models.py tranne auto... mi restituisc e restituisce un json*/}
        {isDivVisible && <WebSocketComponent />}
        <div className={`content ${isDivVisible ? 'content-reduced' : ''}`}></div>
			</div>
    </div>
  );
};

export default Home;