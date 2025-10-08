# AWS S3 Setup Script for Business Website Generator
# Automated setup for AWS Learner Lab environment

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  AWS S3 Setup - Website Generator" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$REGION = "us-east-1"
$BUCKET_NAME = "website-gen-s3-$(Get-Date -Format 'yyyyMMddHHmmss')"

# Step 1: Verify AWS CLI
Write-Host "[1/8] Verifying AWS CLI..." -ForegroundColor Yellow
try {
    $awsVersion = aws --version 2>&1
    Write-Host "✓ AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ AWS CLI not found. Please install it first." -ForegroundColor Red
    exit 1
}

# Step 2: Test AWS credentials
Write-Host "`n[2/8] Testing AWS credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Host "✓ AWS credentials valid" -ForegroundColor Green
    Write-Host "  Account: $($identity.Account)" -ForegroundColor Gray
    Write-Host "  User: $($identity.Arn)" -ForegroundColor Gray
} catch {
    Write-Host "✗ AWS credentials not configured. Run 'aws configure' first." -ForegroundColor Red
    exit 1
}

# Step 3: Create S3 bucket
Write-Host "`n[3/8] Creating S3 bucket: $BUCKET_NAME" -ForegroundColor Yellow
try {
    aws s3 mb "s3://$BUCKET_NAME" --region $REGION 2>&1 | Out-Null
    Write-Host "✓ Bucket created successfully" -ForegroundColor Green
    
    # Save bucket name
    $BUCKET_NAME | Out-File -FilePath "bucket_name.txt" -Encoding utf8 -NoNewline
    Write-Host "✓ Bucket name saved to bucket_name.txt" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create bucket" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Step 4: Disable Block Public Access
Write-Host "`n[4/8] Configuring public access settings..." -ForegroundColor Yellow
try {
    aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false" 2>&1 | Out-Null
    Write-Host "✓ Public access configured" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not configure public access" -ForegroundColor Yellow
}

# Step 5: Apply bucket policy
Write-Host "`n[5/8] Applying bucket policy (public read for generated websites)..." -ForegroundColor Yellow
$bucketPolicy = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/generated-websites/*"
        }
    ]
}
"@

$bucketPolicy | Out-File -FilePath "s3-bucket-policy.json" -Encoding utf8
Start-Sleep -Seconds 2

try {
    aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://s3-bucket-policy.json 2>&1 | Out-Null
    Write-Host "✓ Bucket policy applied" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not apply bucket policy" -ForegroundColor Yellow
}

# Step 6: Configure CORS
Write-Host "`n[6/8] Configuring CORS..." -ForegroundColor Yellow
$corsConfig = @"
{
    "CORSRules": [
        {
            "AllowedOrigins": ["*"],
            "AllowedMethods": ["GET", "POST", "PUT", "HEAD"],
            "AllowedHeaders": ["*"],
            "ExposeHeaders": ["ETag"],
            "MaxAgeSeconds": 3000
        }
    ]
}
"@

$corsConfig | Out-File -FilePath "s3-cors-config.json" -Encoding utf8

try {
    aws s3api put-bucket-cors --bucket $BUCKET_NAME --cors-configuration file://s3-cors-config.json 2>&1 | Out-Null
    Write-Host "✓ CORS configured" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not configure CORS" -ForegroundColor Yellow
}

# Step 7: Create folder structure
Write-Host "`n[7/8] Creating folder structure..." -ForegroundColor Yellow
"" | Out-File -FilePath "placeholder.txt" -Encoding utf8

try {
    aws s3 cp placeholder.txt "s3://$BUCKET_NAME/generated-websites/.placeholder" 2>&1 | Out-Null
    aws s3 cp placeholder.txt "s3://$BUCKET_NAME/templates/.placeholder" 2>&1 | Out-Null
    Remove-Item placeholder.txt -ErrorAction SilentlyContinue
    Write-Host "✓ Folder structure created" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Could not create folder structure" -ForegroundColor Yellow
}

# Step 8: Upload templates (if they exist)
Write-Host "`n[8/8] Uploading templates..." -ForegroundColor Yellow
if (Test-Path ".\templates") {
    try {
        aws s3 cp .\templates "s3://$BUCKET_NAME/templates/" --recursive --exclude "*.md" --exclude "README*" 2>&1 | Out-Null
        $templateCount = (Get-ChildItem ".\templates" -Filter "*.html").Count
        Write-Host "✓ Uploaded $templateCount template(s)" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Warning: Could not upload templates" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Templates folder not found - skipping" -ForegroundColor Yellow
}

# Summary
Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Bucket Name: $BUCKET_NAME" -ForegroundColor White
Write-Host "Region: $REGION" -ForegroundColor White
Write-Host ""
Write-Host "URLs:" -ForegroundColor Yellow
Write-Host "  S3 Console: https://s3.console.aws.amazon.com/s3/buckets/$BUCKET_NAME" -ForegroundColor Cyan
Write-Host "  Base URL: https://$BUCKET_NAME.s3.$REGION.amazonaws.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Update Lambda environment variable: S3_BUCKET=$BUCKET_NAME" -ForegroundColor White
Write-Host "  2. Test upload: aws s3 cp test.html s3://$BUCKET_NAME/generated-websites/test/index.html" -ForegroundColor White
Write-Host "  3. Access URL: https://$BUCKET_NAME.s3.$REGION.amazonaws.com/generated-websites/test/index.html" -ForegroundColor White
Write-Host ""

# Create test file
Write-Host "Creating test website..." -ForegroundColor Yellow
$testHtml = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S3 Setup Test - Success!</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 {
            color: #667eea;
            margin-bottom: 20px;
        }
        .success {
            color: #10b981;
            font-size: 4rem;
            margin-bottom: 10px;
        }
        .info {
            background: #f3f4f6;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .info p {
            margin: 5px 0;
            color: #6b7280;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="success">✅</div>
        <h1>S3 Setup Successful!</h1>
        <p>Your AWS S3 bucket is configured and working correctly.</p>
        <div class="info">
            <p><strong>Bucket:</strong> $BUCKET_NAME</p>
            <p><strong>Region:</strong> $REGION</p>
            <p><strong>Generated:</strong> $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</p>
        </div>
    </div>
</body>
</html>
"@

$testHtml | Out-File -FilePath "s3-test.html" -Encoding utf8

# Upload test file
$testSessionId = "test-$(Get-Date -Format 'yyyyMMddHHmmss')"
aws s3 cp s3-test.html "s3://$BUCKET_NAME/generated-websites/$testSessionId/index.html" --content-type "text/html" 2>&1 | Out-Null
Remove-Item s3-test.html

$testUrl = "https://$BUCKET_NAME.s3.$REGION.amazonaws.com/generated-websites/$testSessionId/index.html"
Write-Host "✓ Test website uploaded!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Test URL: $testUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open this URL in your browser to verify S3 is working!" -ForegroundColor White
Write-Host ""

# Save configuration
$config = @{
    bucket_name = $BUCKET_NAME
    region = $REGION
    test_url = $testUrl
    created_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
} | ConvertTo-Json

$config | Out-File -FilePath "s3-config.json" -Encoding utf8
Write-Host "✓ Configuration saved to s3-config.json" -ForegroundColor Green
