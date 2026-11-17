import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="AdAlert – Misleading Advertisement Chatbot",
    page_icon="🛡️",
    layout="centered",
)

MANUAL = """
1. Introduction
Advertising is a marketing technique used by businesses to promote products and services. However, some companies use false claims, exaggerated promises or hidden information to influence consumers. Such advertisements may be misleading and can harm consumers.

2. Meaning of Misleading Advertisement
A misleading advertisement is promotional content that gives false, deceptive or incomplete information about a product or service and may influence consumers' purchasing decisions.
Example: An advertisement promising guaranteed weight loss of 10 kg in 15 days without exercise or dieting.

3. Types of Misleading Advertisements
1. False Product Claims: Incorrect information about product quality or features.
2. Health Claims: Unsupported medical or weight-loss promises.
3. Beauty Claims: Unrealistic skincare and cosmetic results.
4. Fake Discounts: Artificially inflated original prices.
5. Hidden Charges: Concealing compulsory fees and conditions.
6. Influencer Advertising: Undisclosed paid promotions.
7. Bait Advertising: Attracting customers with offers that cannot reasonably be fulfilled.
8. Greenwashing: False environmental-friendly claims.
9. Educational Claims: Misleading placement and success-rate promises.
10. Celebrity Endorsements: Unsupported or deceptive product recommendations.

4. Important Indian Laws
- Consumer Protection Act, 2019: Protects consumer rights.
- Section 2(28): Defines misleading advertisements.
- Section 2(47): Defines unfair trade practices.
- Section 18: Powers and functions of CCPA.
- Section 21: Directions and penalties.
- Section 89: Punishment for certain false or misleading advertisements.
- CCPA Guidelines, 2022: Regulates misleading advertisements and endorsements.
- Greenwashing Guidelines, 2024: Regulates misleading environmental claims.
- Coaching Guidelines, 2024: Addresses misleading coaching advertisements.
- ASCI Code: Advertising and influencer standards.

5. Consumer Rights
Consumers have six important rights:
- Right to Safety
- Right to Information
- Right to Choose
- Right to Be Heard
- Right to Seek Redressal
- Right to Consumer Awareness

6. Penalties
Under Section 21 of the Consumer Protection Act, 2019:
- First contravention: Penalty up to ₹10 lakh.
- Subsequent contravention: Penalty up to ₹50 lakh.
- Endorsement restrictions may also apply.
Under Section 89, certain offences involving false or misleading advertisements prejudicial to consumers can attract imprisonment and fines.

7. Complaint Platforms
- National Consumer Helpline: 1915
- Website: https://consumerhelpline.gov.in/
- CCPA: https://www.ccpa.gov.in/
- Consumer Commission Portal: https://e-jagriti.gov.in/
- ASCI: https://www.ascionline.in/

8. Main Features of AdAlert Chatbot
1. Advertisement Claim Analyzer
2. Misleading Advertisement Detector
3. Indian Advertising Laws Information
4. Influencer Advertisement Checker
5. Consumer Complaint Guidance
6. Legal Question and Answer System

9. Technology Required
- Python: Programming
- Streamlit: Chatbot interface
- NLP: Understand user queries
- Machine Learning: Classify advertisement types
- RAG: Retrieve information from legal documents
- CSV / Excel: Store knowledge and training data

10. Knowledge Database
The chatbot knowledge base has four main datasets:
1. Legal Knowledge: Indian laws, sections and guidelines.
2. Advertisement Classification: Different types of misleading advertisements.
3. Question & Answer Database: Common consumer questions and answers.
4. Complaint Guidance: Reporting procedures and official links.
"""

SYSTEM_INSTRUCTION = """
You are AdAlert, an educational chatbot that helps users understand potentially
misleading advertisements and consumer-protection information in India.

Rules:
- Answer using the supplied knowledge manual as your primary source.
- Explain concepts in simple, clear language and give practical examples where useful.
- When a user shares an advertisement or claim, identify possible red flags and explain
  what evidence would be needed. Do not declare a company or person guilty based only
  on an allegation or a short description.
- Distinguish between information explicitly stated in the manual and general guidance.
  Never invent legal sections, penalties, deadlines, procedures, or official links.
- For legal questions, provide general educational information, not legal advice.
  Encourage users to verify current rules with the relevant official authority or a
  qualified professional.
- For complaints, guide users to the official channels listed in the manual. Do not
  claim to file a complaint on the user's behalf.
- If the manual does not contain enough information, say so clearly and suggest an
  appropriate official source to check.
- Be respectful, neutral, concise, and avoid making unsupported assumptions.
"""

def get_api_key():
    """Read the Gemini key from Streamlit's secrets.toml."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None

st.title("🛡️ AdAlert")
st.caption("Knowledge-based chatbot for misleading advertisements and consumer awareness in India")
st.info(
    "Ask about misleading advertising, consumer rights, Indian advertising laws, "
    "influencer disclosures, or how to report a concern."
)

api_key = get_api_key()
if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
    st.error(
        "Gemini API key not configured. Add your key to "
        "`.streamlit/secrets.toml` as shown in the README, then restart the app."
    )
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as exc:
    st.error(f"Could not initialize the Gemini client: {exc}")
    st.stop()

model_name = st.sidebar.text_input(
    "Gemini model",
    value=st.secrets.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    help="Change this if the model configured for your Gemini API account is different.",
)
st.sidebar.markdown("---")
st.sidebar.markdown("**About AdAlert**")
st.sidebar.write("This chatbot provides educational guidance based on the knowledge manual included with the app.")
if st.sidebar.button("Clear chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask AdAlert a question...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AdAlert is preparing an answer..."):
            try:
                # Include recent conversation so follow-up questions have context.
                history = st.session_state.messages[-12:]
                conversation = "\n\n".join(
                    f'{item["role"].upper()}: {item["content"]}' for item in history
                )
                response = client.models.generate_content(
                    model=model_name,
                    contents=(
                        "KNOWLEDGE MANUAL:\n"
                        + MANUAL
                        + "\n\nCONVERSATION:\n"
                        + conversation
                        + "\n\nRespond to the latest user message."
                    ),
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.3,
                    ),
                )
                answer = response.text or "I couldn't generate a text response. Please try again."
            except Exception as exc:
                answer = (
                    "Sorry, I couldn't get a response from Gemini. "
                    "Check your API key, model name, and internet connection.\n\n"
                    f"Technical detail: `{exc}`"
                )
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
