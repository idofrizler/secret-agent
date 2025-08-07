# Local Agent Chat Interface

A ChatGPT-style web interface for your local agent that runs on Ollama with gpt-oss:20b.

## Features

✅ **ChatGPT-like Design**: Modern, clean interface with dark theme  
✅ **Agent Capabilities**: Tool execution with visual feedback  
✅ **Background Jobs**: Tools run asynchronously with progress indicators  
✅ **Conversation History**: Full chat history with context  
✅ **Tool Usage Stats**: Track which tools are being used  

## Available Tools

- 👋 **say_hello**: Greets someone by name
- 🌤️ **get_weather**: Gets weather information for a location  
- 🔍 **search_web**: Searches the web for information
- 💻 **run_code**: Executes Python code safely with 10-second timeout

## Quick Start

1. **Make sure Ollama is running** with gpt-oss:20b model:
   ```bash
   ollama serve
   ollama pull gpt-oss:20b
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Start the chat interface**:
   ```bash
   python3 -m streamlit run chat_interface.py
   ```

4. **Open your browser** to: `http://localhost:8501`

## Usage Examples

Try these commands in the chat:

- "Say hello to Alice"
- "What's the weather in Tokyo?"
- "Search for information about machine learning"
- "Run this Python code: print('Hello World')"
- "Tell me a joke" (regular conversation)

## How It Works

1. **User Input**: You type a message in the chat
2. **Agent Processing**: The agent analyzes if any tools should be used
3. **Tool Execution**: If needed, tools run in the background
4. **Response**: Results are displayed with visual indicators for tool usage

## Architecture

- **Frontend**: Streamlit with ChatGPT-style CSS
- **Backend**: Direct Ollama API integration
- **Agent Logic**: Custom prompt-based tool selection
- **Tools**: Python functions that can be extended

## Extending Tools

Add new tools by:

1. Define your function:
   ```python
   def my_new_tool(input_param: str) -> str:
       # Your tool logic here
       return "Tool result"
   ```

2. Add to TOOLS registry:
   ```python
   TOOLS["my_new_tool"] = {
       "func": my_new_tool,
       "description": "Description of what the tool does",
       "icon": "🔧"
   }
   ```

3. Update the prompt template to include the new tool

## Files

- `chat_interface.py` - Main Streamlit app
- `hello.py` - Original command-line agent (for reference)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Troubleshooting

**Interface not loading?**
- Check that Ollama is running: `curl http://localhost:11434/api/tags`
- Ensure gpt-oss:20b is installed: `ollama list`

**Tool execution errors?**
- Check the terminal output for detailed error messages
- Tools run with simulated delays - this is normal

**Performance issues?**
- The gpt-oss:20b model requires significant RAM (16GB+)
- Consider using a smaller model for testing

**Code execution security?**
- Code runs in temporary files with 10-second timeout
- Only standard Python libraries are available
- Be cautious with user-provided code in production

Enjoy your local agent with a professional ChatGPT-style interface! 🚀
