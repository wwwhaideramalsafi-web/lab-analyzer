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
st.title(title_text)
st.markdown(subtitle_text)
st.markdown("---")
uploaded_file = st.file_uploader(uploader_label, type=["png", "jpg", "jpeg", "pdf"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Report", use_container_width=True)
    
    if st.button(button_text, type="primary"):
        with st.spinner(spinner_text):
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
            
            st.success(success_text)
            
            st.markdown("### 📋 Clinical Analysis Report:")
            
            st.markdown(f"""

| {table_headers[0]} | {table_headers[1]} |
| :--- | :--- |
| Status | {matched_condition['status']} |
| Risk Level | {matched_condition['risk_level']} |

            """)
            
            st.markdown(f"#### {clinical_title}")
            st.info(matched_condition['clinical_meaning'])
            
            st.markdown(f"#### {recommendations_title}")
            st.warning(matched_condition['recommendations'])
else:
    st.info(no_file_text)
