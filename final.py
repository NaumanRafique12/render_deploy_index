import gradio as gr
import os
import os
from dotenv import load_dotenv
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
load_dotenv()



# --- OpenAI Key ---
os.environ["OPENAI_API_KEY"] =os.getenv("OPENAI_API_KEY")
LLAMA_CLOUD_API_KEY =os.getenv("LLAMA_CLOUD_API_KEY")
# --- LlamaCloud Indexes ---
index_1 = LlamaCloudIndex(
    name="pleasant-wombat-2025-06-20",
    project_name="Default",
    organization_id="f667c249-a364-44a4-8ddb-93809edc93fb",
    api_key=LLAMA_CLOUD_API_KEY
)

index_2 = LlamaCloudIndex(
    name="skilled-marten-2025-06-20",
    project_name="Default",
    organization_id="f667c249-a364-44a4-8ddb-93809edc93fb",
    api_key=LLAMA_CLOUD_API_KEY
)

# --- Map index name to object ---
index_map = {
    "Index 1 (pleasant-wombat)": index_1,
    "Index 2 (skilled-marten)": index_2
}

# --- Query Function ---
def answer_query(index_choice, query):
    index = index_map.get(index_choice)
    if not index:
        return "Invalid index selected."
    engine = index.as_query_engine()
    response = engine.query(query)
    return getattr(response, "response", str(response))

# --- Gradio App ---
with gr.Blocks() as app:
    gr.Markdown("### 🔍 LlamaIndex Query Tool (Secure Access)")
    index_choice = gr.Dropdown(choices=list(index_map.keys()), label="Select Index")
    query_input = gr.Textbox(label="Enter your question")
    query_btn = gr.Button("Submit")
    response_output = gr.Textbox(label="Response")

    query_btn.click(fn=answer_query, inputs=[index_choice, query_input], outputs=response_output)

# --- Launch App with Built-in Auth ---
app.launch(
    server_name="0.0.0.0",
    server_port=7860,
    auth=[("admin", "llama2025"), ("hassan", "password321")],
    auth_message="🔐 Access  restricted to authorized users only."
)
