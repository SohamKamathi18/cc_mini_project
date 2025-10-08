# Lambda Function: Generate Website

## Purpose
This Lambda function handles the complete website generation workflow using AI agents.

## Flow
1. Receives business information via API Gateway
2. Initializes AI agents (cached per container)
3. Runs multi-agent workflow:
   - Business Analysis
   - Design Generation
   - Content Creation
   - Image Fetching
   - HTML Building
4. Uploads generated HTML to S3
5. Returns S3 URL and pre-signed download URL

## Environment Variables Required
- `GOOGLE_API_KEY`: Google Gemini API key
- `UNSPLASH_ACCESS_KEY`: Unsplash API key (optional)
- `S3_BUCKET`: S3 bucket name for storing websites
- `REGION`: AWS region (default: us-east-1)

## Dependencies
See `requirements.txt` - will be packaged as Lambda Layer

## Configuration
- **Runtime:** Python 3.10+
- **Memory:** 1024 MB (recommended)
- **Timeout:** 5 minutes (300 seconds)
- **IAM Role:** LabRole (Learner Lab)

## Testing Locally
```bash
python lambda_function.py
```

## Deployment
Will be deployed using `create_lambda_functions.ps1` script
