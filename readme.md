# Chatbot API

This is an AWS Lambda-based chatbot that fetches weather data and tells jokes using API Gateway.

## 🚀 Features
- Fetches **current weather** using OpenWeather API 🌤️
- Returns a **random joke** from an external joke API 😂
- Logs all interactions in **AWS DynamoDB** 📝

## 🛠️ Setup Instructions

### **1. Install Dependencies**
Ensure you have Python installed, then install required dependencies from `requirement.txt`:
```sh
pip install -r requirement.txt -t .
```

### **2. Create Source Code Zip File**
Run the following command in PowerShell to package the source code:
```sh
Compress-Archive -Path * -DestinationPath chatbot_lambda.zip
```

### **3. Upload to AWS S3**
Upload the zip file to an S3 bucket `chatbot-code-bucket`:
```sh
aws s3 cp chatbot_lambda.zip s3://chatbot-code-bucket/
```

### **4. Deploy with AWS CloudFormation**
Create an AWS CloudFormation stack using the provided template:
```sh
aws cloudformation create-stack --stack-name chatbot-stack --template-body file://cloud-formation-chat-bot.yaml --capabilities CAPABILITY_NAMED_IAM
```

## **API Deployment**
This chatbot is deployed using **AWS API Gateway**:
- API Gateway is configured for **POST** requests
- The Lambda function is integrated with API Gateway

## **Usage**
#### **Example Request**
```sh
curl --location --request POST 'https://your-api-id.execute-api.us-east-1.amazonaws.com/staging/chatbot' \
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

## **🐞 Debugging**
- Check **CloudWatch logs** for Lambda execution errors.
- Verify **API Gateway method integration** (should be `POST`).

## 📜 License
This project is open-source and available under the MIT License.

---
Made by Sky