from app import create_app
from app.services.nlp_engine import load_hf_model

# -------- CREATE APP --------
app = create_app()

# -------- LOAD MODEL ON STARTUP --------
print("🚀 Loading AI model... (first time may take a few seconds)")
load_hf_model()
print("✅ Model loaded successfully!")

# -------- RUN SERVER --------
if __name__ == "__main__":
    app.run(debug=True)