import './index.css';

export default function Input({ type, name, placeholder, value, onChange }){
  
	const isTypeDate = type === 'date' ? true : false;

	return (
		<input className = {isTypeDate ? "date_input" : "input"}
		type={type}
		name={name}
		placeholder={placeholder}
		value={value}
		onChange={onChange}
	  />
    )
}