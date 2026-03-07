# Deploy to Render Free Tier

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

3. **Deploy from Dashboard**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml` and create:
     - Web Service (your Flask app)
     - PostgreSQL Database (free tier)

4. **Set Environment Variables**
   After deployment, go to your web service dashboard and add:
   - `GEMINI_API_KEY` - Your Google AI API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)
   
   (SECRET_KEY and DATABASE_URL are auto-configured)

5. **Wait for Build**
   - First deployment takes 5-10 minutes
   - You'll get a URL like: `https://quiz-app-xxxx.onrender.com`

## Important Notes

- **Free tier limitations:**
  - Service spins down after 15 minutes of inactivity
  - First request after spin-down takes 30-60 seconds
  - 750 hours/month free (enough for one service)
  - PostgreSQL database: 90 days free, then $7/month

- **Database migrations:**
  - Tables are created automatically on first run
  - For schema changes, you may need to run migrations manually

## Alternative: Manual Setup (without render.yaml)

If you prefer manual setup:

1. New Web Service → Connect GitHub repo
2. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment: Python 3
3. Add PostgreSQL database from Render dashboard
4. Link database to web service
5. Add environment variables

## Troubleshooting

- **500 errors:** Check logs in Render dashboard
- **Database errors:** Ensure DATABASE_URL is linked
- **Slow first load:** Normal for free tier (cold start)
