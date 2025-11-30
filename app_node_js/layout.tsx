// app/layout.tsx
import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "StegVerse CFP Lab",
  description: "Playoff scenarios, chaos brackets, and TTU paths to glory.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
          <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
            <a href="/" className="font-semibold tracking-wide">
              STEGVERSE • CFP LAB
            </a>
            <nav className="flex gap-4 text-sm">
              <a href="/cfp" className="hover:text-emerald-300">
                Today&apos;s CFP
              </a>
              <a href="/ttu" className="hover:text-emerald-300">
                TTU Paths
              </a>
            </nav>
          </div>
        </header>

        <main className="mx-auto max-w-4xl px-4 py-8">{children}</main>

        <footer className="border-t border-slate-800 bg-slate-950/80 mt-12">
          <div className="mx-auto max-w-4xl px-4 py-4 text-xs text-slate-400">
            Unofficial fan analysis for entertainment only. Not affiliated with
            the College Football Playoff, NCAA, or Texas Tech University.
          </div>
        </footer>
      </body>
    </html>
  );
}
