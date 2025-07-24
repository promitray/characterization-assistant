import streamlit as st
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from utils.pdf_loader import extract_text_from_pdfs
from utils.rag_utils import build_vector_store, retrieve_context
from utils.chat import stream_chat_response
from utils.excel_lookup import lookup_technique
from utils.cot_logic import get_cot

import json

st.set_page_config(page_title="Chemistry Characterization Assistant", layout="wide")

# Sidebar - API key and model selection
st.sidebar.title("OpenAI Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
model = st.sidebar.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"])

# PDF upload
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs to inform the assistant", type=["pdf"], accept_multiple_files=True
)

# OpenAI client
client = OpenAI(api_key=api_key) if api_key else None

# Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant specializing in chemistry characterization."}
    ]
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "clarification_count" not in st.session_state:
    st.session_state.clarification_count = 0
if "last_cot" not in st.session_state:
    st.session_state.last_cot = {}
if "last_excel_result" not in st.session_state:
    st.session_state.last_excel_result = ""
if "last_rendered_index" not in st.session_state:
    st.session_state.last_rendered_index = 0

# Process uploaded PDFs
if uploaded_files and api_key:
    with st.spinner("Processing uploaded PDFs..."):
        try:
            full_text = extract_text_from_pdfs(uploaded_files)
            st.session_state.vector_store = build_vector_store(full_text, api_key)
            st.success(f"Uploaded and indexed {len(uploaded_files)} PDF(s).")
        except Exception as e:
            st.error(f"Error processing PDFs: {e}")

st.title("Chemistry Characterization Assistant")

# Render all past messages
for i, msg in enumerate(st.session_state.messages[1:], start=1):
    if i <= st.session_state.last_rendered_index:
        st.chat_message(msg["role"]).write(msg["content"])

# Main chat input
if prompt := st.chat_input("Tell me your characterization needs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not client:
        st.warning("Please enter your OpenAI API key.")
    else:
        try:
            full_reply = stream_chat_response(client, prompt, model, None, st.session_state.vector_store)

            if "[[CALL_EXCEL]]" in full_reply:
                st.write("📊 Looking up internal data store...")

                convo = "\n".join([m["content"] for m in st.session_state.messages if m["role"] != "system"])
                cot_keys = ', '.join([step['key'] for step in get_cot()])

                valid_values = {
                    "sample_type": ["Organic", "Inorganic"],
                    "organic_type": ["Small molecule", "Polymer"],
                    "chirality": ["Chiral", "Achiral"],
                    "analysis_purpose": [
                        "Molar mass measurement", "Functional group analysis", "Absorption behaviour",
                        "Separation and quantification", "Structure elucidation", "Quality control and assurance",
                        "Regulatory compliance and safety", "Water content determination", "Elemental analysis",
                        "Thermodynamic analysis", "Configuration analysis", "Chiral separation"
                    ],
                    "sample_constraints": [
                        "Low sample amount", "Solid", "Liquid", "Solubility issues", "No constraints"
                    ]
                }

                extraction_prompt = (
    f"You are an expert assistant helping a chemist match user inputs to known database categories.\n"
    f"The known categories are:\n\n{json.dumps(valid_values, indent=2)}\n\n"
    f"Your task is to extract and normalize values from the conversation. Normalize values so they match the closest valid values listed above.\n"
    f"For example, if the user says 'organic', choose between 'Small molecule' or 'Polymer' depending on the context.\n"
    f"Return a JSON object with those keys. Use null if no good match is found."
                                    )


                extract_resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": extraction_prompt},
                        {"role": "user", "content": convo}
                    ]
                )

                structured_data = json.loads(extract_resp.choices[0].message.content)
                for k in ["sample_type", "organic_type", "chirality"]:
                    if isinstance(structured_data.get(k), list):
                        structured_data[k] = structured_data[k][0]

                st.session_state.last_cot = structured_data
                st.write("🧪 Normalized CoT Data:", structured_data)

                required_fields = ["sample_type", "organic_type", "analysis_purpose"]
                missing_fields = [k for k in required_fields if not structured_data.get(k)]

                if missing_fields and st.session_state.clarification_count < 1:
                    clarification_prompt = (
                        f"To help you better, could you please provide: {', '.join(missing_fields)}?"
                    )
                    st.session_state.messages.append({"role": "assistant", "content": clarification_prompt})
                    with st.chat_message("assistant"):
                        st.markdown(clarification_prompt)
                    st.session_state.clarification_count += 1
                    st.stop()

                st.session_state.clarification_count = 0

                reco = lookup_technique(structured_data, client)
                st.session_state.last_excel_result = reco
                if st.session_state.vector_store:
                 rag_info = retrieve_context(st.session_state.vector_store, prompt)
                else:
                 rag_info = "_No uploaded documents to reference._"

                cot_explained = "\n".join(
                    [f"- **{k.replace('_',' ').title()}**: {v}" for k, v in structured_data.items() if v]
                )

                final_reply = (
                    f"🧠 **Chain of Thought Analysis:**\n\n{cot_explained}\n\n"
                    f"{reco}\n\n"
                    f"📚 **Insights from uploaded literature:**\n{rag_info}"
                )

                cleaned_final = final_reply.replace("[[CALL_EXCEL]]", "").strip()
                st.session_state.messages.append({"role": "assistant", "content": cleaned_final})
                with st.chat_message("assistant"):
                    st.markdown(cleaned_final)

            elif any(q in prompt.lower() for q in ["why", "explain"]):
                if st.session_state.last_excel_result:
                    explanation_prompt = (
                        f"Please explain this recommendation clearly and logically.\n\n"
                        f"Extracted Parameters:\n{json.dumps(st.session_state.last_cot, indent=2)}\n\n"
                        f"Excel Recommendation:\n{st.session_state.last_excel_result}"
                    )
                    followup = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are a chemistry assistant explaining your reasoning."},
                            {"role": "user", "content": explanation_prompt}
                        ]
                    )
                    explanation = followup.choices[0].message.content.strip()
                    st.session_state.messages.append({"role": "assistant", "content": explanation})
                    with st.chat_message("assistant"):
                        st.markdown(explanation)
                else:
                    st.session_state.messages.append({"role": "assistant", "content": full_reply})
                    with st.chat_message("assistant"):
                        st.markdown(full_reply)

            else:
                cleaned_reply = full_reply.replace("[[CALL_EXCEL]]", "").strip()
                st.session_state.messages.append({"role": "assistant", "content": cleaned_reply})
                with st.chat_message("assistant"):
                    st.markdown(cleaned_reply)

            st.session_state.last_rendered_index = len(st.session_state.messages)

        except Exception as e:
            st.error(f"OpenAI API error: {e}")


