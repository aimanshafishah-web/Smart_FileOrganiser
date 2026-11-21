
import streamlit as st
import os
import io
import zipfile
st.title("📁 Welcome to SORTIFY")

st.write("Your smart assistant for organising digital files.")

# Page settings
st.set_page_config(
    page_title="Smart File Organiser",
    page_icon="📁",
    layout="wide"
)

# Title
st.title("📁 Smart File Organiser")

st.write(
    "Organise your files automatically into categories "
    "and download them in one ZIP folder."
)

st.divider()

# File categories
file_types = {
    "📄Documents": [".pdf", ".docx", ".txt"],
    "🖼️ Images": [".jpg", ".jpeg", ".png"],
    "Spreadsheets": [".xlsx", ".csv"],
    " 🎬Videos": [".mp4", ".mkv"],
    " 🎵 Audio": [".mp3", ".wav"],
    "📦Archives": [".zip", ".rar"]
}

# Function to identify category
def get_category(file_name):

    extension = os.path.splitext(file_name)[1].lower()

    for category, extensions in file_types.items():

        if extension in extensions:
            return category

    return "Others"


# File uploader
st.subheader("📤 Upload your files")

uploaded_files = st.file_uploader(
    "Choose files to organise",
    accept_multiple_files=True
)

if uploaded_files:

    organised_files = {}

    # Classify files
    for file in uploaded_files:

        category = get_category(file.name)

        if category not in organised_files:
            organised_files[category] = []

        organised_files[category].append(file)

    st.success("Your files have been classified!")

    # Display results
    st.subheader("📊 Organisation Summary")

    cols = st.columns(3)

    total_files = len(uploaded_files)

    for index, (category, files) in enumerate(
        organised_files.items()
    ):

        with cols[index % 3]:

            st.metric(
                label=f"📂 {category}",
                value=len(files)
            )

    st.write(f"**Total files uploaded: {total_files}**")

    # Create ZIP file in memory
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
        zip_buffer, "w", zipfile.ZIP_DEFLATED
    ) as zip_file:

        for category, files in organised_files.items():

            for file in files:

                zip_file.writestr(
                    f"{category}/{file.name}",
                    file.getvalue()
                )

    zip_buffer.seek(0)

    st.divider()

    st.subheader("⬇️ Download organised files")

    st.download_button(
        label="📦 Download Organised ZIP",
        data=zip_buffer.getvalue(),
        file_name="Organised_Files.zip",
        mime="application/zip"
    )

else:

    st.info("Upload your files to get started!")
 
