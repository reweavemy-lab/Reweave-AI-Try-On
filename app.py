import streamlit as st
import os
from PIL import Image
from io import BytesIO
from google import genai
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Configure the client with your API key
import os
api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error("🔑 Google API key not found! Please add your GOOGLE_API_KEY or GEMINI_API_KEY to the environment variables.")
    st.stop()

client = genai.Client(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="Reweave - AI Try-On",
    page_icon="🏓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Allow embedding in iframes - this helps with Streamlit Cloud embedding
st.markdown("""
<script>
    // Allow embedding by removing X-Frame-Options restrictions
    if (window.parent !== window) {
        // We're in an iframe
        console.log('Running in iframe');
    }
</script>
""", unsafe_allow_html=True)

# Custom CSS for pickleball-themed styling
st.markdown("""
<style>
    /* Ensure clean white background with black text */
    .main .block-container {
        background-color: white;
        color: black;
    }
    
    .stApp {
        background-color: white;
        color: black;
    }
    
    /* Ensure all text is black and centered */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, div, span {
        color: black !important;
        text-align: center !important;
    }
    
    /* Center all content containers */
    .main .block-container {
        text-align: center !important;
    }
    
    /* Streamlit component styling */
    .stSelectbox label, .stFileUploader label {
        color: black !important;
        text-align: center !important;
    }
    
    /* Center file uploader and selectbox containers */
    .stFileUploader, .stSelectbox {
        text-align: center !important;
    }
    
    /* File uploader styling - more specific targeting */
    .stFileUploader > div > div > div {
        border: 2px dashed #3b82f6 !important;
        border-radius: 10px !important;
        background-color: #f8faff !important;
        color: #1e3a8a !important;
    }
    
    .stFileUploader > div > div > div:hover {
        border-color: #1e3a8a !important;
        background-color: #eff6ff !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #3b82f6 !important;
        border-radius: 10px !important;
        background-color: #f8faff !important;
        color: #1e3a8a !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #1e3a8a !important;
        background-color: #eff6ff !important;
    }
    
    /* Browse files button styling */
    .stFileUploader button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader button:hover {
        background-color: #1e3a8a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"] button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    /* Selectbox styling - more specific targeting */
    .stSelectbox > div > div > div {
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
        background-color: white !important;
        color: black !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
        background-color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #1e3a8a !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Dropdown menu styling - comprehensive targeting */
    .stSelectbox [data-baseweb="popover"] {
        background-color: white !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox [data-baseweb="menu"] {
        background-color: white !important;
    }
    
    .stSelectbox [data-baseweb="option"] {
        background-color: white !important;
        color: black !important;
    }
    
    .stSelectbox [data-baseweb="option"]:hover {
        background-color: #eff6ff !important;
        color: #1e3a8a !important;
    }
    
    /* Additional dropdown targeting */
    .stSelectbox ul {
        background-color: white !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox li {
        background-color: white !important;
        color: black !important;
    }
    
    .stSelectbox li:hover {
        background-color: #eff6ff !important;
        color: #1e3a8a !important;
    }
    
    /* Target the dropdown container more specifically */
    div[data-baseweb="select"] > div {
        background-color: white !important;
    }
    
    /* Target any dropdown menus */
    [role="listbox"] {
        background-color: white !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    
    [role="option"] {
        background-color: white !important;
        color: black !important;
    }
    
    [role="option"]:hover {
        background-color: #eff6ff !important;
        color: #1e3a8a !important;
    }
    
    /* Style Streamlit's fullscreen button - make it blue and visible */
    .stImage button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px !important;
        opacity: 0.9 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
        position: absolute !important;
        top: 10px !important;
        right: 10px !important;
    }
    
    .stImage button:hover {
        background-color: #1e3a8a !important;
        opacity: 1 !important;
        transform: scale(1.1) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stImage button svg {
        fill: white !important;
        width: 16px !important;
        height: 16px !important;
    }
    
    /* Make the button more visible by default */
    .stImage:hover button {
        opacity: 1 !important;
    }
    
    /* Custom image display styling */
    .custom-image-container {
        position: relative;
        display: inline-block;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
    }
    
    .custom-image-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    .bag-preview-image {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 12px;
    }
    
    .custom-fullscreen-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px;
        cursor: pointer;
        opacity: 0.8;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
        z-index: 10;
    }
    
    .custom-fullscreen-btn:hover {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        opacity: 1;
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .custom-fullscreen-btn svg {
        display: block;
        width: 20px;
        height: 20px;
    }
    
    .bag-caption {
        text-align: center;
        margin: 10px 0 0 0;
        font-weight: 500;
        color: #1e3a8a;
    }
    
    /* Mobile-first responsive design with blue theme */
    .main-header {
        text-align: center !important;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
        color: white;
        border-radius: 15px;
        margin: 0 auto 2rem auto;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* FORCE the main title to be black - override everything */
    .main-header h1 {
        color: black !important;
        -webkit-text-fill-color: black !important;
        background: none !important;
        background-clip: unset !important;
        -webkit-background-clip: unset !important;
    }
    
    /* FORCE the Reweave text to be black too */
    .main-header h1 .pickleball-accent {
        color: black !important;
        -webkit-text-fill-color: black !important;
        background: none !important;
        background-clip: unset !important;
        -webkit-background-clip: unset !important;
    }
    
    .pickleball-accent {
        background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
    }
    
    .court-container {
        background: white;
        border: 3px solid #3b82f6;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.1);
        color: black;
    }
    
    .court-container h2, .court-container p, .court-container em {
        color: black !important;
        text-align: center !important;
    }
    
    .court-container::before {
        content: "🏓";
        position: absolute;
        top: -15px;
        left: 20px;
        background: white;
        padding: 0 10px;
        font-size: 1.2em;
    }
    
    .bag-selection {
        border: 2px solid #60a5fa;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
        background: white;
    }
    
    .bag-selection:hover {
        border-color: #1e3a8a;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
    }
    
    .generate-btn {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 25px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .generate-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Streamlit button overrides - more specific targeting */
    .stButton > button[key="generate_btn"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 25px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button[key="generate_btn"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
    }
    
    .stButton > button[key="restart_btn"] {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[key="restart_btn"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4) !important;
    }
    
    .stButton > button[key="regenerate_btn"] {
        background: linear-gradient(135deg, #60a5fa 0%, #93c5fd 100%) !important;
        color: #1e3a8a !important;
        border: 2px solid #1e3a8a !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[key="regenerate_btn"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(96, 165, 250, 0.4) !important;
    }
    
    /* Additional button targeting - even more specific */
    button[data-testid="baseButton-secondary"][key="generate_btn"],
    button[data-testid="baseButton-primary"][key="generate_btn"],
    div[data-testid="stButton"] button[key="generate_btn"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 25px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    button[data-testid="baseButton-secondary"][key="restart_btn"],
    button[data-testid="baseButton-primary"][key="restart_btn"],
    div[data-testid="stButton"] button[key="restart_btn"] {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
    }
    
    button[data-testid="baseButton-secondary"][key="regenerate_btn"],
    button[data-testid="baseButton-primary"][key="regenerate_btn"],
    div[data-testid="stButton"] button[key="regenerate_btn"] {
        background: linear-gradient(135deg, #60a5fa 0%, #93c5fd 100%) !important;
        color: #1e3a8a !important;
        border: 2px solid #1e3a8a !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
    }
    
    /* Universal button override for any grey buttons */
    .stButton button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Style ALL Streamlit components with blue theme */
    
    /* Error messages */
    .stAlert[data-baseweb="notification"] {
        background-color: #fef2f2 !important;
        border-left: 4px solid #ef4444 !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #f0f9ff !important;
        border-left: 4px solid #3b82f6 !important;
        color: #1e3a8a !important;
    }
    
    /* Spinner/Loading */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Headers styling */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1e3a8a !important;
    }
    
    /* Columns styling */
    .stColumns {
        gap: 1rem;
    }
    
    /* Divider lines */
    .stMarkdown hr {
        border-color: #3b82f6 !important;
        opacity: 0.3;
    }
    
    /* Make image captions bigger and more prominent - comprehensive targeting */
    .stImage figcaption {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        margin-top: 15px !important;
        text-align: center !important;
        line-height: 1.4 !important;
    }
    
    .stImage div[data-testid="caption"] {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        margin-top: 15px !important;
        text-align: center !important;
        line-height: 1.4 !important;
    }
    
    .stImage > div > div:last-child {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        margin-top: 15px !important;
        text-align: center !important;
        line-height: 1.4 !important;
    }
    
    /* Target any element containing the champion choice text */
    [class*="caption"], [data-testid*="caption"] {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        text-align: center !important;
    }
    
    .action-buttons {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    .secondary-btn {
        background: linear-gradient(135deg, #60a5fa 0%, #93c5fd 100%) !important;
        color: #1e3a8a !important;
        border: 2px solid #1e3a8a !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .restart-btn {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .result-container {
        text-align: center;
        padding: 2rem 1rem;
        background: white;
        border: 3px solid #3b82f6;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
        color: black;
    }
    
    .result-container h2, .result-container p, .result-container em {
        color: black !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 0.5rem;
        }
        .main-header .logo-container {
            flex-direction: column;
            gap: 10px !important;
        }
        .main-header img {
            height: 80px !important;
        }
        .court-container {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .action-buttons {
            flex-direction: column;
            align-items: center;
        }
        .stButton > button {
            width: 100% !important;
            margin: 5px 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def get_available_bags():
    """Get list of available bag files"""
    bag_files = []
    for file in os.listdir('.'):
        if file.endswith('Bag.png'):
            bag_files.append(file)
    return sorted(bag_files)

def load_image_as_base64(image_path):
    """Convert image to base64 for display"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def load_logo_as_base64():
    """Load the Reweave logo as base64"""
    try:
        with open("logo.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        # Return empty string if logo not found
        return ""

def main():
    # ========== HEADER SECTION (Lines 462-474) ==========
    # Header with logo above title - perfectly centered
    st.markdown("""
    <!-- HEADER: Logo and Title Section -->
    <div class="main-header">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 15px; width: 100%;">
            <img src="data:image/png;base64,{}" style="height: 120px; width: auto; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.3);">
            <div style="text-align: center;">
                <h1 style="margin: 0; text-align: center; color: black;">🏓 <span class="pickleball-accent">Reweave</span> - Pickleball Bag Try-On</h1>
            </div>
        </div>
        <p style="text-align: center; margin: 1rem 0;">Step onto the court with style! Upload your photo and try on premium pickleball bags with AI magic!</p>
        <p style="text-align: center; margin: 0;">🎾 Perfect your court look • 👜 Premium bag collection • 🤖 AI-powered fitting</p>
    </div>
    """.format(load_logo_as_base64()), unsafe_allow_html=True)
    
    # Single column layout for smooth flow (like mobile)
    
    # ========== STEP 1: UPLOAD SECTION (Lines 480-500) ==========
    st.header("📸 Step 1: Upload Your Court Photo")
    st.markdown("*Upload a photo of yourself to see how you'd look with our premium pickleball bags!*")
    
    # Check if we should reset the file uploader
    file_uploader_key = "file_uploader"
    if 'reset_triggered' in st.session_state:
        file_uploader_key = f"file_uploader_{st.session_state.get('reset_counter', 0)}"
    
    uploaded_file = st.file_uploader(
        "Choose an image of yourself",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear photo of yourself for the best court-ready results! 🏓",
        key=file_uploader_key
    )
    
    if uploaded_file is not None:
        # Display uploaded image in a centered column
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = Image.open(uploaded_file)
            st.image(image, caption="Ready for the court! 🎾", use_container_width=True)
        
        # Store in session state
        st.session_state['uploaded_image'] = image
        st.session_state['uploaded_file'] = uploaded_file
    
    # ========== STEP 2: BAG SELECTION (Lines 505-535) ==========
    st.header("👜 Step 2: Choose Your Pickleball Bag")
    st.markdown("*Select from our premium collection of pickleball bags designed for champions!*")
    
    # Get available bags
    bags = get_available_bags()
    
    if not bags:
        st.error("No bag files found!")
        return
    
    # Create bag selection with pickleball theme
    selectbox_key = "bag_selector"
    if 'reset_triggered' in st.session_state:
        selectbox_key = f"bag_selector_{st.session_state.get('reset_counter', 0)}"
        
    selected_bag = st.selectbox(
        "Select your champion bag:",
        bags,
        format_func=lambda x: f"🏆 {x.replace('Bag.png', '').replace('Bag', ' Bag')} Collection",
        help="Choose from our exclusive pickleball bag collection! 🎾",
        key=selectbox_key
    )
    
    if selected_bag:
        # Display selected bag preview in a centered column
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            bag_image = Image.open(selected_bag)
            st.image(bag_image, caption=f"🏆 Champion Choice: {selected_bag.replace('Bag.png', '')} Collection", use_container_width=True)
        
        # Store in session state
        st.session_state['selected_bag'] = selected_bag
    
    # Generate button section
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>🎾 Ready to Step onto the Court?</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_clicked = st.button("🏆 Generate Your Champion Look!", key="generate_btn", use_container_width=True)
        
        # Add restart button if image exists - centered layout
        if 'generated_image' in st.session_state or 'uploaded_image' in st.session_state:
            st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
            
            # Center the Start Over button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Start Over", key="restart_btn", use_container_width=True):
                    # Clear all session state
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    # Set reset trigger to force component refresh
                    st.session_state['reset_triggered'] = True
                    st.session_state['reset_counter'] = st.session_state.get('reset_counter', 0) + 1
                    # Force a complete page refresh
                    st.rerun()
            
            # Add regenerate button below if image is generated
            if 'generated_image' in st.session_state:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🎨 Regenerate Image", key="regenerate_btn", use_container_width=True):
                        # Keep the same inputs but regenerate
                        generate_clicked = True
            st.markdown('</div>', unsafe_allow_html=True)
        
        if generate_clicked:
            if 'uploaded_image' not in st.session_state:
                st.error("🏓 Please upload your court photo first!")
            elif 'selected_bag' not in st.session_state:
                st.error("👜 Please select your champion bag first!")
            else:
                # Show loading with pickleball theme
                with st.spinner("🏓 Preparing your champion look... AI is working its magic on the court! 🎾"):
                    try:
                        # Prepare images
                        person_image = st.session_state['uploaded_image']
                        bag_image = Image.open(st.session_state['selected_bag'])
                        logo_image = Image.open('logo.png')
                        
                        # Focused AI prompt with 3 key elements
                        prompt = """CRITICAL: Use the EXACT person from the first image. Do not create a new person.

Create a composition with these 3 elements:
- IMAGE 1 (person): Use this EXACT person - preserve their face, skin tone, hair, body, and clothing completely. This is the main subject.
- IMAGE 2 (bag): Add this handbag to the person from IMAGE 1. The person should hold/wear it naturally.
- IMAGE 3 (logo): Place this logo as a subtle watermark in the top-left corner.

IMPORTANT - BALL SPECIFICATION:
- Use PICKLEBALL balls only - these are plastic balls with holes (like wiffle balls)
- DO NOT use tennis balls (fuzzy, yellow, solid)
- Pickleball balls are typically white or bright colored with circular holes
- They are smaller and lighter than tennis balls
- This is crucial for sport authenticity

Setting: Professional pickleball court with proper pickleball balls scattered in background.
Style: Natural sports photography - person ready to play pickleball with their new bag.

MANDATORY: The person's appearance from IMAGE 1 must remain completely unchanged."""
                        
                        # Call the API
                        response = client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[prompt, person_image, bag_image, logo_image]
                        )
                        
                        # Process response
                        generated_image = None
                        for part in response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                generated_image = Image.open(BytesIO(part.inline_data.data))
                                break
                        
                        if generated_image:
                            st.session_state['generated_image'] = generated_image
                            st.success("🏆 Your champion look is ready! You're court-ready! 🎾")
                        else:
                            st.error("❌ Failed to generate image. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating image: {str(e)}")
    
    # Display generated image
    if 'generated_image' in st.session_state:
        st.markdown("---")
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.header("🏆 Your Champion Court Look!")
        st.markdown("*You're ready to dominate the pickleball court with style!* 🎾")
        
        generated_img = st.session_state['generated_image']
        st.image(generated_img, caption="🏓 Court-ready with your champion bag!", use_container_width=True)
        
        # Download button with pickleball theme
        img_buffer = BytesIO()
        generated_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        st.download_button(
            label="📱 Save Your Champion Look",
            data=img_buffer.getvalue(),
            file_name="pickleball-champion-look.png",
            mime="image/png",
            use_container_width=True,
            help="Download your image to share your court-ready style! 🏆"
        )
        
        st.markdown("### 🎾 Share Your Style!")
        st.markdown("*Show off your champion look with your friends!*")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with blue theme
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #1e3a8a; padding: 2rem;">
        <p><strong>🏓 Reweave - Style with a Serve, Woven for Winners </strong></p>
        <p><strong>Powered by Google Gemini AI • Made with ❤️ for Pickleball Players</strong></p>
        <p><strong>"Step onto the court with confidence!"</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Floating Chat Button - Shieldbase AI Chatbot
    st.markdown("""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
        <a href="https://demo.sbai.cloud/chat/ca61bc90-3fb9-4cde-a7ed-aef28d127c1a" 
           target="_blank" 
           style="display: inline-block; width: 60px; height: 60px; background: #4F00ED; 
                  border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                  color: white; text-decoration: none; box-shadow: 0 4px 12px rgba(79, 0, 237, 0.4);
                  transition: all 0.3s ease; border: none; cursor: pointer;"
           onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 6px 20px rgba(79, 0, 237, 0.6)'"
           onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 12px rgba(79, 0, 237, 0.4)'">
            <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" viewBox="0 0 16 16" fill="white">
                <path d="M8.006 0a8.006 8.006 0 0 0-6.829 3.826 7.995 7.995 0 0 0-.295 7.818l-.804 2.402a1.48 1.48 0 0 0 1.877 1.876l2.403-.8a8.006 8.006 0 0 0 11.42-5.25 7.994 7.994 0 0 0-4.28-9.066A8.007 8.007 0 0 0 8.006 0Zm0 14.22a6.226 6.226 0 0 1-3.116-.836.89.89 0 0 0-.727-.074l-2.207.736.736-2.206a.888.888 0 0 0-.074-.727A6.218 6.218 0 0 1 7.19 1.831a6.227 6.227 0 0 1 6.565 3.784 6.218 6.218 0 0 1-1.96 7.318 6.227 6.227 0 0 1-3.789 1.286Z"></path>
            </svg>
        </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
