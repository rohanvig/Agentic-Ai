from rich.console import Console
from dotenv import load_dotenv
from openai import OpenAI
import os 
import json 
load_dotenv(override=True)


def show(text):
    try:
        Console().print(text)
    except Exception:
        print(text)

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_api_key =os.getenv("GEMINI_API_KEY")
gemini=OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)


market_data = {

    "BTC": {
        "price": 64250,
        "rsi": 71,
        "ema_20": 63500,
        "ema_50": 62000,
        "trend": "bullish",
        "volume": "high",
        "support": 62800,
        "resistance": 65500
    },

    "ETH": {
        "price": 3150,
        "rsi": 58,
        "ema_20": 3100,
        "ema_50": 2950,
        "trend": "bullish",
        "volume": "medium",
        "support": 3000,
        "resistance": 3250
    },

    "SOL": {
        "price": 142,
        "rsi": 49,
        "ema_20": 145,
        "ema_50": 138,
        "trend": "sideways",
        "volume": "low",
        "support": 135,
        "resistance": 150
    },

    "DOGE": {
        "price": 0.18,
        "rsi": 77,
        "ema_20": 0.17,
        "ema_50": 0.15,
        "trend": "bullish",
        "volume": "very high",
        "support": 0.16,
        "resistance": 0.20
    },

    "XRP": {
        "price": 0.61,
        "rsi": 41,
        "ema_20": 0.63,
        "ema_50": 0.67,
        "trend": "bearish",
        "volume": "medium",
        "support": 0.58,
        "resistance": 0.65
    }
}

def get_market_data(symbol:str):
    return market_data.get(symbol.upper(),{})


def evaluate_trade(rsi:int,trend:str,volume:str):
    if rsi > 70 and trend == "bullish" and volume in ["high","very high"]:
        return "strong buy"
    elif rsi > 60 and trend == "bullish":
        return "buy"
    elif rsi < 30 and trend == "bearish" and volume in ["high","very high"]:
        return "strong sell"
    elif rsi < 40 and trend == "bearish":
        return "sell"
    else:
        return "hold"
    

get_market_data_json={
    "name":"get_market_data",
    "description":"Fetches the latest market data for a given cryptocurrency symbol.",
    "parameters":{
        "type":"object",
        "properties":{
            "symbol":{
                "type":"string",
                "description":"The ticker symbol of the cryptocurrency (e.g., BTC, ETH)."
            }
        },
        "required":["symbol"],
        "additionalProperties":False
    }
}

evaluate_trade_json={
    "name":"evaluate_trade",
    "description":"Evaluates whether to buy, sell, or hold a cryptocurrency based on its RSI, trend, and volume.",
    "parameters":{
        "type":"object",
        "properties":{
            "rsi":{
                "type":"integer",
                "description":"Relative Strength Index of the cryptocurrency."
            },
            "trend":{
                "type":"string",
                "description":"Current market trend (e.g., bullish, bearish, sideways)."
            },
            "volume":{
                "type":"string",
                "description":"Trading volume level (e.g., low, medium, high, very high)."
            }
        },
        "required":["rsi","trend","volume"],
        "additionalProperties":False
    }
}

tools=[{
    "type":"function",
    "function":get_market_data_json
}, {
    "type":"function",
    "function":evaluate_trade_json
}]


def handle_tool_calls(tool_calls):
    results=[]
    for tool_call in tool_calls:
        tool_name=tool_call.function.name
        arguments=json.loads(tool_call.function.arguments)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results 


def loop(messages):
    done=False
    while not done:
        response = gemini.chat.completions.create(model="gemini-2.5-flash-lite", messages=messages, tools=tools, reasoning_effort="none")
        finish_reason = response.choices[0].finish_reason
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    show(response.choices[0].message.content)


system_message = """
You are a crypto trading analysis agent.

Your job is to:
1. Analyze market conditions
2. Use tools to gather market data
3. Evaluate trade quality
4. Provide a final trading suggestion

Always use tools before giving a conclusion.
Explain reasoning clearly.
"""

user_message = """
Analyze BTC for a possible swing trade setup.
"""

loop([{"role": "system", "content": system_message},
       {"role": "user", "content": user_message}])