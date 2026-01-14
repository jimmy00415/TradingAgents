# 🚀 TradingAgents Deployment Guide

## Overview

Currently, TradingAgents is a **CLI application**. To make it accessible to your team through a web UI, you have several deployment options.

---

## 📊 Current State vs. Web Application

### **Current State (CLI):**
- ✅ Python command-line interface
- ✅ Generates markdown reports locally
- ✅ Runs on individual machines
- ❌ No web interface
- ❌ No remote access

### **What You Need for Web Deployment:**
1. **Web UI** (Frontend) - HTML/React/Vue interface
2. **Web API** (Backend) - Flask/FastAPI to serve requests
3. **Cloud Hosting** - Azure/AWS/GitHub
4. **Database** (Optional) - Store analysis history
5. **Authentication** - Secure team access

---

## 🎯 Deployment Options

### **Option 1: Quick Solution - Streamlit Web App (Recommended for Beginners)**

**Best for:** Quick deployment, team collaboration, minimal setup

**Pros:**
- ✅ Python-only (no JavaScript needed)
- ✅ Built-in UI components
- ✅ Can deploy to Streamlit Cloud (FREE)
- ✅ Easy to build and maintain
- ✅ Ready in hours, not days

**Cons:**
- ⚠️ Limited customization
- ⚠️ Shared resources on free tier

**Implementation Steps:**

1. **Install Streamlit:**
```bash
pip install streamlit
```

2. **Create `streamlit_app.py`:**
```python
import streamlit as st
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="TradingAgents", page_icon="📈", layout="wide")

st.title("📈 TradingAgents - AI Trading Analysis")

# Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    ticker = st.text_input("Stock Ticker", value="AAPL")
    date = st.date_input("Analysis Date")
    
    st.subheader("Model Settings")
    llm_model = st.selectbox("LLM Model", ["gpt-5", "gpt-4o", "gpt-4o-mini"])
    debate_rounds = st.slider("Debate Rounds", 1, 5, 1)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing market data... This may take a few minutes..."):
            try:
                # Configure
                config = DEFAULT_CONFIG.copy()
                config["deep_think_llm"] = llm_model
                config["quick_think_llm"] = llm_model
                config["max_debate_rounds"] = debate_rounds
                
                # Run analysis
                ta = TradingAgentsGraph(debug=False, config=config)
                _, decision = ta.propagate(ticker, date.strftime("%Y-%m-%d"))
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                # Show decision
                st.subheader("Trading Decision")
                if decision and "action" in decision:
                    action = decision["action"]
                    if action.lower() == "buy":
                        st.success(f"🟢 **BUY** {ticker}")
                    elif action.lower() == "sell":
                        st.error(f"🔴 **SELL** {ticker}")
                    else:
                        st.warning(f"⚪ **HOLD** {ticker}")
                
                # Display full report
                st.subheader("Detailed Analysis")
                st.json(decision)
                
                # Show report files
                report_path = f"./results/{ticker}/{date.strftime('%Y-%m-%d')}/reports"
                if os.path.exists(report_path):
                    st.subheader("Generated Reports")
                    for file in os.listdir(report_path):
                        if file.endswith('.md'):
                            with open(os.path.join(report_path, file), 'r') as f:
                                st.markdown(f"### {file}")
                                st.markdown(f.read())
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with col2:
    st.subheader("Recent Analyses")
    if os.path.exists("./results"):
        results = []
        for ticker in os.listdir("./results"):
            ticker_path = os.path.join("./results", ticker)
            if os.path.isdir(ticker_path):
                for date in os.listdir(ticker_path):
                    results.append(f"{ticker} - {date}")
        
        if results:
            for result in sorted(results, reverse=True)[:10]:
                st.text(result)
        else:
            st.info("No analyses yet")

# Footer
st.markdown("---")
st.markdown("**TradingAgents** - Multi-Agent LLM Trading Framework")
```

3. **Test locally:**
```bash
streamlit run streamlit_app.py
```

4. **Deploy to Streamlit Cloud (FREE):**
   - Push code to GitHub
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repo
   - Set environment variables (API keys) in Streamlit Cloud settings
   - Deploy!

**Cost:** FREE (Streamlit Community Cloud)

---

### **Option 2: Full Web App - FastAPI + React (Professional)**

