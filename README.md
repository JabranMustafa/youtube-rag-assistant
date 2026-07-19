# 🎥 YouTube RAG Assistant

An AI-powered application that automatically extracts YouTube transcripts, generates intelligent summaries, and enables semantic question answering using Retrieval-Augmented Generation (RAG).

Built with FastAPI, OpenAI GPT-4o, OpenAI Embeddings, Pinecone, Streamlit, and n8n, this project demonstrates end-to-end AI workflow automation, vector search, and modern LLM application development.

---

## ✨ Features

- 📺 Extract transcripts from YouTube videos
- 🧠 Generate AI-powered video summaries using OpenAI GPT-4o
- ✂️ Automatically split long transcripts into manageable chunks
- 🔍 Semantic search using OpenAI Embeddings and Pinecone
- 💬 Ask questions about any processed video using RAG
- ⚡ Workflow automation with n8n
- 🌐 REST APIs built with FastAPI
- 🖥️ Interactive frontend built with Streamlit
- 📧 Optional email delivery of generated summaries

---

## 🏗️ Architecture

```text
                User
                  │
                  ▼
             Streamlit UI
                  │
                  ▼
             n8n Webhook
                  │
     ┌────────────┴────────────┐
     │                         │
     ▼                         ▼
FastAPI Transcript API    AI Processing
                               │
                               ▼
                  Transcript Chunking
                               │
                               ▼
                  OpenAI Embeddings
                               │
                               ▼
                    Pinecone Vector DB
                               │
                               ▼
                     OpenAI GPT-4o
                               │
                               ▼
                  Summary / RAG Answer
                               │
                               ▼
                Google Sheets / Email
```

---

# 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Python

### AI & LLM
- OpenAI GPT-4o
- OpenAI Embeddings
- Retrieval-Augmented Generation (RAG)

### Workflow Automation
- n8n

### Vector Database
- Pinecone

### Storage
- Google Sheets

---

# 🚀 How It Works

1. The user enters a YouTube video URL.
2. FastAPI retrieves the transcript.
3. n8n orchestrates the complete workflow.
4. The transcript is split into smaller chunks.
5. Each chunk is summarized using OpenAI GPT-4o.
6. Chunk summaries are combined into a final structured summary.
7. Transcript chunks are embedded using OpenAI Embeddings and stored in Pinecone.
8. Users can ask questions about the processed video using Retrieval-Augmented Generation (RAG).
9. The generated summary can be stored in Google Sheets or delivered via email.

---



# 📂 Project Structure

```text
youtube-rag-assistant/
│
├── backend/
│   ├── app.py
│   ├── transcript.py
│   ├── requirements.txt
│
├── frontend/
│   ├── app.py
│
├── n8n/
│   └── workflow.json
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── .env.example
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/JabranMustafa/youtube-rag-assistant.git
cd youtube-rag-assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the FastAPI backend

```bash
uvicorn app:app --reload
```

Run the Streamlit application

```bash
streamlit run app.py
```

Start n8n and import the provided workflow.

---

# 🔐 Environment Variables

Create a `.env` file.

```text
OPENAI_API_KEY=your_api_key
PINECONE_API_KEY=your_api_key
PINECONE_INDEX=your_index_name
TRANSCRIPT_API=http://localhost:8000
```

---

# 🔮 Future Improvements

- Multi-language transcript support
- PDF and Markdown export
- Docker deployment
- Cloud deployment
- Authentication and user accounts
- Batch video processing
- Support for additional LLM providers

---

# 👨‍💻 Author

**Hasnain Shafiq**

M.Sc. Artificial Intelligence  
Brandenburg University of Technology Cottbus–Senftenberg

- LinkedIn: https://www.linkedin.com/in/https://www.linkedin.com/in/jabran-mustafa-80443a245 
- GitHub: https://github.com/https://github.com/JabranMustafa
