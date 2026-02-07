# Quickstart: Frontend UI & API Integration

**Feature Branch**: `003-frontend-todo-ui`
**Date**: 2026-02-06

## Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn
- Backend API running at `http://localhost:8000` (Spec 001)
- Better Auth configured (Spec 002)

## Project Setup

### 1. Create Next.js Application

```bash
npx create-next-app@latest frontend --typescript --app --tailwind --eslint
cd frontend
```

### 2. Environment Configuration

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Directory Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout with AuthProvider
│   ├── page.tsx             # Landing/redirect page
│   ├── login/
│   │   └── page.tsx         # Login page
│   └── tasks/
│       └── page.tsx         # Protected tasks page
├── components/
│   ├── TaskList.tsx         # Task list container
│   ├── TaskItem.tsx         # Individual task display
│   ├── AddTaskForm.tsx      # Task creation form
│   └── auth/
│       ├── LoginForm.tsx    # Login UI
│       └── LogoutButton.tsx # Logout control
├── lib/
│   ├── api.ts               # Centralized API client
│   └── auth-context.tsx     # Authentication context
└── types/
    └── index.ts             # TypeScript interfaces
```

## Development Commands

```bash
# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

## Testing the Setup

1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open `http://localhost:3000`
4. Verify login page appears for unauthenticated users

## API Client Usage

```typescript
import { api } from '@/lib/api';

// List tasks (token auto-attached)
const tasks = await api.getTasks(userId);

// Create task
const newTask = await api.createTask(userId, { title: 'New task' });

// Toggle completion
const updated = await api.toggleComplete(userId, taskId);
```

## Common Issues

| Issue | Solution |
|-------|----------|
| CORS errors | Ensure backend has CORS configured for `http://localhost:3000` |
| 401 on API calls | Check token is being passed; verify with backend auth |
| Tasks not loading | Verify backend is running and accessible |

## Related Documentation

- [Spec](./spec.md) - Feature requirements
- [Research](./research.md) - Technical decisions
- [Data Model](./data-model.md) - TypeScript interfaces
- [Plan](./plan.md) - Implementation phases
