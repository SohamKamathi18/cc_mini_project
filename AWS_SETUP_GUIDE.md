# 🎓 AWS Learner Lab Setup Guide

## Step 1: Activate AWS Learner Lab

1. **Login to AWS Academy:**
   - Go to your AWS Academy course
   - Click on "Modules"
   - Find "Learner Lab - Foundational Services"

2. **Start Lab:**
   - Click "Start Lab" button
   - Wait for the circle to turn GREEN (2-3 minutes)
   - Note: Lab sessions last **4 hours** - save your work frequently!

3. **Get AWS Credentials:**
   ```
   Click "AWS Details" button
   Click "Show" next to AWS CLI credentials
   Copy the entire credential block
   ```

   You'll see something like:
   ```bash
   [default]
   aws_access_key_id=ASIAXXXXXXXXXXX
   aws_secret_access_key=XXXXXXXXXXXXXXXXXX
   aws_session_token=XXXXXXXXXXXXXXXXXX
   ```

---

## Step 2: Configure AWS CLI

### Install AWS CLI (if not installed)
```powershell
# Check if AWS CLI is installed
aws --version

# If not installed, download from:
# https://aws.amazon.com/cli/
```

### Configure Credentials
```powershell
# Option 1: Manual configuration
aws configure

# When prompted, paste:
# - Access Key ID
# - Secret Access Key
# - Default region: us-east-1
# - Default output: json

# Option 2: Credential file (Recommended for Learner Lab)
# Create/Edit: C:\Users\YourUsername\.aws\credentials
```

**Important for Learner Lab:**
Since credentials include a **session token**, create a credentials file:

1. Create file: `C:\Users\YourUsername\.aws\credentials`
2. Paste the entire credential block from AWS Details
3. Save the file

**Test Connection:**
```powershell
aws sts get-caller-identity
```

If successful, you'll see your AWS account details!

---

## Step 3: Understand Learner Lab Constraints

### ✅ What You CAN Do:
- Create Lambda functions
- Create S3 buckets
- Create API Gateway
- Create CloudWatch logs
- Create IAM roles (limited - use LabRole)
- Create DynamoDB tables

### ❌ What You CANNOT Do:
- Create IAM users
- Create custom VPCs
- Use Route53 (DNS)
- Create NAT Gateways
- Modify account settings
- Access some regions (usually locked to us-east-1)

### ⚠️ Important Limits:
- **Session Duration:** 4 hours (then you need to restart lab)
- **Budget:** $50-100 (check remaining credit in lab)
- **Region:** Usually us-east-1 only
- **IAM Roles:** Must use provided `LabRole`

---

## Step 4: Verify Your Setup

Run these commands to verify everything is ready:

```powershell
# 1. Check AWS CLI version
aws --version

# 2. Verify credentials
aws sts get-caller-identity

# 3. Check available regions (should show us-east-1)
aws ec2 describe-regions --output table

# 4. List existing Lambda functions (should be empty)
aws lambda list-functions

# 5. List S3 buckets
aws s3 ls

# 6. Check your IAM role
aws iam get-role --role-name LabRole
```

---

## Step 5: Install Required Tools

### AWS SAM CLI (for Lambda testing)
```powershell
# Check if installed
sam --version

# Install using pip
pip install aws-sam-cli

# Verify installation
sam --version
```

### Python Dependencies for Lambda
```powershell
# Navigate to your project
cd d:\cc_mini_project\cc_mini_project\cc_mini_project

# Install dependencies locally (needed for packaging)
pip install --target ./lambda_package google-generativeai langgraph requests python-dotenv
```

---

## Step 6: Create Project Structure for Lambda

We'll organize Lambda functions in a new directory:

```
cc_mini_project/
├── lambda/
│   ├── generate_website/
│   │   ├── lambda_function.py
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── fetch_templates/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   ├── fetch_images/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   └── layers/
│       └── python_dependencies/
│           └── python/
│               └── (packages)
├── frontend/
├── templates/
└── README.md
```

---

## Step 7: Lambda Execution Role (Using LabRole)

In Learner Lab, you **cannot create custom IAM roles**, so we'll use `LabRole`:

```bash
# Get LabRole ARN (save this!)
aws iam get-role --role-name LabRole --query 'Role.Arn' --output text
```

**Expected Output:**
```
arn:aws:iam::123456789012:role/LabRole
```

**Save this ARN** - you'll need it when creating Lambda functions!

---

## Step 8: Create S3 Bucket for Lambda Code

```powershell
# Create a unique bucket name (S3 bucket names must be globally unique)
$BUCKET_NAME = "website-generator-lambda-$(Get-Date -Format 'yyyyMMddHHmmss')"

# Create bucket
aws s3 mb s3://$BUCKET_NAME --region us-east-1

# Verify bucket was created
aws s3 ls

# Save bucket name for later
echo $BUCKET_NAME > bucket_name.txt
```

---

## Step 9: Environment Variables for Lambda

Create a file to store Lambda environment variables:

