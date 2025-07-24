def get_cot():
    return [
  {
    "key": "sample_state",
    "question": "Is the sample solid, liquid, or gas?",
    "options": ["Solid", "Liquid", "Gas"]
  },
  {
    "key": "sample_amount",
    "question": "What is the amount of sample available?",
    "options": ["<1 mg", "1–10 mg", ">10 mg"]
  },
  {
    "key": "sample_stability",
    "question": "Is the sample stable under light, air, or heat?",
    "options": ["Yes", "No"]
  },
  {
    "key": "sample_type",
    "question": "What kind of material do you want to analyze?",
    "options": ["Organic material", "Inorganic material"]
  },
  {
    "key": "organic_type",
    "question": "Is the organic material a small molecule or a polymer?",
    "options": ["Small molecule", "Polymer"],
    "depends_on": {
      "sample_type": "Organic material"
    }
  },
  {
    "key": "chirality",
    "question": "Is the compound chiral?",
    "options": ["Chiral", "Achiral"],
    "depends_on": {
      "organic_type": "Small molecule"
    }
  },
  {
    "key": "analysis_goal",
    "question": "What is the primary analysis goal?",
    "options": [
      "Structural identification",
      "Composition",
      "Impurity/purity check",
      "Mechanical/thermal behavior",
      "Regulatory compliance"
    ]
  },
  {
    "key": "analysis_purpose",
    "question": "What do you want to analyze?",
    "options": [
      "Molar mass measurement",
      "Functional group analysis",
      "Absorption behaviour",
      "Separation and quantification",
      "Structure elucidation",
      "Product safety/reliability/responsibility",
      "Regulatory and safety compliance",
      "Water content determination",
      "Elemental analysis",
      "Thermodynamic/thermal analysis",
      "Crystallizing density",
      "Mechanical properties",
      "Configuration analysis",
      "Chiral separation"
    ]
  }
]
