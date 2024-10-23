export const onHandleSubmit = async (e, username, email, password, navigate) => {
  e.preventDefault();
  if (email && password) {
		console.log('Username:', username);
    console.log('Username:', email);
    console.log('Password:', password);
    try {
      const response = await fetch('http://localhost:8000/login/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Risposta dal server:', data);
        // Gestisci la risposta del server, ad esempio, naviga a un'altra pagina
        navigate('/login');
      } else {
				const errorData = await response.json();
				console.error('Errore nella risposta del server:', errorData.error);
				if (errorData.error === "['email already in use']") {
          alert('L\'email inserita è già in uso. Scegli un\'altra email.');
        } else if (errorData.error === "['weak password']") {
          alert('La password deve contenere almeno 8 caratteri.');
        } else if (errorData.error === "['username already in use']") {
          alert('Per favore, inserisci un nome utente valido.');
        } else {
          alert('Si è verificato un errore. Per favore, riprova.');
        }
        console.error('Errore nella risposta del server:', response.statusText);
      }
    } catch (error) {
      console.error('Errore nella richiesta:', error);
    }
  } else {
    console.log('Per favore, inserisci sia username che password.');
  }
};
