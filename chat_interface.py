import streamlit as st
import requests
import json
import time
import threading
from datetime import datetime
from typing import Dict, Any, List
import asyncio

# Set page config for ChatGPT-like appearance
st.set_page_config(
    page_title="Local Agent Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #343541;
        border: 1px solid #565869;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .assistant-message {
        background-color: #444654;
        border: 1px solid #565869;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .tool-execution {
        background-color: #2d4a3a;
        border: 1px solid #4d7c5a;
        padding: 10px;
        border-radius: 8px;
        margin: 8px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    h1 {
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Define available tools
def say_hello(name: str) -> str:
    time.sleep(1)  # Simulate some processing time
    return f"Hello, {name}! 👋"

def get_weather(location: str) -> str:
    time.sleep(2)  # Simulate API call
    return f"The weather in {location} is sunny and 72°F ☀️"

def search_web(query: str) -> str:
    time.sleep(3)  # Simulate web search
    return f"Found information about '{query}': This is a simulated search result. 🔍"

def run_code(code: str) -> str:
    time.sleep(1)
    # Simple safe code execution (just return the code for now)
    return f"Code executed:\n```python\n{code}\n```\nOutput: Simulated execution result"

# Tool registry
TOOLS = {
    "say_hello": {
        "func": say_hello,
        "description": "Greets someone by name",
        "icon": "👋"
    },
    "get_weather": {
        "func": get_weather,
        "description": "Gets weather information for a location",
        "icon": "🌤️"
    },
    "search_web": {
        "func": search_web,
        "description": "Searches the web for information",
        "icon": "🔍"
    },
    "run_code": {
        "func": run_code,
        "description": "Executes Python code",
        "icon": "💻"
    }
}

class OllamaAgent:
    def __init__(self, model_name: str = "gpt-oss:20b"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        
    def create_prompt(self, user_input: str, conversation_history: List[Dict]) -> str:
        # Create context from conversation history
        context = ""
        for msg in conversation_history[-6:]:  # Last 6 messages for context
            role = msg["role"]
            content = msg["content"]
            context += f"{role.title()}: {content}\n"
        
        tool_descriptions = ""
        for tool_name, tool_info in TOOLS.items():
            tool_descriptions += f"- {tool_name}: {tool_info['description']}\n"
        
        prompt = f"""You are a helpful AI assistant with access to the following tools:

{tool_descriptions}

Previous conversation:
{context}

Current user request: {user_input}

Instructions:
- If the user request can be handled with a tool, respond EXACTLY with: USE_TOOL:tool_name:parameters
- For greetings, use: USE_TOOL:say_hello:name
- For weather, use: USE_TOOL:get_weather:location
- For web search, use: USE_TOOL:search_web:query
- For code execution, use: USE_TOOL:run_code:code
- Otherwise, respond conversationally as a helpful assistant
- Be concise but friendly

Response:"""
        return prompt
    
    def call_ollama_api(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: Ollama API returned status {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
    
    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        if tool_name in TOOLS:
            tool_func = TOOLS[tool_name]["func"]
            try:
                result = tool_func(tool_input)
                return result
            except Exception as e:
                return f"Error executing {tool_name}: {str(e)}"
        else:
            return f"Unknown tool: {tool_name}"
    
    def process_message(self, user_input: str, conversation_history: List[Dict]) -> tuple[str, bool, str, str]:
        """Returns (response, used_tool, tool_name, tool_result)"""
        prompt = self.create_prompt(user_input, conversation_history)
        llm_response = self.call_ollama_api(prompt)
        
        # Check if LLM wants to use a tool
        if "USE_TOOL:" in llm_response:
            try:
                tool_part = llm_response.split("USE_TOOL:")[1].strip()
                parts = tool_part.split(":", 2)
                
                if len(parts) >= 2:
                    tool_name = parts[0].strip()
                    tool_input = parts[1].strip()
                    
                    tool_result = self.execute_tool(tool_name, tool_input)
                    return tool_result, True, tool_name, tool_input
                    
            except Exception as e:
                return f"Error parsing tool call: {str(e)}", False, "", ""
        
        return llm_response, False, "", ""

# Initialize session state
if "conversation_history" in st.session_state:
    conversation_history = st.session_state.conversation_history
else:
    conversation_history = []
    st.session_state.conversation_history = conversation_history

if "agent" not in st.session_state:
    st.session_state.agent = OllamaAgent()

# Sidebar
with st.sidebar:
    st.title("🤖 Local Agent")
    
    st.markdown("### Available Tools")
    for tool_name, tool_info in TOOLS.items():
        st.markdown(f"{tool_info['icon']} **{tool_name}**")
        st.caption(tool_info['description'])
    
    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.conversation_history = []
        st.rerun()
    
    st.divider()
    
    st.markdown("### Model Info")
    st.info("**Model**: gpt-oss:20b\n**Status**: ✅ Connected")
    
    st.markdown("### Stats")
    st.metric("Messages", len(conversation_history))
    
    # Show tool usage stats
    tool_usage = {}
    for msg in conversation_history:
        if msg.get("tool_used"):
            tool_name = msg.get("tool_name", "unknown")
            tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1
    
    if tool_usage:
        st.markdown("**Tool Usage:**")
        for tool, count in tool_usage.items():
            st.caption(f"{TOOLS.get(tool, {}).get('icon', '🔧')} {tool}: {count}")

# Main chat interface
st.title("💬 Local Agent Chat")

# Display conversation history
chat_container = st.container()

with chat_container:
    for message in conversation_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                if message.get("tool_used"):
                    # Show tool execution
                    tool_name = message.get("tool_name", "")
                    tool_input = message.get("tool_input", "")
                    tool_icon = TOOLS.get(tool_name, {}).get("icon", "🔧")
                    
                    st.markdown(f"""
                    <div class="tool-execution">
                        {tool_icon} <strong>Executed Tool:</strong> {tool_name}<br>
                        <strong>Input:</strong> {tool_input}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Message Local Agent..."):
    # Add user message to history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process with agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response, used_tool, tool_name, tool_input = st.session_state.agent.process_message(
                prompt, conversation_history
            )
        
        # Show tool execution if used
        if used_tool:
            tool_icon = TOOLS.get(tool_name, {}).get("icon", "🔧")
            st.markdown(f"""
            <div class="tool-execution">
                {tool_icon} <strong>Executed Tool:</strong> {tool_name}<br>
                <strong>Input:</strong> {tool_input}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(response)
    
    # Add assistant response to history
    assistant_msg = {
        "role": "assistant", 
        "content": response,
        "tool_used": used_tool,
        "tool_name": tool_name,
        "tool_input": tool_input
    }
    conversation_history.append(assistant_msg)
    
    # Update session state
    st.session_state.conversation_history = conversation_history
    st.rerun()
