'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/lib/auth-context';
import { RegisterForm } from '@/components/auth/RegisterForm';
import { LoadingSpinner } from '@/components/LoadingSpinner';

export default function RegisterPage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  // Redirect authenticated users from /register to /tasks
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/tasks');
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading while checking auth state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  // Don't render register form if already authenticated
  if (isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Back to Home link */}
        <Link
          href="/"
          className="inline-flex items-center text-sm text-blue-600 hover:text-blue-500"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Home
        </Link>

        <div>
          <h1 className="text-center text-3xl font-extrabold text-gray-900">
            Todo App
          </h1>
          <h2 className="mt-2 text-center text-lg text-gray-600">
            Create your account
          </h2>
        </div>
        <RegisterForm />
      </div>
    </div>
  );
}
