# 🚀 Deployment Guide for Streamlit Cloud

This guide will help you deploy your CliftonStrengths Comparison App to Streamlit Cloud with proper security.

## Prerequisites

- A GitHub account
- Your OpenAI API key
- A custom password for your app

## Step-by-Step Deployment

### 1. Push to GitHub

1. Create a new repository on GitHub (can be private or public)
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit - CliftonStrengths Comparison App"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account if you haven't already
4. Select your repository and branch
5. Set the main file path to: `app.py`
6. Click "Advanced settings"

### 3. Configure Secrets

In the "Secrets" section, add the following in TOML format:

```toml
# OpenAI API Key (REQUIRED)
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"

# App Password (REQUIRED) - Change this to your own secure password
app_password = "YourSecurePassword123!"
```

**Important:** 
- Replace `sk-your-actual-openai-api-key-here` with your real OpenAI API key
- Replace `YourSecurePassword123!` with a strong, unique password
- Keep these secrets confidential!

### 4. Deploy

1. Click "Deploy!"
2. Wait for the app to build and deploy (usually 2-5 minutes)
3. Your app will be available at: `https://your-app-name.streamlit.app`

### 5. Share with Users

Share the following with authorized users:
- **App URL**: `https://your-app-name.streamlit.app`
- **Password**: The password you set in secrets (e.g., `YourSecurePassword123!`)

## Security Best Practices

### Choosing a Strong Password

Your app password should:
- Be at least 12 characters long
- Include uppercase and lowercase letters
- Include numbers and special characters
- NOT be a common word or phrase
- Be unique to this app

Example strong passwords:
- `CliftonStr3ngth$2024!`
- `MyT3am$Comparis0n!`
- `SecureAnalysis#2024`

### Managing Access

1. **Keep the password private** - Only share with people who should have access
2. **Change the password periodically** - Update it in Streamlit Cloud secrets
3. **Monitor usage** - Check your OpenAI API usage at [platform.openai.com/usage](https://platform.openai.com/usage)
4. **Set spending limits** - Configure billing limits in your OpenAI account

## Updating the Password

To change your password after deployment:

1. Go to your app on [share.streamlit.io](https://share.streamlit.io)
2. Click "⚙️ Settings"
3. Go to "Secrets"
4. Update the `app_password` value
5. Click "Save"
6. The app will automatically restart with the new password

## Troubleshooting

### Users can't log in
- Verify you shared the correct password
- Check that the password in Streamlit secrets doesn't have extra spaces
- Passwords are case-sensitive!

### API key not working
- Verify the OPENAI_API_KEY in secrets is correct
- Check your OpenAI account has available credits
- Ensure the API key hasn't been revoked

### App is slow or timing out
- Check your OpenAI API usage limits
- Verify you have enough credits in your OpenAI account
- The first load after inactivity may take longer (Streamlit Cloud "wakes up" the app)

## Cost Management

### Monitor Your Costs

1. Check OpenAI usage: [platform.openai.com/usage](https://platform.openai.com/usage)
2. Set up billing alerts in your OpenAI account
3. Consider setting a monthly budget limit

### Estimated Costs

- Each comparison = 3 API calls to GPT-4o
- Cost per comparison: ~$0.005-0.015
- 100 comparisons/month: ~$0.50-1.50
- 1000 comparisons/month: ~$5-15

## Support

If you need help:
1. Check the main [README.md](README.md)
2. Review Streamlit Cloud docs: [docs.streamlit.io](https://docs.streamlit.io)
3. Check OpenAI API docs: [platform.openai.com/docs](https://platform.openai.com/docs)
