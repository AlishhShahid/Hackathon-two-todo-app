'use client';

import { useState, FormEvent } from 'react';
import { api } from '@/lib/api';
import { Task } from '@/types';
import { LoadingSpinner } from './LoadingSpinner';

interface AddTaskFormProps {
  userId: number;
  onTaskCreated: (task: Task) => void;
}

export function AddTaskForm({ userId, onTaskCreated }: AddTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Client-side validation (T043)
  const isValid = title.trim() !== '';

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation check (FR-011)
    if (!isValid) {
      setError('Please enter a task title');
      return;
    }

    setIsLoading(true);

    try {
      // Create task API call (T045)
      const newTask = await api.createTask(userId, {
        title: title.trim(),
        description: description.trim() || undefined,
        due_date: dueDate || undefined,
      });
      onTaskCreated(newTask);
      // Form reset on success (T047)
      setTitle('');
      setDescription('');
      setDueDate('');
      setIsExpanded(false);
    } catch (err) {
      // Error display (T046)
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-lg shadow-sm p-4">
      <div className="flex gap-3">
        <div className="flex-1">
          <label htmlFor="new-task-title" className="sr-only">
            New task title
          </label>
          <input
            id="new-task-title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Add a new task..."
            className="w-full px-4 py-2 min-h-[44px] border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={isLoading}
          />
        </div>
        <button
          type="button"
          onClick={() => setIsExpanded(!isExpanded)}
          className="min-w-[44px] min-h-[44px] px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors flex items-center justify-center"
          title={isExpanded ? 'Hide details' : 'Add details'}
        >
          <svg
            className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <button
          type="submit"
          disabled={isLoading || !isValid}
          className="min-w-[44px] min-h-[44px] px-6 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed rounded-lg shadow-sm transition-colors flex items-center justify-center"
        >
          {isLoading ? (
            <LoadingSpinner size="small" />
          ) : (
            'Add'
          )}
        </button>
      </div>

      {/* Expanded fields for description and due date */}
      {isExpanded && (
        <div className="mt-4 space-y-4">
          <div>
            <label htmlFor="new-task-description" className="block text-sm font-medium text-gray-700 mb-1">
              Description (optional)
            </label>
            <textarea
              id="new-task-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add more details about this task..."
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              disabled={isLoading}
            />
          </div>
          <div>
            <label htmlFor="new-task-due-date" className="block text-sm font-medium text-gray-700 mb-1">
              Due Date (optional)
            </label>
            <input
              id="new-task-due-date"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-4 py-2 min-h-[44px] border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              disabled={isLoading}
            />
          </div>
        </div>
      )}

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}
    </form>
  );
}
