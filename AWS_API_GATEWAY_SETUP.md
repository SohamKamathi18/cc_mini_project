# 🌐 AWS API Gateway Setup Guide

## 📋 Overview

This guide sets up Amazon API Gateway to create RESTful API endpoints for the Business Website Generator, connecting your React frontend to Lambda functions.

---

## 🎯 API Gateway Architecture

```
React Frontend
    ↓
API Gateway (REST API)
    ├── GET  /health          → health-check
    ├── POST /generate        → generate-website Lambda
    ├── GET  /templates       → list-templates Lambda (future)
    └── GET  /download/{id}   → download Lambda (future)
    ↓
Lambda Functions
    ↓
S3 Storage
```

---

## 📡 API Endpoints Design

### 1. Health Check Endpoint
```
GET /health
Response: { "status": "ok", "timestamp": "2025-10-08T12:00:00Z" }
```

### 2. Generate Website Endpoint
```
POST /generate
Headers: Content-Type: application/json
Body: {
  "business_name": "My Business",
  "description": "Business description",
  "services": "Service list",
  "target_audience": "Target customers",
  "color_preference": "blue",
  "style_preference": "modern",
  "template_id": "modern_glass"
}
Response: {
  "success": true,
  "session_id": "mybusiness-20251008120000",
  "s3_url": "https://bucket.s3.amazonaws.com/...",
  "html": "<html>...</html>"
}
```

### 3. List Templates Endpoint (Future)
```
GET /templates
Response: {
  "templates": [
    { "id": "modern_glass", "name": "Modern Glass" },
    { "id": "minimal_elegant", "name": "Minimal Elegant" }
  ]
}
```

---

## ✅ Prerequisites

1. AWS Lambda function created (`generate-website`)
2. AWS CLI configured
3. Lambda function ARN available

---

## 🚀 Quick Setup Commands

### Step 1: Get Lambda Function ARN

```powershell
# Get Lambda ARN
$lambdaArn = (aws lambda get-function --function-name generate-website --query 'Configuration.FunctionArn' --output text)
Write-Host "Lambda ARN: $lambdaArn"

# Save for later use
$lambdaArn | Out-File -FilePath "lambda_arn.txt" -Encoding utf8
```

### Step 2: Create REST API

```powershell
# Create API Gateway REST API
$apiName = "website-generator-api"
$apiDescription = "REST API for Business Website Generator"

$apiId = (aws apigateway create-rest-api `
    --name $apiName `
    --description $apiDescription `
    --endpoint-configuration types=REGIONAL `
    --query 'id' --output text)

Write-Host "✓ API Created: $apiId"

# Save API ID
$apiId | Out-File -FilePath "api_gateway_id.txt" -Encoding utf8
```

### Step 3: Get Root Resource ID

```powershell
# Get root resource ID
$rootResourceId = (aws apigateway get-resources `
    --rest-api-id $apiId `
    --query 'items[0].id' --output text)

Write-Host "✓ Root Resource ID: $rootResourceId"
```

### Step 4: Create /health Resource

```powershell
# Create /health resource
$healthResourceId = (aws apigateway create-resource `
    --rest-api-id $apiId `
    --parent-id $rootResourceId `
    --path-part "health" `
    --query 'id' --output text)

Write-Host "✓ Created /health resource: $healthResourceId"
```

### Step 5: Create GET Method for /health

```powershell
# Create GET method for /health (mock response)
aws apigateway put-method `
    --rest-api-id $apiId `
    --resource-id $healthResourceId `
    --http-method GET `
    --authorization-type NONE

# Set up mock integration
aws apigateway put-integration `
    --rest-api-id $apiId `
    --resource-id $healthResourceId `
    --http-method GET `
    --type MOCK `
    --request-templates '{"application/json": "{\"statusCode\": 200}"}'

# Set up method response
aws apigateway put-method-response `
    --rest-api-id $apiId `
    --resource-id $healthResourceId `
    --http-method GET `
    --status-code 200 `
    --response-models '{"application/json": "Empty"}'

# Set up integration response
aws apigateway put-integration-response `
    --rest-api-id $apiId `
    --resource-id $healthResourceId `
    --http-method GET `
    --status-code 200 `
    --response-templates '{"application/json": "{\"status\":\"ok\",\"message\":\"API is healthy\"}"}'

Write-Host "✓ GET /health configured"
```

### Step 6: Create /generate Resource

```powershell
# Create /generate resource
$generateResourceId = (aws apigateway create-resource `
    --rest-api-id $apiId `
    --parent-id $rootResourceId `
    --path-part "generate" `
    --query 'id' --output text)

Write-Host "✓ Created /generate resource: $generateResourceId"
```

### Step 7: Create POST Method for /generate

```powershell
# Get AWS Account ID
$accountId = (aws sts get-caller-identity --query 'Account' --output text)
$region = "us-east-1"

