'use client';

import { useState, useEffect, useCallback } from 'react';
import { Task, LoadingState } from '@/types';
import { api } from '@/lib/api';
import { TaskItem } from './TaskItem';
import { LoadingSpinner } from './LoadingSpinner';
import { ErrorMessage } from './ErrorMessage';

interface TaskListProps {
  userId: number;
  refreshTrigger?: number;
}

export function TaskList({ userId, refreshTrigger }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loadingState, setLoadingState] = useState<LoadingState>('idle');
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks on mount and when refreshTrigger changes (T030)
  const fetchTasks = useCallback(async () => {
    setLoadingState('loading');
    setError(null);
    try {
      const fetchedTasks = await api.getTasks(userId);
      setTasks(fetchedTasks);
      setLoadingState('success');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
      setLoadingState('error');
    }
  }, [userId]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks, refreshTrigger]);

  // Handle task updated (T037, T054)
  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks((prev) =>
      prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
    );
  };

  // Handle task deleted (T072)
  const handleTaskDeleted = (taskId: number) => {
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  };

  // Loading state (T031)
  if (loadingState === 'loading' && tasks.length === 0) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  // Error state with retry (T033)
  if (loadingState === 'error') {
    return (
      <ErrorMessage
        message={error || 'Failed to load tasks'}
        onRetry={fetchTasks}
      />
    );
  }

  // Empty state (T032)
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-4 text-lg font-medium text-gray-900">No tasks yet</h3>
        <p className="mt-2 text-sm text-gray-500">
          Get started by creating your first task above.
        </p>
      </div>
    );
  }

  // Task list rendering (T037)
  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          userId={userId}
          onTaskUpdated={handleTaskUpdated}
          onTaskDeleted={handleTaskDeleted}
        />
      ))}
    </div>
  );
}
