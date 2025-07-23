import pandas as pd

EXCEL_PATH = "data/Small_Mol_Polymers.xlsx"
df = pd.read_excel(EXCEL_PATH)

def lookup_technique(user_inputs: dict, client) -> str:
    if not client:
        return "❗ No OpenAI client provided for LLM-based matching."

    # Reduce the Excel to relevant text entries for the model
    rows = []
    for idx, row in df.iterrows():
        entry = {
            "Technique": row.get("Technique", ""),
            "Abbreviation": row.get("Abbreviation", ""),
            "Main Use": row.get("Main Use", ""),
            "Sample Type": row.get("Sample Type", ""),
            "Sample Requirements": ", ".join(
                [str(row[col]) for col in df.columns if col.startswith("Sample Requirements") and pd.notna(row[col])]
            )
        }
        rows.append(entry)

    context_snippets = "\n\n".join(
        f"[{i+1}] {r['Technique']} ({r['Abbreviation']}): {r['Main Use']} | {r['Sample Type']} | Requirements: {r['Sample Requirements']}"
        for i, r in enumerate(rows)
    )[:6000]  # trim for token limits

    user_desc = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in user_inputs.items() if v])

    prompt = f"""
You are a chemistry assistant. The user needs help selecting the most suitable characterization technique from a database.

Here is the user's input:
{user_desc}

Here are available techniques from the internal database:
{context_snippets}

Pick the single most appropriate technique. Respond with a clear suggestion and explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a chemistry assistant selecting the best technique from a database."},
            {"role": "user", "content": prompt}
        ]
    )

    return f"🔬 GPT-Based Recommendation:\n\n{response.choices[0].message.content.strip()}"




