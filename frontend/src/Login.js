import React, { useState, useRef } from 'react';
import axios from 'axios';

const apiBaseUrl = process.env.REACT_APP_API_URL;

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const wsRef = useRef(null);

  const handleWebSocketConnect = () => {
    const token = localStorage.getItem('token');
    const wsUrl = `${apiBaseUrl.replace('http', 'ws')}/api/ws/${email}?token=${token}`;
    wsRef.current = new WebSocket(wsUrl); // Assign to ref

    wsRef.current.onopen = () => console.log('WebSocket connected');
    wsRef.current.onmessage = (message) => {
      try {
        const data = JSON.parse(message.data);
        console.log('Received data:', data);
      } catch (e) {
        console.error('Error parsing message data:', e);
      }
    };
    wsRef.current.onclose = () => console.log('WebSocket disconnected');
    wsRef.current.onerror = (error) => console.error('WebSocket error:', error);
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
          <input data-testid="email-input" id="email" onChange={(e) => setEmail(e.target.value)} required type="email" value={email}/>
        </div>
        <div>
        <label htmlFor="password">Password:</label>
          <input data-testid="password-input" id="password" onChange={(e) => setPassword(e.target.value)} required
                 type="password" value={password}/>
        </div>
        <button data-testid="login-button" type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
