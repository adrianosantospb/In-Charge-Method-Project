import { type FormEvent, useEffect, useState } from "react";
import { api, ApiError, type Task, type User } from "./api";

type Props = { user: User; onSignOut: () => void; onSessionEnded: () => void };

export function TaskList({ user, onSignOut, onSessionEnded }: Props) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listTasks()
      .then(setTasks)
      .catch((caught) => {
        if (sessionEnded(caught)) onSessionEnded();
        else setError("Could not load your tasks. Reload the page to try again.");
      });
  }, [onSessionEnded]);

  async function run(action: () => Promise<void>) {
    setError(null);
    try {
      await action();
    } catch (caught) {
      if (sessionEnded(caught)) onSessionEnded();
      else setError("That did not save. Try again.");
    }
  }

  function add(event: FormEvent) {
    event.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) return;
    run(async () => {
      const task = await api.createTask(trimmed);
      setTasks((current) => [...current, task]);
      setTitle("");
    });
  }

  const toggle = (task: Task) =>
    run(async () => {
      const saved = await api.updateTask(task.id, { done: !task.done });
      setTasks((current) => current.map((item) => (item.id === saved.id ? saved : item)));
    });

  const remove = (task: Task) =>
    run(async () => {
      await api.deleteTask(task.id);
      setTasks((current) => current.filter((item) => item.id !== task.id));
    });

  return (
    <section className="card">
      <header className="bar">
        <h1>Your tasks</h1>
        <span className="who">{user.email}</span>
        <button type="button" className="link" onClick={onSignOut}>
          Sign out
        </button>
      </header>
      <form className="add" onSubmit={add}>
        <label className="sr-only" htmlFor="new-task">
          New task
        </label>
        <input
          id="new-task"
          placeholder="What needs doing?"
          maxLength={200}
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
        <button type="submit">Add task</button>
      </form>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      {tasks.length === 0 ? (
        <p className="empty">No tasks yet. Add the first one above.</p>
      ) : (
        <ul className="tasks">
          {tasks.map((task) => (
            <li key={task.id} className={task.done ? "done" : undefined}>
              <label>
                <input type="checkbox" checked={task.done} onChange={() => toggle(task)} />
                {task.title}
              </label>
              <button
                type="button"
                className="link"
                aria-label={`Delete ${task.title}`}
                onClick={() => remove(task)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

// The session cookie expired or was removed: go back to the sign-in form.
function sessionEnded(error: unknown): boolean {
  return error instanceof ApiError && error.status === 401;
}
