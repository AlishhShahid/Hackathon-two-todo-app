'use client';

import { useAuth } from '@/lib/auth-context';

interface LogoutButtonProps {
  className?: string;
}

export function LogoutButton({ className = '' }: LogoutButtonProps) {
  const { logout } = useAuth();

  return (
    <button
      onClick={logout}
      className={`min-w-[44px] min-h-[44px] px-4 py-2 text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 border border-gray-300 rounded-md shadow-sm transition-colors ${className}`}
      type="button"
    >
      Sign out
    </button>
  );
}
