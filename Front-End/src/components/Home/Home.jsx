import React from 'react';
import AvatarCard from '../AvatarCard/AvatarCard';
import Navbar from '../Navbar/Navbar';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <Navbar />
      <div className="home-content">
        <div className="avatar-and-graphics">
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
            bottomText="Some bottom text"
            experience={70} 
          />
          <div className="task-graphics">
            {/* Add your task graphics and other elements here */}
            <p>Task statistics and graphics will be displayed here.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;