# Create POST method
aws apigateway put-method `
    --rest-api-id $apiId `
    --resource-id $generateResourceId `
    --http-method POST `
    --authorization-type NONE `
    --request-parameters "method.request.header.Content-Type=false"

# Set up Lambda integration
$lambdaUri = "arn:aws:apigateway:${region}:lambda:path/2015-03-31/functions/${lambdaArn}/invocations"

aws apigateway put-integration `
    --rest-api-id $apiId `
    --resource-id $generateResourceId `
    --http-method POST `
    --type AWS_PROXY `
    --integration-http-method POST `
    --uri $lambdaUri

Write-Host "✓ POST /generate configured with Lambda integration"
```

### Step 8: Grant API Gateway Permission to Invoke Lambda

```powershell
# Add Lambda permission for API Gateway
$sourceArn = "arn:aws:execute-api:${region}:${accountId}:${apiId}/*/*"

aws lambda add-permission `
    --function-name generate-website `
    --statement-id apigateway-invoke-permission `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn $sourceArn

Write-Host "✓ Lambda permission granted to API Gateway"
```

### Step 9: Enable CORS

```powershell
# Enable CORS on /generate resource
# Create OPTIONS method
aws apigateway put-method `
    --rest-api-id $apiId `
    --resource-id $generateResourceId `
    --http-method OPTIONS `
    --authorization-type NONE

# Set up mock integration for OPTIONS
aws apigateway put-integration `
    --rest-api-id $apiId `
    --resource-id $generateResourceId `
    --http-method OPTIONS `
    --type MOCK `
    --request-templates '{"application/json": "{\"statusCode\": 200}"}'

# Configure CORS response
aws apigateway put-method-response `
    --rest-api-id $apiId `
    --resource-id $generateResourceId `
    --http-method OPTIONS `
    --status-code 200 `
    --response-parameters "method.response.header.Access-Control-Allow-Headers=true,method.response.header.Access-Control-Allow-Methods=true,method.response.header.Access-Control-Allow-Origin=true" `
    --response-models '{"application/json": "Empty"}'

aws apigateway put-integration-response `
    --rest-api-id $apiId `
    --resource-id $generateResourceId `
    --http-method OPTIONS `
    --status-code 200 `
    --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\":\"'"'"'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"'"'\",\"method.response.header.Access-Control-Allow-Methods\":\"'"'"'GET,POST,OPTIONS'"'"'\",\"method.response.header.Access-Control-Allow-Origin\":\"'"'"'*'"'"'\"}'

