---
name: nextjs_api_client_gen
description: Generate typed TypeScript functions for frontend/lib/api.ts based on a backend OpenAPI/FastAPI schema. Ideal for Next.js frontend integration.
---

# Next.js API Client Generator

## Instructions

1. **Input**
   - Provide the OpenAPI / FastAPI backend schema URL or JSON object.
   - Specify the folder where the TypeScript API client should be generated (e.g., `frontend/lib/api.ts`).

2. **Generated Output**
   - Typed TypeScript functions for each endpoint.
   - Request and response types inferred from OpenAPI schema.
   - Functions compatible with `fetch` or `axios` for making API calls.
   - Automatic handling of query parameters, path parameters, and request bodies.

3. **Implementation Notes**
   - Use TypeScript interfaces or types for request/response objects.
   - Generate reusable functions for GET, POST, PUT, PATCH, DELETE.
   - Include proper error handling and typing for response errors.
   - Ensure generated functions are ready to import in Next.js pages or components.
   - Optionally, include authentication headers if specified in the schema.

## Best Practices
- Keep function names clear and consistent with API endpoints.
- Use camelCase for function names and parameters.
- Provide default values for optional query parameters.
- Include JSDoc comments for better developer experience and IDE support.
- Ensure the client code is tree-shakable and minimal.

## Example Structure

```ts
// frontend/lib/api.ts

export interface User {
  id: number;
  name: string;
  email: string;
}

export async function getUsers(): Promise<User[]> {
  const response = await fetch("/api/users");
  if (!response.ok) throw new Error("Failed to fetch users");
  return response.json();
}

export async function getUser(userId: number): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error("Failed to fetch user");
  return response.json();
}

export async function createUser(user: Partial<User>): Promise<User> {
  const response = await fetch("/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });
  if (!response.ok) throw new Error("Failed to create user");
  return response.json();
}

export async function updateUser(userId: number, user: Partial<User>): Promise<User> {
  const response = await fetch(`/api/users/${userId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });
  if (!response.ok) throw new Error("Failed to update user");
  return response.json();
}

export async function deleteUser(userId: number): Promise<void> {
  const response = await fetch(`/api/users/${userId}`, { method: "DELETE" });
  if (!response.ok) throw new Error("Failed to delete user");
}
