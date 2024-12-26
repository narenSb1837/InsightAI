import gradio as gr
import requests
import os
import shutil
API_URL = "http://127.0.0.1:8000"

def send_chat(query):
    """
    Sends a POST request to the /chat endpoint with the user's query
    and returns the response.
    """
    endpoint = f"{API_URL}/chat"
    payload = {"question": query}
    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            return response.json().get("answer", "No answer returned.")
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"

def upload_file(file):
    """
    Sends the uploaded file to the /upload-doc endpoint using multipart form data.
    """
    endpoint = f"{API_URL}/upload-doc"
    try:
        with open(file.name, "rb") as f:
            files = {"file": (file.name, f, "application/octet-stream")}
            response = requests.post(endpoint, files=files)
            if response.status_code == 200:
                return response.json().get("message", "File upload response not available.")
            else:
                return f"Error: {response.text}"
    except Exception as e:
        return f"Upload request failed: {str(e)}"

def build_interface():
    """
    Builds the Gradio interface with two main functions:
    1) Chat interface (textbox and output)
    2) File upload (upload component and status message)
    """
    with gr.Blocks() as demo:
        gr.Markdown("# InsightAI")
        with gr.Tab("Chat"):
            chat_input = gr.Textbox(label="Enter your question:")
            chat_output = gr.Textbox(label="AI Response")
            chat_button = gr.Button("Send")
            chat_button.click(fn=send_chat, inputs=chat_input, outputs=chat_output)
        
        with gr.Tab("Upload Document"):
            file_input = gr.File(label="Upload a PDF, DOCX, HTML, or TXT")
            gr.Info("File uploaded sucessfully !!")            
            upload_button = gr.Button("Upload")
            upload_output = gr.Textbox(label="Upload Status")
            upload_button.click(fn=upload_file, inputs=file_input, outputs=upload_output)
            
    return demo

if __name__ == "__main__":
    interface = build_interface()
    interface.launch(share=True)