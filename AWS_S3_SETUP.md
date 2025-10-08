# 🗄️ AWS S3 Setup for Business Website Generator

## 📋 Overview

This guide will help you set up Amazon S3 to store:
- Generated HTML websites
- Template files
- User-uploaded images (future)
- React frontend static files

---

## 🎯 S3 Bucket Structure

```
website-generator-{timestamp}/
├── generated-websites/
│   ├── {session-id-1}/
│   │   └── index.html
│   ├── {session-id-2}/
│   │   └── index.html
│   └── ...
├── templates/
│   ├── modern_glass.html
│   ├── minimal_elegant.html
│   └── ...
└── frontend/ (React app - optional)
    ├── index.html
    ├── static/
    └── ...
```

---

## ✅ Prerequisites

1. AWS Learner Lab activated
2. AWS CLI installed and configured
3. Valid AWS credentials (session token)

---

## 🚀 Quick Setup Commands

### 1. Create S3 Bucket

```powershell
# Set bucket name with timestamp for uniqueness
$BUCKET_NAME = "website-generator-$(Get-Date -Format 'yyyyMMddHHmmss')"
$REGION = "us-east-1"

# Create bucket
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Save bucket name for later use
$BUCKET_NAME | Out-File -FilePath "bucket_name.txt" -Encoding utf8
Write-Host "✅ Bucket created: $BUCKET_NAME"
```

### 2. Configure Bucket for Public Read Access (Generated Websites)

```powershell
# Create bucket policy JSON
@"
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
"@ | Out-File -FilePath "s3-bucket-policy.json" -Encoding utf8

# Apply bucket policy
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://s3-bucket-policy.json
Write-Host "✅ Bucket policy applied"
```

### 3. Enable CORS (for frontend access)

```powershell
# Create CORS configuration
@"
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
"@ | Out-File -FilePath "s3-cors-config.json" -Encoding utf8

# Apply CORS configuration
aws s3api put-bucket-cors --bucket $BUCKET_NAME --cors-configuration file://s3-cors-config.json
Write-Host "✅ CORS configured"
```

### 4. Create Folder Structure

```powershell
# Create placeholder files to establish folder structure
"" | Out-File -FilePath "placeholder.txt" -Encoding utf8

aws s3 cp placeholder.txt "s3://$BUCKET_NAME/generated-websites/.placeholder"
aws s3 cp placeholder.txt "s3://$BUCKET_NAME/templates/.placeholder"

Remove-Item placeholder.txt
Write-Host "✅ Folder structure created"
```

### 5. Upload Templates to S3

```powershell
# Upload all template files
$templatesPath = ".\templates"
if (Test-Path $templatesPath) {
    aws s3 cp $templatesPath "s3://$BUCKET_NAME/templates/" --recursive --exclude "*.md"
    Write-Host "✅ Templates uploaded"
} else {
    Write-Host "⚠️ Templates folder not found"
}
```

### 6. Set Lifecycle Policy (Optional - Auto-delete old websites)

```powershell
# Create lifecycle policy (delete after 30 days)
@"
{
    "Rules": [
        {
            "Id": "DeleteOldWebsites",
            "Status": "Enabled",
            "Prefix": "generated-websites/",
            "Expiration": {
                "Days": 30
            }
        }
    ]
}
"@ | Out-File -FilePath "s3-lifecycle-policy.json" -Encoding utf8

# Apply lifecycle policy
aws s3api put-bucket-lifecycle-configuration --bucket $BUCKET_NAME --lifecycle-configuration file://s3-lifecycle-policy.json
Write-Host "✅ Lifecycle policy configured (30-day auto-delete)"
```

### 7. Enable Versioning (Optional but Recommended)

```powershell
# Enable versioning
aws s3api put-bucket-versioning --bucket $BUCKET_NAME --versioning-configuration Status=Enabled
Write-Host "✅ Versioning enabled"
```

---

## 🧪 Test S3 Setup

### Upload Test HTML File

```powershell
# Create test HTML
@"
<!DOCTYPE html>
<html>
<head>
    <title>Test Website</title>
</head>
<body>
    <h1>S3 Upload Test - Success!</h1>
    <p>Generated at: $(Get-Date)</p>
</body>
</html>
"@ | Out-File -FilePath "test-website.html" -Encoding utf8

# Upload to S3
$sessionId = "test-$(Get-Date -Format 'yyyyMMddHHmmss')"
aws s3 cp test-website.html "s3://$BUCKET_NAME/generated-websites/$sessionId/index.html" --content-type "text/html"

# Generate public URL
$publicUrl = "https://$BUCKET_NAME.s3.$REGION.amazonaws.com/generated-websites/$sessionId/index.html"
Write-Host "`n✅ Test website uploaded!"
Write-Host "🔗 Access URL: $publicUrl"

