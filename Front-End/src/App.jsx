import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Home from './components/Home/Home';
import ExternalRedirect from './components/ExternalRedirect/ExternalRedirect';
import AvatarCard from './components/AvatarCard/AvatarCard';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<Navigate to="/login" />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/mine" element={<ExternalRedirect to="https://minesweeper.online/it/" />} />
                    <Route 
                        path="/AvatarCard" 
                        element={
                            <AvatarCard 
                                title="User Title"
                                imageUrl="https://via.placeholder.com/150" 
                                linesOfText={[
                                    "Simone Gariglio",
                                    "Line 2 of text",
                                    "Line 3 of text",
                                    "Line 4 of text",
                                    "Line 5 of text"
                                ]}
                                bottomText="lvl 1"
                                experience={70} 
                            />
                        } 
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;