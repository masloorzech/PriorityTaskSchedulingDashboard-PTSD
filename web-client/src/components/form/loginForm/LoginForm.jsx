import { useState } from 'react';
import { Link, useNavigate} from 'react-router-dom';
import './loginForm.css'

function LoginForm({onLogin}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try{
      const response = await fetch("http://127.0.0.1:5000/users/log_in",{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({username,password}),
      })

      const data = await response.json();

      if (response.ok){
        console.log('Login succesfully')
        onLogin(data.user_id, username);
        localStorage.setItem("userId", data.user_id);
        localStorage.setItem("username", username);
        navigate('/dashboard');

      }else{
        console.error('Login failend', data.error)
        alert(data.error)
      }
    }catch (error){
        console.error(error)
        alert('Failed to connect to server');
      }
    };

  return (
    <div className="login-form">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label htmlFor="username">Username:</label><br />
          <input
            type="text"
            id="username"
            placeholder='ex. pinky23'
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        
        <div>
          <label htmlFor="password">Password:</label><br />
          <input
            type="password"
            id="password"
            placeholder='ex. 12345'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Login</button>
      </form>

      <p style={{ marginTop: '1rem' }}>
        Don't have an account?{' '}
        <Link to="/register">Register</Link>
      </p>
    </div>
  );
}

export default LoginForm;
