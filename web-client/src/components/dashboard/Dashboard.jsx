import { useEffect, useState } from 'react';
import './dashboard.css';
import Tasklist from './tasklist/Tasklist.jsx';
import { Link, useNavigate} from 'react-router-dom';


function Dashboard({ userId, username }) {
  const [tasklists, setTasklists] = useState([]);
  const [newListTitle, setNewListTitle] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`)
      .then(res => res.json())
      .then(data => setTasklists(data))
      .catch(err => alert("Failed to load tasklists"));
  }, [userId]);

  const createTaskList = async () => {
    if (newListTitle==""){
      alert("Please add tasklist name")
      return
  }
    const res = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newListTitle })
    });
    if (res.status === 201) {
      setNewListTitle('');
      const updated = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`).then(r => r.json());
      setTasklists(updated);
    } else {
      alert("Failed to create list");
    }
  };

  return (
    <div className='content'>
      <div className='title_segment'>
        <h2>Welcome, {username}</h2>
        <button className='logout_button'
        onClick={() => {
          localStorage.clear();
          navigate("/");
        } }
        >Log out</button>
      </div>
      

      <div className='content_fields'>
        <input
          placeholder="New list title"
          value={newListTitle}
          onChange={(e) => setNewListTitle(e.target.value)}
        />
        <button onClick={createTaskList}>Add List</button>
      </div>

      {tasklists.map((list) => (
        <Tasklist key={list.title} userId={userId} tasklistName={list.title} tasks={list.tasks} setTasklists={setTasklists}  />
      ))}
    </div>
  );
}

export default Dashboard;
