# Flask Security Monitoring App

A production-ready Flask application with Auth0 authentication, custom logging, and Azure Monitor integration for detecting suspicious user activity.

## Project Overview

This project combines SSO authentication with comprehensive monitoring to create a secure, observable web application. The app logs user activities and uses Azure Monitor with KQL queries to detect potential security threats.

### Key Features

- **Auth0 SSO Integration**: Secure user authentication
- **Custom Logging**: Tracks user logins, protected route access, and unauthorized attempts
- **Azure Monitor Integration**: Real-time log analysis and alerting
- **Threat Detection**: KQL queries to identify excessive access patterns
- **Automated Alerts**: Email notifications for suspicious activity

## Architecture

- **Frontend**: Flask web application with Auth0 authentication
- **Backend**: Python Flask with structured logging
- **Monitoring**: Azure Monitor + Log Analytics
- **Alerting**: Azure Action Groups for email notifications

## Setup Instructions

### Prerequisites

- Python 3.8+
- Azure account with active subscription
- Auth0 account
- Azure CLI installed

### 1. Clone the Repository

```bash
git clone <repository-url>
cd flask-security-monitoring
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Fill in the required values:

```env
AUTH0_DOMAIN=your-auth0-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

### 4. Auth0 Setup

1. Create an Auth0 application
2. Set callback URLs: `http://localhost:5000/callback`, `https://your-app.azurewebsites.net/callback`
3. Configure allowed logout URLs
4. Copy domain, client ID, and client secret to `.env`

### 5. Azure Deployment

1. **Create Azure App Service:**
   ```bash
   az webapp create --resource-group <resource-group> --plan <app-service-plan> --name <app-name> --runtime "PYTHON|3.9"
   ```

2. **Enable Application Logs:**
   ```bash
   az webapp log config --name <app-name> --resource-group <resource-group> --application-logging filesystem
   ```

3. **Deploy the application:**
   ```bash
   az webapp deployment source config-zip --resource-group <resource-group> --name <app-name> --src <zip-file>
   ```

### 6. Configure Azure Monitor

1. Create Log Analytics Workspace
2. Connect App Service to Log Analytics
3. Enable AppServiceConsoleLogs collection

## Monitoring & Detection

### Logging Implementation

The application logs the following events:

- **User Login**: `user_id`, `email`, `timestamp`
- **Protected Route Access**: User access to `/protected` endpoint
- **Unauthorized Attempts**: Failed authentication attempts

### KQL Query for Threat Detection

```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where ResultDescription contains "protected route access"
| extend user_id = extract(@"user_id: ([^,]+)", 1, ResultDescription)
| where isnotempty(user_id)
| summarize AccessCount = count() by user_id, bin(TimeGenerated, 1m)
| where AccessCount > 10
| project user_id, TimeGenerated, AccessCount
| order by AccessCount desc
```

### Alert Configuration

- **Trigger**: User accesses `/protected` more than 10 times in 15 minutes
- **Severity**: Low (3)
- **Action**: Email notification via Action Group
- **Frequency**: Every 5 minutes

## Testing

Use the provided `test-app.http` file to simulate various scenarios:

```http
### Valid login and access
GET http://localhost:5000/login

### Access protected route (repeat multiple times)
GET http://localhost:5000/protected

### Unauthorized access attempt
GET http://localhost:5000/protected
```

## Usage

1. **Start the application locally:**
   ```bash
   python app.py
   ```

2. **Access the app**: Navigate to `http://localhost:5000`

3. **Login with Auth0**: Use the login button to authenticate

4. **Access protected routes**: Visit `/protected` to generate logs

5. **Monitor in Azure**: Check Log Analytics for real-time logs

6. **Trigger alerts**: Access `/protected` more than 10 times in 15 minutes

## Detection Logic

The monitoring system identifies suspicious activity through:

1. **Real-time Logging**: Every user action is logged with structured data
2. **Pattern Analysis**: KQL queries analyze access patterns
3. **Threshold Detection**: Alerts trigger when access exceeds normal patterns
4. **Automated Response**: Email notifications for immediate awareness

## Project Structure

```
flask-security-monitoring/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── test-app.http         # HTTP test requests
├── README.md             # This file
└── templates/
    ├── index.html        # Home page
    ├── login.html        # Login page
    └── protected.html    # Protected route
```

## Key Learnings

### What Worked Well

- Auth0 integration provided robust authentication
- Azure Monitor effectively captured and analyzed logs
- KQL queries enabled powerful pattern detection
- Action Groups provided reliable alerting

### Areas for Improvement

- Add more sophisticated anomaly detection
- Implement rate limiting at the application level
- Enhance log correlation across multiple services
- Add dashboard visualization for security metrics

## Security Considerations

- Environment variables for sensitive configuration
- Secure session management with Auth0
- Structured logging without sensitive data exposure
- Regular monitoring and alert fine-tuning

## Production Deployment

For production use, consider:

- Use Azure Key Vault for secrets management
- Implement proper CORS policies
- Add request rate limiting
- Set up automated security scanning
- Configure backup and disaster recovery

## YOUTUBE VIDEO
https://youtu.be/8AyZc0iWhn4
