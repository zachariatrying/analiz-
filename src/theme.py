CSS_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    .stApp { font-family: 'Outfit', sans-serif; }

    /* Animated Dark Background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #1a103c 0%, #0f0c29 50%, #0f172a 100%);
        background-size: 200% 200%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar Glass */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Premium Glassmorphism Cards */
    .glass-card {
        background: rgba(20, 25, 45, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        border-left: 1px solid rgba(255, 255, 255, 0.15);
        padding: 24px; 
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 15px 45px rgba(99, 102, 241, 0.2);
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(99,102,241,0.08) 0%, rgba(168,85,247,0.05) 100%);
        border-radius: 16px;
        border: 1px solid rgba(99,102,241,0.15);
        padding: 20px; 
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.05), transparent);
        transform: skewX(-20deg);
        transition: 0.5s;
    }
    .metric-card:hover::before { left: 150%; }
    .metric-card:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 10px 30px rgba(99,102,241,0.25); 
        border-color: rgba(99,102,241,0.4);
    }

    /* Metric Values with Neon Glow */
    .metric-value {
        font-size: 2rem; font-weight: 800;
        line-height: 1.2;
        margin: 8px 0;
        background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 100%);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(168,85,247,0.3);
    }

    .metric-label {
        font-size: 0.8rem; color: #cbd5e1;
        text-transform: uppercase; letter-spacing: 2px; font-weight: 600;
    }

    .metric-delta-up { color: #4ade80; font-weight: 600; font-size: 0.95rem; text-shadow: 0 0 10px rgba(74,222,128,0.3); }
    .metric-delta-down { color: #f87171; font-weight: 600; font-size: 0.95rem; text-shadow: 0 0 10px rgba(248,113,113,0.3); }
    
    /* Native Metrics override */
    div[data-testid="stMetricValue"] { color: #818cf8; font-family: 'Outfit', monospace; font-weight: 800; }
    
    /* Streamlit Native Inputs Styling */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div, 
    .stNumberInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus, 
    .stSelectbox > div > div > div:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.25) !important;
    }

    /* Primary Buttons Animated */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #d946ef) !important;
        background-size: 200% auto !important;
        border: none !important; 
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        padding: 12px 28px !important;
        transition: 0.5s !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-position: right center !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Progress bars */
    .stProgress > div > div { background: linear-gradient(90deg, #6366f1, #a78bfa, #c084fc) !important; border-radius: 8px; }

    hr { border-color: rgba(255,255,255,0.06) !important; margin: 2rem 0 !important; }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.8); }
    ::-webkit-scrollbar-thumb { background: linear-gradient(to bottom, #6366f1, #c084fc); border-radius: 4px; }
</style>
"""
