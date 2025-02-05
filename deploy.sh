#!/bin/bash

# Define variables
ZIP_FILE="chatbot_lambda.zip"
S3_BUCKET="chatbot-code-bucket"
STACK_NAME="Chatbot-stack"
TEMPLATE_PATH="file://cloud-formation-chat-bot.yaml"

echo "Starting deployment..."

# Step 1: Remove existing zip file if it exists
if [ -f "$ZIP_FILE" ]; then
  echo "Removing existing $ZIP_FILE..."
  rm "$ZIP_FILE"
fi

# Step 2: Compress the source code into a zip file
echo "Creating new zip file $ZIP_FILE..."
zip -r "$ZIP_FILE" ./*

# Step 3: Create the S3 bucket if it doesn't exist
echo "Checking if S3 bucket $S3_BUCKET exists..."
if ! aws s3 ls "s3://$S3_BUCKET" > /dev/null 2>&1; then
  echo "Creating S3 bucket $S3_BUCKET..."
  aws s3 mb "s3://$S3_BUCKET"
else
  echo "S3 bucket $S3_BUCKET already exists."
fi

# Step 4: Upload the zip file to the S3 bucket
echo "Uploading $ZIP_FILE to S3 bucket $S3_BUCKET..."
aws s3 cp "$ZIP_FILE" "s3://$S3_BUCKET/"

# Step 5: Deploy with AWS CloudFormation
echo "Deploying $STACK_NAME to AWS CloudFormation..."

if ! aws cloudformation describe-stacks --stack-name "$STACK_NAME" > /dev/null 2>&1; then
  echo "Creating a new CloudFormation stack..."
  aws cloudformation create-stack \
    --stack-name "$STACK_NAME" \
    --template-body "$TEMPLATE_PATH" \
    --capabilities CAPABILITY_NAMED_IAM

  echo "Waiting for stack creation to complete..."
  aws cloudformation wait stack-create-complete --stack-name "$STACK_NAME"
else
  echo "Updating existing CloudFormation stack..."
  aws cloudformation update-stack \
    --stack-name "$STACK_NAME" \
    --template-body "$TEMPLATE_PATH" \
    --capabilities CAPABILITY_NAMED_IAM

  echo "Waiting for stack update to complete..."
  aws cloudformation wait stack-update-complete --stack-name "$STACK_NAME"
fi

echo "Deployment completed successfully!"
