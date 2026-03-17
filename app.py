import streamlit as st
import json
import google.generativeai as genai

# -------------------------------
# 🔑 SET YOUR API KEY HERE
# -------------------------------
GEMINI_API_KEY = "AIzaSyAHB3yeJVUDlaRhwtwmOZ-6gHuvmRnOqQA"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI News Fact Checker (Gemini)",
    page_icon="📰",
    layout="centered"
)

# -------------------------------
# Header
# -------------------------------
st.title("📰 AI News Fact Checker")
st.markdown("### 🔍 Fact Verification using Gemini")

st.write(
    "Enter a news claim or headline. The system will analyze it using Google's Gemini model."
)

st.warning(
    "⚠️ AI predictions may contain errors. Always verify with trusted sources."
)

# -------------------------------
# Input Section
# -------------------------------
st.subheader("✍️ Enter News Claim")

user_input = st.text_area(
    "Type a news claim or headline",
    placeholder="Example: Government bans all petrol cars by 2027"
)

# -------------------------------
# Analyze Button
# -------------------------------
if st.button("Analyze Claim"):

    if user_input.strip() == "":
        st.warning("Please enter a valid claim.")
        st.stop()

    with st.spinner("Analyzing with Gemini..."):

        prompt = f"""
You are a strict AI fact-checking system.

Return ONLY valid JSON. Do NOT include any extra text.

Format:
{{
"verdict": "Likely True" or "Uncertain" or "Likely False",
"confidence": integer between 0 and 100,
"reason": "clear and short explanation",
"sources": ["source1", "source2"]
}}

Claim:
{user_input}
"""

        try:
            response = model.generate_content(prompt)
            result_text = response.text.strip()
        except Exception as e:
            st.error(f"❌ Gemini API Error: {e}")
            st.stop()

    # -------------------------------
    # Output Section
    # -------------------------------
    st.subheader("📊 Fact Check Result")

    with st.expander("🔍 View Raw AI Response"):
        st.code(result_text)

    # -------------------------------
    # Parse JSON safely
    # -------------------------------
    try:
        result = json.loads(result_text)

    except json.JSONDecodeError:
        try:
            start = result_text.find("{")
            end = result_text.rfind("}") + 1
            result = json.loads(result_text[start:end])
        except:
            st.warning("⚠️ Could not parse AI response.")
            st.stop()

    # -------------------------------
    # Extract values
    # -------------------------------
    verdict = str(result.get("verdict", "Uncertain")).strip()
    confidence = int(result.get("confidence", 50))
    reason = result.get("reason", "No explanation provided.")
    sources = result.get("sources", [])

    confidence = max(0, min(100, confidence))

    # -------------------------------
    # Display Results
    # -------------------------------
    st.subheader("📈 Factometer Score")

    st.progress(confidence)
    st.write(f"Confidence: {confidence}%")

    if "False" in verdict:
        st.error("⚠️ This claim is likely FALSE")
    elif "Uncertain" in verdict:
        st.warning("⚠️ The claim is UNCERTAIN")
    else:
        st.success("✅ This claim is likely TRUE")

    st.write("---")

    st.subheader("🧠 Explanation")
    st.write(reason)

    st.subheader("🔗 Suggested Sources")

    if isinstance(sources, list) and sources:
        for src in sources:
            st.write("•", src)
    else:
        st.write("No sources available.")