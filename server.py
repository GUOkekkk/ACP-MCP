from mcp.server.fastmcp import FastMCP
import os
import json
from typing import Dict, List, Optional, Any

# Create an MCP server
mcp = FastMCP("FileSystem MCP Server")

# Define a tool to find files based on user input
@mcp.tool()
def find_files(directory: str, pattern: str = None, file_type: str = None) -> List[str]:
    """
    Find files in the specified directory that match the given pattern and/or file type.

    Args:
        directory: The directory to search in
        pattern: Optional pattern to match in filenames
        file_type: Optional file extension to filter by (e.g., 'json', 'txt')

    Returns:
        A list of matching file paths
    """
    results = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Check if file matches the pattern
                pattern_match = True if pattern is None else pattern.lower() in file.lower()
                # Check if file matches the file type
                type_match = True if file_type is None else file.lower().endswith(f'.{file_type.lower()}')

                if pattern_match and type_match:
                    results.append(file_path)
        return results
    except Exception as e:
        return [f"Error finding files: {str(e)}"]

# Define a tool to read file content
@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read and return the content of a file.

    Args:
        file_path: Path to the file to read

    Returns:
        The content of the file as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Define a tool to modify file content
@mcp.tool()
def modify_file(file_path: str, content: str) -> str:
    """
    Modify the content of a file.

    Args:
        file_path: Path to the file to modify
        content: New content to write to the file

    Returns:
        Success message or error message
    """
    try:
        # Create a backup of the file
        if os.path.exists(file_path):
            backup_path = f"{file_path}.bak"
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())

        # Write the new content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return f"File modified successfully: {file_path}"
    except Exception as e:
        return f"Error modifying file: {str(e)}"

# Define a tool to handle JSON files specifically
@mcp.tool()
def update_json(file_path: str, updates: Dict[str, Any]) -> str:
    """
    Update specific fields in a JSON file.

    Args:
        file_path: Path to the JSON file
        updates: Dictionary of key-value pairs to update in the JSON

    Returns:
        Success message or error message
    """
    try:
        # Read the existing JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Create a backup
        backup_path = f"{file_path}.bak"
        with open(backup_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        # Update the data
        def update_nested(d, updates):
            for k, v in updates.items():
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    update_nested(d[k], v)
                else:
                    d[k] = v

        update_nested(data, updates)

        # Write the updated JSON
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        return f"JSON file updated successfully: {file_path}"
    except Exception as e:
        return f"Error updating JSON file: {str(e)}"

# Define a resource for file operations
@mcp.resource("file://{path}")
def get_file_info(path: str) -> Dict[str, Any]:
    """
    Get information about a file.

    Args:
        path: Path to the file

    Returns:
        Dictionary with file information
    """
    try:
        if os.path.exists(path):
            stats = os.stat(path)
            return {
                "exists": True,
                "size": stats.st_size,
                "last_modified": stats.st_mtime,
                "is_directory": os.path.isdir(path),
                "path": path
            }
        else:
            return {"exists": False, "path": path}
    except Exception as e:
        return {"error": str(e), "path": path}

# Start the server if this script is run directly
if __name__ == "__main__":
    # Start the server on port 8000
    import uvicorn
    print("Starting FileSystem MCP Server on http://localhost:8000")
    uvicorn.run(mcp.fastapi_app, host="127.0.0.1", port=8000)
