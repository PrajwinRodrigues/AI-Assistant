
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
from Utilities.utilities import log
import json
import os

load_dotenv(override=True)

MAX_STEPS = 5

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "Respond within 10 words"
    }
]

while True:
    user_input = input("Me:\n")

    if user_input.lower() in ["exit", "bye", "goodbye", "quit"]:
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS
        )

        msg = response.choices[0].message

        # No more tool calls: assistant has responded
        if not msg.tool_calls:
            break

        # Add assistant message containing tool calls
        messages.append(msg)

        # Execute each requested tool
        log(f" ->Step {step}:Model requested {len(msg.tool_calls)} tool calls")
        for tool_call in msg.tool_calls:
            try:
                fname = tool_call.function.name

                fargs = json.loads(
                    tool_call.function.arguments or "{}"
                )
                log(f"  ->Tool {fname} called with {fargs} arguments")
                fn = FUNCTION_NAME_TO_FUNCTION_MAP[fname]

                result = fn(**fargs)

            except Exception as e:
                result = f"Tool execution failed: {type(e).__name__}: {e}"
            log(f" Model response:{result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    else:
        # Maximum steps reached; request a final response
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )
        msg = response.choices[0].message

    messages.append({
        "role": "assistant",
        "content": msg.content or ""
    })

    print("\nAssistant:", msg.content or "")
