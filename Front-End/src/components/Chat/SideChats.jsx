import "./SideChats.css";
import React from "react";
import Chat from "./Chat";

export default function SideChats() {
	return (
		<div className="sidechat">
			<Chat />
			<Chat />
		</div>
	);
}