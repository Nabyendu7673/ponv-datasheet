import streamlit as st
import pandas as pd

st.set_page_config(page_title="PONV Risk Pro Hybrid Scoring Table", layout="wide")

st.title("PONV Risk Pro Hybrid Scoring System Details")

st.write("""
This application displays the detailed breakdown of the Postoperative Nausea and Vomiting (PONV) risk factors and their contribution in the Hybrid Scoring System used by PONV RISK PRO. The table is styled to fit the screen width, with text wrapping in cells. The 'Score Contribution' column is color-coded. Note that Age > 50 now contributes +1 to the score in the scoring logic (not calculated in this display).
""")

# --- Define the Detailed Table Data ---
# Using a list of dictionaries to represent the table rows
table_data = [
    {"Factor": "**Patient Factors**", "Condition/Description": "", "Common in Established Score(s)": "", "Score Contribution (calculate_hybrid_score)": "", "Described Score Range (Sidebar for Drugs)": "", "Mechanism/Rationale (Based on Literature)": ""},
    {"Factor": "Female Gender", "Condition/Description": "Yes (Biological differences influencing neuroendocrine responses)", "Common in Established Score(s)": "Apfel, Koivuranta, Bellville", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Women are consistently found to have a higher incidence of PONV, likely due to hormonal influences on chemoreceptor trigger zone sensitivity."},
    {"Factor": "Non-Smoker", "Condition/Description": "Yes (selected as \"Yes\" in UI) (Lack of chronic nicotine-induced enzyme induction)", "Common in Established Score(s)": "Apfel, Koivuranta", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Non-smokers have a higher risk compared to smokers. Chronic nicotine exposure in smokers may induce hepatic enzymes that accelerate the metabolism of some anesthetic agents, leading to a lower effective dose and reduced emetic stimulation."},
    {"Factor": "History of PONV or Motion Sickness", "Condition/Description": "Yes (Predisposition to emetic stimuli)", "Common in Established Score(s)": "Apfel, Koivuranta, Bellville", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "A personal history of PONV or motion sickness indicates an increased sensitivity to emetic triggers, involving pathways in the vestibular system and central nervous system."},
    {"Factor": "Age", "Condition/Description": "> 50 years", "Common in Established Score(s)": "Bellville, Koivuranta (Age < 50 is lower risk)", "Score Contribution (calculate_hybrid_score)": "+1 (if > 50)", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "While younger age is typically a risk factor, some data suggests altered physiology or reduced sensitivity in older adults, though the specific age cutoff can vary. This model adds a point for age > 50 based on the requested modification."},
    {"Factor": "Preoperative Anxiety", "Condition/Description": "Yes (Psychological factors influencing autonomic nervous system)", "Common in Established Score(s)": "Less common in simplified scores", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "High anxiety levels preoperatively can activate stress responses that may contribute to gastrointestinal upset and increased PONV risk."},
    {"Factor": "History of Migraine", "Condition/Description": "Yes (Association with motion sensitivity and altered neurochemical responses)", "Common in Established Score(s)": "Less common in simplified scores", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Individuals with a history of migraines often have heightened sensitivity to sensory stimuli and altered serotonin pathway activity, which are also involved in the emetic reflex."},
    {"Factor": "Obesity (BMI > 30)", "Condition/Description": "Yes (Potential for altered drug pharmacokinetics and respiratory effects)", "Common in Established Score(s)": "Less common in simplified scores", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Obesity can potentially influence the distribution and metabolism of anesthetic and analgesic drugs, although its direct, independent contribution to PONV is debated in some studies."},
    {"Factor": "**Surgical Factors**", "Condition/Description": "", "Common in Established Score(s)": "", "Score Contribution (calculate_hybrid_score)": "", "Described Score Range (Sidebar for Drugs)": "", "Mechanism/Rationale (Based on Literature)": ""},
    {"Factor": "Abdominal or Laparoscopic Surgery", "Condition/Description": "Yes (Visceral manipulation and peritoneal irritation)", "Common in Established Score(s)": "Some scores include surgery type", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Surgeries involving the abdomen, particularly laparoscopic procedures, are associated with increased PONV risk due to visceral stretch, peritoneal irritation, and insufflation."},
    {"Factor": "ENT/Neurosurgery/Ophthalmic Surgery", "Condition/Description": "Yes (Proximity to cranial nerves and emetic centers)", "Common in Established Score(s)": "Some scores include surgery type", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Procedures in these areas can directly or indirectly stimulate cranial nerves (like the vagus nerve) or affect central emetic pathways, increasing PONV risk."},
    {"Factor": "Gynecological or Breast Surgery", "Condition/Description": "Yes (Potential hormonal influences and surgical site proximity to diaphragm)", "Common in Established Score(s)": "Some scores include surgery type", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "These surgeries, particularly in pre-menopausal women, may involve hormonal factors and surgical manipulation that can contribute to PONV."},
    {"Factor": "Surgery Duration > 60 min", "Condition/Description": "Yes (Increased exposure to anesthetic agents and longer periods of immobility)", "Common in Established Score(s)": "Koivuranta, Bellville", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Longer surgical duration increases cumulative exposure to volatile anesthetics and opioids, and prolonged immobility can also play a role in PONV."},
    {"Factor": "Major Blood Loss > 500 mL", "Condition/Description": "Yes (Physiological stress and potential for hypoperfusion)", "Common in Established Score(s)": "Less common in simplified scores", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Significant blood loss can lead to physiological stress and hypoperfusion, potentially affecting gastrointestinal motility and increasing susceptibility to nausea and vomiting."},
    {"Factor": "**Anesthetic Factors**", "Condition/Description": "", "Common in Established Score(s)": "", "Score Contribution (calculate_hybrid_score)": "", "Described Score Range (Sidebar for Drugs)": "", "Mechanism/Rationale (Based on Literature)": ""},
    {"Factor": "Use of Volatile Agents (Sevo/Iso/Des)", "Condition/Description": "Yes (Direct stimulation of the chemoreceptor trigger zone)", "Common in Established Score(s)": "Bellville", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "0 to +2", "Mechanism/Rationale (Based on Literature)": "Inhalational anesthetics are known to directly stimulate the chemoreceptor trigger zone (CTZ) and are a significant risk factor for PONV."},
    {"Factor": "Use of Nitrous Oxide", "Condition/Description": "Yes (Potential for increased middle ear pressure and synergistic effects)", "Common in Established Score(s)": "Bellville", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "Nitrous oxide can accumulate in closed air spaces, potentially increasing middle ear pressure and stimulating the vestibular system. It may also have synergistic effects with other emetic agents."},
    {"Factor": "Propofol Mode", "Condition/Description": "TIVA (Total Intravenous Anesthesia) (Known antiemetic properties of Propofol)", "Common in Established Score(s)": "Often considered in management", "Score Contribution (calculate_hybrid_score)": "-3", "Described Score Range (Sidebar for Drugs)": "-30 to -3", "Mechanism/Rationale (Based on Literature)": "Propofol has inherent antiemetic properties, likely due to effects on dopaminergic transmission. TIVA with propofol significantly reduces PONV risk compared to volatile anesthetics."},
    {"Factor": "Propofol Mode", "Condition/Description": "Induction Only (Transient antiemetic effect)", "Common in Established Score(s)": "", "Score Contribution (calculate_hybrid_score)": "-1", "Described Score Range (Sidebar for Drugs)": "-10 to -1", "Mechanism/Rationale (Based on Literature)": "A bolus dose for induction provides a transient antiemetic effect, but the continuous infusion in TIVA offers more sustained protection."},
    {"Factor": "Propofol Mode", "Condition/Description": "None (No antiemetic benefit from propofol)", "Common in Established Score(s)": "", "Score Contribution (calculate_hybrid_score)": "0", "Described Score Range (Sidebar for Drugs)": "0", "Mechanism/Rationale (Based on Literature)": "No propofol administration means no contribution from its antiemetic properties."},
    {"Factor": "**Drug Administration (Based on Dose)**", "Condition/Description": "", "Common in Established Score(s)": "", "Score Contribution (calculate_hybrid_score)": "", "Described Score Range (Sidebar for Drugs)": "", "Mechanism/Rationale (Based on Literature)": ""},
    {"Factor": "Midazolam", "Condition/Description": "Dose > 0 mg entered (Anxiolytic and potential mild antiemetic effect)", "Common in Established Score(s)": "Less common in primary scores", "Score Contribution (calculate_hybrid_score)": "-1", "Described Score Range (Sidebar for Drugs)": "0 to -2 (Protective benefit increases with dose)", "Mechanism/Rationale (Based on Literature)": "Benzodiazepines like Midazolam can reduce anxiety, a PONV risk factor, and may have some mild antiemetic properties through central mechanisms."},
    {"Factor": "Ondansetron", "Condition/Description": "Dose >= 4 mg entered (5-HT3 receptor antagonism)", "Common in Established Score(s)": "Used for prophylaxis", "Score Contribution (calculate_hybrid_score)": "-2", "Described Score Range (Sidebar for Drugs)": "0 to -2 (4 mg or higher effective)", "Mechanism/Rationale (Based on Literature)": "Ondansetron is a serotonin 5-HT3 receptor antagonist, blocking serotonin's action in the CTZ and vagal afferents, a key pathway in PONV. Doses of 4 mg or higher are commonly used for prophylaxis."},
    {"Factor": "Dexamethasone", "Condition/Description": "Dose >= 4 mg entered (Anti-inflammatory and central mechanisms)", "Common in Established Score(s)": "Used for prophylaxis", "Score Contribution (calculate_hybrid_score)": "-2", "Described Score Range (Sidebar for Drugs)": "0 to -1 (4 mg or higher useful)", "Mechanism/Rationale (Based on Literature)": "Dexamethasone, a corticosteroid, provides anti-inflammatory effects and may reduce PONV by inhibiting prostaglandin synthesis and influencing opioid receptor sensitivity in the brainstem. Doses >= 4 mg are considered effective."},
    {"Factor": "Glycopyrrolate", "Condition/Description": "Dose > 0 mg entered (Anticholinergic effects)", "Common in Established Score(s)": "Less common as a direct factor", "Score Contribution (calculate_hybrid_score)": "-1", "Described Score Range (Sidebar for Drugs)": "0 to +1 (Increases risk slightly)", "Mechanism/Rationale (Based on Literature)": "An anticholinergic agent, primarily used to reduce salivary secretions and prevent bradycardia. While generally not considered pro-emetic at standard doses, high doses or certain contexts *could* theoretically slow GI motility. This score may reflect a potential minor influence or be part of a combination effect within the model, differing slightly from some classic scores that might assign a positive value."},
    {"Factor": "Nalbuphine", "Condition/Description": "Dose > 0 mg entered (Opioid effects with mixed agonist/antagonist activity)", "Common in Established Score(s)": "Opioid use is a factor", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "0 to +1 (Mild to moderate emetogenicity)", "Mechanism/Rationale (Based on Literature)": "Nalbuphine is an opioid analgesic. Opioids are known to cause nausea and vomiting through stimulation of the CTZ and delayed gastric emptying. As a mixed agonist/antagonist, it may have slightly less emetic potential than pure agonists, but still contributes to risk."},
    {"Factor": "Fentanyl", "Condition/Description": "Dose > 100 mcg entered (Potent opioid effects)", "Common in Established Score(s)": "Opioid use is a factor", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "0 to +3 (Strongest dose-dependent risk)", "Mechanism/Rationale (Based on Literature)": "Fentanyl is a potent opioid agonist and a significant contributor to PONV due to its effects on the CTZ and gastric motility. Higher doses (like > 100 mcg) are associated with a greater risk."},
    {"Factor": "Butorphanol", "Condition/Description": "Dose > 0 mg entered (Opioid effects with mixed agonist/antagonist activity)", "Common in Established Score(s)": "Opioid use is a factor", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "0 to +1 (Partial agonist, less risky)", "Mechanism/Rationale (Based on Literature)": "Similar to Nalbuphine, Butorphanol is an opioid with mixed activity. It contributes to PONV risk through opioid mechanisms but may be less emetogenic than pure agonists."},
    {"Factor": "Pentazocine", "Condition/Description": "Dose > 0 mg entered (Opioid effects with agonist/antagonist activity)", "Common in Established Score(s)": "Opioid use is a factor", "Score Contribution (calculate_hybrid_score)": "+1", "Described Score Range (Sidebar for Drugs)": "0 to +3 (Strongly emetogenic)", "Mechanism/Rationale (Based on Literature)": "Pentazocine is another opioid agonist-antagonist that can cause nausea and vomiting via central and peripheral mechanisms. It is often considered to have a relatively higher emetic potential among this class."},
    {"Factor": "Muscle Relaxant Used", "Condition/Description": "(Any type selected)", "Common in Established Score(s)": "Not a primary factor", "Score Contribution (calculate_hybrid_score)": "Does not contribute to Hybrid Score", "Described Score Range (Sidebar for Drugs)": "N/A", "Mechanism/Rationale (Based on Literature)": "The type of muscle relaxant itself is generally not considered a primary independent risk factor for PONV in most established scoring systems."},
]

# Create a Pandas DataFrame from the data
df = pd.DataFrame(table_data)

# Function to apply color coding based on score contribution
def color_score(val):
    if isinstance(val, str):
        if val.startswith('+'):
            return 'background-color: #ffcccc;' # Light red
        elif val.startswith('-'):
            return 'background-color: #ccffcc;' # Light green
        elif val == "0" or val == "Does not directly contribute to Hybrid Score":
            return 'background-color: #ffffcc;' # Light yellow
    return ''

# Apply the styling to the DataFrame
styled_df = df.style.applymap(color_score, subset=['Score Contribution (calculate_hybrid_score)'])

# Convert the styled DataFrame to HTML
# Add CSS for table layout and text wrapping
html_table = styled_df.to_html(index=False)

# Inject CSS into the HTML
css_style = """
<style>
    table {
        table-layout: fixed; /* Fix table layout */
        width: 100% !important; /* Use full container width */
        border-collapse: collapse; /* Collapse borders */
    }
    th, td {
        padding: 8px;
        border: 1px solid #dddddd;
        text-align: left;
        word-wrap: break-word; /* Break long words */
        overflow-wrap: break-word; /* Modern standard for word wrapping */
    }
    th {
        background-color: #f2f2f2;
    }
    /* Optional: Adjust column widths - percentages should add up to 100% */
    /* You might need to fine-tune these percentages based on content and desired look */
    td:nth-child(1) { width: 15%; } /* Factor */
    td:nth-child(2) { width: 15%; } /* Condition/Description */
    td:nth-child(3) { width: 15%; } /* Common in Established Score(s) */
    td:nth-child(4) { width: 10%; } /* Score Contribution */
    td:nth-child(5) { width: 15%; } /* Described Score Range */
    td:nth-child(6) { width: 30%; } /* Mechanism/Rationale */

    /* Style for the section headers */
    tr:has(> td:first-child > strong) {
        background-color: #e0e0e0 !important; /* Grey background for headers */
        font-weight: bold;
    }
</style>
"""

# Combine CSS and HTML
html_output = css_style + html_table

# Display the HTML table in Streamlit
st.markdown(html_output, unsafe_allow_html=True)

st.write("""
This table provides a detailed overview of the factors considered in the PONV RISK PRO Hybrid Scoring System, referencing their commonality with established scores like Apfel, Koivuranta, and Bellville, and explaining their rationale based on medical literature.
""")
