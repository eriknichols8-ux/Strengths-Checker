# CliftonStrengths Comparison Tool

A Streamlit web application that compares CliftonStrengths profiles between two people using OpenAI's GPT-4o to provide insights on potential conflicts, collaboration strategies, and effective communication approaches.

## Features

- 📊 **Compare CliftonStrengths**: Input top 5 strengths for two people
- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT-4o for intelligent insights
- ⚠️ **Conflict Identification**: Understand potential areas of tension
- 🤝 **Collaboration Tips**: Learn how to work together effectively
- 💬 **Communication Guidance**: Get personalized communication strategies
- 💾 **Save & Load Profiles**: Save people and their strengths for quick access
- 🔒 **Password Protected**: Secure access to protect your API costs
- 🐳 **Docker Support**: Easy deployment with Docker containers

## What are CliftonStrengths?

CliftonStrengths (formerly StrengthsFinder) is an assessment tool developed by Gallup that identifies your top talent themes from a list of 34 strengths. This app helps you understand how different strength profiles interact.

## Prerequisites

- Docker and Docker Compose installed, OR
- Python 3.11+ (for local development)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## 🔒 Password Protection

The app is password protected to prevent unauthorized access and protect your OpenAI API costs.

**Default Password (Local Development):** `strengths2024`

**For Streamlit Cloud Deployment:** Set your custom password in the Secrets section (see deployment instructions below)

## Quick Start with Docker

### 1. Clone or download this repository

### 2. Set your OpenAI API key

**Option A: Using environment variable (recommended)**
```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=your_api_key_here clifton-strengths-app
```

**Option B: Using Docker Compose**

Create a `.env` file in the project directory:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

### 4. Access the app

Open your browser and navigate to:
```
http://localhost:8501
```

## Docker Commands

### Build the Docker image
```bash
docker build -t clifton-strengths-app .
```

### Run the container
```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key_here clifton-strengths-app
```

### Stop the container
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

## Local Development (Without Docker)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your OpenAI API key
```bash
# On Linux/Mac
export OPENAI_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"

# On Windows (Command Prompt)
set OPENAI_API_KEY=your_api_key_here
```

### 3. (Optional) Change the default password
To change the default password for local testing, edit `app.py` and modify the default password in the `get_password()` function, or create a `.streamlit/secrets.toml` file:

```toml
app_password = "your_custom_password"
```

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Open your browser
Navigate to `http://localhost:8501` and enter the password: **`strengths2024`** (or your custom password)

## How to Use

1. **Enter Password**: Use the app password to access (default: `strengths2024`)
2. **Select or Add People**: 
   - Choose "➕ Add New Person" to create a new profile
   - Or select from previously saved people
3. **Enter Strengths**: Choose 5 CliftonStrengths for each person
4. **Save Profiles**: Click "💾 Save Person" to save profiles for future use
5. **Compare**: Press the "🔍 Compare Strengths" button
6. **Review Results**: Read the AI-generated insights on:
   - Potential conflicts between the two profiles
   - Ways to collaborate effectively
   - How to communicate most effectively

## The 34 CliftonStrengths

The app includes all 34 CliftonStrengths themes:

**Executing Domain:**
- Achiever, Arranger, Belief, Consistency, Deliberative, Discipline, Focus, Responsibility, Restorative

**Influencing Domain:**
- Activator, Command, Communication, Competition, Maximizer, Self-Assurance, Significance, Woo

**Relationship Building Domain:**
- Adaptability, Connectedness, Developer, Empathy, Harmony, Includer, Individualization, Positivity, Relator

**Strategic Thinking Domain:**
- Analytical, Context, Futuristic, Ideation, Input, Intellection, Learner, Strategic

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── strengths.py            # CliftonStrengths data and validation
├── openai_service.py       # OpenAI API integration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Files to exclude from Docker build
├── .env.example           # Example environment variables
└── README.md              # This file
```

## Troubleshooting

### "OPENAI_API_KEY environment variable is not set"
- Make sure you've set the API key as an environment variable
- If using Docker, ensure you've passed it with `-e` flag or in `.env` file

### Port 8501 already in use
- Stop any other Streamlit apps running on port 8501
- Or change the port mapping: `-p 8502:8501`

### Docker build fails
- Ensure Docker is running
- Check that you have internet connectivity
- Try cleaning Docker cache: `docker system prune`

## API Costs

This app makes 3 API calls to OpenAI GPT-4o per comparison. As of January 2026:
- GPT-4o costs approximately $0.005-0.015 per comparison
- Monitor your usage at: https://platform.openai.com/usage

**Important:** The app is password protected to help control access and manage API costs. Only share the password with people you want to have access.

## License

This project is provided as-is for educational and personal use.

**Note:** CliftonStrengths® is a registered trademark of Gallup, Inc. This application is not affiliated with, endorsed by, or sponsored by Gallup, Inc.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool!

## Disclaimer

The insights provided by this tool are generated by AI and should be used as guidance, not absolute truth. For professional team development and official CliftonStrengths coaching, please consult certified Gallup coaches.
