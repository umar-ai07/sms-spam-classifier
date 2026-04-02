import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.markdown("""
<style>
    /* App Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }

    /* Hide Sidebar for clean look */
    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Main Heading */
    h1 {
        text-align: center;
        color: #00d2ff !important;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
        font-size: 2.8rem !important;
        margin-bottom: -20px !important;
    }

    /* Paragraph Text */
    .stMarkdown p {
        text-align: center;
        color: #a0a0a0 !important;
        font-size: 1.1rem;
    }

    /* Text Area */
    .stTextArea > div > div > textarea {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #0f3460 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        font-size: 18px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stTextArea > div > div > textarea:focus {
        border: 2px solid #00d2ff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
    }
    .stTextArea > div {
        border-radius: 15px !important;
    }

    /* Predict Button */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 20px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 210, 255, 0.6);
        background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    }

    /* Result Header */
    h2 {
        text-align: center !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin-top: 20px !important;
        font-size: 2.5rem !important;
        animation: fadeIn 0.5s ease-in-out;
    }

    /* Spam result styling */
    .spam-result {
        background-color: rgba(255, 77, 77, 0.1) !important;
        border: 2px solid #ff4d4d !important;
        color: #ff4d4d !important;
        text-shadow: 0 0 10px rgba(255, 77, 77, 0.5);
    }

    /* Ham result styling */
    .ham-result {
        background-color: rgba(40, 167, 69, 0.1) !important;
        border: 2px solid #28a745 !important;
        color: #28a745 !important;
        text-shadow: 0 0 10px rgba(40, 167, 69, 0.5);
    }

    /* Warning Box */
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid #ffc107 !important;
        border-radius: 10px !important;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Hide Streamlit branding */
    footer, header, #MainMenu {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# --- Frontend Layout ---

st.markdown("<h1>🛡️ SMS Spam Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p>Paste your message below and the AI will detect whether it is <b>Spam</b> or <b>Safe</b>.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input Area
input_sms = st.text_area(
    "📨 **Enter the message**",
    height=180,
    placeholder="e.g: Congratulations! You have won a $1000 Walmart gift card. Call now..."
)

if st.button(' Predict'):

    if input_sms.strip() == "":
        st.warning(" Please enter a message first. The text area is empty.")
    else:
        # 1. preprocess
        transformed_sms = transform_text(input_sms)
        # 2. vectorize
        vector_input = tfidf.transform([transformed_sms])
        # 3. predict
        result = model.predict(vector_input)[0]
        
        # 4. Display result
        if result == 1:
            st.markdown("<h2 class='spam-result'>🚨 Spam Message!</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #ff8a8a;'>Do not trust this message. It appears to be spam.</p>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 class='ham-result'> Not Spam (Safe)</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #7ddf93;'>This message looks safe. You can interact with it.</p>", unsafe_allow_html=True)
 
