import React, { useState } from 'react';
import axios from 'axios';

const apiBaseUrl = process.env.REACT_APP_API_URL;

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [ws, setWs] = useState(null);

  const handleWebSocketConnect = () => {
    const token = localStorage.getItem('token');
    const wsUrl = `${apiBaseUrl.replace('http', 'ws')}/api/ws/${email}?token=${token}`;
    const newWs = new WebSocket(wsUrl);

    newWs.onopen = () => console.log('WebSocket connected');
    newWs.onmessage = (message) => {
      try {
        const data = JSON.parse(message.data);
        console.log('Received data:', data);
      } catch (e) {
        console.error('Error parsing message data:', e);
      }
    };
    newWs.onclose = () => console.log('WebSocket disconnected');
    newWs.onerror = (error) => console.error('WebSocket error:', error);

    setWs(newWs);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await axios.post(`${apiBaseUrl}/api/login`, formData);
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      setLoggedIn(true);
      setErrorMessage('');
      handleWebSocketConnect(); // Establish WebSocket connection after successful login
    } catch (error) {
      console.error('Login error:', error);
      processError(error);
    }
  };

  const processError = (error) => {
    let errorDetails = 'Error occurred';
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        errorDetails = error.response.data.detail.msg || JSON.stringify(error.response.data.detail);
      }
    } else {
      errorDetails = error.message || 'No response from server';
    }
    setErrorMessage(errorDetails);
  };

  if (loggedIn) {
    return <div data-testid="welcome-message">Welcome! You are logged in.</div>;
  }

  return (
    <div>
      <h2>Login</h2>
      {errorMessage && <div className="error-message" data-testid="error-message">{errorMessage}</div>}
      <form onSubmit={handleSubmit} data-testid="login-form">
        <div>
          <label htmlFor="email">Email:</label>
          <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required data-testid="email-input" />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required data-testid="password-input" />
        </div>
        <button type="submit" data-testid="login-button">Login</button>
      </form>
    </div>
  );
};

export default Login;