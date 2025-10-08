# AWS API Gateway Setup Script for Business Website Generator
# Automated REST API creation with Lambda integration

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  API Gateway Setup - Website Gen" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$REGION = "us-east-1"
$API_NAME = "website-generator-api"
$STAGE_NAME = "prod"
$LAMBDA_FUNCTION_NAME = "generate-website"

# Step 1: Get Lambda Function ARN
Write-Host "[1/10] Getting Lambda function ARN..." -ForegroundColor Yellow
try {
    $lambdaArn = (aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME --region $REGION --query 'Configuration.FunctionArn' --output text 2>&1)
    if ($LASTEXITCODE -ne 0) { throw "Lambda function not found" }
    Write-Host "✓ Lambda ARN: $lambdaArn" -ForegroundColor Green
    $lambdaArn | Out-File -FilePath "lambda_arn.txt" -Encoding utf8 -NoNewline
} catch {
    Write-Host "✗ Failed to get Lambda ARN. Make sure Lambda function exists." -ForegroundColor Red
    exit 1
}

# Step 2: Get AWS Account ID
Write-Host "`n[2/10] Getting AWS Account ID..." -ForegroundColor Yellow
try {
    $accountId = (aws sts get-caller-identity --query 'Account' --output text 2>&1)
    Write-Host "✓ Account ID: $accountId" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to get account ID" -ForegroundColor Red
    exit 1
}

