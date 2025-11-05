import streamlit as st
import requests
import os

# Page configuration
st.set_page_config(page_title="CodeGenius", page_icon="🤖", layout="wide")

# App header
st.title("CodeGenius — Auto Repo Documenter")
st.write("Enter a GitHub repository link to generate AI-powered documentation.")

# Input field
repo_url = st.text_input("🔗 GitHub Repo URL", placeholder="https://github.com/jaseci/jaseci.git")

# Backend endpoint
API_URL = "http://localhost:8000/walker/codegenius_supervisor"

# Generate button
if st.button("Generate Documentation"):
    if not repo_url.strip():
        st.error("Please enter a valid GitHub URL.")
    else:
        st.info("Processing... this may take a few seconds ⏳")
        try:
            # Send request to backend
            res = requests.post(API_URL, json={"repo_url": repo_url}, timeout=50000)
            data = res.json()

            # Handle error from backend
            if "error" in data:
                st.error(data["error"])
            else:
                reports = data.get("reports", [])
                if not reports:
                    st.warning("No report returned by the backend.")
                else:
                    report = reports[0]

                    # Extract stats with fallback
                    total_files = report.get("total_files", 0)
                    sampled_files = report.get("sampled_files", 0)
                    parsed_files = report.get("files_parsed", 0)

                    # Display stats
                    st.success(
                        f"✅ **Repository processed successfully!**\n\n"
                        f"- 🗂️ **Total files detected:** {total_files}\n"
                        f"- 🔍 **Sampled files analyzed:** {sampled_files}\n"
                        f"- 📄 **Files successfully parsed:** {parsed_files}"
                    )

                    # Display markdown info
                    summary_path = report.get("output_md", "")
                    if summary_path:
                        st.write(f"📘 **Markdown generated:** `{summary_path}`")

                    # Display generated markdown content
                    markdown_text = report.get("markdown_text", "")
                    if markdown_text:
                        st.divider()
                        st.markdown("### 📄 Generated Documentation")
                        st.markdown(
                            f"<div style='max-height:600px; overflow:auto; padding:10px; "
                            f"border-radius:8px; background-color:#0e1117'>{markdown_text}</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("No markdown content received.")
        except Exception as e:
            st.error(f"Error: {e}")
