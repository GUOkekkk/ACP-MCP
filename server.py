from typing import Any, List, Dict, Optional
import os
import re
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("filesystem")

# Constants
MAX_SEARCH_DEPTH = 5  # Maximum search depth
MAX_RESULTS = 50  # Maximum number of results


def search_files(
    directory: str, pattern: str, max_depth: int = MAX_SEARCH_DEPTH
) -> List[str]:
    """Search for files matching the pattern in the specified directory.

    Args:
        directory: Directory path to search
        pattern: File name pattern (supports regular expressions)
        max_depth: Maximum search depth

    Returns:
        List of matching file paths
    """
    results = []
    pattern_compiled = re.compile(pattern)

    # Use os.walk to traverse the directory
    for root, _, files in os.walk(directory):
        # Check search depth
        relative_path = os.path.relpath(root, directory)
        current_depth = len(relative_path.split(os.sep)) if relative_path != "." else 0
        if current_depth > max_depth:
            continue

        # Match files
        for file in files:
            if pattern_compiled.search(file):
                file_path = os.path.join(root, file)
                results.append(file_path)

                # Limit the number of results
                if len(results) >= MAX_RESULTS:
                    return results

    return results


def read_file_content(file_path: str) -> Optional[str]:
    """Read file content.

    Args:
        file_path: File path

    Returns:
        File content or None (if reading fails)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return None


def modify_file_parameter(
    file_path: str, param_pattern: str, new_value: str
) -> Dict[str, Any]:
    """Modify specific parameters in a file.

    Args:
        file_path: File path
        param_pattern: Parameter matching pattern (regular expression)
        new_value: New parameter value

    Returns:
        Dictionary containing operation results
    """
    try:
        # Read file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find and replace parameters
        pattern = re.compile(param_pattern)
        if not pattern.search(content):
            return {
                "success": False,
                "message": f"Parameter pattern not found: {param_pattern}",
            }

        # Execute replacement
        new_content = pattern.sub(new_value, content)

        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return {
            "success": True,
            "message": f"Successfully modified file parameter",
            "file_path": file_path,
            "pattern": param_pattern,
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error modifying file parameter: {str(e)}",
        }


@mcp.tool()
async def find_files(directory: str, pattern: str, max_depth: int = 3) -> str:
    """Find files matching the specified pattern.

    Args:
        directory: Directory path to search
        pattern: File name pattern (supports regular expressions)
        max_depth: Maximum search depth (default is 3)
    """
    # Verify directory exists
    if not os.path.isdir(directory):
        return f"Error: Directory '{directory}' does not exist"

    # Search files
    results = search_files(directory, pattern, max_depth)

    # Format results
    if not results:
        return f"No files matching '{pattern}' found in '{directory}'"

    formatted_results = "\n".join(results)
    return f"Found {len(results)} matching files:\n{formatted_results}"


@mcp.tool()
async def view_file(file_path: str) -> str:
    """View file content.

    Args:
        file_path: File path
    """
    # Verify file exists
    if not os.path.isfile(file_path):
        return f"Error: File '{file_path}' does not exist"

    # Read file content
    content = read_file_content(file_path)
    if content is None:
        return f"Error: Unable to read file '{file_path}'"

    return f"Content of file '{file_path}':\n\n{content}"


@mcp.tool()
async def update_parameter(file_path: str, param_pattern: str, new_value: str) -> str:
    """Update specific parameters in a file.

    Args:
        file_path: File path
        param_pattern: Parameter matching pattern (regular expression)
        new_value: New parameter value
    """
    # Verify file exists
    if not os.path.isfile(file_path):
        return f"Error: File '{file_path}' does not exist"

    # Modify parameter
    result = modify_file_parameter(file_path, param_pattern, new_value)

    if result["success"]:
        return f"Success: {result['message']}\nFile: {file_path}\nParameter pattern: {param_pattern}"
    else:
        return f"Error: {result['message']}"


@mcp.tool()
async def list_directory(directory: str) -> str:
    """List directory contents.

    Args:
        directory: Directory path
    """
    # Verify directory exists
    if not os.path.isdir(directory):
        return f"Error: Directory '{directory}' does not exist"

    try:
        # Get directory contents
        items = os.listdir(directory)

        # Distinguish between files and directories
        dirs = []
        files = []

        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                dirs.append(f"[Directory] {item}/")
            else:
                files.append(f"[File] {item}")

        # Format results
        result = f"Contents of directory '{directory}':\n"
        if dirs:
            result += "\nDirectories:\n" + "\n".join(dirs)
        if files:
            result += "\n\nFiles:\n" + "\n".join(files)

        return result

    except Exception as e:
        return f"Error listing directory contents: {str(e)}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
