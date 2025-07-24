def get_cot():
    return [
  {
    "key": "particle_type",
    "question": "What type of nanoparticle are you analyzing?",
    "options": ["Metal-based", "Polymer-based", "Biological", "Inorganic non-metallic", "Hybrid/Composite"]
  },
  {
    "key": "matrix_type",
    "question": "What matrix is the nanoparticle in?",
    "options": ["Liquid", "Solid", "Powder", "Gas"]
  },
  {
    "key": "analysis_goal",
    "question": "What is the main analytical goal?",
    "options": [
      "Particle size and distribution",
      "Shape and morphology",
      "Surface chemistry",
      "Elemental composition",
      "Crystallinity",
      "Zeta potential",
      "Stability and agglomeration",
      "Functionalization verification",
      "Optical/electronic properties",
      "Magnetic properties",
      "Surface area and porosity",
      "Contaminant or impurity analysis"
    ]
  },
  {
    "key": "sample_constraints",
    "question": "Are there specific constraints in the sample?",
    "options": ["Low concentration", "Polydisperse sample", "High ionic strength", "Fluorescent labeling", "No constraints"],
    "optional": True
  },
  {
    "key": "measurement_conditions",
    "question": "What are the measurement conditions or requirements?",
    "options": ["Dry state", "In solution", "Real-time monitoring", "Cryogenic conditions", "Ambient conditions"]
  },
  {
    "key": "instrument_access",
    "question": "Which instruments do you have access to?",
    "options": ["DLS", "NTA", "SEM", "TEM", "AFM", "XPS", "XRD", "BET", "FTIR", "Raman", "UV-Vis", "Zeta sizer", "ICP-MS"],
    "optional": True
  }
]