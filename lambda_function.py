import json
import os
import boto3
import requests
import uuid
from datetime import datetime

# Load environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

# Initialize AWS services
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

# API Endpoints
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"

def get_weather(city):
    """Fetch current weather data for a given city."""
    print(f"Fetching weather for {city}")  # Debug log
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(WEATHER_API_URL, params=params)
    print(f"Weather API Response: {response}")  # Debug log
    if response.status_code == 200:
        data = response.json()
        return f"Current weather in {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C."
    return "Sorry, I couldn't retrieve the weather for that location."

def get_joke():
    """Fetch a random joke."""
    response = requests.get(JOKE_API_URL)
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} {data['punchline']}"
    return "Sorry, I couldn't fetch a joke at the moment."

def log_query(user_query, response_text):
    """Log the chatbot query and response in DynamoDB."""
    table.put_item(
        Item={
            "id": str(uuid.uuid4()),
            "query": user_query,
            "response": response_text,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def lambda_handler(event, context):
    """Handle incoming API Gateway requests."""
    try:
        body = json.loads(event["body"])
        user_query = body.get("query", "").lower()

        # Determine response based on query
        if "weather" in user_query:
            city = user_query.split("in")[-1].strip() if "in" in user_query else "London"
            response_text = get_weather(city)
        elif "joke" in user_query:
            response_text = get_joke()
        else:
            response_text = "I can fetch weather data and tell jokes. Try asking about the weather or a joke!"

        # Log to DynamoDB
        log_query(user_query, response_text)

        # Return response
        return {
            "statusCode": 200,
            "body": json.dumps({"response": response_text}),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
