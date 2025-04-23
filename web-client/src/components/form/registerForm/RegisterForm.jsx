import { useState } from 'react';
import { Link, useNavigate} from 'react-router-dom';

import './registerForm.css';

function RegisterForm({onRegister}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [repeated_password, setRepeatedPassword] = useState('');
  const navigate = useNavigate();


  const handleRegister = async (e) => {
    e.preventDefault();

    if (password !== repeated_password){
        alert('Passwords are not the same');
        return
    }
    try{
        const response = await fetch("http://127.0.0.1:5000/users/register", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username, password})
        })

        const data = await response.json();
        if (response.ok){
            console.log('Registered succesfully')
            navigate('/')
            alert('User registered succesfuly, pleaste log in')
        }else {
            console.error('Register failed', data.error)
            alert(data.error)
        }

    }catch(error){
        console.error(error)
        alert('Failed to connect to server');
    }
  };

  return (
    <div className="register-form">
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div>
          <label>Username:</label><br />
          <input
            type="username"
            placeholder='ex. pinky21@'
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label><br />
          <input
            type="password"
            placeholder='ex. 12345'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Repeat password:</label><br />
          <input
            type="password"
            placeholder='ex. 12345'
            value={repeated_password}
            onChange={(e) => setRepeatedPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>

      <p style={{ marginTop: '1rem' }}>
        Already have an account?{' '}
        <Link to="/">Login</Link>
      </p>
    </div>
  );
}

export default RegisterForm;
