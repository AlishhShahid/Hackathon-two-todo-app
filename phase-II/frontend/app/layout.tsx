import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/lib/auth-context';

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'Manage your tasks efficiently',
};

// Root layout with AuthProvider wrapper (T019)
// Note: suppressHydrationWarning on body prevents warnings from browser extensions
// that inject attributes (e.g., Grammarly, LastPass, translation tools)
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-gray-50" suppressHydrationWarning>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
