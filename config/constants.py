# ─────────────────────────────────────────────
# config/constants.py
# All static data: languages, suggestions, topics, placeholders
# ─────────────────────────────────────────────

LANGUAGES = {
    "English": {"code": "en", "flag": "🇬🇧", "tts": "en-IN"},
    "हिंदी":   {"code": "hi", "flag": "🇮🇳", "tts": "hi-IN"},
}

PLACEHOLDERS = {
    "English": "यहाँ अपना प्रश्न लिखें…  /  Type your question here…",
    "हिंदी":   "यहाँ अपना प्रश्न लिखें…",
}

SUGGESTIONS = [
    "🌾 What are the main systems of farming?",
    "💧 what is irrigation management in fall irrigation ?",
    "🐛 How to control pest in wheat crop?",
    "🌱 What are organic farming techniques?",
]

TOPICS = [
    ("🌾", "फसल प्रबंधन एवं उत्पादन"),# different ways to dispose of straw   पुआल को ठिकाने लगाने के तरीके
    ("💧", "सिंचाई एवं जल प्रबंधन"),   
    ("🐛", "कीट एवं रोग नियंत्रण"),#The diseases of bees and their treatments
    ("🌱", "जैविक खेती"),
    ("🧪", "मृदा स्वास्थ्य एवं उर्वरक"),
    ("🌿", "पर्यावरण एवं प्रकृति"),
    ("🐄", "पशुपालन एवं डेयरी"),
    ("🔬", "कृषि प्रौद्योगिकी"),
    ("📊", "कृषि अर्थशास्त्र"),
    ("🏛️", "सरकारी योजनाएँ एवं सब्सिडी"),#government schemes and subsidies
    ("🌦️", "मौसम एवं जलवायु"),
    ("🌾", "परंपरागत सिंचाई प्रणाली"),
]

LOGO_FILENAME = "Pantnagar_logo.jpg"

PAGE_CONFIG = {
    "page_title": "Agriculture Chatbot — GB Pant University, Pantnagar",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}