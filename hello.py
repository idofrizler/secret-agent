from langchain_ollama import OllamaLLM
from langchain.agents import Tool
from langchain_core.prompts import PromptTemplate

# Initialize your local model
llm = OllamaLLM(model="gpt-oss:20b")

# Define a simple tool
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny and 72°F."

# Create a simple tool dispatcher
tools = {
    "say_hello": say_hello,
    "get_weather": get_weather
}

# Simple agent logic without complex parsing
def simple_agent(user_input: str):
    # Create a prompt that explains available tools
    prompt_template = PromptTemplate(
        input_variables=["input", "tools"],
        template="""You are a helpful assistant with access to the following tools:

Tools available:
- say_hello(name): Greets someone by name
- get_weather(location): Gets weather for a location

User request: {input}

If the user wants to greet someone, respond with: USE_TOOL:say_hello:NAME
If the user wants weather info, respond with: USE_TOOL:get_weather:LOCATION
Otherwise, just respond normally.

Response:"""
    )
    
    tool_descriptions = "\n".join([f"- {name}: {func.__doc__ or 'No description'}" for name, func in tools.items()])
    
    prompt = prompt_template.format(
        input=user_input,
        tools=tool_descriptions
    )
    
    response = llm.invoke(prompt)
    print(f"🤖 LLM Response: {response}")
    
    # Check if the LLM wants to use a tool
    if "USE_TOOL:" in response:
        try:
            parts = response.split("USE_TOOL:")[1].split(":")
            tool_name = parts[0].strip()
            tool_input = parts[1].strip()
            
            if tool_name in tools:
                tool_result = tools[tool_name](tool_input)
                return f"Tool '{tool_name}' executed: {tool_result}"
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Error parsing tool call: {e}"
    
    return response

# Test the simple agent
print("🚀 Testing Simple Agent with gpt-oss:20b")
print("=" * 50)

test_inputs = [
    "Say hello to Ido",
    "What's the weather in New York?",
    "Tell me a joke"
]

for test_input in test_inputs:
    print(f"\n📝 Input: {test_input}")
    result = simple_agent(test_input)
    print(f"✅ Result: {result}")
    print("-" * 30)
