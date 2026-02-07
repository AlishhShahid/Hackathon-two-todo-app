"""Simple test to isolate import errors."""

try:
    from src.main import create_app
    print("Successfully imported create_app from main")

    app = create_app()
    print("Successfully created app instance")
except Exception as e:
    print(f"Error importing: {e}")
    import traceback
    traceback.print_exc()