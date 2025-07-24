import pandas as pd

EXCEL_PATH = "data/Nanoparticles.xlsx"
df = pd.read_excel(EXCEL_PATH)

def lookup_nanoparticle_technique(user_inputs: dict, client) -> str:
    if not client:
        return "❗ No OpenAI client provided for LLM-based matching."

    rows = []
    for idx, row in df.iterrows():
        entry = {
            "Technique": row.get("Full Form", ""),
            "Abbreviation": row.get("Acronym", ""),
            "Properties": row.get("Properties Measured", ""),
            "Resolution": row.get("Resolution", ""),
            "Sample Preparation": row.get("Sample Preparation", ""),
            "Sample Amount": row.get("Sample Amount (solid)", ""),
            "Sample Volume": row.get("Sample volume (liquid)", ""),
            "Recommended For": row.get("Recommeded for ", ""),
            "Not Recommended For": row.get("Not recommended for ", ""),
            "Cost Effectiveness": row.get("Cost-Effectiveness", ""),
            "Previous Characterizations": row.get("Previous characterisations", "")
        }
        rows.append(entry)

    context_snippets = "\n\n".join(
        f"[{i+1}] {r['Technique']} ({r['Abbreviation']}): Properties: {r['Properties']} | Resolution: {r['Resolution']} | Sample Prep: {r['Sample Preparation']} | Sample Amount: {r['Sample Amount']} | Sample Volume: {r['Sample Volume']} | Recommended: {r['Recommended For']} | Not Recommended: {r['Not Recommended For']} | Cost: {r['Cost Effectiveness']} | Previous: {r['Previous Characterizations']}"
        for i, r in enumerate(rows)
    )[:6000]  # trim for token limits

    user_desc = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in user_inputs.items() if v])

    prompt = f"""
You are a chemistry assistant specializing in nanoparticle characterization. The user needs help selecting the most suitable characterization technique from a nanoparticle database.

Here is the user's input:
{user_desc}

Here are available nanoparticle characterization techniques from the internal database:
{context_snippets}

Pick the single most appropriate technique for nanoparticle analysis. Respond with a clear suggestion and explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a chemistry assistant specializing in nanoparticle characterization techniques."},
            {"role": "user", "content": prompt}
        ]
    )

    return f"🔬 GPT-Based Nanoparticle Recommendation:\n\n{response.choices[0].message.content.strip()}"
