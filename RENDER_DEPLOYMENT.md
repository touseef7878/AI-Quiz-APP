# Deploy to Render Free Tier (100% FREE)

## Quick Setup Steps

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `quiz-app`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - **Instance Type: FREE**

4. **Set Environment Variables**
   In the Environment section, add:
   - `GEMINI_API_KEY` - Your Google AI API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)
   - `SECRET_KEY` - Generate a random string (or let Render auto-generate)
   - `QUIZ_QUESTIONS_COUNT` - `10`

5. **Deploy**
   - Click "Create Web Service"
   - First deployment takes 5-10 minutes
   - You'll get a URL like: `https://quiz-app-xxxx.onrender.com`

## Important Notes

- **100% Free tier includes:**
  - Web service with 750 hours/month (enough for one service)
  - SQLite database (stored in memory, resets on restart)
  - Automatic HTTPS

- **Free tier limitations:**
  - Service spins down after 15 minutes of inactivity
  - First request after spin-down takes 30-60 seconds
  - **Database resets when service restarts** (use paid tier for persistent storage)
  - 512 MB RAM, shared CPU

- **Database behavior:**
  - User registrations and quiz history will be lost on restart
  - Good for testing and demos
  - For persistent data, upgrade to paid tier ($7/month with PostgreSQL)

## Alternative: Use Blueprint (render.yaml)

The included `render.yaml` file allows one-click deployment:
1. Click "New +" → "Blueprint"
2. Connect your repository
3. Render auto-configures everything
4. Just add `GEMINI_API_KEY` after deployment

## Troubleshooting

- **500 errors:** Check logs in Render dashboard
- **Data disappeared:** Normal on free tier - database resets on restart
- **Slow first load:** Normal for free tier (cold start after 15 min idle)