# Clean up local file
Remove-Item test-website.html
```

---

## 🔐 Generate Pre-Signed URLs (for Private Access)

```powershell
# Generate temporary download URL (expires in 1 hour)
$sessionId = "your-session-id-here"
$preSignedUrl = aws s3 presign "s3://$BUCKET_NAME/generated-websites/$sessionId/index.html" --expires-in 3600

Write-Host "🔗 Pre-signed URL (valid for 1 hour):"
Write-Host $preSignedUrl
```

---

## 📊 Monitor S3 Usage

### Check Bucket Size

```powershell
# Get bucket size and object count
aws s3 ls s3://$BUCKET_NAME --recursive --summarize | Select-String -Pattern "Total"
```

### List Generated Websites

```powershell
# List all generated websites
aws s3 ls s3://$BUCKET_NAME/generated-websites/ --recursive
```

### Download Website from S3

```powershell
# Download a specific website
$sessionId = "your-session-id"
aws s3 cp "s3://$BUCKET_NAME/generated-websites/$sessionId/index.html" "./downloaded-website.html"
```

---

## 🗑️ Cleanup Commands

### Delete Specific Website

```powershell
# Delete a session's website
$sessionId = "session-to-delete"
aws s3 rm "s3://$BUCKET_NAME/generated-websites/$sessionId/" --recursive
```

### Delete All Generated Websites (Keep Templates)

```powershell
# Delete all generated websites
aws s3 rm "s3://$BUCKET_NAME/generated-websites/" --recursive
```

### Delete Entire Bucket (Complete Cleanup)

```powershell
# ⚠️ WARNING: This deletes EVERYTHING
aws s3 rb s3://$BUCKET_NAME --force
```

---

## 🔧 Troubleshooting

### Issue: "Access Denied" errors

**Solution:**
```powershell
# Check bucket policy
aws s3api get-bucket-policy --bucket $BUCKET_NAME

# Re-apply bucket policy
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://s3-bucket-policy.json
```

### Issue: CORS errors in browser

**Solution:**
```powershell
# Verify CORS configuration
aws s3api get-bucket-cors --bucket $BUCKET_NAME

# Re-apply CORS
aws s3api put-bucket-cors --bucket $BUCKET_NAME --cors-configuration file://s3-cors-config.json
```

### Issue: Files not accessible publicly

**Solution:**
```powershell
# Disable "Block Public Access"
aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
```

---

## 📈 Cost Estimation

**S3 Pricing (us-east-1):**
- Storage: $0.023 per GB/month
- PUT requests: $0.005 per 1,000 requests
- GET requests: $0.0004 per 1,000 requests

**Example Monthly Cost:**
- 100 websites × 5MB = 500MB = ~$0.01/month storage
- 1000 downloads = ~$0.0004
- **Total: ~$0.02/month** (essentially free!)

---

## ✅ S3 Setup Checklist

- [ ] Bucket created with unique name
- [ ] Bucket policy applied (public read for generated websites)
- [ ] CORS configuration enabled
- [ ] Folder structure created
- [ ] Templates uploaded
- [ ] Lifecycle policy configured (30-day auto-delete)
- [ ] Versioning enabled
- [ ] Test upload successful
- [ ] Test download successful
- [ ] Public URL accessible
- [ ] Bucket name saved to `bucket_name.txt`

---

## 🔗 Next Steps

After S3 setup is complete:
1. ✅ Update Lambda function to upload to S3
2. ✅ Update Lambda environment variables with bucket name
3. ✅ Modify `lambda_function.py` to use S3 instead of local files
4. ✅ Test end-to-end flow (Generate → Upload to S3 → Access via URL)

---

## 📚 Useful AWS CLI Commands

```powershell
# List all buckets
aws s3 ls

# Get bucket location
aws s3api get-bucket-location --bucket $BUCKET_NAME

# Get bucket ACL
aws s3api get-bucket-acl --bucket $BUCKET_NAME

# Sync local folder to S3
aws s3 sync ./local-folder s3://$BUCKET_NAME/remote-folder/

# Copy from S3 to S3
aws s3 cp s3://$BUCKET_NAME/source/ s3://$BUCKET_NAME/destination/ --recursive

# Make specific file public
aws s3api put-object-acl --bucket $BUCKET_NAME --key "path/to/file.html" --acl public-read
```

---

## 🎓 Learning Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
- [S3 CORS Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html)
- [S3 Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)

---

**Created:** October 8, 2025  
**Last Updated:** October 8, 2025  
**Author:** GitHub Copilot  
**Project:** Business Website Generator - AWS Integration
