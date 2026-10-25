import gradio as gr
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the hidden API key securely
load_dotenv()

# Point the OpenAI library to Groq's servers using your Groq key
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=3"
    response = requests.get(url).json()
    items = response.get("items", [])
    
    results = []
    for item in items:
        info = item.get("volumeInfo", {})
        title = info.get("title", "Unknown Title")
        authors = ", ".join(info.get("authors", ["Unknown Author"]))
        desc = info.get("description", "No description available.")[:400] + "..."
        results.append(f"Title: {title}\nAuthors: {authors}\nDescription: {desc}")
    
    return "\n\n".join(results) if results else "No books found."

def chat_with_agent(user_message, history):
    # Step A: Extract keywords
    search_prompt = [{"role": "system", "content": "Extract 2 to 3 main keywords from the user's research query to search a book database. Reply ONLY with the keywords."}]
    search_prompt.append({"role": "user", "content": user_message})
    
    keyword_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=search_prompt
    )
    keywords = keyword_response.choices[0].message.content
    
    # Step B: Search Google Books
    book_data = search_books(keywords)
    
    # Step C: Synthesize response
    system_msg = """You are an expert architectural research librarian. 
    Recommend the provided books to the user based on their specific query. 
    Write elegantly, using Markdown formatting for readability. Explain exactly why these texts align with their conceptual or spatial research."""
    
    messages = [{"role": "system", "content": system_msg}]
    messages.append({"role": "user", "content": f"My query: {user_message}\n\nFound Books from Database:\n{book_data}"})
    
    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )
    
    return final_response.choices[0].message.content

# Soft, Minimalist Editorial Theme
custom_theme = gr.themes.Soft(
    primary_hue="zinc",
    secondary_hue="stone",
    neutral_hue="stone",
    font=[gr.themes.GoogleFont("Lora"), gr.themes.GoogleFont("Inter"), "sans-serif"]
).set(
    body_background_fill="#FBFBF9",
    block_background_fill="#FFFFFF",
    block_border_width="0px",
    block_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
    button_primary_background_fill="#2C2C2A",
    button_primary_background_fill_hover="#4A4A48",
    button_primary_text_color="#FFFFFF",
    button_secondary_background_fill="#F4F4F0",
    button_secondary_background_fill_hover="#E9E9E5",
    input_background_fill="#F4F4F0",
    input_border_color="#E9E9E5",
    input_border_width="1px",
    input_border_color_focus="#2C2C2A",
)

with gr.Blocks(theme=custom_theme) as demo:
    gr.HTML("""
    <div style="text-align: center; max-width: 700px; margin: 0 auto; padding: 40px 0 20px 0;">
        <h1 style="font-family: 'Lora', serif; font-weight: 400; color: #2C2C2A; font-size: 2.2rem; margin-bottom: 10px;">ArchAgent Librarian</h1>
        <p style="font-family: 'Inter', sans-serif; font-weight: 300; color: #666666; font-size: 1.1rem; line-height: 1.5;">
            An AI-powered architectural research assistant. Ask a conceptual question, and it will curate and synthesize relevant literature.
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.ChatInterface(
                fn=chat_with_agent,
                examples=[
                    "How can I design occupant-centric adaptive building environments?", 
                    "Explore the spatial psychology of enclosed spaces, similar to the dungeons in Le Comte de Monte-Cristo.",
                    "Can you find theoretical texts linking artificial intelligence with Value Sensitive Design?"
                ],
            )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port, css="footer {visibility: hidden;}")