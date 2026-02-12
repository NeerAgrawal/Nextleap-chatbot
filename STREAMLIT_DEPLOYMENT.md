# Nextleap RAG Chatbot - Streamlit Deployment

## 🚀 Quick Start with Streamlit

### Local Development

1. **Install Streamlit**
   ```bash
   cd phase_3
   pip install -r requirements.txt
   ```

2. **Configure Secrets**
   ```bash
   # Copy the example secrets file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   
   # Edit .streamlit/secrets.toml and add your Groq API key
   ```

3. **Run the App**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open Browser**
   - The app will automatically open at `http://localhost:8501`
   - Or manually navigate to the URL shown in terminal

---

## ☁️ Deploy to Streamlit Cloud (FREE!)

### Prerequisites
- GitHub account
- Groq API key

### Step-by-Step Deployment

#### 1. Push to GitHub

```bash
# Initialize git (if not already done)
cd Nextleap
git init
git add .
git commit -m "Add Streamlit chatbot"

# Push to GitHub
git remote add origin https://github.com/yourusername/nextleap-chatbot.git
git branch -M main
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository: `yourusername/nextleap-chatbot`
4. Set **Main file path**: `phase_3/streamlit_app.py`
5. Click **"Advanced settings"**
6. Add secrets in the "Secrets" section:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   GROQ_TEMPERATURE = "0.3"
   GROQ_MAX_TOKENS = "1024"
   TOP_K_RESULTS = "5"
   ```
7. Click **"Deploy"**

Your app will be live at: `https://yourusername-nextleap-chatbot.streamlit.app`

---

## 📁 Required Files for Streamlit Deployment

Make sure these files are in your repository:

```
Nextleap/
├── phase_1/               # Data collection (needed for reference)
│   └── data/processed/   # JSON files
├── phase_2/              # Embeddings (REQUIRED)
│   ├── database/
│   │   ├── vector_db/   # FAISS index files
│   │   └── metadata.db  # SQLite database
│   └── src/             # Database clients
└── phase_3/             # Streamlit app (REQUIRED)
    ├── streamlit_app.py # Main app file
    ├── requirements.txt # Dependencies
    ├── .streamlit/
    │   └── config.toml  # Theme configuration
    └── src/             # Chatbot logic
        ├── query/
        ├── retrieval/
        ├── llm/
        └── api/
```

---

## 🎨 Features

### Chat Interface
- ✅ **Native Streamlit Chat**: Beautiful built-in chat UI
- ✅ **Conversation History**: Maintains chat context
- ✅ **Quick Questions**: Sidebar buttons for common queries
- ✅ **Premium Design**: Custom gradient theme

### Functionality
- ✅ **Vector Search**: FAISS semantic search
- ✅ **LLM Integration**: Groq llama-3.3-70b-versatile
- ✅ **Session State**: Persistent conversation in session
- ✅ **Error Handling**: Graceful error messages

---

## 🔧 Configuration

### Theme (`.streamlit/config.toml`)
```toml
[theme]
primaryColor="#764ba2"
backgroundColor="#667eea"
secondaryBackgroundColor="#5a67d8"
textColor="#ffffff"
```

### Secrets (Streamlit Cloud or `.streamlit/secrets.toml`)
```toml
GROQ_API_KEY = "your_key"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = "0.3"
GROQ_MAX_TOKENS = "1024"
TOP_K_RESULTS = "5"
```

---

## 🆚 Streamlit vs Flask Comparison

| Feature | Streamlit | Flask (Previous) |
|---------|-----------|------------------|
| **Setup** | Single Python file | Separate frontend + backend |
| **Deployment** | Streamlit Cloud (free) | Requires hosting |
| **UI** | Built-in components | Custom HTML/CSS/JS |
| **Chat Interface** | `st.chat_message()` | Custom implementation |
| **Session State** | `st.session_state` | Manual/cookies |
| **Complexity** | Low ⭐ | Medium ⭐⭐⭐ |
| **Deployment Time** | 5 minutes | 30+ minutes |

**Recommendation**: Use Streamlit for simpler deployment and maintenance!

---

## 📊 Resource Requirements

### Streamlit Cloud (Free Tier)
- ✅ **RAM**: 1 GB (sufficient for our app)
- ✅ **vCPUs**: Shared
- ✅ **Storage**: 50 GB (we use ~500 MB)
- ✅ **Bandwidth**: Unlimited

### Local Development
- **RAM**: 2 GB minimum
- **Storage**: 1 GB for models + databases
- **Python**: 3.14+

---

## 🐛 Troubleshooting

### App won't start
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Verify Phase 2 databases exist
ls ../phase_2/database/
# Should show: vector_db/ and metadata.db
```

### "Module not found" errors
```bash
# Make sure you're in the phase_3 directory
cd phase_3
streamlit run streamlit_app.py
```

### Secrets not loading
**Local**: Ensure `.streamlit/secrets.toml` exists and has your API key

**Streamlit Cloud**: 
1. Go to app settings
2. Click "Secrets" 
3. Paste your secrets in TOML format

### Database errors
```bash
# Re-run Phase 2 to regenerate databases
cd ../phase_2
python scripts/run_phase2.py
```

---

## 🔄 Updating the App

### Update Content
```bash
# Update course data
cd phase_1
python scripts/web_scraper.py

# Regenerate embeddings
cd ../phase_2
python scripts/run_phase2.py

# Push to GitHub - Streamlit Cloud auto-deploys!
git add .
git commit -m "Update course content"
git push
```

### Update Code
```bash
# Make changes to streamlit_app.py
git add phase_3/streamlit_app.py
git commit -m "Improve chat interface"
git push
# Streamlit Cloud automatically redeploys!
```

---

## ✅ Deployment Checklist

### Before Deployment
- [ ] All Phase 2 databases generated
- [ ] `requirements.txt` includes streamlit
- [ ] `.streamlit/config.toml` exists
- [ ] Code pushed to GitHub
- [ ] Groq API key ready

### Streamlit Cloud Setup
- [ ] Create account on share.streamlit.io
- [ ] Connect GitHub repository
- [ ] Set main file path: `phase_3/streamlit_app.py`
- [ ] Add secrets (GROQ_API_KEY, etc.)
- [ ] Deploy

### After Deployment
- [ ] Test all quick questions
- [ ] Verify responses are accurate
- [ ] Check conversation history works
- [ ] Monitor usage on Groq dashboard

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud**: https://share.streamlit.io
- **Groq API**: https://console.groq.com

---

**Ready to deploy! 🚀**

Your Streamlit app is simpler, faster, and easier to maintain than the Flask version!
