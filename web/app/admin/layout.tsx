import Link from "next/link";
import { LogOut } from "lucide-react";
import { currentUser } from "@/lib/auth";
import { signOut } from "./actions";
import ThemeToggle from "@/components/ThemeToggle";

export const dynamic = "force-dynamic";

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const user = await currentUser();

  // The sign-in page lives under /admin too, and it has no session to draw a bar from.
  if (!user) return <>{children}</>;

  return (
    <>
      <header className="admin-bar">
        <Link className="logo" href="/admin">
          LEARN · EDITOR
        </Link>
        <nav>
          <Link href="/admin">Books</Link>
          <Link href="/admin/media">Media</Link>
          <Link href="/admin/archive">Archive</Link>
          <Link href="/">View site</Link>
        </nav>
        <span className="chip">{user}</span>
        <ThemeToggle />
        <form action={signOut}>
          <button className="btn" type="submit">
            <LogOut size={13} strokeWidth={1.7} /> Sign out
          </button>
        </form>
      </header>
      {children}
    </>
  );
}
