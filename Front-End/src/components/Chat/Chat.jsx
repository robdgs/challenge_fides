import "./Chat.css";
import React, { useState } from 'react';

export default function Chat()
{
	const [isExpanded, setIsExpanded] = useState(false);
	const [isExpanded2, setIsExpanded2] = useState(false);

	const handleExpand = () => {
			setIsExpanded(!isExpanded);
	};
	const handleExpand2 = () => {
		setIsExpanded2(!isExpanded2);
};

	return (
		<div className="chat">

			<div className={`chat2 separated ${isExpanded ? 'expanded' : ''}`}>
				<button className="clickable-div" onClick={handleExpand}>
					<div className="chat-header">
						<h1>Chat</h1>
					</div>
				</button>
				{isExpanded && (
          <div className="expanded-content">
              <p>Contenuto aggiuntivo</p>
          </div>
        )}
			</div>

			<div className={`chat2 separated ${isExpanded2 ? 'expanded' : ''}`}>
				<button className="clickable-div" onClick={handleExpand2}>
					<div className="chat-header">
						<h1>Chat</h1>
					</div>
				</button>
				{isExpanded2 && (
          <div className="expanded-content2">
              <p>Contenuto aggiuntivo</p>
          </div>
        )}
			</div>

		</div>

		
	);
}