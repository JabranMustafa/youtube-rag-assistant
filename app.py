import re
import requests
import streamlit as st

st.set_page_config(page_title="YouTube RAG Assistant", page_icon="🎥", layout="wide")

# -----------------------------
#  N8N WEBHOOK URLS
# -----------------------------
INGEST_WEBHOOK_URL = ""
QA_WEBHOOK_URL = ""


# -----------------------------
# HELPERS
# -----------------------------
def extract_video_id(url: str) -> str | None:
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def reset_chat_state() -> None:
    st.session_state["chat_history"] = []
    st.session_state["selected_question"] = ""


# -----------------------------
# SESSION STATE
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "selected_question" not in st.session_state:
    st.session_state["selected_question"] = ""

if "video_id" not in st.session_state:
    st.session_state["video_id"] = None

if "video_url" not in st.session_state:
    st.session_state["video_url"] = ""

if "session_id" not in st.session_state:
    st.session_state["session_id"] = "user1"

if "summary" not in st.session_state:
    st.session_state["summary"] = ""


# -----------------------------
# UI HEADER
# -----------------------------
st.title("🎥 YouTube RAG Assistant")
st.write("Paste a YouTube link, analyze the video, and ask questions about it.")

# -----------------------------
# INPUTS
# -----------------------------
video_url = st.text_input("YouTube URL", value=st.session_state["video_url"])
session_id = st.text_input("Session ID", value=st.session_state["session_id"])
email = st.text_input("Email for summary (optional)", value="")

col1, col2 = st.columns([1, 1])
with col1:
    send_email = st.checkbox("Send summary by email", value=False)
with col2:
    analyze_clicked = st.button("Analyze Video", use_container_width=True)

# -----------------------------
# ANALYZE VIDEO
# -----------------------------
if analyze_clicked:
    if not video_url.strip():
        st.error("Please enter a YouTube URL.")
    else:
        video_id = extract_video_id(video_url)

        if not video_id:
            st.error("Could not detect a valid YouTube video ID.")
        else:
            output_type = "email" if send_email else "screen"

            payload = {
                "video_url": video_url,
                "output_type": output_type,
                "email": email if send_email else ""
            }

            try:
                with st.spinner("Analyzing video and preparing knowledge base..."):
                    response = requests.post(INGEST_WEBHOOK_URL, json=payload, timeout=240)
                    response.raise_for_status()
                    data = response.json()

                st.session_state["video_id"] = video_id
                st.session_state["video_url"] = video_url
                st.session_state["session_id"] = session_id
                reset_chat_state()

                status = data.get("status", "")
                summary = data.get("summary", "")

                if status == "success":
                    st.success("Video analyzed successfully.")
                    if summary:
                        st.session_state["summary"] = summary
                    else:
                        st.session_state["summary"] = "Video processed successfully, but no summary was returned."

                elif status == "already_processed":
                    st.info("This video was already processed.")
                    st.session_state["summary"] = data.get("message", "This video was already processed.")

                elif status == "no_transcript":
                    st.warning("Transcript not available for this video.")
                    st.session_state["summary"] = data.get("message", "Transcript not available for this video.")

                else:
                    st.warning("Received an unexpected response from n8n.")
                    st.json(data)

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
            except ValueError:
                st.error("The ingestion webhook did not return valid JSON.")

# -----------------------------
# SHOW VIDEO STATUS / SUMMARY
# -----------------------------
if st.session_state["video_id"]:
    st.write("---")
    st.subheader("Current Video")
    st.write(f"**Video ID:** {st.session_state['video_id']}")
    st.write(f"**Session ID:** {st.session_state['session_id']}")

    if st.session_state["summary"]:
        st.write("### Video Summary / Status")
        st.write(st.session_state["summary"])

    # -----------------------------
    # SUGGESTED QUESTIONS
    # -----------------------------
    st.write("### Suggested Questions")

    suggested_questions = [
        "What is this video mainly about?",
        "Explain the key concepts simply.",
        "What are the most important takeaways?",
        "Summarize this video in easy words.",
        "What is the difference between the main ideas in this video?"
    ]

    cols = st.columns(2)
    for i, question in enumerate(suggested_questions):
        with cols[i % 2]:
            if st.button(question, key=f"suggested_{i}"):
                st.session_state["selected_question"] = question

    # -----------------------------
    # ASK QUESTIONS
    # -----------------------------
    st.write("### Ask Questions About the Video")

    user_question = st.text_input(
        "Your question",
        value=st.session_state["selected_question"],
        key="question_input"
    )

    ask_clicked = st.button("Ask Question", use_container_width=True)

    if ask_clicked:
        if not user_question.strip():
            st.error("Please enter a question.")
        else:
            payload = {
                "videoId": st.session_state["video_id"],
                "question": user_question,
                "sessionId": st.session_state["session_id"]
            }

            try:
                with st.spinner("Getting answer from the video..."):
                    response = requests.post(QA_WEBHOOK_URL, json=payload, timeout=240)
                    response.raise_for_status()
                    data = response.json()

                answer = data.get("answer", "No answer returned.")

                st.session_state["chat_history"].append({
                    "role": "user",
                    "content": user_question
                })
                st.session_state["chat_history"].append({
                    "role": "assistant",
                    "content": answer
                })

                st.session_state["selected_question"] = ""

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
            except ValueError:
                st.error("The QA webhook did not return valid JSON.")

    # -----------------------------
    # CHAT DISPLAY
    # -----------------------------
    st.write("### Chat")
    if not st.session_state["chat_history"]:
        st.info("Ask a question to start chatting with the video.")
    else:
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])