import './index.css';

export default function Button({onclick, text}){
    /* passare funzione onclick come prop(?)*/
    /* guarda gestione eventi */
    return (
<button onClick={onclick}>{text}</button>
    )
}