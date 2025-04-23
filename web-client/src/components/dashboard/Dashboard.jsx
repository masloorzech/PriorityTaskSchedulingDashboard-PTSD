import { useEffect, useState } from 'react';

function Dashboard({ userId, username }) {
  const [tasklists, setTasklists] = useState([]);
  const [newListTitle, setNewListTitle] = useState('');

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`)
      .then(res => res.json())
      .then(data => setTasklists(data))
      .catch(err => alert("Failed to load tasklists"));
  }, [userId]);

  const createTaskList = async () => {
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
    <div>
      <h2>Welcome, {username}</h2>

      <div>
        <input
          placeholder="New list title"
          value={newListTitle}
          onChange={(e) => setNewListTitle(e.target.value)}
        />
        <button onClick={createTaskList}>Add List</button>
      </div>

      {tasklists.map((list) => (
        <div key={list.title}>
          <h3>{list.title}</h3>
          <ul>
            {list.tasks.map((task) => (
              <li key={task.title}>
                <input
                  type="checkbox"
                  checked={task.done}
                  onChange={async () => {
                    const endpoint = `http://127.0.0.1:5000/tasks/${userId}/tasklists/${list.title}/tasks/${task.title}/${task.done ? "undone" : "done"}`
                    await fetch(endpoint, { method: 'PATCH' });
                    // reload lists
                    const updated = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`).then(r => r.json());
                    setTasklists(updated);
                  }}
                />
                {task.title}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;