Write-Host "✓ CORS enabled on /generate"
```

### Step 10: Deploy API to Stage

```powershell
# Create deployment
$deploymentId = (aws apigateway create-deployment `
    --rest-api-id $apiId `
    --stage-name prod `
    --stage-description "Production Stage" `
    --description "Initial deployment" `
    --query 'id' --output text)

Write-Host "✓ API deployed to 'prod' stage"

# Get API endpoint URL
$apiUrl = "https://${apiId}.execute-api.${region}.amazonaws.com/prod"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  API Gateway Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Endpoint URL:" -ForegroundColor Yellow
Write-Host $apiUrl -ForegroundColor White
Write-Host ""
Write-Host "Available Endpoints:" -ForegroundColor Yellow
Write-Host "  GET  ${apiUrl}/health" -ForegroundColor Cyan
Write-Host "  POST ${apiUrl}/generate" -ForegroundColor Cyan
Write-Host ""

# Save API URL
$apiUrl | Out-File -FilePath "api_gateway_url.txt" -Encoding utf8
```

---

## 🧪 Test API Endpoints

### Test 1: Health Check

```powershell
# Test health endpoint
$apiUrl = Get-Content "api_gateway_url.txt" -Raw
Invoke-RestMethod -Uri "$apiUrl/health" -Method GET
```

Expected Response:
```json
{
  "status": "ok",
  "message": "API is healthy"
}
```

### Test 2: Generate Website

```powershell
# Test generate endpoint
$apiUrl = Get-Content "api_gateway_url.txt" -Raw

$body = @{
    business_name = "Test Cafe"
    description = "A cozy cafe"
    services = "Coffee, Snacks"
    target_audience = "Students"
    color_preference = "blue"
    style_preference = "modern"
    template_id = "modern_glass"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

$response = Invoke-RestMethod -Uri "$apiUrl/generate" -Method POST -Headers $headers -Body $body

Write-Host "Response:"
$response | ConvertTo-Json -Depth 5
```

### Test 3: Test with cURL (alternative)

```bash
# Health check
curl https://{api-id}.execute-api.us-east-1.amazonaws.com/prod/health

# Generate website
curl -X POST https://{api-id}.execute-api.us-east-1.amazonaws.com/prod/generate \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test Cafe",
    "description": "A cozy cafe",
    "services": "Coffee, Snacks",
    "target_audience": "Students",
    "color_preference": "blue",
    "style_preference": "modern",
    "template_id": "modern_glass"
  }'
```

---

## 📊 Monitor API Usage

### View API Logs in CloudWatch

```powershell
# Enable CloudWatch logging for API Gateway
aws apigateway update-stage `
    --rest-api-id $apiId `
    --stage-name prod `
    --patch-operations "op=replace,path=/*/*/logging/loglevel,value=INFO" `
                       "op=replace,path=/*/*/logging/dataTrace,value=true" `
                       "op=replace,path=/*/*/metrics/enabled,value=true"

Write-Host "✓ CloudWatch logging enabled"
```

### View API Metrics

```powershell
# Get API metrics (last 1 hour)
$endTime = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
$startTime = (Get-Date).AddHours(-1).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")

aws cloudwatch get-metric-statistics `
    --namespace AWS/ApiGateway `
    --metric-name Count `
    --dimensions Name=ApiName,Value=website-generator-api `
    --start-time $startTime `
    --end-time $endTime `
    --period 3600 `
    --statistics Sum
```

---

## 🔧 Update and Redeploy API

```powershell
# After making changes, redeploy
$apiId = Get-Content "api_gateway_id.txt" -Raw

aws apigateway create-deployment `
    --rest-api-id $apiId `
    --stage-name prod `
    --description "Updated deployment"

Write-Host "✓ API redeployed"
```

---

## 🗑️ Cleanup Commands

### Delete API Gateway

```powershell
# Delete API Gateway
$apiId = Get-Content "api_gateway_id.txt" -Raw

aws apigateway delete-rest-api --rest-api-id $apiId

Write-Host "✓ API Gateway deleted"
```

### Remove Lambda Permission

```powershell
# Remove API Gateway permission from Lambda
aws lambda remove-permission `
    --function-name generate-website `
    --statement-id apigateway-invoke-permission

Write-Host "✓ Lambda permission removed"
```

---

## 💰 Cost Estimation

**API Gateway Pricing (us-east-1):**
- First 333 million requests: $3.50 per million requests
- Free tier: 1 million requests/month (first 12 months)

**Example Monthly Cost:**
- 1000 API calls = ~$0.0035
- 10,000 API calls = ~$0.035
- **Within Free Tier: $0.00**

---

## 🔐 Security Enhancements (Optional)

### Add API Key Authentication

```powershell
# Create API Key
$apiKeyId = (aws apigateway create-api-key `
    --name "website-generator-key" `
    --description "API Key for Website Generator" `
    --enabled `
    --query 'id' --output text)

# Create Usage Plan
$usagePlanId = (aws apigateway create-usage-plan `
    --name "website-generator-plan" `
    --description "Usage plan for Website Generator" `
    --throttle burstLimit=10,rateLimit=5 `
    --quota limit=1000,period=MONTH `
    --api-stages apiId=$apiId,stage=prod `
    --query 'id' --output text)

# Associate API Key with Usage Plan
aws apigateway create-usage-plan-key `
    --usage-plan-id $usagePlanId `
    --key-id $apiKeyId `
    --key-type API_KEY

Write-Host "✓ API Key created and associated with usage plan"
```

### Add Rate Limiting

```powershell
# Update stage to add throttling
aws apigateway update-stage `
    --rest-api-id $apiId `
    --stage-name prod `
    --patch-operations "op=replace,path=/throttle/burstLimit,value=100" `
                       "op=replace,path=/throttle/rateLimit,value=50"

Write-Host "✓ Rate limiting configured (50 req/sec, 100 burst)"
```

---

## 🎓 API Gateway Concepts

### Integration Types
- **AWS_PROXY**: Lambda proxy integration (passes entire request)
- **AWS**: Lambda custom integration (transform request/response)
- **HTTP**: Integrate with HTTP endpoints
- **MOCK**: Return fixed response (no backend)

### Stage Variables
Use to parameterize API configurations:
```powershell
aws apigateway create-deployment `
    --rest-api-id $apiId `
    --stage-name dev `
    --variables lambdaAlias=DEV
```

---

## ✅ API Gateway Setup Checklist

- [ ] API Gateway created
- [ ] /health endpoint configured (GET)
- [ ] /generate endpoint configured (POST)
- [ ] Lambda integration set up
- [ ] Lambda permission granted
- [ ] CORS enabled
- [ ] API deployed to 'prod' stage
- [ ] Health endpoint tested
- [ ] Generate endpoint tested
- [ ] CloudWatch logging enabled
- [ ] API URL saved for frontend

---

## 🔗 Next Steps

After API Gateway setup:
1. ✅ Update React frontend to use API Gateway URL
2. ✅ Test end-to-end flow (Frontend → API → Lambda → S3)
3. ✅ Add error handling in frontend
4. ✅ (Optional) Set up custom domain with Route53
5. ✅ (Optional) Add CloudFront distribution

---

**Created:** October 8, 2025  
**Last Updated:** October 8, 2025  
**Author:** GitHub Copilot  
**Project:** Business Website Generator - AWS Integration
