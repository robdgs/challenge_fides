export const onHandleSubmit = async (e, email, password, navigate) => {
  e.preventDefault();
  if (email && password) {
    console.log('Username:', email);
    console.log('Password:', password);
    try {
      const response = await fetch('http://localhost:8000/login/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Risposta dal server:', data);
        // Gestisci la risposta del server, ad esempio, naviga a un'altra pagina
        navigate('/home');
      } else {
        console.error('Errore nella risposta del server:', response.statusText);
      }
    } catch (error) {
      console.error('Errore nella richiesta:', error);
    }
  } else {
    console.log('Per favore, inserisci sia username che password.');
  }
};
