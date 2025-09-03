async function handleLogin() {
    const email = document.getElementById('email-address').value;
    const password = document.getElementById('password').value;
    // const errorElement = document.getElementById('errorMessage');

    if (!email || !password) {
        alert("Preencha todos os campos!");

        // errorElement.textContent = "Preencha todos os campos!";
        // errorElement.classList.remove('d-none');
        return;
    }

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (data.success) {
            window.location.href = data.redirect;
        } else {
            alert("Erro desconhecido");
            // errorElement.textContent = data.message;
            // errorElement.classList.remove('d-none');
        }
    } catch (error) {
        // errorElement.textContent = "Erro ao tentar fazer login";
        // errorElement.classList.remove('d-none');
        alert("Erro ao tentar fazer login");
        console.error('Error:', error);
    }
}