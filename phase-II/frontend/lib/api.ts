import { Task, CreateTaskRequest, UpdateTaskRequest, ApiError } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Token getter - will be set by auth context
let getToken: (() => string | null) | null = null;
let onUnauthorized: (() => void) | null = null;

// Configure auth handlers (called by AuthProvider)
export function configureAuth(
  tokenGetter: () => string | null,
  unauthorizedHandler: () => void
) {
  getToken = tokenGetter;
  onUnauthorized = unauthorizedHandler;
}

// Base fetch wrapper with auth and error handling
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken?.();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Attach Authorization header if token exists (FR-005)
  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle 401 Unauthorized - redirect to login (FR-006)
  if (response.status === 401) {
    onUnauthorized?.();
    throw new Error('Unauthorized - please log in again');
  }

  // Handle error responses
  if (!response.ok) {
    let errorData: ApiError;
    try {
      errorData = await response.json();
    } catch {
      errorData = {
        error: 'unknown_error',
        message: 'An unexpected error occurred',
      };
    }
    throw new Error(errorData.message || 'Request failed');
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// API methods - typed for all endpoints (T011)
// Note: userId is kept for interface compatibility but not used in URL
// The backend extracts user ID from the JWT token

export async function getTasks(userId: number): Promise<Task[]> {
  void userId; // User ID extracted from JWT token on backend
  return apiFetch<Task[]>(`/api/tasks`);
}

export async function getTask(userId: number, taskId: number): Promise<Task> {
  void userId; // User ID extracted from JWT token on backend
  return apiFetch<Task>(`/api/tasks/${taskId}`);
}

export async function createTask(
  userId: number,
  data: CreateTaskRequest
): Promise<Task> {
  void userId; // User ID extracted from JWT token on backend
  return apiFetch<Task>(`/api/tasks`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateTask(
  userId: number,
  taskId: number,
  data: UpdateTaskRequest
): Promise<Task> {
  void userId; // User ID extracted from JWT token on backend
  return apiFetch<Task>(`/api/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteTask(
  userId: number,
  taskId: number
): Promise<void> {
  void userId; // User ID extracted from JWT token on backend
  return apiFetch<void>(`/api/tasks/${taskId}`, {
    method: 'DELETE',
  });
}

export async function toggleComplete(
  userId: number,
  taskId: number
): Promise<Task> {
  void userId; // User ID extracted from JWT token on backend
  return apiFetch<Task>(`/api/tasks/${taskId}/complete`, {
    method: 'PATCH',
  });
}

// Export API object for convenience
export const api = {
  getTasks,
  getTask,
  createTask,
  updateTask,
  deleteTask,
  toggleComplete,
  configureAuth,
};
