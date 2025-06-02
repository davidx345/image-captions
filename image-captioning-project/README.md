# 🖼️ Image Captioning AI

This is a full-stack web application that allows users to upload an image and receive an AI-generated caption for it. The backend is built with Python and Flask, utilizing the Google Gemini API for caption generation. The frontend is a modern interface built with React, Vite, and TypeScript.

## ✨ Features

- Upload images via a user-friendly interface.
- View a preview of the uploaded image.
- Receive AI-generated captions for the image.
- Loading indicators and error handling.

## 🛠️ Tech Stack

- **Backend:**
  - Python 3.11+
  - Flask
  - Google Generative AI (Gemini API)
  - Pillow
  - Gunicorn (for production)
- **Frontend:**
  - React
  - Vite
  - TypeScript
  - CSS

## 📂 Project Structure

```
image-captioning-project/  # Backend (Flask)
├── backend_app.py         # Main Flask application
├── config.py              # Configuration for API keys
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (GEMINI_API_KEY) - Gitignored
├── src/                   # Source code for the backend
│   ├── __init__.py
│   ├── inference/         # Image captioning logic
│   │   └── generate_captions.py
│   └── ...
└── ...

my-project/                # Frontend (React + Vite)
├── index.html             # Main HTML file
├── vite.config.ts         # Vite configuration (including proxy to backend)
├── package.json           # Node.js dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── src/                   # Source code for the frontend
│   ├── App.tsx            # Main React component
│   ├── main.tsx           # Entry point for React app
│   ├── App.css            # Styles for App component
│   ├── index.css          # Global styles
└── ...
```

## Prerequisites

- Node.js (v18 or later recommended) and npm or yarn
- Python (v3.11 or later recommended) and pip
- A Google Gemini API Key

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Backend Setup (`image-captioning-project`)

Navigate to the backend directory:

```bash
cd image-captioning-project
```

Create a virtual environment (recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the `image-captioning-project` directory and add your Gemini API key:

```
GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
```

### 3. Frontend Setup (`my-project`)

Navigate to the frontend directory:

```bash
cd ../my-project
```

Install Node.js dependencies:

```bash
npm install
# or
# yarn install
```

## 🏃 Running the Application

You'll need to run both the backend and frontend servers.

### 1. Start the Backend Server

Navigate to the `image-captioning-project` directory:

```bash
cd ../image-captioning-project # If you are in my-project
# Ensure your virtual environment is activated
```

Run the Flask application:

```bash
python backend_app.py
```

The backend server will start, typically at `http://127.0.0.1:5000`.

### 2. Start the Frontend Development Server

Navigate to the `my-project` directory:

```bash
cd ../my-project # If you are in image-captioning-project
```

Run the Vite development server:

```bash
npm run dev
```

The frontend development server will start, typically at `http://localhost:5173` (or another port if 5173 is busy). It's configured to proxy API requests to the backend.

Open your browser and go to the frontend URL (e.g., `http://localhost:5173`) to use the application.

## 📦 Building the Frontend for Production

To create a production build of the frontend:

1. Navigate to the `my-project` directory.
2. Run the build command:

   ```bash
   npm run build
   ```

   This will create a `dist` folder in `my-project` containing the static assets.
3. The Flask backend is configured to serve these static files from `../my-project/dist` when not in development mode (i.e., when `FLASK_ENV` is not `development`).

## ☁️ Hosting

See the "Hosting Guide" section below for deploying to platforms like Render or Vercel.

## Hosting Guide

### Option 1: Render (Recommended for this setup)

Render can host both the Python backend and the static React frontend. You'll create two services on Render:

1. **Backend (Web Service):**
   - **Repository:** Your GitHub repository.
   - **Root Directory:** `image-captioning-project` (Set this in Render's settings for this service).
   - **Environment:** Python.
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend_app:app`
   - **Environment Variables:**
     - `GEMINI_API_KEY`: Your Gemini API key.
     - `PYTHON_VERSION`: Specify your Python version (e.g., `3.11.7`).
     - `FLASK_APP`: `backend_app.py`
     - `FLASK_ENV`: `production`

2. **Frontend (Static Site):**
   - **Repository:** Your GitHub repository.
   - **Root Directory:** `my-project` (Set this in Render's settings for this service).
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist` (This is relative to the Root Directory, so it will be `my-project/dist`).

**Important:**

- Ensure `gunicorn` is added to your `image-captioning-project/requirements.txt`.
- The Flask app is already configured to serve the frontend from `../my-project/dist`. When deployed, Render will build the frontend, and the backend service (running Flask/Gunicorn) will serve its `index.html` and other static assets. API calls from the frontend to `/api/caption` will be routed to the Flask backend on the same domain.

### Option 2: Vercel

Vercel is excellent for hosting frontend applications and can also host Python serverless functions.

1. **Frontend (Static Site on Vercel):**
   - Connect your GitHub repository to Vercel.
   - **Framework Preset:** Vite (usually auto-detected).
   - **Root Directory:** `my-project`.
   - **Build Command:** `npm run build` (or let Vercel auto-detect).
   - **Output Directory:** `dist` (or let Vercel auto-detect).

2. **Backend (Several Options):**

   - **a) Vercel Serverless Functions:**
     - You would need to restructure your Flask backend into serverless functions. Typically, you'd create an `api` directory in the root of your project (or within `image-captioning-project` if that's the Vercel project root). Each route (e.g., `/api/caption`) would become a Python file in this `api` directory (e.g., `api/caption.py`).
     - Your `requirements.txt` would need to be accessible by Vercel, usually at the root of the directory Vercel considers the project root.
     - The frontend, deployed on Vercel, would make requests to `/api/caption` which Vercel routes to your serverless function.
     - Environment Variables: Set `GEMINI_API_KEY` in Vercel project settings.

   - **b) Separate Backend Hosting (e.g., Render):**
     - Deploy your Flask backend on Render (as described in Option 1) or another platform.
     - In your frontend code (`my-project/src/App.tsx`), you would need to change the `fetch` URL for the API to be the absolute URL of your deployed backend.
       ```typescript
       // Example in App.tsx
       // const apiUrl = process.env.VITE_API_URL || '/api/caption'; // For Vercel env var
       const response = await fetch('YOUR_DEPLOYED_BACKEND_URL/api/caption', { /* ... */ });
       ```
     - You'd set `VITE_API_URL` as an environment variable in your Vercel frontend project settings.

**Recommendation:**
For the current project structure where the Flask app serves the React build, **Render is likely the more straightforward path** as it can handle both parts cohesively with minimal changes to your existing setup.

If you prefer Vercel for its frontend capabilities, you'll need to decide how to host the backend (either by refactoring to Vercel Serverless Functions or hosting it elsewhere and configuring the API endpoint in your frontend).