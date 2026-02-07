'use client';

import { useState } from 'react';
import { Task } from '@/types';
import { api } from '@/lib/api';
import { LoadingSpinner } from './LoadingSpinner';

interface TaskItemProps {
  task: Task;
  userId: number;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}

// Format date for display
function formatDate(dateString: string | null | undefined): string {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

// Check if date is overdue
function isOverdue(dateString: string | null | undefined): boolean {
  if (!dateString) return false;
  const dueDate = new Date(dateString);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return dueDate < today;
}

export function TaskItem({ task, userId, onTaskUpdated, onTaskDeleted }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [editDueDate, setEditDueDate] = useState(task.due_date ? task.due_date.split('T')[0] : '');
  const [editError, setEditError] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Toggle completion (US3: T051-T057)
  const handleToggle = async () => {
    if (isToggling) return;
    setIsToggling(true);
    try {
      const updated = await api.toggleComplete(userId, task.id);
      onTaskUpdated(updated);
    } catch (err) {
      setEditError(err instanceof Error ? err.message : 'Failed to update task');
    } finally {
      setIsToggling(false);
    }
  };

  // Inline editing (US4: T058-T066)
  const handleSaveEdit = async () => {
    if (!editTitle.trim()) {
      setEditError('Title cannot be empty');
      return;
    }
    setEditError(null);
    try {
      const updated = await api.updateTask(userId, task.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
        due_date: editDueDate || undefined,
      });
      onTaskUpdated(updated);
      setIsEditing(false);
    } catch (err) {
      setEditError(err instanceof Error ? err.message : 'Failed to update task');
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setEditDueDate(task.due_date ? task.due_date.split('T')[0] : '');
    setEditError(null);
    setIsEditing(false);
  };

  // Delete with confirmation (US5: T067-T074)
  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await api.deleteTask(userId, task.id);
      onTaskDeleted(task.id);
    } catch (err) {
      setEditError(err instanceof Error ? err.message : 'Failed to delete task');
      setShowDeleteConfirm(false);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="flex items-center gap-3 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
      {/* Completion checkbox (T035, T056) */}
      <button
        onClick={handleToggle}
        disabled={isToggling}
        className="flex-shrink-0 w-11 h-11 flex items-center justify-center rounded-md hover:bg-gray-100 disabled:opacity-50"
        aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
      >
        {isToggling ? (
          <LoadingSpinner size="small" />
        ) : (
          <div
            className={`w-6 h-6 border-2 rounded-md flex items-center justify-center ${
              task.completed
                ? 'bg-blue-600 border-blue-600'
                : 'border-gray-300'
            }`}
          >
            {task.completed && (
              <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </div>
        )}
      </button>

      {/* Task content with editing (T034, T036, T060) */}
      <div className="flex-1 min-w-0">
        {isEditing ? (
          <div className="flex flex-col gap-3">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              placeholder="Task title"
              className="w-full px-3 py-2 min-h-[44px] border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              autoFocus
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              placeholder="Description (optional)"
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
            <input
              type="date"
              value={editDueDate}
              onChange={(e) => setEditDueDate(e.target.value)}
              className="w-full px-3 py-2 min-h-[44px] border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {editError && (
              <p className="text-sm text-red-600">{editError}</p>
            )}
            <div className="flex gap-2">
              <button
                onClick={handleSaveEdit}
                className="min-h-[44px] px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
              >
                Save
              </button>
              <button
                onClick={handleCancelEdit}
                className="min-h-[44px] px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div>
            <span
              className={`block ${
                task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
              }`}
              title={task.title}
            >
              {task.title}
            </span>
            {task.description && (
              <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
            <div className="mt-2 flex items-center gap-3 text-xs">
              {task.due_date && (
                <span
                  className={`flex items-center gap-1 ${
                    task.completed
                      ? 'text-gray-400'
                      : isOverdue(task.due_date)
                      ? 'text-red-600 font-medium'
                      : 'text-gray-500'
                  }`}
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {isOverdue(task.due_date) && !task.completed ? 'Overdue: ' : 'Due: '}
                  {formatDate(task.due_date)}
                </span>
              )}
              <span className="text-gray-400">
                Created: {formatDate(task.created_at)}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Action buttons (T059, T067) */}
      {!isEditing && (
        <div className="flex gap-2 flex-shrink-0">
          <button
            onClick={() => setIsEditing(true)}
            className="min-w-[44px] min-h-[44px] p-2 text-gray-600 hover:bg-gray-100 rounded-md"
            aria-label="Edit task"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>

          {showDeleteConfirm ? (
            <div className="flex gap-2">
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="min-w-[44px] min-h-[44px] px-3 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 disabled:opacity-50 rounded-md"
              >
                {isDeleting ? <LoadingSpinner size="small" /> : 'Delete'}
              </button>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="min-w-[44px] min-h-[44px] px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                Cancel
              </button>
            </div>
          ) : (
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="min-w-[44px] min-h-[44px] p-2 text-gray-600 hover:bg-red-50 hover:text-red-600 rounded-md"
              aria-label="Delete task"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}
        </div>
      )}

      {/* Error display */}
      {editError && !isEditing && (
        <p className="text-sm text-red-600">{editError}</p>
      )}
    </div>
  );
}
