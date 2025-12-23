# 🤖 AI Chatbot Mentor

AI Chatbot Mentor is a **domain-specific AI learning assistant** built with Streamlit and LangChain.
It provides **focused mentoring** by answering questions **only within a selected module**, avoiding irrelevant or misleading responses.

---
## AI mentor Application UI
<img width="1419" height="693" alt="ai mentor interface snapshot" src="https://github.com/user-attachments/assets/29e22230-25d3-43e2-9870-f6555e378804" />


## ✨ Features

* 🎯 Module-based AI mentoring
* 🧠 Strict domain restriction
* 💬 Continuous chat experience
* 📥 Download full chat history (.txt)
* 🧼 Simple and clean Streamlit UI

---

## 📚 Supported Modules

* Python
* SQL
* Power BI
* EDA
* Machine Learning
* Deep Learning
* Generative AI
* Agentic AI

---

## ⚠️ Domain Restriction

If a question is unrelated to the selected module, the chatbot replies:

```
Sorry, I don’t know about this question. Please ask something related to the selected module.
```

---

## 🛠 Tech Stack

* Streamlit
* LangChain
* DeepSeek / Hugging Face
* Python

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add your API key in `.env`:

```env
hf=YOUR_HUGGINGFACE_API_KEY
```

---
## Demo Video
### [video](https://youtu.be/v59zJBFJB0Y)
## 🎯 Purpose

This project demonstrates how to build **controlled, reliable AI mentor systems** with real-world features like chat history export and strict domain control.

⭐ *Star the repo if you find it useful!*
