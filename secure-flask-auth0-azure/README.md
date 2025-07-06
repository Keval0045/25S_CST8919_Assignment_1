# Secure Flask App with Auth0 and Azure Monitor

## Overview
This app demonstrates a Flask web app with:
- Auth0 authentication
- Azure deployment
- Structured logging
- Monitoring with KQL and Alerts

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure `.env`
Use `.env.example` and fill in your Auth0 values.

### 3. Run the app
```bash
python app.py
```

### 4. Deploy to Azure
Use Azure CLI or GitHub Actions.

### 5. KQL Query (to detect suspicious activity)
```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where Message has "/protected accessed"
| parse Message with * "user_id=" user_id ","
| summarize Count = count(), Times = make_list(TimeGenerated) by user_id
| where Count > 10
```

## Alert
Trigger an alert if any user accesses `/protected` >10 times in 15 mins.

## test-app.http
Simulates valid and invalid accesses.

## Demo
📺 [YouTube Demo Link Placeholder]

## Reflection
Things that worked well: Integration, Logging  
Improvements: Add more granular RBAC controls
