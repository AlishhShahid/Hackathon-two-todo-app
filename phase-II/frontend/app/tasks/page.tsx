'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { TaskList } from '@/components/TaskList';
import { AddTaskForm } from '@/components/AddTaskForm';
import { LogoutButton } from '@/components/auth/LogoutButton';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { Task } from '@/types';

export default function TasksPage() {
  const { isAuthenticated, isLoading, userId, userEmail } = useAuth();
  const router = useRouter();
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Protected route - redirect unauthenticated to /login (T026)
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading while checking auth
  if (isLoading || !isAuthenticated || !userId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  // Handle new task created - refresh list (T049, T050)
  const handleTaskCreated = (_task: Task) => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with logout (T040) */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">My Tasks</h1>
            {userEmail && (
              <p className="text-sm text-gray-500">{userEmail}</p>
            )}
          </div>
          <LogoutButton />
        </div>
      </header>

      {/* Main content - responsive layout (T039) */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Add task form (T049) */}
        <div className="mb-8">
          <AddTaskForm userId={userId} onTaskCreated={handleTaskCreated} />
        </div>

        {/* Task list (T038) */}
        <TaskList userId={userId} refreshTrigger={refreshTrigger} />
      </main>
    </div>
  );
}
