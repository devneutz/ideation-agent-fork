"""
Input helper functions for CLI interaction
"""

import os
from typing import Optional, List


def get_user_input(prompt: str, required: bool = True, multiline: bool = False) -> str:
    """
    Get input from user with validation.

    Args:
        prompt: The question/prompt to show user
        required: Whether input is required
        multiline: Whether to accept multiline input

    Returns:
        User's input as string
    """
    suffix = " (required)" if required else " (optional, press Enter to skip)"

    if multiline:
        print(f"{prompt}{suffix}")
        print("(Enter '###' on a new line when done)")
        lines = []
        while True:
            line = input()
            if line.strip() == "###":
                break
            lines.append(line)
        response = "\n".join(lines).strip()
    else:
        response = input(f"{prompt}{suffix}\n> ").strip()

    if required and not response:
        print("This field is required. Please provide a response.")
        return get_user_input(prompt, required, multiline)

    return response


def confirm(prompt: str) -> bool:
    """
    Get yes/no confirmation from user.

    Args:
        prompt: The confirmation question

    Returns:
        True if user confirms, False otherwise
    """
    response = input(f"{prompt} (y/n)\n> ").strip().lower()

    if response in ["y", "yes"]:
        return True
    elif response in ["n", "no"]:
        return False
    else:
        print("Please answer 'y' or 'n'")
        return confirm(prompt)


def get_choice(prompt: str, options: List[str]) -> str:
    """
    Get a choice from a list of options.

    Args:
        prompt: The question to ask
        options: List of valid options

    Returns:
        Selected option
    """
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True:
        choice = input(f"\nEnter choice (1-{len(options)}): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print(f"Please enter a valid number between 1 and {len(options)}")


def get_rating(prompt: str, min_val: int = 1, max_val: int = 5) -> int:
    """
    Get a numeric rating from user.

    Args:
        prompt: The question to ask
        min_val: Minimum valid value
        max_val: Maximum valid value

    Returns:
        Rating as integer
    """
    while True:
        response = input(f"{prompt} ({min_val}-{max_val})\n> ").strip()
        try:
            rating = int(response)
            if min_val <= rating <= max_val:
                return rating
            else:
                print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print(f"Please enter a valid number between {min_val} and {max_val}")


def read_file_content(file_path: str) -> Optional[str]:
    """
    Read content from a file.

    Args:
        file_path: Path to the file

    Returns:
        File content as string, or None if error
    """
    try:
        # Expand user home directory
        expanded_path = os.path.expanduser(file_path)

        if not os.path.exists(expanded_path):
            print(f"Error: File not found: {file_path}")
            return None

        if os.path.isdir(expanded_path):
            # If it's a directory, read all text files in it
            content_parts = []
            for filename in os.listdir(expanded_path):
                file_full_path = os.path.join(expanded_path, filename)
                if os.path.isfile(file_full_path) and filename.endswith(('.txt', '.md')):
                    with open(file_full_path, 'r', encoding='utf-8') as f:
                        content_parts.append(f"=== {filename} ===\n{f.read()}\n")
            return "\n".join(content_parts) if content_parts else None

        # Read single file
        with open(expanded_path, 'r', encoding='utf-8') as f:
            return f.read()

    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None


def get_input_with_file_option(prompt: str, required: bool = True) -> Optional[str]:
    """
    Get input from user with option to provide file path or direct text.

    Args:
        prompt: The question to ask
        required: Whether input is required

    Returns:
        Content as string
    """
    print(f"\n{prompt}")
    choice = get_choice(
        "How would you like to provide this?",
        ["Type it directly", "Provide file/folder path", "Skip"]
    )

    if choice == "Type it directly":
        return get_user_input("Please enter the content:", required=required, multiline=True)

    elif choice == "Provide file/folder path":
        file_path = get_user_input(
            "Enter the file or folder path:",
            required=False
        )
        if file_path:
            content = read_file_content(file_path)
            if content:
                print(f"✓ Successfully loaded content ({len(content)} characters)")
                return content
            else:
                print("Failed to read file. Let's try again.")
                return get_input_with_file_option(prompt, required)
        return None

    else:  # Skip
        if required:
            print("This field is required.")
            return get_input_with_file_option(prompt, required)
        return None
