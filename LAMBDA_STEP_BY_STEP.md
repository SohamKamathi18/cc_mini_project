# 🚀 AWS Lambda Implementation - Step by Step Guide

## 📋 Overview

This guide will help you deploy your AI Website Generator to AWS Lambda using your Learner Lab account.

---

## ✅ Prerequisites Checklist

Before starting, make sure you have:

- [ ] AWS Learner Lab activated (green circle)
- [ ] AWS CLI installed and configured
- [ ] Python 3.10+ installed
- [ ] Your project files in: `d:\cc_mini_project\cc_mini_project\cc_mini_project`
- [ ] Google Gemini API key
- [ ] (Optional) Unsplash API key

---

## 🎯 Step 1: Initial Setup

### Run the Setup Script

```powershell
cd d:\cc_mini_project\cc_mini_project\cc_mini_project
.\setup_aws.ps1
```

**This script will:**
- ✅ Verify AWS CLI installation
- ✅ Check your AWS credentials
- ✅ Get LabRole ARN
- ✅ Create S3 bucket for deployments
- ✅ Create Lambda directory structure
- ✅ Create environment variables template

**Expected Output:**
```
========================================
  AWS Lambda Setup - Learner Lab
========================================

1. Checking AWS CLI...
   ✓ AWS CLI found: aws-cli/2.13.0

2. Verifying AWS credentials...
   ✓ Account ID: 123456789012
   ✓ User ARN: arn:aws:sts::123456789012:assumed-role/voclabs/...

3. Getting LabRole ARN...
   ✓ LabRole ARN: arn:aws:iam::123456789012:role/LabRole
   ✓ Saved to: lab_role_arn.txt

4. Creating S3 bucket for Lambda deployment...
   ✓ Bucket created: website-gen-lambda-20251008120000
   ✓ Saved to: bucket_name.txt

5. Creating Lambda directory structure...
   ✓ Created: lambda
   ✓ Created: lambda\generate_website
   ✓ Created: lambda\fetch_templates
   ✓ Created: lambda\fetch_images
   ✓ Created: lambda\health_check
   ✓ Created: lambda\layers
   ✓ Created: lambda\layers\python_dependencies

========================================
  Setup Complete!
========================================
```

---

## 🎯 Step 2: Configure Environment Variables

### Edit `lambda_env.json`

```powershell
notepad lambda_env.json
```

**Update with your actual API keys:**

```json
{
  "Variables": {
    "GOOGLE_API_KEY": "AIzaSyXXXXXXXXXXXXXXXXXXXXXX",
    "UNSPLASH_ACCESS_KEY": "your_unsplash_key_or_leave_empty",
    "S3_BUCKET": "website-gen-lambda-20251008120000",
    "REGION": "us-east-1"
  }
}
```

**⚠️ Important:**
- Replace `GOOGLE_API_KEY` with your actual Gemini API key
- Get key from: https://aistudio.google.com/app/apikey
- S3_BUCKET is automatically set by setup script
- UNSPLASH_ACCESS_KEY is optional

**Save the file!**

---

## 🎯 Step 3: Copy Your Agent Code

Lambda needs access to your `tasks.py` file (contains all agents).

### Copy tasks.py to Lambda function:

```powershell
Copy-Item -Path "app.py" -Destination "lambda\generate_website\tasks.py"
```

### OR Create a simplified version:

The `generate_website` Lambda function needs:
- `BusinessAnalysisAgent`
- `DesignAgent`
- `ContentAgent`
- `ImageAgent`
- `HTMLAgent`
- `BusinessInfo` dataclass

**Option 1:** Copy entire `app.py` and rename to `tasks.py`
**Option 2:** Extract only agent classes (recommended for smaller package)

---

## 🎯 Step 4: Create Lambda Layer (Python Dependencies)

Lambda functions need dependencies packaged as a "Layer".

### Install Dependencies to Layer Directory:

```powershell
# Navigate to layers directory
cd lambda\layers\python_dependencies

# Create python directory (Lambda Layer requirement)
New-Item -ItemType Directory -Path "python" -Force

# Install packages
pip install --target .\python `
    google-generativeai `
    langgraph `
    requests `
    beautifulsoup4 `
    python-dotenv

# Go back to project root
cd ..\..\..
```

**This will create:**
```
lambda/
  └── layers/
      └── python_dependencies/
          └── python/
              ├── google/
              ├── langgraph/
              ├── requests/
              ├── bs4/
              └── ...
```

### Create Layer ZIP:

```powershell
# Compress the layer
Compress-Archive -Path "lambda\layers\python_dependencies\*" `
    -DestinationPath "lambda_layer.zip" -Force
```

### Upload Layer to AWS:

```powershell
# Read bucket name
$bucketName = Get-Content "bucket_name.txt" -Raw

# Upload to S3
aws s3 cp lambda_layer.zip s3://$bucketName/layers/lambda_layer.zip

# Create Lambda Layer
aws lambda publish-layer-version `
    --layer-name website-generator-dependencies `
    --description "Python dependencies for AI Website Generator" `
    --content S3Bucket=$bucketName,S3Key=layers/lambda_layer.zip `
    --compatible-runtimes python3.10 python3.11 `
    --region us-east-1
