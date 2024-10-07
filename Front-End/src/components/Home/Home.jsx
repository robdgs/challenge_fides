import React from 'react';
import './index.css';
// import { Nav, navbar } from 'react-bootstrap';
// import 'bootstrap/dist/css/bootstrap.min.css';

const Home = () => {
  return (
    <div className="global">
			<div className="navbar">
				<h1>logo</h1>
				<p>panino</p>
				{/* Aggiungi il contenuto della tua home page qui */}
			</div>
			<div className="undernavbar">
				<div className="sidebar"></div>
				<div className="content"></div>
			</div>
    </div>
  );
};

export default Home;