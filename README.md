# 🏛️ ArchAgent Librarian

An AI-powered architectural research assistant and literature curation tool. Designed for architectural theorists, researchers, and designers to query complex spatial concepts and dynamically synthesize academic literature.

## 🌟 Key Features
* **Autonomous Agent Architecture:** Uses the OpenAI library connected to high-speed Groq open-source models (`openai/gpt-oss-20b`) to extract search intent and synthesize research findings.
* **External API Integration:** Programmatically queries the **Google Books API** in real time to fetch relevant theoretical texts and publications.
* **Minimalist Editorial UI:** Built with **Gradio**, featuring a custom soft duotone theme (`Lora` and `Inter` typography, warm off-white palette) tailored for design professionals.
* **Secure Environment Management:** Implements strict secret handling via `.env` and `.gitignore`.

## 🛠️ Tech Stack
* **Language:** Python
* **UI Framework:** Gradio (v6.0+)
* **AI Engine:** Groq API (via OpenAI client compatibility layer)
* **Data Source:** Google Books REST API

## 🚀 Getting Started Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/bessaihadjer-jpg/arch-agent-librarian.git](https://github.com/bessaihadjer-jpg/arch-agent-librarian.git)
   cd arch-agent-librarian