const API_BASE_URL = 'http://127.0.0.1:5000';

async function createItem() {
    const name = document.getElementById('full-name').value;
    const email = document.getElementById('email-address').value;
    const password = document.getElementById('password').value;

    if (!email) {
        alert('O e-mail é obrigatório!');
        return
    }

    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        // const data = await response.json()
        // document.getElementById('').textContent = JSON.stringify(data, null, 2);

        if (response.status === 201) {
            alert('OK!')
            document.getElementById('full-name').value = '';
            // document.getElementById('email-address').value = '';
            // document.getElementById('password').value = '';
        }
    } catch (error) {
        alert(`Erro: ${error.message}`)
        // document.getElementById('').textContent = 'Erro: ' + error.message;
    }
}
