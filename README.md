# BugSeer - Research on Code Analysis & Bug Risk Prediction at the Source Code Level

BugSeer is a production-grade AI-powered system that analyzes Python code to predict potential bugs and assess code quality. Built with modern web technologies and machine learning, it provides developers with actionable insights to improve their code.

## 🏗️ System Architecture

The system consists of three main components:

1. **Frontend** (React + Vite + TailwindCSS)
2. **Backend API** (Node.js + Express + PostgreSQL)
3. **ML Microservice** (FastAPI + Python + Scikit-learn)

## 📁 Project Structure

```
BugSeer/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   └── contexts/        # React contexts
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── node/                 # Node.js backend API
│   │   ├── controllers/      # Request handlers
│   │   ├── routes/          # API routes
│   │   ├── models/          # Database models
│   │   ├── middleware/      # Express middleware
│   │   ├── migrations/      # Database migrations
│   │   └── package.json
│   └── fastapi/              # Python ML microservice
│       ├── app/
│       │   ├── routes/      # FastAPI routes
│       │   ├── services/    # ML services
│       │   ├── utils/       # Utility functions
│       │   └── schemas/     # Pydantic schemas
│       └── requirements.txt
└── model/                   # ML model files
    └── random_forest_model.pkl


```

## 🚀 Quick Start

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.10 or higher)
- PostgreSQL
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd BugSeer
   ```

2. **Set up the database**

   ```bash
   # Create PostgreSQL database
   create database bugseerdb

   # Navigate to Node.js backend
   cd backend/node

   # Copy environment file and configure
   cp .env
   # Edit .env with your database credentials

   # Install dependencies and run migrations
   npm install
   npm run migrate
   ```

3. **Train the ML Model (Required)**

   ```bash
   cd backend/fastapi

   # Install dependencies
   pip install -r requirements.txt

   # Train the Random Forest model - model/BugSeer_Model.ipynb
   It is recommended to train the model on Google Collab, and download the trained model as .pkl file in the model/ folder.

   # This will fetch Python repositories from GitHub and train the model
   # You can adjust the number of repositories with --repos flag
   ```

4. **Start the backend services**

   **Node.js Backend:**

   ```bash
   cd backend/node
   npm run dev
   ```

   **FastAPI ML Service:**

   ```bash
   cd backend/fastapi
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Start the frontend**

   ```bash
   cd frontend
   npm install
   cp .env
   npm run dev
   ```

6. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000
   - ML API: http://localhost:8000

## 🔧 Configuration

### Environment Variables

**Backend (.env):**

```env
PORT=5000
NODE_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/bugseerdb
DATABASE_URL_PROD=...
JWT_SECRET=...
FASTAPI_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

**FastAPI (.env):**

```env
MODEL_PATH=../model/random_forest_model.pkl
HOST=0.0.0.0
PORT=8000
```

**Frontend (.env):**

```env
VITE_API_URL=http://localhost:5000/api
```

## 📊 Features

### Core Functionality

- **Code Analysis**: Upload Python files or provide GitHub repository URLs for analysis
- **Risk Prediction**: ML-powered bug risk assessment with detailed metrics
- **User Authentication**: Secure JWT-based authentication system
- **Analysis History**: Track and review past analyses
- **Dashboard**: Comprehensive statistics and visualizations
- **Responsive Design**: Modern UI with smooth animations

### Code Metrics Analyzed

- Lines of Code (LOC)
- Number of Functions
- Cyclomatic Complexity
- Nesting Depth
- Number of Imports
- Number of Classes
- Average Function Length

## 🤖 Machine Learning Model

The system uses a Random Forest classifier trained on real Python code repositories from GitHub. The model analyzes various code metrics to predict the likelihood of bugs and code quality issues with high accuracy.

### Model Training Pipeline

1. **Data Collection**: Fetches Python repositories from GitHub API
2. **Feature Extraction**: Extracts 7 key code quality metrics from each file
3. **Label Generation**: Uses heuristics to generate training labels (can be replaced with actual bug data)
4. **Model Training**: Trains Random Forest with cross-validation
5. **Evaluation**: Provides detailed accuracy metrics and feature importance

### Model Features

- **Real Random Forest**: Trained on actual GitHub repository data
- **Feature Extraction**: Automatic extraction of code complexity metrics
- **Risk Scoring**: Probability-based risk assessment (0-100%)
- **Feature Importance**: Shows which metrics contribute most to risk prediction
- **Function-Level Analysis**: Identifies high-risk functions within code
- **Model Confidence**: Provides confidence levels for predictions
- **Actionable Recommendations**: ML-driven suggestions for code improvement

### Training Metrics

The training script provides:

- Training and test accuracy
- Cross-validation scores
- Classification report (precision, recall, F1-score)
- Feature importance ranking
- Confusion matrix

### Code Metrics Analyzed

1. **Lines of Code (LOC)**: Total non-empty lines
2. **Number of Functions**: Function definitions in the file
3. **Cyclomatic Complexity**: Control flow complexity
4. **Nesting Depth**: Maximum indentation level
5. **Number of Imports**: External dependencies
6. **Number of Classes**: Class definitions
7. **Average Function Length**: Mean lines per function

## 🔌 API Endpoints

### Authentication

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Analysis

- `POST /api/analysis` - Analyze code or repository
- `GET /api/analyze/health` - Health check with model status
- `GET /api/model/info` - Get detailed model information

### History

- `GET /api/history` - Get user's analysis history
- `GET /api/history/:id` - Get specific analysis details
- `DELETE /api/history/:id` - Delete analysis record

## 🎨 Frontend Pages

1. **Landing Page** (`/`) - Introduction and call-to-action
2. **Authentication** (`/login`, `/signup`) - User registration and login
3. **Home** (`/home`) - Code analysis interface
4. **Dashboard** (`/dashboard`) - Statistics and visualizations
5. **History** (`/history`) - Analysis history and management
6. **Profile** (`/profile`) - User profile and settings
7. **About** (`/about`) - Research methodology and technology stack

## 🛠️ Technology Stack

### Frontend

- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Framer Motion** - Animations
- **React Router** - Navigation
- **React Query** - Data fetching
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Backend

- **Node.js** - Runtime
- **Express** - Web framework
- **PostgreSQL** - Database
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Axios** - HTTP client

### ML Service

- **FastAPI** - Python web framework
- **Scikit-learn** - Machine learning
- **Pandas** - Data manipulation
- **AST** - Python code parsing
- **Pydantic** - Data validation

## 🚀 Deployment

### Production Deployment

The system is designed for deployment on platforms like Render, Vercel, or AWS:

1. **Frontend**: Deploy to Render, Vercel or Netlify
2. **Backend API**: Deploy to Render or AWS ECS
3. **ML Service**: Deploy to Render or AWS Lambda
4. **Database**: Use managed PostgreSQL (AWS RDS, Render PostgreSQL, Supabase)

### Environment Setup

1. Configure production environment variables
2. Set up PostgreSQL database
3. Deploy ML model to accessible storage
4. Configure CORS for production domains
5. Set up SSL certificates

## 🔒 Security

### Security Measures

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt for password storage
- **CORS Configuration**: Proper cross-origin settings
- **Rate Limiting**: API abuse prevention
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Prevention**: Parameterized queries

---

By Ebrima Gajaga under the supervision of Mrs. Pritibala Patel
