import argparse
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from prompts import system_prompt
from functions.call_function import available_functions
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError(
        "OPENROUTER_API_KEY not found. Make sure your .env file exists and contains it."
    )
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
response = client.chat.completions.create(
    model       = "openrouter/free",
    messages    = messages,
    tools       = available_functions,
)
if response.usage is None:
    raise Exception("Response usage is None - API request may have failed")
if args.verbose is True:  
    print(f"User prompt: {args.user_prompt}")  
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")
else:
    print(message.content)