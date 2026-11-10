import { useCallback, useEffect, useState } from "react";
import { api, ApiError, type User } from "./api";
import { SignIn } from "./SignIn";
import { TaskList } from "./TaskList";

export function App() {
  const [user, setUser] = useState<User | null>(null);
  const [checking, setChecking] = useState(true);
  const signedOut = useCallback(() => setUser(null), []);

  useEffect(() => {
    api
      .me()
      .then(setUser)
      .catch((error) => {
        if (!(error instanceof ApiError && error.status === 401)) console.error(error);
      })
      .finally(() => setChecking(false));
  }, []);

  if (checking) return <main className="page" aria-busy="true" />;

  return (
    <main className="page">
      {user ? (
        <TaskList
          user={user}
          onSessionEnded={signedOut}
          onSignOut={() => {
            // Forget the user even if the request fails; the cookie expires on its own.
            api.logout().catch(console.error).finally(signedOut);
          }}
        />
      ) : (
        <SignIn onSignedIn={setUser} />
      )}
    </main>
  );
}
