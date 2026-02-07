// Task entity - represents a user's todo item
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
  due_date?: string;   // ISO 8601 datetime (optional)
}

// Request DTOs
export interface CreateTaskRequest {
  title: string;          // Required, max 255 chars
  description?: string;   // Optional
  due_date?: string;      // Optional ISO 8601 datetime
}

export interface UpdateTaskRequest {
  title?: string;         // Optional, max 255 chars
  description?: string;   // Optional
  due_date?: string;      // Optional ISO 8601 datetime
}

// API Error Response
export interface ApiError {
  error: string;    // Error code
  message: string;  // Human-readable message
}

// Authentication State
export interface AuthState {
  isAuthenticated: boolean;
  token: string | null;      // JWT token (in-memory only)
  userId: number | null;     // Extracted from token
  userEmail: string | null;  // Extracted from token
}

// UI State Types
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface TaskListState {
  tasks: Task[];
  loadingState: LoadingState;
  error: string | null;
}

export interface TaskItemState {
  isEditing: boolean;
  isToggling: boolean;
  isDeleting: boolean;
  editError: string | null;
}