# Step 3: Create REST API
Write-Host "`n[3/10] Creating REST API..." -ForegroundColor Yellow
try {
    $apiId = (aws apigateway create-rest-api `
        --name $API_NAME `
        --description "REST API for Business Website Generator" `
        --endpoint-configuration types=REGIONAL `
        --region $REGION `
        --query 'id' --output text 2>&1)
    
    if ($LASTEXITCODE -ne 0) { throw "Failed to create API" }
    Write-Host "✓ API Created: $apiId" -ForegroundColor Green
    $apiId | Out-File -FilePath "api_gateway_id.txt" -Encoding utf8 -NoNewline
} catch {
    Write-Host "✗ Failed to create API Gateway" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 2

# Step 4: Get Root Resource ID
Write-Host "`n[4/10] Getting root resource..." -ForegroundColor Yellow
try {
    $rootResourceId = (aws apigateway get-resources `
        --rest-api-id $apiId `
        --region $REGION `
        --query 'items[0].id' --output text 2>&1)
    
    Write-Host "✓ Root Resource ID: $rootResourceId" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to get root resource" -ForegroundColor Red
    exit 1
}

# Step 5: Create /health Resource
Write-Host "`n[5/10] Creating /health endpoint..." -ForegroundColor Yellow
try {
    $healthResourceId = (aws apigateway create-resource `
        --rest-api-id $apiId `
        --parent-id $rootResourceId `
        --path-part "health" `
        --region $REGION `
        --query 'id' --output text 2>&1)
    
    # Create GET method
    aws apigateway put-method `
        --rest-api-id $apiId `
        --resource-id $healthResourceId `
        --http-method GET `
        --authorization-type NONE `
        --region $REGION 2>&1 | Out-Null
    
    # Set up mock integration
    aws apigateway put-integration `
        --rest-api-id $apiId `
        --resource-id $healthResourceId `
        --http-method GET `
        --type MOCK `
        --region $REGION `
        --request-templates '{\"application/json\": \"{\\\"statusCode\\\": 200}\"}' 2>&1 | Out-Null
    
    # Method response
    aws apigateway put-method-response `
        --rest-api-id $apiId `
        --resource-id $healthResourceId `
        --http-method GET `
        --status-code 200 `
        --region $REGION `
        --response-models '{\"application/json\": \"Empty\"}' 2>&1 | Out-Null
    
    # Integration response
    aws apigateway put-integration-response `
        --rest-api-id $apiId `
        --resource-id $healthResourceId `
        --http-method GET `
        --status-code 200 `
        --region $REGION `
        --response-templates '{\"application/json\": \"{\\\"status\\\":\\\"ok\\\",\\\"message\\\":\\\"API is healthy\\\",\\\"timestamp\\\":\\\"\$context.requestTime\\\"}\"}' 2>&1 | Out-Null
    
    Write-Host "✓ GET /health configured" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not create /health endpoint" -ForegroundColor Yellow
}

Start-Sleep -Seconds 1

# Step 6: Create /generate Resource
Write-Host "`n[6/10] Creating /generate endpoint..." -ForegroundColor Yellow
try {
    $generateResourceId = (aws apigateway create-resource `
        --rest-api-id $apiId `
        --parent-id $rootResourceId `
        --path-part "generate" `
        --region $REGION `
        --query 'id' --output text 2>&1)
    
    Write-Host "✓ /generate resource created: $generateResourceId" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create /generate resource" -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 1

# Step 7: Create POST Method for /generate
Write-Host "`n[7/10] Configuring POST /generate with Lambda..." -ForegroundColor Yellow
try {
    # Create POST method
    aws apigateway put-method `
        --rest-api-id $apiId `
        --resource-id $generateResourceId `
        --http-method POST `
        --authorization-type NONE `
        --region $REGION 2>&1 | Out-Null
    
    # Set up Lambda proxy integration
    $lambdaUri = "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/${lambdaArn}/invocations"
    
    aws apigateway put-integration `
        --rest-api-id $apiId `
        --resource-id $generateResourceId `
        --http-method POST `
        --type AWS_PROXY `
        --integration-http-method POST `
        --uri $lambdaUri `
        --region $REGION 2>&1 | Out-Null
    
    Write-Host "✓ POST /generate configured with Lambda" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to configure POST method" -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 1

# Step 8: Grant API Gateway Permission to Invoke Lambda
Write-Host "`n[8/10] Granting Lambda permissions..." -ForegroundColor Yellow
try {
    $sourceArn = "arn:aws:execute-api:${REGION}:${accountId}:${apiId}/*/*"
    
    # Remove existing permission if any
    aws lambda remove-permission `
        --function-name $LAMBDA_FUNCTION_NAME `
        --statement-id apigateway-invoke-permission `
        --region $REGION 2>&1 | Out-Null
    
    Start-Sleep -Seconds 1
    
    # Add new permission
    aws lambda add-permission `
        --function-name $LAMBDA_FUNCTION_NAME `
        --statement-id apigateway-invoke-permission `
        --action lambda:InvokeFunction `
        --principal apigateway.amazonaws.com `
        --source-arn $sourceArn `
        --region $REGION 2>&1 | Out-Null
    
    Write-Host "✓ Lambda permission granted" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not set Lambda permissions (may already exist)" -ForegroundColor Yellow
}

Start-Sleep -Seconds 1

# Step 9: Enable CORS on /generate
Write-Host "`n[9/10] Enabling CORS..." -ForegroundColor Yellow
try {
    # Create OPTIONS method
    aws apigateway put-method `
        --rest-api-id $apiId `
        --resource-id $generateResourceId `
        --http-method OPTIONS `
        --authorization-type NONE `
        --region $REGION 2>&1 | Out-Null
    
    # Mock integration for OPTIONS
    aws apigateway put-integration `
        --rest-api-id $apiId `
        --resource-id $generateResourceId `
        --http-method OPTIONS `
        --type MOCK `
        --region $REGION `
        --request-templates '{\"application/json\": \"{\\\"statusCode\\\": 200}\"}' 2>&1 | Out-Null
    
    # Method response for OPTIONS
    aws apigateway put-method-response `
        --rest-api-id $apiId `
        --resource-id $generateResourceId `
        --http-method OPTIONS `
        --status-code 200 `
        --region $REGION `
        --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\":true,\"method.response.header.Access-Control-Allow-Methods\":true,\"method.response.header.Access-Control-Allow-Origin\":true}' `
        --response-models '{\"application/json\": \"Empty\"}' 2>&1 | Out-Null
    
    # Integration response for OPTIONS
    aws apigateway put-integration-response `
        --rest-api-id $apiId `
        --resource-id $generateResourceId `
        --http-method OPTIONS `
        --status-code 200 `
        --region $REGION `
        --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\":\"'"'"'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"'"'\",\"method.response.header.Access-Control-Allow-Methods\":\"'"'"'GET,POST,OPTIONS'"'"'\",\"method.response.header.Access-Control-Allow-Origin\":\"'"'"'*'"'"'\"}' 2>&1 | Out-Null
    
    Write-Host "✓ CORS enabled" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not enable CORS" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# Step 10: Deploy API
Write-Host "`n[10/10] Deploying API to 'prod' stage..." -ForegroundColor Yellow
try {
    $deploymentId = (aws apigateway create-deployment `
        --rest-api-id $apiId `
        --stage-name $STAGE_NAME `
        --stage-description "Production Stage" `
        --description "Initial deployment" `
        --region $REGION `
        --query 'id' --output text 2>&1)
    
    Write-Host "✓ API deployed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to deploy API" -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 2

# Generate API URLs
$apiUrl = "https://${apiId}.execute-api.${REGION}.amazonaws.com/${STAGE_NAME}"
$healthUrl = "${apiUrl}/health"
$generateUrl = "${apiUrl}/generate"

# Save API URL
$apiUrl | Out-File -FilePath "api_gateway_url.txt" -Encoding utf8 -NoNewline

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  API Gateway Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Gateway Details:" -ForegroundColor Yellow
Write-Host "  API ID:    $apiId" -ForegroundColor White
Write-Host "  Region:    $REGION" -ForegroundColor White
Write-Host "  Stage:     $STAGE_NAME" -ForegroundColor White
Write-Host ""
Write-Host "Base URL:" -ForegroundColor Yellow
Write-Host "  $apiUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "Endpoints:" -ForegroundColor Yellow
Write-Host "  GET  $healthUrl" -ForegroundColor Cyan
Write-Host "  POST $generateUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "Console URL:" -ForegroundColor Yellow
Write-Host "  https://console.aws.amazon.com/apigateway/home?region=${REGION}#/apis/${apiId}/resources" -ForegroundColor Cyan
Write-Host ""

# Save configuration
$config = @{
    api_id = $apiId
    api_url = $apiUrl
    health_endpoint = $healthUrl
    generate_endpoint = $generateUrl
    region = $REGION
    stage = $STAGE_NAME
    created_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
} | ConvertTo-Json

$config | Out-File -FilePath "api_gateway_config.json" -Encoding utf8
Write-Host "✓ Configuration saved to api_gateway_config.json" -ForegroundColor Green
Write-Host ""

# Test health endpoint
Write-Host "Testing /health endpoint..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

try {
    $healthResponse = Invoke-RestMethod -Uri $healthUrl -Method GET -ErrorAction Stop
    Write-Host "✓ Health check successful!" -ForegroundColor Green
    Write-Host "  Response: $($healthResponse | ConvertTo-Json -Compress)" -ForegroundColor Gray
} catch {
    Write-Host "⚠ Health check failed (API may need a moment to propagate)" -ForegroundColor Yellow
    Write-Host "  You can test manually: curl $healthUrl" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Test health endpoint: curl $healthUrl" -ForegroundColor White
Write-Host "  2. Test generate endpoint with POST request" -ForegroundColor White
Write-Host "  3. Update React frontend to use: $apiUrl" -ForegroundColor White
Write-Host "  4. Enable CloudWatch logging (optional)" -ForegroundColor White
Write-Host ""
