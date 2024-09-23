import './index.css';
import Button from '../Button/Button';

export default function Login()
{
    console.log("aiuto");
    const onHandleClick = (e) => { 
        console.log("sono stato cliccato");
    };

    const onHandleSubmit = (e) => {
        e.preventDefault();
        console.log("sono stato submittato");
      };

    return(
    <div className="global">
        <div className="login_box">
                <h1>Login</h1>
        <div className="login_form">
            <form className="login_form" onSubmit={onHandleSubmit}>
                    <input type="text" name="username" placeholder='username' />
                    <input type="password" name="password" placeholder='password' />
                    <Button onclick={onHandleClick} text={"Login"} />
            </form>
        </div>
        </div>
    </div>
    )
}