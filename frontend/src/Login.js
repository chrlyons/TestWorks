import React, { useState, useRef } from 'react';
import axios from 'axios';

const apiBaseUrl = process.env.REACT_APP_API_URL;

const InputField = ({ id, type, value, setValue, testId }) => (
  <div>
    <label htmlFor={id}>{id.charAt(0).toUpperCase() + id.slice(1)}:</label>
    <input data-testid={testId} id={id} onChange={(e) => setValue(e.target.value)} required type={type} value={value} />
  </div>
);

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const wsRef = useRef(null);

  const handleWebSocketConnect = () => {
    const token = localStorage.getItem('access_token');
    const wsUrl = `${apiBaseUrl.replace('http', 'ws')}/api/ws/${email}?access_token=${token}`;
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
      const { access_token, user_id } = response.data;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_id', user_id);
      setLoggedIn(true);
      setErrorMessage('');
      handleWebSocketConnect();
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

  const handleLogout = async () => {
    const user_id = localStorage.getItem('user_id');
    try {
      await axios.post(`${apiBaseUrl}/api/login/logout`, { user_id });
    } catch (error) {
      console.error('Logout error:', error);
    }
    if (wsRef.current) {
      wsRef.current.close();
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id');
    setLoggedIn(false);
  };

  if (loggedIn) {
    return (
      <div>
        <div data-testid="welcome-message">Welcome! You are logged in.</div>
        <button data-testid="logout-button" onClick={handleLogout}>Logout</button>
      </div>
    );
  }

  return (
    <div>
      <h2>Login</h2>
      {errorMessage && <div className="error-message" data-testid="error-message">{errorMessage}</div>}
      <form onSubmit={handleSubmit} data-testid="login-form">
        <InputField id="email" type="email" value={email} setValue={setEmail} testId="email-input" />
        <InputField id="password" type="password" value={password} setValue={setPassword} testId="password-input" />
        <button data-testid="login-button" type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;