**File: `lambda_env.json`**
```json
{
  "Variables": {
    "GOOGLE_API_KEY": "your_gemini_api_key_here",
    "UNSPLASH_ACCESS_KEY": "your_unsplash_key_here",
    "S3_BUCKET": "your_bucket_name_here",
    "REGION": "us-east-1"
  }
}
```

**Security Note:** Never commit this file to Git! Add to `.gitignore`.

---

## Step 10: Quick Setup Script

Run this script to set up everything automatically:

**File: `setup_aws.ps1`**
```powershell
# AWS Lambda Setup Script for Learner Lab

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AWS Lambda Setup - Learner Lab" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check AWS CLI
Write-Host "1. Checking AWS CLI..." -ForegroundColor Yellow
try {
    $awsVersion = aws --version
    Write-Host "   ✓ AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ AWS CLI not found! Please install it first." -ForegroundColor Red
    exit 1
}

# 2. Verify credentials
Write-Host "2. Verifying AWS credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Host "   ✓ Account ID: $($identity.Account)" -ForegroundColor Green
    Write-Host "   ✓ User ARN: $($identity.Arn)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Invalid credentials! Please configure AWS CLI." -ForegroundColor Red
    exit 1
}

# 3. Get LabRole ARN
Write-Host "3. Getting LabRole ARN..." -ForegroundColor Yellow
try {
    $labRoleArn = aws iam get-role --role-name LabRole --query 'Role.Arn' --output text
    Write-Host "   ✓ LabRole ARN: $labRoleArn" -ForegroundColor Green
    $labRoleArn | Out-File -FilePath "lab_role_arn.txt" -Encoding UTF8
} catch {
    Write-Host "   ✗ Could not find LabRole!" -ForegroundColor Red
    exit 1
}

# 4. Create S3 bucket
Write-Host "4. Creating S3 bucket..." -ForegroundColor Yellow
$bucketName = "website-gen-lambda-$(Get-Date -Format 'yyyyMMddHHmmss')"
try {
    aws s3 mb "s3://$bucketName" --region us-east-1
    Write-Host "   ✓ Bucket created: $bucketName" -ForegroundColor Green
    $bucketName | Out-File -FilePath "bucket_name.txt" -Encoding UTF8
} catch {
    Write-Host "   ✗ Failed to create bucket!" -ForegroundColor Red
}

# 5. Create lambda directory structure
Write-Host "5. Creating Lambda directory structure..." -ForegroundColor Yellow
$lambdaDirs = @(
    "lambda",
    "lambda\generate_website",
    "lambda\fetch_templates",
    "lambda\fetch_images",
    "lambda\layers"
)
foreach ($dir in $lambdaDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✓ Created: $dir" -ForegroundColor Green
    }
}

# 6. Install SAM CLI
Write-Host "6. Checking SAM CLI..." -ForegroundColor Yellow
try {
    $samVersion = sam --version
    Write-Host "   ✓ SAM CLI found: $samVersion" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ SAM CLI not found. Installing..." -ForegroundColor Yellow
    pip install aws-sam-cli
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Update lambda_env.json with your API keys"
Write-Host "2. Run: .\create_lambda_functions.ps1"
Write-Host ""
Write-Host "Saved Files:" -ForegroundColor Yellow
Write-Host "- lab_role_arn.txt (LabRole ARN)"
Write-Host "- bucket_name.txt (S3 Bucket Name)"
Write-Host ""
```

---

## ✅ Setup Verification Checklist

Before proceeding to create Lambda functions:

- [ ] AWS Learner Lab is ACTIVE (green circle)
- [ ] AWS CLI is installed and configured
- [ ] `aws sts get-caller-identity` works
- [ ] LabRole ARN is saved in `lab_role_arn.txt`
- [ ] S3 bucket is created and name saved in `bucket_name.txt`
- [ ] SAM CLI is installed
- [ ] `lambda/` directory structure exists
- [ ] `.env` file has your API keys
- [ ] `lambda_env.json` is created with API keys

---

## 🚨 Troubleshooting

### Issue: "Unable to locate credentials"
**Solution:**
```powershell
# Re-copy credentials from AWS Details
# Update C:\Users\YourUsername\.aws\credentials
# Make sure to include the session_token!
```

### Issue: "Access Denied" when creating resources
**Solution:**
- Learner Lab has restrictions
- Make sure you're in **us-east-1** region
- Some services may be restricted - try a different approach

### Issue: "Session expired"
**Solution:**
- Lab sessions expire after 4 hours
- Click "Start Lab" again
- Re-copy credentials from AWS Details
- Update credentials file

### Issue: "Bucket already exists"
**Solution:**
- S3 bucket names are globally unique
- Use timestamp in bucket name
- Try: `website-gen-lambda-$(Get-Date -Format 'yyyyMMddHHmmss')`

---

## 📞 Need Help?

If you encounter issues:
1. Check AWS Learner Lab status (must be GREEN)
2. Verify credentials are copied correctly
3. Ensure you're in us-east-1 region
4. Check remaining lab budget
5. Restart lab if session expired

---

**Next:** Once setup is complete, we'll create the Lambda functions!

Run: `.\setup_aws.ps1` to begin automated setup.
