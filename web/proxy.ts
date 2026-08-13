import { NextResponse, type NextRequest } from "next/server";
import { jwtVerify } from "jose";
import { SESSION_COOKIE } from "@/lib/auth";

/**
 * Nothing under /admin or /api/admin is reachable without a valid session cookie. The
 * check runs before any page or route handler is invoked, so an unsigned request never
 * reaches the database. (`proxy` is Next 16's name for what used to be `middleware`.)
 */
export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const token = request.cookies.get(SESSION_COOKIE)?.value;
  let signedIn = false;
  if (token && process.env.SESSION_SECRET) {
    try {
      await jwtVerify(token, new TextEncoder().encode(process.env.SESSION_SECRET));
      signedIn = true;
    } catch {
      signedIn = false;
    }
  }

  if (pathname === "/admin/login") {
    return signedIn ? NextResponse.redirect(new URL("/admin", request.url)) : NextResponse.next();
  }

  if (signedIn) return NextResponse.next();

  if (pathname.startsWith("/api/")) {
    return NextResponse.json({ error: "Not signed in" }, { status: 401 });
  }

  const login = new URL("/admin/login", request.url);
  login.searchParams.set("next", pathname);
  return NextResponse.redirect(login);
}

export const config = {
  matcher: ["/admin/:path*", "/api/admin/:path*", "/api/upload"],
};
