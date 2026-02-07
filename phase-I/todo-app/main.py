#!/usr/bin/env python3
"""
Todo In-Memory Python Console App
Main entry point for the application
"""

from cli import TodoCLI


def main():
    """Main application entry point"""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()