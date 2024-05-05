import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  const handleSubmit = async (e) => {
  e.preventDefault();

  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  try {
    const response = await axios.post('http://localhost/api/login', formData);

    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    setLoggedIn(true);
    setErrorMessage('');
  } catch (error) {
    console.log(error.response.data);
    if (error.response && error.response.data) {
      let errorDetails = 'Error occurred';
      if (error.response.data.detail) {
        console.log(error.response.data.detail);
        if (Array.isArray(error.response.data.detail)) {
          errorDetails = error.response.data.detail.map(d => d.msg).join(", ");
        } else {
          errorDetails = error.response.data.detail.msg || JSON.stringify(error.response.data.detail);
        }
      } else {
        errorDetails = 'Error response has no detail';
      }
      setErrorMessage(errorDetails);
    } else if (error.request) {
      setErrorMessage('No response from server');
    } else {
      setErrorMessage('Error: ' + error.message);
    }
  }

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
