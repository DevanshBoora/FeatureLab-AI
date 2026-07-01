import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FeatureLab AI",
  description: "Enterprise Machine Learning Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} min-h-screen bg-background text-foreground antialiased`}>
        <div className="relative flex min-h-screen flex-col">
          <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 items-center">
              <div className="mr-4 flex">
                <a className="mr-6 flex items-center space-x-2" href="/">
                  <span className="hidden font-bold sm:inline-block">
                    FeatureLab AI
                  </span>
                </a>
                <nav className="flex items-center space-x-6 text-sm font-medium">
                  <a className="transition-colors hover:text-foreground/80 text-foreground/60" href="/dashboard">Dashboard</a>
                  <a className="transition-colors hover:text-foreground/80 text-foreground/60" href="/datasets">Datasets</a>
                  <a className="transition-colors hover:text-foreground/80 text-foreground/60" href="/experiments">Experiments</a>
                </nav>
              </div>
            </div>
          </header>
          <main className="flex-1">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
