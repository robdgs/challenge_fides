import './index.css';

export default function Input({ type, name, placeholder, value, onChange }){
    return (
		<input
		className = "input"
		type={type}
		name={name}
		placeholder={placeholder}
		value={value}
		onChange={onChange}
	  />
    )
}