---
name: sqlmodel_to_pydantic
description: "A utility to automatically generate Pydantic request/response models from SQLModel classes. Ensures database models and API models remain perfectly synced to prevent type errors."
---

# SQLModel to Pydantic Utility

## Instructions

1. **Input**
   - Provide a SQLModel class representing your database table.
   - Example:
   ```python
   from sqlmodel import SQLModel, Field

   class User(SQLModel, table=True):
       id: int = Field(default=None, primary_key=True)
       name: str
       email: str
