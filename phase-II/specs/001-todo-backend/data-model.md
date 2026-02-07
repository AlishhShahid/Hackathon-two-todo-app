# Data Model: Database & Backend Infrastructure for Todo App

## Overview
This document defines the database schema and entity relationships for the Todo application backend. All models are implemented using SQLModel to ensure type safety and database compatibility.

## Entities

### 1. User Entity

**Entity Name**: User
**Description**: Represents a registered user in the system with unique identification and authentication information.

**Fields**:
- `id` (Integer, Primary Key, Auto-increment): Unique identifier for the user
- `email` (String, Unique, Not Null): User's email address for identification
- `password_hash` (String, Not Null): Hashed password for authentication
- `first_name` (String, Optional): User's first name
- `last_name` (String, Optional): User's last name
- `created_at` (DateTime, Not Null): Timestamp when the user account was created
- `updated_at` (DateTime, Not Null): Timestamp when the user account was last updated
- `is_active` (Boolean, Not Null, Default: True): Flag indicating if the user account is active

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password hash must not be empty
- Created_at timestamp is set automatically on creation
- Updated_at timestamp is updated automatically on modification

### 2. Task Entity

**Entity Name**: Task
**Description**: Represents a todo item that belongs to a specific user with title, description, and completion status.

**Fields**:
- `id` (Integer, Primary Key, Auto-increment): Unique identifier for the task
- `user_id` (Integer, Foreign Key, Not Null): Reference to the user who owns this task
- `title` (String, Not Null): Brief title or description of the task
- `description` (String, Optional): Detailed description of what needs to be done
- `completed` (Boolean, Not Null, Default: False): Flag indicating if the task is completed
- `created_at` (DateTime, Not Null): Timestamp when the task was created
- `updated_at` (DateTime, Not Null): Timestamp when the task was last modified
- `due_date` (DateTime, Optional): Optional deadline for the task

**Validation Rules**:
- Title must not be empty
- User_id must reference an existing user
- Created_at timestamp is set automatically on creation
- Updated_at timestamp is updated automatically on modification
- Completed status can be toggled by the user

## Relationships

### User-Task Relationship
- **Relationship Type**: One-to-Many (One User can have Many Tasks)
- **Cardinality**: 1:N
- **Foreign Key**: Task.user_id references User.id
- **Constraint**: ON DELETE CASCADE - When a user is deleted, all their tasks are automatically deleted
- **Access Pattern**: From User, access tasks via "user.tasks" relationship

## State Transitions

### Task Completion State Transition
- **Initial State**: completed = False
- **Trigger**: PATCH /api/{user_id}/tasks/{id}/complete endpoint called
- **Transition**: completed = !completed (toggle current value)
- **Result**: Task completion status is inverted

## Indexes

### 1. User Table Indexes
- Primary Key: id (Auto-indexed)
- Unique Index: email
- Index: is_active (for filtering active users)

### 2. Task Table Indexes
- Primary Key: id (Auto-indexed)
- Foreign Key Index: user_id (for efficient user-based queries)
- Index: completed (for filtering completed/incomplete tasks)
- Index: created_at (for chronological sorting)

## Constraints

### 1. User Table Constraints
- NOT NULL constraints on required fields
- UNIQUE constraint on email field
- CHECK constraint on email format (valid email pattern)

### 2. Task Table Constraints
- NOT NULL constraints on required fields
- FOREIGN KEY constraint linking user_id to User.id
- Length constraints on title (max 255 characters)

## Default Values

### 1. User Defaults
- `is_active`: True
- `created_at`: Current timestamp on creation
- `updated_at`: Current timestamp on creation/modification

### 2. Task Defaults
- `completed`: False
- `created_at`: Current timestamp on creation
- `updated_at`: Current timestamp on creation/modification