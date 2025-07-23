from openai import OpenAI
from utils.rag_utils import retrieve_context

def stream_chat_response(client: OpenAI, prompt: str, model: str, box=None, vector_store=None) -> str:
    context = retrieve_context(vector_store, prompt)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant specializing in chemistry characterization. "
                "If the user's query seems relevant to selecting a characterization technique, "
                "and enough information is available (like sample type, molecule type, analysis goals, or constraints), "
                "then include the special token [[CALL_EXCEL]] in your response to trigger a structured internal data lookup. "
                "If the information is not sufficient, ask clarifying questions. Use the provided context to supplement your answer."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {prompt}"
        }
    ]

    full_reply = ""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            full_reply += chunk.choices[0].delta.content

    return full_reply


