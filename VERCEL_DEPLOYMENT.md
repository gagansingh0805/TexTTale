# AI Story Generator - Vercel Deployment Guide

This guide will help you deploy your AI Story Generator to Vercel.

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository

1. Push your code to GitHub
2. Make sure you have a Google Gemini API key

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Configure the following settings:

#### Build Settings:

- **Framework Preset**: Other
- **Root Directory**: Leave empty (uses root)
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/build`

#### Environment Variables:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `REACT_APP_API_URL`: Will be set automatically to your Vercel domain

### 3. Deploy

Click "Deploy" and wait for the build to complete.

## 📁 Project Structure for Vercel

```
├── frontend/           # React frontend
├── api/               # Vercel serverless functions
│   ├── generate-story.py
│   ├── text-to-speech.py
│   ├── story-options.py
│   └── requirements.txt
├── backend/           # Original backend (used by API functions)
├── vercel.json       # Vercel configuration
└── package.json      # Root package.json
```

## 🔧 Configuration Files

### vercel.json

- Configures builds for frontend and API functions
- Sets up routing for API endpoints
- Defines environment variables
- Sets function timeout to 30 seconds

### API Functions

- `api/generate-story.py`: Handles story generation
- `api/text-to-speech.py`: Handles text-to-speech conversion
- `api/story-options.py`: Returns available options

## 🌐 Environment Variables

### Required:

- `GEMINI_API_KEY`: Your Google Gemini API key for AI story generation

### Automatic:

- `REACT_APP_API_URL`: Automatically set to your Vercel domain

## 🎯 API Endpoints

After deployment, your API will be available at:

- `https://your-app.vercel.app/api/generate-story`
- `https://your-app.vercel.app/api/text-to-speech`
- `https://your-app.vercel.app/api/story-options`

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**:

   - Check that all dependencies are in `frontend/package.json`
   - Ensure Python dependencies are in `api/requirements.txt`

2. **API Errors**:

   - Verify `GEMINI_API_KEY` is set correctly
   - Check function logs in Vercel dashboard

3. **CORS Issues**:

   - API functions include CORS headers for all origins

4. **Timeout Issues**:
   - Functions are set to 30-second timeout
   - For longer operations, consider breaking into smaller chunks

### Debugging:

- Check Vercel function logs in the dashboard
- Use browser dev tools to inspect API calls
- Test API endpoints directly using curl or Postman

## 📝 Notes

- Audio files are generated temporarily and cleaned up automatically
- The app uses Google Gemini AI for story generation
- Text-to-speech uses Google TTS (gTTS)
- Background noise generation is included

## 🔄 Updates

To update your deployment:

1. Push changes to GitHub
2. Vercel will automatically redeploy
3. Check the deployment status in your Vercel dashboard

## 📞 Support

If you encounter issues:

1. Check Vercel deployment logs
2. Verify environment variables
3. Test API endpoints individually
4. Check browser console for frontend errors
