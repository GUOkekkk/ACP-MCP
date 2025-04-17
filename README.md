# FileSystem MCP (Model Context Protocol) Server

## Overview
The Model Context Protocol (MCP) server is designed to process user text inputs and intelligently locate and modify appropriate files based on those inputs. This server leverages Azure's GPT API to understand user requests and perform contextual file operations. The MCP client is designed to run within VSCode Insider, providing a seamless integration with your development environment.

## Architecture

### Components
1. **MCP Server**: Python-based backend that processes requests and manages file operations, use python mcp package
2. **MCP Client**: VSCode Insider extension that captures user inputs and displays results
3. **Azure GPT API Integration**: Natural language processing component for understanding user intent
4. **File Management System**: Component for locating and modifying files based on processed requests

## Implementation Process

### 1. Server Setup
- Create a Python-based server using mcp package
- Implement authentication and secure communication channels
- Set up Azure GPT API integration with appropriate models
- Develop file search and modification algorithms

### 2. Client Development
- Create a VSCode Insider extension
- Implement user input interface
- Establish secure communication with the MCP server
- Design result display and file preview components

### 3. File Processing Logic
- Develop intelligent file search based on user input context
- Implement file type detection (JSON, XML, text, etc.)
- Create safe file modification procedures with backup capabilities
- Implement validation for modified files

### 4. Azure GPT Integration
- Configure Azure OpenAI service
- Implement prompt engineering for accurate file operations
- Develop context management for maintaining conversation history
- Optimize token usage for cost efficiency

## Technical Standards

### Server Requirements
- Python 3.8+
- FastAPI/Flask for API endpoints
- Azure SDK for Python
- Secure token-based authentication
- Comprehensive logging and error handling

### Client Requirements
- VSCode Insider compatible extension
- TypeScript/JavaScript implementation
- WebSocket support for real-time communication
- Responsive UI with appropriate feedback mechanisms

### API Standards
- RESTful API design with appropriate HTTP methods
- JSON request/response format
- Proper error codes and messages
- Rate limiting and request throttling
- API versioning for future compatibility

### Security Standards
- HTTPS for all communications
- API key management and rotation
- Input validation and sanitization
- Secure storage of credentials
- Regular security audits

## API Reference

The MCP server provides the following API endpoints for file operations:

### find_files

Find files matching the specified pattern in a directory.

**Parameters:**
- `directory` (string): Directory path to search
- `pattern` (string): File name pattern (supports regular expressions)
- `max_depth` (integer, optional): Maximum search depth (default is 3)

**Returns:**
A formatted string containing the list of matching files or an error message.

**Example:**
```python
result = await find_files("/path/to/directory", "*.json", 2)
```

### view_file

View the content of a specified file.

**Parameters:**
- `file_path` (string): Path to the file

**Returns:**
A string containing the file content or an error message if the file doesn't exist or can't be read.

**Example:**
```python
content = await view_file("/path/to/file.txt")
```

### update_parameter

Update specific parameters in a file using regular expression pattern matching.

**Parameters:**
- `file_path` (string): Path to the file
- `param_pattern` (string): Parameter matching pattern (regular expression)
- `new_value` (string): New parameter value

**Returns:**
A string indicating success or failure of the operation.

**Example:**
```python
result = await update_parameter("/path/to/config.json", "\"version\":\s*\"[^\"]*\"", "\"version\": \"2.0\"")
```

### list_directory

List the contents of a specified directory, distinguishing between files and subdirectories.

**Parameters:**
- `directory` (string): Directory path

**Returns:**
A formatted string containing the list of files and directories or an error message.

**Example:**
```python
contents = await list_directory("/path/to/directory")
```

## Installation

### Server Installation
```bash
# Clone the repository
git clone https://gitlab.com/ai-hackathon2/acp-mcp.git
cd acp-mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


# Configure environment variables
cp .env.example .env
# Edit .env with your Azure API keys and other configurations

# Start the server
# Need to download the npm first
mcp dev server.py

# MCP Inspector is up and running at http://127.0.0.1:6274
```

### Client Installation
1. Open VSCode Insider
2. Go to Extensions (Ctrl+Shift+X)
3. Click on "..." and select "Install from VSIX"
4. Navigate to the downloaded MCP client VSIX file and install
5. Restart VSCode Insider
6. Configure the extension with your MCP server URL and credentials

## Usage

### Basic Commands
1. Open the command palette (Ctrl+Shift+P)
2. Type "MCP: Connect" to establish connection with your MCP server
3. Use "MCP: New Request" to start a new file modification request
4. Type your natural language request describing the file changes needed
5. Review the suggested changes before applying them

### Example Requests
- "Find the configuration file and update the database connection string to use the new server address"
- "Locate the user model and add a new field for storing user preferences"
- "Find all JSON files containing API endpoints and update the version number to 2.0"

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Azure OpenAI team for providing the GPT API
- VSCode team for the extensible editor platform
- All contributors and testers