**Best for:** Production deployment, full customization, enterprise use

**Pros:**
- ✅ Full control over UI/UX
- ✅ RESTful API architecture
- ✅ Scalable and professional
- ✅ Better performance
- ✅ Can deploy to Azure, AWS, GCP

**Cons:**
- ⚠️ More complex setup
- ⚠️ Requires frontend development
- ⚠️ Higher maintenance

**Architecture:**
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI   │─────▶│ TradingAgent│
│  Frontend   │◀─────│   Backend   │◀─────│   Engine    │
└─────────────┘      └─────────────┘      └─────────────┘
     │                      │                     │
     │                      │                     │
     ▼                      ▼                     ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Azure     │      │  PostgreSQL │      │   Results   │
│  Static Web │      │   Database  │      │   Storage   │
└─────────────┘      └─────────────┘      └─────────────┘
```

**Implementation Steps:**

1. **Create FastAPI Backend (`api/main.py`):**
```python
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import uvicorn

app = FastAPI(title="TradingAgents API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    ticker: str
    date: str
    llm_model: str = "gpt-5"
    debate_rounds: int = 1

@app.post("/api/analyze")
async def analyze_stock(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Run trading analysis for a stock"""
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = request.llm_model
    config["quick_think_llm"] = request.llm_model
    config["max_debate_rounds"] = request.debate_rounds
    
    ta = TradingAgentsGraph(debug=False, config=config)
    _, decision = ta.propagate(request.ticker, request.date)
    
    return {
        "status": "success",
        "ticker": request.ticker,
        "date": request.date,
        "decision": decision
    }

@app.get("/api/history")
async def get_history():
    """Get analysis history"""
    # Read from results directory
    # Return list of past analyses
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

2. **Create React Frontend** (see full instructions in later sections)

3. **Deploy to Azure:**
   - Backend: Azure App Service or Container Instances
   - Frontend: Azure Static Web Apps
   - Database: Azure PostgreSQL (optional)

**Cost:** ~$10-50/month (depending on scale)

---

### **Option 3: GitHub Codespaces (Team Development)**

**Best for:** Remote development, team collaboration, testing

**Pros:**
- ✅ Cloud-based VS Code
- ✅ Pre-configured environment
- ✅ Team can access same environment
- ✅ No local setup needed

**Cons:**
- ⚠️ Not for end-user access
- ⚠️ Still requires CLI knowledge
- ⚠️ Limited free hours

**Setup:**

1. **Create `.devcontainer/devcontainer.json`:**
```json
{
  "name": "TradingAgents",
  "image": "mcr.microsoft.com/devcontainers/python:3.13",
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  },
  "forwardPorts": [8501, 8000],
  "secrets": {
    "OPENAI_API_KEY": "",
    "ALPHA_VANTAGE_API_KEY": ""
  }
}
```

2. **Enable Codespaces** in your GitHub repo settings

3. **Team members click** "Code" → "Codespaces" → "Create codespace"

**Cost:** 60 hours/month FREE per user, then $0.18/hour

---

## 🌟 Recommended Approach

### **For Your Use Case:**

Based on your needs, I recommend this **phased approach**:

### **Phase 1: Immediate (This Week) - Streamlit**
✅ Build a Streamlit web app (see Option 1)  
✅ Deploy to Streamlit Cloud (FREE)  
✅ Share URL with team  
✅ Team can run analyses through web browser  

**Time:** 2-4 hours  
**Cost:** FREE  
**Technical Skill:** Low  

### **Phase 2: Short-term (Next Month) - Azure Container**
✅ Containerize with Docker  
✅ Deploy to Azure Container Instances  
✅ Add basic authentication  
✅ Connect to Azure Blob Storage for reports  

**Time:** 1-2 days  
**Cost:** ~$20/month  
**Technical Skill:** Medium  

### **Phase 3: Long-term (Future) - Full Production**
✅ Build React frontend  
✅ FastAPI backend with database  
✅ Deploy to Azure App Service  
✅ User management & role-based access  
✅ Email notifications  
✅ Scheduled analyses  

**Time:** 1-2 weeks  
**Cost:** ~$50-100/month  
**Technical Skill:** High  

---

## 🛠️ Quick Start: Streamlit Deployment

### **Step 1: Create Streamlit App**

I'll create the basic files for you (run the command below):

```bash
# Create streamlit app
code streamlit_app.py
```

### **Step 2: Add to requirements.txt**

```bash
streamlit>=1.30.0
plotly>=5.18.0
```

### **Step 3: Test Locally**

```bash
pip install streamlit plotly
streamlit run streamlit_app.py
```

### **Step 4: Deploy to Streamlit Cloud**

1. Push to GitHub:
```bash
git add streamlit_app.py
git commit -m "Add Streamlit web interface"
git push origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and `streamlit_app.py`
6. Add secrets (API keys) in Advanced settings:
```toml
OPENAI_API_KEY = "bb806427-7dd1-4f92-86a2-aa8748197cca"
AZURE_OPENAI_API_KEY = "bb806427-7dd1-4f92-86a2-aa8748197cca"
ALPHA_VANTAGE_API_KEY = "5GK3NBVL9YVJI3QV"
FINNHUB_API_KEY = "d227u3pr01qt86776u90d227u3pr01qt86776u9g"
```
7. Click "Deploy"
8. Share the URL: `https://yourapp.streamlit.app`

**Done!** Your team can now access it from anywhere.

---

## 🏗️ Azure Deployment Guide

### **Option A: Azure Container Instances (Simple)**

1. **Create Dockerfile:**
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and push to Azure Container Registry:**
```bash
# Login to Azure
az login

# Create resource group
az group create --name tradingagents-rg --location eastus

# Create container registry
az acr create --resource-group tradingagents-rg --name tradingagentsacr --sku Basic

# Build and push
az acr build --registry tradingagentsacr --image tradingagents:v1 .

# Deploy to Container Instances
az container create \
  --resource-group tradingagents-rg \
  --name tradingagents-app \
  --image tradingagentsacr.azurecr.io/tradingagents:v1 \
  --dns-name-label tradingagents-app \
  --ports 8501 \
  --environment-variables \
    OPENAI_API_KEY="your_key" \
    ALPHA_VANTAGE_API_KEY="your_key"
```

3. **Access your app:**
```
http://tradingagents-app.eastus.azurecontainer.io:8501
```

**Cost:** ~$15-30/month

### **Option B: Azure App Service (Advanced)**

1. **Create Web App:**
```bash
# Create App Service Plan
az appservice plan create --name tradingagents-plan --resource-group tradingagents-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group tradingagents-rg --plan tradingagents-plan --name tradingagents-app --runtime "PYTHON:3.13"

# Configure environment variables
az webapp config appsettings set --resource-group tradingagents-rg --name tradingagents-app --settings \
  OPENAI_API_KEY="your_key" \
  ALPHA_VANTAGE_API_KEY="your_key"

# Deploy code
az webapp up --name tradingagents-app --resource-group tradingagents-rg
```

**Cost:** ~$13/month (B1 tier)

---

## 📊 Cost Comparison

| Option | Setup Time | Monthly Cost | Best For |
|--------|------------|--------------|----------|
| **Streamlit Cloud** | 2 hours | FREE | Small teams, testing |
| **GitHub Codespaces** | 1 hour | FREE (60hrs) | Development only |
| **Azure Container** | 4 hours | $15-30 | Medium teams |
| **Azure App Service** | 1 day | $13-50 | Production use |
| **Full Stack (FastAPI+React)** | 1-2 weeks | $50-100 | Enterprise |

---

## 🔐 Security Considerations

### **For Team Deployment:**

1. **Never commit API keys** - Already protected by `.gitignore` ✅
2. **Use environment variables** in cloud platforms
3. **Add authentication** - Streamlit has built-in auth
4. **Use HTTPS** - Automatic on Streamlit Cloud and Azure
5. **Implement rate limiting** - Prevent API abuse
6. **User access control** - Track who runs what analysis

### **Streamlit Authentication:**

Add to `streamlit_app.py`:
```python
import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "your_team_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Rest of your app
```

---

## 📈 Next Steps

1. **Review options** and choose deployment method
2. **Set up Streamlit app** (recommended starting point)
3. **Test with team** and gather feedback
4. **Scale to Azure** if needed for performance
5. **Add features** based on team needs

---

## 🆘 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/
- **Azure Docs**: https://docs.microsoft.com/azure/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

**Ready to deploy?** Let me know which option you prefer, and I'll help you implement it! 🚀
