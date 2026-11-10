// Calls to the backend. The session lives in an HttpOnly cookie that the browser
// sends on its own; this code never sees the token.

export type User = { id: string; email: string };
export type Task = { id: string; title: string; done: boolean };

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...init,
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", ...init.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = typeof body?.detail === "string" ? body.detail : "Something went wrong. Try again.";
    throw new ApiError(response.status, detail);
  }
  return response.status === 204 ? (undefined as T) : ((await response.json()) as T);
}

const json = (body: unknown) => JSON.stringify(body);

export const api = {
  me: () => request<User>("/auth/me"),
  register: (email: string, password: string) =>
    request<User>("/auth/register", { method: "POST", body: json({ email, password }) }),
  login: (email: string, password: string) =>
    request<User>("/auth/login", { method: "POST", body: json({ email, password }) }),
  logout: () => request<void>("/auth/logout", { method: "POST" }),
  listTasks: () => request<Task[]>("/tasks"),
  createTask: (title: string) => request<Task>("/tasks", { method: "POST", body: json({ title }) }),
  updateTask: (id: string, changes: Partial<Pick<Task, "title" | "done">>) =>
    request<Task>(`/tasks/${id}`, { method: "PATCH", body: json(changes) }),
  deleteTask: (id: string) => request<void>(`/tasks/${id}`, { method: "DELETE" }),
};
