import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";

export const SESSION_COOKIE = "learn_session";
const MAX_AGE = 60 * 60 * 24 * 14; // two weeks

function secret() {
  const value = process.env.SESSION_SECRET;
  if (!value || value.length < 24) {
    throw new Error("SESSION_SECRET must be set to a long random string");
  }
  return new TextEncoder().encode(value);
}

/**
 * Credentials are compared as plain text against the environment, by request — there is
 * no hash and no user table. The consequence is that anyone who can read the environment
 * (a leaked deploy log, a shared dashboard account, a stolen `.env`) can sign in as the
 * admin, so keep ADMIN_PASSWORD out of the repo and rotate it if it is ever exposed.
 */
export function checkCredentials(user: string, password: string): boolean {
  const expectedUser = process.env.ADMIN_USER ?? "";
  const expectedPassword = process.env.ADMIN_PASSWORD ?? "";
  if (!expectedUser || !expectedPassword) return false;
  return user === expectedUser && password === expectedPassword;
}

/** The session itself is signed, so the cookie cannot be forged even though the password is plain. */
export async function issueSession(user: string) {
  const token = await new SignJWT({ user })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(`${MAX_AGE}s`)
    .sign(secret());

  const jar = await cookies();
  jar.set(SESSION_COOKIE, token, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: MAX_AGE,
  });
}

export async function clearSession() {
  const jar = await cookies();
  jar.delete(SESSION_COOKIE);
}

export async function verifySession(token: string | undefined): Promise<string | null> {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, secret());
    return typeof payload.user === "string" ? payload.user : null;
  } catch {
    return null;
  }
}

/** The current admin, or null. Server components and server actions both use this. */
export async function currentUser(): Promise<string | null> {
  const jar = await cookies();
  return verifySession(jar.get(SESSION_COOKIE)?.value);
}

/** Throws unless a valid session is present — the guard on every mutating action. */
export async function requireAdmin(): Promise<string> {
  const user = await currentUser();
  if (!user) throw new Error("Not signed in");
  return user;
}
