import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import Login from './components/Login/Login';
import Register from './components/Register/Register';
import Home from './components/Home/Home';
import Tasks from './components/Tasks/Tasks';
import ExternalRedirect from './components/ExternalRedirect/ExternalRedirect';
import AvatarCard from './components/AvatarCard/AvatarCard';

const AppContent = () => {
  const location = useLocation();
  const [isNavbarReduced, setIsNavbarReduced] = useState(false);
  const showNavbar = location.pathname !== '/login' && location.pathname !== '/egister';

  const toggleNavbar = () => {
    setIsNavbarReduced(!isNavbarReduced);
  };

  return (
    <div className="App">
      {showNavbar && <Navbar isReduced={isNavbarReduced} toggleNavbar={toggleNavbar} />}
      <div className={`content ${showNavbar ? '' : 'full-width'}`}>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/home" element={<Home />} />
          <Route path="/tasks" element={<Tasks isNavbarReduced={isNavbarReduced} />} />
          <Route path="/mine" element={<ExternalRedirect to="https://minesweeper.online/it/" />} />
          <Route 
            path="/AvatarCard" 
            element={
              <AvatarCard 
                title="User Title"
                imageUrl="https://via.placeholder.com/150" 
                linesOfText={[
                  "Line 1 of text",
                  "Line 2 of text",
                  "Line 3 of text",
                  "Line 4 of text",
                  "Line 5 of text"
                ]}
                bottomText="LVL 1"
                experience={70} 
              />
            } 
          />
        </Routes>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;