def get_cot():
    return [
        {"key": "sample_type", "question": "What kind of material do you want to analyze?", "options": ["Organic", "Inorganic"]},
        {"key": "organic_type", "question": "Is the organic material a small molecule or a polymer?", "options": ["Small molecule", "Polymer"], "depends_on": {"sample_type": "Organic"}},
        {"key": "chirality", "question": "Is the molecule chiral or achiral?", "options": ["Chiral", "Achiral"], "depends_on": {"organic_type": "Small molecule"}},
        {"key": "analysis_purpose", "question": "What is the main purpose of your analysis?", "options": ["Molar mass measurement", "Functional group analysis", "Absorption behaviour", "Separation and quantification", "Structure elucidation", "Quality control and assurance", "Regulatory compliance and safety", "Water content determination", "Elemental analysis", "Thermodynamic analysis", "Configuration analysis", "Chiral separation"]},
        {"key": "sample_constraints", "question": "Are there any constraints related to the sample?", "options": ["Low sample amount", "Solid", "Liquid", "Solubility issues", "No constraints"], "optional": True}
    ]