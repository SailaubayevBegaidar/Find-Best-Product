document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            };

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    window.location.href = '/products';
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred during login');
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value
            };

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                if (response.ok) {
                    alert('Registration successful! Please login.');
                    window.location.href = '/login';
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred during registration');
            }
        });
    }
}); 