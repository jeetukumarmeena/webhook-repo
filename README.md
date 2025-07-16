# GitHub Webhook Receiver

A Flask application that receives GitHub webhooks and displays repository events in a real-time web interface. This project monitors Push, Pull Request, and Merge events from your GitHub repositories and stores them in MongoDB.

## 🚀 Features

- **Real-time webhook processing** for GitHub events
- **MongoDB integration** using PyMongo for event storage
- **Web dashboard** with auto-refresh every 15 seconds
- **Event categorization** with color-coded display
- **Clean, responsive UI** for monitoring repository activities

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **MongoDB** (local installation or MongoDB Atlas account)
- **ngrok** (for exposing your local server to the internet)
- **Git** (for cloning the repository)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jeetukumarmeena/webhook-repo.git
cd webhook-repo
```

### 2. Set Up MongoDB

#### Option A: Local MongoDB Installation

**On macOS (using Homebrew):**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**On Windows:**
- Download MongoDB Community Server from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
- Follow the installation wizard
- Start MongoDB service

#### Option B: MongoDB Atlas (Cloud)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string
4. Update the `.env` file with your connection details

### 3. Install Dependencies

#### Using pip (Traditional method)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Using uv (Modern, faster alternative)

```bash
# Install uv (if not already installed)
pip install uv

# Install dependencies (uv automatically handles virtual environment)
uv sync
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=github_webhooks
COLLECTION_NAME=events
```

For MongoDB Atlas, update the URI:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### 5. VS Code Setup

If you're using VS Code, make sure to select the correct Python environment:

1. Open the project in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the Command Palette
3. Type "Python: Select Interpreter"
4. Choose the `.venv` environment that was created in the project folder
   - Look for something like: `./venv/bin/python` (macOS/Linux) or `.\venv\Scripts\python.exe` (Windows)

This ensures VS Code uses the correct Python environment with all your project dependencies.

## 🚀 Running the Application

### Method 1: Using Python directly

```bash
python main.py
```

### Method 2: Using uv

```bash
uv run main.py
```

### Method 3: Using Flask command

```bash
export FLASK_APP=main.py  # On Windows: set FLASK_APP=main.py
flask run --host=0.0.0.0 --port=5000
```

The application will be available at `http://localhost:5000`

## 🌐 Exposing Your App with ngrok

To receive webhooks from GitHub, you need to expose your local server to the internet using ngrok.

### 1. Install ngrok

**Option A: Download from website**
- Go to [ngrok.com](https://ngrok.com/)
- Download and install for your operating system

**Option B: Using package managers**
```bash
# macOS (Homebrew)
brew install ngrok

# Windows (Chocolatey)
choco install ngrok

# Linux (Snap)
sudo snap install ngrok
```

### 2. Expose your Flask app

```bash
# In a new terminal window, while your Flask app is running
ngrok http 5000
```

You'll see output like:
```
ngrok by @inconshreveable

Session Status                online
Account                       your-email@example.com
Version                       2.3.40
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
```

**Your webhook URL will be:** `https://abc123.ngrok.io/webhook/receiver`

## ⚙️ GitHub Webhook Configuration

### 1. Navigate to Your Repository Settings

1. Go to your GitHub repository
2. Click on **Settings** tab
3. Click on **Webhooks** in the left sidebar
4. Click **Add webhook**

### 2. Configure the Webhook

- **Payload URL:** `https://your-ngrok-url.ngrok.io/webhook/receiver`
- **Content type:** `application/json`
- **Secret:** (optional, leave blank for now)
- **Events:** Select "Just the push event" and "Pull requests"
- **Active:** ✅ Checked

### 3. Save the Webhook

Click **Add webhook** to save your configuration.

## 📊 Usage

### Web Interface

Visit `http://localhost:5000` to view the dashboard where you can:

- Monitor real-time webhook events
- See push, pull request, and merge activities
- View event timestamps and details
- Auto-refresh every 15 seconds

### API Endpoints

- **`GET /`** - Main dashboard
- **`GET /api/events`** - JSON API for events
- **`POST /webhook/receiver`** - GitHub webhook endpoint

### Testing Your Setup

1. **Make a commit** to your repository
2. **Create a pull request**
3. **Merge the pull request**
4. **Check your dashboard** for the events

## 📁 Project Structure

```
webhook-repo/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── extensions.py            # MongoDB connection
│   ├── routes.py               # Flask routes and webhook handlers
│   └── templates/
│       └── index.html          # Dashboard template
├── requirements.txt            # Python dependencies
├── main.py                     # Application entry point
├── .env                       # Environment variables
├── .gitignore                 # Git ignore file
├── pyproject.toml             # Project configuration and dependencies
├── uv.lock                    # Dependency lock file
└── README.md                  # This file
```

## 🔧 Troubleshooting

### Common Issues

**1. MongoDB Connection Error**
```bash
# Check if MongoDB is running
ps aux | grep mongo

# Start MongoDB (macOS)
brew services start mongodb-community

# Start MongoDB (Linux)
sudo systemctl start mongod
```

**2. Port Already in Use**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

**3. ngrok Connection Issues**
- Ensure your Flask app is running before starting ngrok
- Check that ngrok is pointing to the correct port (5000)
- Verify the webhook URL in GitHub settings

**4. Webhook Not Receiving Events**
- Check ngrok is still running and the URL hasn't changed
- Verify the webhook URL in GitHub repository settings
- Check the Flask app logs for any errors


### Viewing Logs

The application logs will show in your terminal where you ran `python main.py`. Look for:
- Connection successful messages
- Event processing logs
- Error messages


If you encounter any issues:

1. Run the test scripts to verify your setup
2. Check the application logs for error messages
3. Create an issue in the GitHub repository

---

**Happy coding! 🚀**