```

**Save the Layer ARN from output:**
```json
{
    "LayerArn": "arn:aws:lambda:us-east-1:123456789012:layer:website-generator-dependencies",
    "LayerVersionArn": "arn:aws:lambda:us-east-1:123456789012:layer:website-generator-dependencies:1",
    "Version": 1
}
```

**Copy the `LayerVersionArn` - you'll need it!**

Save it to a file:
```powershell
"arn:aws:lambda:us-east-1:123456789012:layer:website-generator-dependencies:1" | 
    Out-File -FilePath "layer_arn.txt"
```

---

## 🎯 Step 5: Package Lambda Function

### Create deployment package for generate_website:

```powershell
# Navigate to function directory
cd lambda\generate_website

# Create deployment package (zip)
Compress-Archive -Path lambda_function.py,tasks.py `
    -DestinationPath "..\generate_website.zip" -Force

# Go back to root
cd ..\..
```

---

## 🎯 Step 6: Create Lambda Function in AWS

### Read required values:

```powershell
$labRoleArn = Get-Content "lab_role_arn.txt" -Raw
$layerArn = Get-Content "layer_arn.txt" -Raw
$bucketName = Get-Content "bucket_name.txt" -Raw
```

### Upload function code to S3:

```powershell
aws s3 cp lambda\generate_website.zip s3://$bucketName/functions/generate_website.zip
```

### Create the Lambda function:

```powershell
aws lambda create-function `
    --function-name generate-website `
    --runtime python3.10 `
    --role $labRoleArn `
    --handler lambda_function.lambda_handler `
    --code S3Bucket=$bucketName,S3Key=functions/generate_website.zip `
    --timeout 300 `
    --memory-size 1024 `
    --layers $layerArn `
    --environment file://lambda_env.json `
    --region us-east-1
```

**Expected Output:**
```json
{
    "FunctionName": "generate-website",
    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:generate-website",
    "Runtime": "python3.10",
    "Role": "arn:aws:iam::123456789012:role/LabRole",
    "Handler": "lambda_function.lambda_handler",
    "State": "Active"
}
```

**✅ Lambda function created!**

---

## 🎯 Step 7: Test Lambda Function

### Test with AWS CLI:

```powershell
# Create test event
$testEvent = @"
{
  "body": "{\"business_name\":\"Test Coffee Shop\",\"description\":\"A cozy coffee shop\",\"services\":\"Coffee, Pastries\",\"target_audience\":\"Students\",\"color_preference\":\"Warm browns\",\"style_preference\":\"Cozy\",\"template_id\":\"modern_glass\"}"
}
"@

# Save to file
$testEvent | Out-File -FilePath "test_event.json" -Encoding UTF8

# Invoke Lambda
aws lambda invoke `
    --function-name generate-website `
    --payload file://test_event.json `
    --region us-east-1 `
    output.json

# View result
Get-Content output.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Check CloudWatch Logs:

```powershell
# Get latest log stream
aws logs describe-log-streams `
    --log-group-name /aws/lambda/generate-website `
    --order-by LastEventTime `
    --descending `
    --max-items 1 `
    --region us-east-1

# View logs
aws logs tail /aws/lambda/generate-website --follow
```

---

## 🎯 Step 8: Create API Gateway (Next)

After Lambda is working, you'll create API Gateway to expose HTTP endpoints.

**Coming next:** `API_GATEWAY_SETUP.md`

---

## 🔧 Troubleshooting

### Error: "Unable to import module 'lambda_function'"
**Solution:**
- Check that `tasks.py` is in the deployment package
- Verify Layer is attached to function
- Check CloudWatch logs for specific import errors

### Error: "Task timed out after 300.00 seconds"
**Solution:**
- Increase Lambda timeout
- Check if Gemini API is responding
- Optimize agent code

### Error: "No module named 'google.generativeai'"
**Solution:**
- Layer not attached correctly
- Re-create layer with correct dependencies
- Verify layer ARN is correct

### Error: "Access Denied" when accessing S3
**Solution:**
- LabRole needs S3 permissions
- Check bucket exists
- Verify bucket name in environment variables

---

## 📊 Current Progress

✅ Step 1: Initial Setup
✅ Step 2: Configure Environment
✅ Step 3: Copy Agent Code
✅ Step 4: Create Lambda Layer
✅ Step 5: Package Function
✅ Step 6: Create Lambda Function
✅ Step 7: Test Lambda Function
⏳ Step 8: Create API Gateway (Next)

---

## 🎓 Learner Lab Tips

1. **Save frequently** - Sessions expire after 4 hours
2. **Monitor costs** - Check remaining budget
3. **Use CloudWatch** - Debug with logs
4. **Test locally first** - Use `python lambda_function.py`
5. **Keep credentials updated** - Restart lab refreshes tokens

---

## 📞 Next Steps

Once Lambda is working:
1. Create API Gateway
2. Connect frontend to API
3. Test end-to-end flow
4. Deploy frontend to S3

**Run:** `.\create_api_gateway.ps1` (coming next)

---

**Need help? Check CloudWatch Logs or AWS Lambda console!**
