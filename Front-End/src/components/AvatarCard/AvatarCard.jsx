import React from 'react';
import './AvatarCard.css';

const AvatarCard = ({ title, imageUrl, linesOfText = [], bottomText, experience }) => {
  return (
    <div className="avatar-card">
      <h2 className="avatar-title">{title}</h2>
      <div className="avatar-content">
        <img src={imageUrl} alt="Avatar" className="avatar-image" />
        <div className="avatar-text">
          {linesOfText.map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
      </div>
      <p className="bottom-text">{bottomText}</p>
      <div className="experience-bar">
        <div className="experience-fill" style={{ width: `${experience}%` }}></div>
      </div>
    </div>
  );
};

export default AvatarCard;