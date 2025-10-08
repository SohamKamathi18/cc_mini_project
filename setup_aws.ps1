# AWS Lambda Setup Script for Learner Lab

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AWS Lambda Setup - Learner Lab" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check AWS CLI
Write-Host "1. Checking AWS CLI..." -ForegroundColor Yellow
try {
    $awsVersion = aws --version
    Write-Host "   OK AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "   ERROR AWS CLI not found! Please install it first." -ForegroundColor Red
    Write-Host "   Download from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    exit 1
}

# 2. Verify credentials
Write-Host "2. Verifying AWS credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "   OK Account ID: $($identity.Account)" -ForegroundColor Green
    Write-Host "   OK User ARN: $($identity.Arn)" -ForegroundColor Green
} catch {
    Write-Host "   ERROR Invalid credentials! Please configure AWS CLI." -ForegroundColor Red
    Write-Host "   Run: aws configure" -ForegroundColor Yellow
    exit 1
}

# 3. Get LabRole ARN
Write-Host "3. Getting LabRole ARN..." -ForegroundColor Yellow
try {
    $labRoleArn = aws iam get-role --role-name LabRole --query 'Role.Arn' --output text
    Write-Host "   OK LabRole ARN: $labRoleArn" -ForegroundColor Green
    $labRoleArn | Out-File -FilePath "lab_role_arn.txt" -Encoding UTF8
    Write-Host "   OK Saved to: lab_role_arn.txt" -ForegroundColor Green
} catch {
    Write-Host "   ERROR Could not find LabRole!" -ForegroundColor Red
    Write-Host "   Make sure you are using AWS Learner Lab account" -ForegroundColor Yellow
    exit 1
}

# 4. Create S3 bucket
Write-Host "4. Creating S3 bucket for Lambda deployment..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$bucketName = "website-gen-lambda-$timestamp"
try {
    aws s3 mb "s3://$bucketName" --region us-east-1 2>&1 | Out-Null
    Write-Host "   OK Bucket created: $bucketName" -ForegroundColor Green
    $bucketName | Out-File -FilePath "bucket_name.txt" -Encoding UTF8
    Write-Host "   OK Saved to: bucket_name.txt" -ForegroundColor Green
} catch {
    Write-Host "   ERROR Failed to create bucket!" -ForegroundColor Red
    Write-Host "   Bucket name: $bucketName" -ForegroundColor Yellow
}

# 5. Create lambda directory structure
Write-Host "5. Creating Lambda directory structure..." -ForegroundColor Yellow
$lambdaDirs = @(
    "lambda",
    "lambda\generate_website",
    "lambda\fetch_templates",
    "lambda\fetch_images",
    "lambda\health_check",
    "lambda\layers",
    "lambda\layers\python_dependencies"
)
foreach ($dir in $lambdaDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   OK Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "   Already exists: $dir" -ForegroundColor Gray
    }
}

# 6. Check Python
Write-Host "6. Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "   OK Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ERROR Python not found!" -ForegroundColor Red
    exit 1
}

# 7. Install SAM CLI
Write-Host "7. Checking SAM CLI..." -ForegroundColor Yellow
try {
    $samVersion = sam --version
    Write-Host "   OK SAM CLI found: $samVersion" -ForegroundColor Green
} catch {
    Write-Host "   WARNING SAM CLI not found. Installing..." -ForegroundColor Yellow
    pip install aws-sam-cli
    Write-Host "   OK SAM CLI installed" -ForegroundColor Green
}

# 8. Create lambda_env.json template
Write-Host "8. Creating environment variables template..." -ForegroundColor Yellow
$envTemplate = @"
{
  "Variables": {
    "GOOGLE_API_KEY": "your_gemini_api_key_here",
    "UNSPLASH_ACCESS_KEY": "your_unsplash_key_here",
    "S3_BUCKET": "$bucketName",
    "REGION": "us-east-1"
  }
}
"@

if (!(Test-Path "lambda_env.json")) {
    $envTemplate | Out-File -FilePath "lambda_env.json" -Encoding UTF8
    Write-Host "   OK Created: lambda_env.json" -ForegroundColor Green
    Write-Host "   WARNING Remember to update with your actual API keys!" -ForegroundColor Yellow
} else {
    Write-Host "   Already exists: lambda_env.json" -ForegroundColor Gray
}

# 9. Update .gitignore
Write-Host "9. Updating .gitignore..." -ForegroundColor Yellow
$gitignoreEntries = @"

# AWS Lambda files
lambda_env.json
lab_role_arn.txt
bucket_name.txt
lambda/layers/python_dependencies/
*.zip
"@

Add-Content -Path ".gitignore" -Value $gitignoreEntries
Write-Host "   OK Updated .gitignore" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files Created:" -ForegroundColor Yellow
Write-Host "   - lab_role_arn.txt (LabRole ARN)"
Write-Host "   - bucket_name.txt (S3 Bucket Name)"
Write-Host "   - lambda_env.json (Environment variables template)"
Write-Host "   - lambda/ directory structure"
Write-Host ""
Write-Host "Important Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Edit lambda_env.json and add your API keys:"
Write-Host "      - GOOGLE_API_KEY (from Google AI Studio)"
Write-Host "      - UNSPLASH_ACCESS_KEY (optional)"
Write-Host ""
Write-Host "   2. Read AWS_SETUP_GUIDE.md for detailed instructions"
Write-Host ""
Write-Host "   3. Follow LAMBDA_STEP_BY_STEP.md for deployment"
Write-Host ""
Write-Host "Learner Lab Reminder:" -ForegroundColor Cyan
Write-Host "   - Lab sessions expire after 4 hours"
Write-Host "   - Save your work frequently"
Write-Host "   - Check remaining budget in AWS Academy"
Write-Host ""
