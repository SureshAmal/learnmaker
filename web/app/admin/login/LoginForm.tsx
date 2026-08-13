"use client";

import { useActionState } from "react";
import { LogIn } from "lucide-react";
import { signIn } from "../actions";

export default function LoginForm({ next }: { next: string }) {
  const [state, action, pending] = useActionState(signIn, undefined);

  return (
    <div className="login">
      <form action={action}>
        <h1>Editor</h1>
        <p>Sign in to write.</p>

        {state?.error ? <p className="notice bad">{state.error}</p> : null}

        <input type="hidden" name="next" value={next} />
        <label className="field">
          <span>Username</span>
          <input name="user" autoComplete="username" autoFocus required />
        </label>
        <label className="field">
          <span>Password</span>
          <input name="password" type="password" autoComplete="current-password" required />
        </label>

        <button className="btn primary" type="submit" disabled={pending}>
          <LogIn size={13} strokeWidth={1.9} /> {pending ? "Checking…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
