import "./index.css";

export default function Button({ onclick, text, type })
{
  return (
    <button className="button" onClick={onclick} type={type}>
      {text}
    </button>
  );
}
