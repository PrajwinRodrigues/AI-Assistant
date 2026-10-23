
import requests
import json
from datetime import datetime
from Utilities.utilities import log


def get_date_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_date_time",
            "description": "Returns the current date and time as a formatted string",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "Returns the weather of the city provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City to get weather details for"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }
]


FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_date_time": get_date_time,
    "get_city_weather": get_city_weather,
}


def run_tools(tool_call):
    try:
        fname = tool_call.function.name
        fargs = json.loads(tool_call.function.arguments or "{}")

        logs(f"Tool {fname} called with {fargs} arguments")

        fn = FUNCTION_NAME_TO_FUNCTION_MAP[fname]
        result = fn(**fargs)

    except Exception as e:
        result = f"Tool execution failed: {type(e).__name__}: {e}"
        logs(result)

    return result
