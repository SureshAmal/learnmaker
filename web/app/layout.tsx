import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Learn", template: "%s · Learn" },
  description: "Technical books, built from their sources.",
};

// The theme is read and applied before the first paint, so a dark reader never gets a
// white flash on navigation. It has to be inline and synchronous for that reason.
const THEME_BOOT = `(function(){try{
var t=localStorage.getItem('learn-theme');
if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
document.documentElement.setAttribute('data-theme',t);
}catch(e){document.documentElement.setAttribute('data-theme','light')}})()`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: THEME_BOOT }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
