'use client';

import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  ReactNode,
} from 'react';
import { useRouter } from 'next/navigation';
import { configureAuth } from './api';
import { AuthState } from '@/types';

interface AuthContextType extends AuthState {
  login: (token: string) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

// Parse JWT token to extract user info (T018)
function parseJwtPayload(token: string): { userId: number; email: string } | null {
  try {
    const base64Payload = token.split('.')[1];
    const payload = JSON.parse(atob(base64Payload));
    return {
      userId: payload.sub || payload.user_id || payload.id,
      email: payload.email || '',
    };
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();

  // Track if component has mounted (prevents hydration mismatch)
  const [isMounted, setIsMounted] = useState(false);

  // In-memory token storage (T016) - most secure option per research.md
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    token: null,
    userId: null,
    userEmail: null,
  });

  // Login function (T017)
  const login = useCallback((token: string) => {
    const payload = parseJwtPayload(token);
    if (payload) {
      setAuthState({
        isAuthenticated: true,
        token,
        userId: payload.userId,
        userEmail: payload.email,
      });
    }
  }, []);

  // Logout function (T017)
  const logout = useCallback(() => {
    setAuthState({
      isAuthenticated: false,
      token: null,
      userId: null,
      userEmail: null,
    });
    router.push('/login');
  }, [router]);

  // Set mounted state after hydration completes
  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Configure API client with auth handlers (T028)
  useEffect(() => {
    if (isMounted) {
      configureAuth(
        () => authState.token,
        () => logout()
      );
    }
  }, [authState.token, logout, isMounted]);

  // Provide consistent initial state for SSR and first client render
  const contextValue: AuthContextType = {
    ...authState,
    login,
    logout,
    isLoading: !isMounted,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
