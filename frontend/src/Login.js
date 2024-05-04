import React, { useState } from 'react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (password === 'password') {
      setErrorMessage('Password cannot be "password"');
      return;
    }

    // Perform dummy login validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setErrorMessage('Invalid email address');
      return;
    }

    // Login successful
    setLoggedIn(true);
    setErrorMessage('');
  };

  if (loggedIn) {
    return <div data-testid="welcome-message">Welcome! You are logged in.</div>;
  }

  return (
    <div>
      <h2>Login</h2>
      {errorMessage && (
        <div className="error-message" data-testid="error-message">
          {errorMessage}
        </div>
      )}
      <form onSubmit={handleSubmit} data-testid="login-form">
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            data-testid="email-input"
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            data-testid="password-input"
          />
        </div>
        <button type="submit" data-testid="login-button">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;