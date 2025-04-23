import { useState } from "react";
import './tasklist.css'

function Tasklist({ userId, tasklistName, tasks , setTasklists}) {
  const [newTaskTitle, setNewTaskTitle] = useState("");

  const createTask = async () => {
    if (newTaskTitle==""){
        alert("Please add taskname")
        return
    }
    const res = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists/${tasklistName}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTaskTitle })
    });
    if (res.status === 201) {
      setNewTaskTitle('');
      const updated = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`).then(r => r.json());
      setTasklists(updated);
    } else {
      alert("Failed to create task");
    }
  };

  return (
    <>
    <div className="tasklist_container">
      <div className="tasklist_header">
      <h3>{tasklistName}</h3>
      <div className = "tasklist_controls">
            <input
            placeholder="New task title"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            />
            <button onClick={createTask}>Add Task</button>
            <button className="delete_tasklist_button"
                onClick={
                    async () => {
                        const endpoint = `http://127.0.0.1:5000/tasks/${userId}/tasklists/${tasklistName}`;
                        await fetch(endpoint, { method: 'DELETE' });
                        const updated = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`).then(r => r.json());
                        setTasklists(updated);
                    }
                }
              >⨉</button>
              </div>
        </div>

      <div className="tasklist">
        <ul>
          {tasks.map((task) => (
            <li key={task.title}>
                <div className="tasklist_row">
                    <input className="pretty_checkbox"
                        type="checkbox"
                        checked={task.done}
                        onChange={async () => {
                        const endpoint = `http://127.0.0.1:5000/tasks/${userId}/tasklists/${tasklistName}/tasks/${task.title}/${task.done ? "undone" : "done"}`;
                        await fetch(endpoint, { method: 'PATCH' });
                        const updated = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`).then(r => r.json());
                        setTasklists(updated);
                        }}
                    />
                    <div className="task_title">{task.title}</div>
                    <button className="delete_task_button"
                        onClick={
                            async () => {
                                const endpoint = `http://127.0.0.1:5000/tasks/${userId}/tasklists/${tasklistName}/tasks/${task.title}`;
                                await fetch(endpoint, { method: 'DELETE' });
                                const updated = await fetch(`http://127.0.0.1:5000/tasks/${userId}/tasklists`).then(r => r.json());
                                setTasklists(updated);
                            }
                        }
                    >⨉
                    </button>
              </div>
            </li>
            
          ))}
        </ul>
      </div>
      </div>
    </>
  );
}

export default Tasklist;
