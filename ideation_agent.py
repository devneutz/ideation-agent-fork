#!/usr/bin/env python3
"""
Ideation Agent - Interactive CLI for generating solution ideas
Main entry point for the application
"""

import sys
from typing import Optional
from session_manager import SessionManager
from config import Config


def main():
    """Main entry point for the ideation agent CLI."""
    print("\n" + "="*60)
    print("  IDEATION AGENT")
    print("  Generate innovative solutions for customer opportunities")
    print("="*60 + "\n")

    # Initialize configuration
    config = Config()

    # Create session manager
    session = SessionManager(config)

    try:
        # Run the ideation session
        session.run()

    except KeyboardInterrupt:
        print("\n\nSession interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
