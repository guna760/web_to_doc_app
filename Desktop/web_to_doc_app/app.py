import streamlit as st
from scraper import fetch_website_content
from doc_generator import create_docx, create_pdf

st.set_page_config(page_title="Web To Document Converter", page_icon="📄", layout="centered")

st.title("🌐 URL to Document Converter")
st.write("Input any website URL below to automatically scrape its text content and convert it into a Word or PDF file instantly.")

url = st.text_input("Enter Website URL:", placeholder="https://gunadhar.com")
file_format = st.radio("Select Output Format:", ("Word Document (.docx)", "PDF Document (.pdf)"))

if st.button("Extract and Prepare File"):
    if not url:
        st.warning("Please enter a valid URL first!")
    elif not (url.startswith("http://") or url.startswith("https://")):
        st.error("Please enter a complete URL starting with http:// or https://")
    else:
        with st.spinner("Connecting and downloading content..."):
            result = fetch_website_content(url)
            
        if "error" in result:
            st.error(result['error'])
        else:
            st.success(f"Successfully processed: '{result['title']}'!")
            
            with st.expander("Preview Extracted Snippets"):
                for item in result['content'][:5]:
                    if item['type'] == 'text':
                        st.write(f"- {item['value']}")
                    elif item['type'] == 'image':
                        st.caption("📷 [Image Object Located]")
                        
                if len(result['content']) > 5:
                    st.write("...and more lines extracted below.")

            if file_format == "Word Document (.docx)":
                file_data = create_docx(result)
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                file_ext = "docx"
            else:
                file_data = create_pdf(result)
                mime_type = "application/pdf"
                file_ext = "pdf"
                
            st.download_button(
                label=f"📥 Download .{file_ext} File",
                data=file_data,
                file_name=f"scraped_website.{file_ext}",
                mime=mime_type
            )