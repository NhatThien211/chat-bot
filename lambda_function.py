import json
import os
import boto3
import requests
import uuid
from datetime import datetime
from typing import Optional, Dict

# Load environment variables
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "")
OPEN_ROUTER_API_KEY: str = os.getenv("MISTRAL_LLM_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "")

# Initialize AWS services
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

# API Endpoints
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"
LLM_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def remove_special_characters(city: str):
    return "".join(char for char in city if char.isalnum() or char.isspace())

def get_weather(city: str) -> str:
    """Fetch current weather data for a given city."""
    print(f"Fetching weather for {city}")  # Debug log
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(WEATHER_API_URL, params=params)
    print(f"Weather API Response: {response.json()}")  # Debug log
    if response.status_code == 200:
        data = response.json()
        return f"Current weather in {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C."
    return "Sorry, I couldn't retrieve the weather for that location."

def get_joke() -> str:
    """Fetch a random joke."""
    response = requests.get(JOKE_API_URL)
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} {data['punchline']}"
    return "Sorry, I couldn't fetch a joke at the moment."

def get_data_from_llm(message: str):
    response = requests.post(
        url=LLM_API_URL,
        headers={
            "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",  # Optional
        },
        data=json.dumps({
            "model": LLM_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        })
    )
    return response.json()["choices"][0]["message"]["content"]

def log_query(user_query: str, response_text: str) -> None:
    """Log the chatbot query and response in DynamoDB."""
    table.put_item(
        Item={
            "id": str(uuid.uuid4()),
            "query": user_query,
            "response": response_text,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def lambda_handler(event: Dict[str, str], context: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Handle incoming API Gateway requests."""
    try:
        body: Dict[str, str] = json.loads(event["body"])
        user_query: str = body.get("query", "").lower()

        # Determine response based on query
        if "weather" in user_query:
            city = user_query.split("in")[-1].strip() if "in" in user_query else "London"
            response_text = get_weather(remove_special_characters(city))
        elif "joke" in user_query:
            response_text = get_joke()
        else:
            response_text = get_data_from_llm(user_query)

        # Log to DynamoDB
        log_query(user_query, response_text)

        # Return response
        return {
            "statusCode": 200,
            "body": json.dumps({"response": response_text}),
            "headers": {"Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Allow all origins, you can restrict this
                "Access-Control-Allow-Methods": "OPTIONS, POST, GET",  # Allow specific HTTP methods
                "Access-Control-Allow-Headers": "Content-Type",  # Allow specific headers}
        }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers":  {"Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Allow all origins, you can restrict this
                "Access-Control-Allow-Methods": "OPTIONS, POST, GET",  # Allow specific HTTP methods
                "Access-Control-Allow-Headers": "Content-Type",  # Allow specific headers}
        }
        }
