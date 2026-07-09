# Deployment Report

## Overview
This document covers how to run the application locally and 
deploy it to Render for public access.

---

## Local Setup

### Requirements
- Python 3.10+
- pip

### Steps
1. Clone the repository
   git clone https://github.com/ishekaa12/predictive-maintenance-project.git
   cd predictive-maintenance-project

2. Install dependencies
   pip install -r requirements.txt

3. Train models (required before running Flask)
   python src/train.py

4. Start the Flask server
   cd deployment
   python app.py

5. Open in browser
   http://localhost:5000

---

## Requirements File

Generate with:
   pip freeze > requirements.txt

Key dependencies:
- flask
- pandas
- numpy
- scikit-learn
- xgboost
- plotly
- seaborn
- jupyter

---

## Production Deployment — Render

### Steps
1. Push all code to GitHub
2. Go to render.com and create a free account
3. Click New → Web Service
4. Connect your GitHub repository
5. Set the following:
   - Build Command: pip install -r requirements.txt
   - Start Command: python deployment/app.py
   - Environment: Python 3
6. Click Deploy

### Notes
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Models must be committed to GitHub for Render to access them
  (remove models/ from .gitignore before deploying to Render)
- Chat history resets on every server restart

---

## Environment Variables
None required for current version.

---

## Known Limitations
- Chat history is stored in memory — resets on restart
- Models are retrained locally — no automated retraining pipeline
- No user authentication
- Render free tier has cold start delay

---

## Status
- [x] Local deployment working
- [ ] Render deployment — Week 6