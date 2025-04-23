import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import LoginForm from './components/form/loginForm/LoginForm.jsx';
import RegisterForm from './components/form/registerForm/RegisterForm.jsx';
import Dashboard from './components/dashboard/Dashboard.jsx';
import { useState } from 'react';


function App() {
  
  const [userId, setUserId] = useState(localStorage.getItem("userId"));
  const [username, setUsername] = useState(localStorage.getItem("username"));

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm onLogin={(id, name) => { setUserId(id); setUsername(name); }} />} />
        <Route path="/register" element={<RegisterForm onRegister={(id,name) => {setUserId(id); setUsername(name);}} />}/>
        <Route path="/dashboard" element={<Dashboard userId={userId} username={username} />} />
      </Routes>
  </Router>
);
}

export default App
