# Define variables
$zipFileName = "chatbot_lambda.zip"
$s3BucketName = "chatbot-code-bucket"
$stackName = "Chatbot-stack"
$templatePath = "file://cloud-formation-chat-bot.yaml"
$prefix = "prefix_v1"

Write-Host "Starting deployment..."

# Step 1: Remove existing zip file if it exists
if (Test-Path $zipFileName) {
    Write-Host "Removing existing $zipFileName..."
    Remove-Item $zipFileName
}

# Step 2: Compress the source code into a zip file
Write-Host "Creating new zip file $zipFileName..."
Compress-Archive -Path * -DestinationPath $zipFileName

# Step 3: Create the S3 bucket if it doesn't exist
Write-Host "Checking if S3 bucket $s3BucketName exists..."
$s3BucketCheck = aws s3 ls "s3://$s3BucketName" 2>&1

if ($s3BucketCheck -like "*NoSuchBucket*") {
    Write-Host "Creating S3 bucket $s3BucketName..."
    aws s3 mb "s3://$s3BucketName"
} else {
    Write-Host "S3 bucket $s3BucketName already exists."
}

# Step 4: Upload the zip file to the S3 bucket
Write-Host "Uploading $zipFileName to S3 bucket $s3BucketName..."
aws s3 cp $zipFileName "s3://$s3BucketName/"

# Step 5: Deploy with AWS CloudFormation
Write-Host "Deploying $stackName to AWS CloudFormation..."

try {
    # Check if the stack exists
    Write-Host "Checking if the CloudFormation stack $stackName exists..."
    $stackCheck = aws cloudformation describe-stacks --stack-name $stackName 2>&1

    if ($stackCheck -like "*does not exist*") {
        Write-Host "Creating a new CloudFormation stack..."
        aws cloudformation create-stack `
            --stack-name $stackName `
            --template-body $templatePath `
            --capabilities CAPABILITY_NAMED_IAM `
            --parameters ParameterKey=Prefix,ParameterValue="$prefix"

        Write-Host "Waiting for stack creation to complete..."
        aws cloudformation wait stack-create-complete --stack-name $stackName
    } else {
        Write-Host "Updating existing CloudFormation stack..."
        aws cloudformation update-stack `
            --stack-name $stackName `
            --template-body $templatePath `
            --capabilities CAPABILITY_NAMED_IAM `
            --parameters ParameterKey=Prefix,ParameterValue="$prefix"

        Write-Host "Waiting for stack update to complete..."
        aws cloudformation wait stack-update-complete --stack-name $stackName
    }
    Write-Host "Deployment completed successfully!"
} catch {
    Write-Host "An error occurred: $_"
}