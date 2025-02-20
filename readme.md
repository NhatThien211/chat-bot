# Chatbot API

This is an AWS Lambda-based chatbot that fetches weather data and tells jokes using API Gateway.

## 🚀 Features
- Fetches **current weather** using OpenWeather API 🌤️
- Returns a **random joke** from an external joke API 😂
- Logs all interactions in **AWS DynamoDB** 📝


## 🏗️ System Architecture
This chatbot system is built using AWS services and follows the architecture below:

1. **API Gateway**: Handles incoming HTTP requests and routes them to Lambda.
2. **AWS Lambda**: Processes user queries, fetches data from external APIs, and interacts with DynamoDB.
3. **DynamoDB**: Stores chatbot interaction logs and user queries.
4. **AWS S3**: Stores the chatbot's Lambda function code.
4. **AWS Secret Manager**: Stores the weather API key.
5. **AWS CloudFormation**: Automates the deployment and management of all AWS resources.

### **Architecture Diagram**
```mermaid
graph TD;
    User -->|HTTP Request| APIGateway[API Gateway]
    APIGateway -->|Invoke| Lambda[AWS Lambda]
    Lambda -->|Fetch Weather| WeatherAPI[Weather API]
    Lambda -->|Fetch Joke| JokeAPI[Joke API]
    Lambda -->|Store Query| DynamoDB[AWS DynamoDB]
    Lambda -->|Response| APIGateway
    APIGateway -->|HTTP Response| User
    Lambda -->|Code Storage| S3[AWS S3]
    Lambda -->|API Key Storage| PMS[AWS Secret Manager]
```

## 🛠️ Setup Instructions

### **1. Install Dependencies**
1.1. Ensure you have Python installed, then install required dependencies from `requirement.txt`:
```sh
pip install -r requirement.txt -t .
```
1.2. Ensure you have AWS CLI installed

### **2. Create parameter store**
Create parameter store `weatherApiKey` and add Your Weather API KEY (Created from https://openweathermap.org/api):
```sh
aws secretsmanager create-secret --name "weatherApiKey" --secret-string '{\"API_KEY\":\"YOUR_KEY_HERE\"}'
```

Create parameter store `openRouterApiKey` and add Your Open Router API KEY (Created from https://openrouter.ai):
```sh
aws secretsmanager create-secret --name "openRouterApiKey" --secret-string '{\"API_KEY\":\"YOUR_KEY_HERE\"}'
```

### **3. Run Deployment**
### For Window: ###
#### 3.1. Open PowerShell as Administrator ####
#### 3.2. Grant execute permissions ####
```sh
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
#### 3.3. Run the deployment script ####
```sh
.\deploy.ps1
```

### For MacOS/Linux: ###
#### 3.1. Open Terminal ####
#### 3.2. Grant execute permissions ####
```sh
chmod +x deploy.sh
```
#### 3.3. Run the deployment script ####
```sh
./deploy.sh
```

## **API Deployment**
This chatbot is deployed using **AWS API Gateway**:
- API Gateway is configured for **POST** requests
- The Lambda function is integrated with API Gateway
- API information:
    + Invoke URL: Created API gateway id -> Stages -> Invoke URL
    + Method: POST

## **Usage**
#### **1. Example Request**
```sh
curl --location --request POST 'your_invoke_url/chatbot' \
--header 'Content-Type: application/json' \
--data '{
    "query": "tell me a joke"
}'
```

#### **Example Response**
```json
{
    "response": "Why did the scarecrow win an award? Because he was outstanding in his field!"
}
```

#### **2. Example Request**
```sh
curl --location --request POST 'your_invoke_url/chatbot' \
--header 'Content-Type: application/json' \
--data '{
    "query": "what is the weather in London"
}'
```

#### **Example Response**
```json
{
    "response": "Current weather in london: broken clouds, 0.58°C."
}
```

## **🐞 Debugging**
- Check **CloudWatch logs** for Lambda execution errors.
- Verify **API Gateway method integration** (should be `POST`).

## 📜 License
This project is open-source and available under the MIT License.

---
Made by Sky