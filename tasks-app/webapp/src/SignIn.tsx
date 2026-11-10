import { type FormEvent, useState } from "react";
import { api, ApiError, type User } from "./api";

type Mode = "signIn" | "register";

export function SignIn({ onSignedIn }: { onSignedIn: (user: User) => void }) {
  const [mode, setMode] = useState<Mode>("signIn");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const user =
        mode === "signIn" ? await api.login(email, password) : await api.register(email, password);
      onSignedIn(user);
    } catch (caught) {
      setError(caught instanceof ApiError ? errorText(caught) : "Could not reach the server.");
    } finally {
      setBusy(false);
    }
  }

  const title = mode === "signIn" ? "Sign in" : "Create an account";

  return (
    <form className="card" onSubmit={submit}>
      <h1>{title}</h1>
      <label>
        Email
        <input
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
      </label>
      <label>
        Password
        <input
          type="password"
          autoComplete={mode === "signIn" ? "current-password" : "new-password"}
          minLength={12}
          required
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
      </label>
      {mode === "register" && <p className="hint">Use at least 12 characters.</p>}
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      <button type="submit" disabled={busy}>
        {title}
      </button>
      <button
        type="button"
        className="link"
        onClick={() => {
          setMode(mode === "signIn" ? "register" : "signIn");
          setError(null);
        }}
      >
        {mode === "signIn" ? "Create an account instead" : "I already have an account"}
      </button>
    </form>
  );
}

function errorText(error: ApiError): string {
  if (error.status === 422) return "Check the email, and use a password of at least 12 characters.";
  return error.message;
}
