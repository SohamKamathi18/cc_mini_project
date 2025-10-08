// API Configuration for AWS API Gateway
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'https://p9mlg0d8ia.execute-api.us-east-1.amazonaws.com/prod',
  timeout: 120000, // 2 minutes for website generation
};
