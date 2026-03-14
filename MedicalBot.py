import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 1. Setup Gemini 2.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key="AIzaSyAzsuPv9EPNmBIUvD2aPQj7_IBXZX69FvY", 
    temperature=0.2
)

# 2. Medical System Prompt
system_prompt = SystemMessage(
    content="""
You are a responsible medical assistant.
Rules:
- Provide general medical information only.
- Do NOT diagnose.
- Do NOT prescribe medication.
- Suggest consulting a licensed doctor.
- If symptoms are serious, advise immediate medical help.
"""
)

def predict(message, history):
    # Always start with the system prompt
    messages = [system_prompt]
    
    # 3. New Gradio Memory Logic (Dictionary format)
    # We want the last 4 messages (2 full turns)
    # Gradio 6.x history: [{"role": "user", "content": "hello"}, ...]
    last_messages = history[-4:] if len(history) > 0 else []
    
    for msg in last_messages:
        role = msg.get("role")
        content = msg.get("content")
        
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
    
    # Add the current user query
    messages.append(HumanMessage(content=message))
    
    # 4. Generate Response
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Medical AI Error: {str(e)}"

# 5. Gradio Interface (NO 'type' or 'theme' keywords here)
demo = gr.ChatInterface(
    fn=predict,
    title="⚕️ Medical Assistant AI",
    description="I am a Gemini-powered medical info bot. I do not provide diagnoses.",
    examples=["Symptoms of flu?", "Treating a minor scrape"],
)

if __name__ == "__main__":
    # Apply theme during launch
    demo.launch(theme="soft")