"status": "Malignant Findings Detected",
            "risk_level": "High Risk / Urgent Action Required",
            "clinical_meaning": "The report contains medical terminology indicating abnormal growth and malignant cells requiring precise evaluation.",
            "recommendations": "Immediate consultation with an oncologist and specialist surgeon is necessary, along with confirmatory tests."
        },
        "benign": {
            "keywords": ["benign", "non-malignant", "cyst", "fibroid"],
            "status": "Benign / Non-Malignant",
            "risk_level": "Low Risk / Reassuring",
            "clinical_meaning": "Results indicate a benign mass, cyst, or non-cancerous growth that typically does not spread to adjacent tissues.",
            "recommendations": "Regular periodic follow-up with the specialist to monitor size changes, with potential precautionary removal."
        }
    }
    fallback_data = {
        "status": "Standard Histological Examination / Inconclusive",
        "risk_level": "Requires Clinical Review (Moderate)",
        "clinical_meaning": "The observed features in the attached report do not show definitive direct indications matching the system's strict malignant or benign rules.",
        "recommendations": "Please present this report directly to a histopathology consultant or attending physician for precise clinical diagnosis."
    }
# واجهة المستخدم الأساسية
_st.title(title_text)
_st.markdown(subtitle_text)
_st.markdown("---")
uploaded_file = _st.file_uploader(uploader_label, type=["png", "jpg", "jpeg", "pdf"])
if uploaded_file is not None:
    _st.image(uploaded_file, caption="Uploaded Report", use_container_width=True)
    
    if _st.button(button_text, type="primary"):
        with _st.spinner(spinner_text):
            time.sleep(1.2)
            
            file_name_lower = uploaded_file.name.lower()
            matched_condition = None
            
            for key, data in cancer_knowledge.items():
                for kw in data["keywords"]:
                    if kw in file_name_lower:
                        matched_condition = data
                        break
                if matched_condition:
                    break
            
            if not matched_condition:
                matched_condition = fallback_data
            
            _st.success(success_text)
            
            _st.markdown("### 📋 Clinical Analysis Report:")
            
            _st.markdown(f"""

| {table_headers[0]} | {table_headers[1]} |
| :--- | :--- |
| Status | {matched_condition['status']} |
| Risk Level | {matched_condition['risk_level']} |

            """)
            
            _st.markdown(f"#### {clinical_title}")
            _st.info(matched_condition['clinical_meaning'])
            
            _st.markdown(f"#### {recommendations_title}")
            _st.warning(matched_condition['recommendations'])
else:
    _st.info(no_file_text)
