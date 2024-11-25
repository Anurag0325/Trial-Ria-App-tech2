<template>
    <div>
        <nav class="navbar">
            <div class="navbar-brand">
                <img src="Xploit2Secure.jpeg" alt="Logo" class="logo" />
                <div class="navbar-buttons">
                    <button @click="gotohome">Home</button>
                </div>
            </div>
        </nav>

        <div class="register-container">
            <h2>Register</h2>
            <form @submit.prevent="register">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" v-model="email" id="email" required />
                </div>

                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" v-model="username" id="username" required />
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" v-model="password" id="password" required />
                </div>

                <div class="form-group">
                    <label for="confirmPassword">Confirm Password</label>
                    <input type="password" v-model="confirmPassword" id="confirmPassword" required />
                </div>

                <button type="submit">Register</button>

                <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
                <p v-if="successMessage" class="success">{{ successMessage }}</p>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            email: '',
            username: '',
            password: '',
            confirmPassword: '',
            errorMessage: null,
            successMessage: null,
        };
    },

    methods: {
        async register() {
            this.errorMessage = null;
            this.successMessage = null;

            if (this.password !== this.confirmPassword) {
                this.errorMessage = "Passwords do not match.";
                return;
            }

            try {
                const response = await fetch('https://trial-ria-app.onrender.com/register', {
                // const response = await fetch('http://127.0.0.1:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: this.email,
                        username: this.username,
                        password: this.password,
                    }),
                });

                const result = await response.json();
                if (response.ok) {
                    this.successMessage = "Registration successful! Please log in.";
                    this.email = '';
                    this.username = '';
                    this.password = '';
                    this.confirmPassword = '';
                    alert('Registration successful! You can now log in.');
                    this.$router.push('/'); // Redirect to login page
                } else {
                    this.errorMessage = result.message || 'Registration failed. Please try again.';
                }
            } catch (error) {
                this.errorMessage = "An error occurred during registration. Please try again.";
                console.error(error);
            }
        },

        gotohome() {
            this.$router.push('/')
        },
    },
};
</script>

<style scoped>
/* Styling similar to Login.vue for consistency */
.register-container {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease;
}

.register-container:hover {
    transform: scale(1.02);
}

/* Reuse other styles from Login.vue */
h2 {
    text-align: center;
    color: #2a4d85;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 20px;
}

body {
    background: linear-gradient(135deg, #b3e5fc, #e1bee7);
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.navbar {
    background-color: #26c8bb;
    color: rgb(154, 242, 132);
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
    display: flex;
    align-items: center;
}

.logo {
    height: 40px;
    margin-right: 1rem;
    transition: transform 0.3s ease;
}

.logo:hover {
    transform: rotate(20deg) scale(1.1);
}

.login-container {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease;
}

.login-container:hover {
    transform: scale(1.02);
}

h2 {
    text-align: center;
    color: #2a4d85;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #333;
}

input {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    font-size: 14px;
    box-sizing: border-box;
    transition: border-color 0.3s ease;
}

input:focus {
    border-color: #26c8bb;
    outline: none;
    box-shadow: 0 0 5px rgba(38, 200, 187, 0.5);
}

button {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #4df19f, #26c8bb);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
}

button:hover {
    background: linear-gradient(135deg, #74cff3, #4df19f);
    transform: scale(1.05);
}

button:active {
    transform: scale(0.98);
}

.error {
    color: red;
    text-align: center;
    margin-top: 15px;
    font-size: 14px;
}

.error, .form-group, h2 {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.success {
    color: green;
    text-align: center;
    margin-top: 15px;
    font-size: 14px;
}

.navbar-buttons {
    margin-left: auto;
}

.navbar-buttons button {
    margin-left: auto;
    background-color: #9de764;
}

.navbar-buttons button:hover {
    margin-left: auto;
    background-color: #529af3;
}
</style>
