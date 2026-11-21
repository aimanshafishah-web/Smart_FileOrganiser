
import streamlit as st
import os
import io
import zipfile

# Page configuration
st.set_page_config(
    page_title="SORTIFY",
    page_icon="📁",
    layout="wide"
)

# Application heading
st.title("📁 Welcome to SORTIFY")
st.write("Your smart assistant for organising digital files.")
st.sidebar.image("logo.png", width=120)
st.sidebar.title("SORTIFY")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Organise Files", "About", "Help"]
)
st.divider()

# File categories
file_types = {
    "Documents": [".pdf", ".docx", ".txt"],
    "Images": [".jpg", ".jpeg", ".png"],
    "Spreadsheets": [".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"]
}

# Function to identify file category
def get_category(file_name):

    extension = os.path.splitext(file_name)[1].lower()

    for category, extensions in file_types.items():

        if extension in extensions:
            return category

    return "Others"


# Upload files
st.subheader("📤 Upload Your Files")

uploaded_files = st.file_uploader(
    "Choose files",
    accept_multiple_files=True
)

# Process uploaded files
if uploaded_files:

    organised_files = {}

    # Classify uploaded files
    for file in uploaded_files:

        category = get_category(file.name)

        if category not in organised_files:
            organised_files[category] = []

        organised_files[category].append(file)

    # Calculate file counts
    total_files = len(uploaded_files)

    documents = len(organised_files.get("Documents", []))
    images = len(organised_files.get("Images", []))
    spreadsheets = len(organised_files.get("Spreadsheets", []))
    videos = len(organised_files.get("Videos", []))
    audio = len(organised_files.get("Audio", []))
    archives = len(organised_files.get("Archives", []))
    others = len(organised_files.get("Others", []))

    # Display dashboard
    st.divider()
    st.subheader("📊 Your File Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📁 Total Files", total_files)
    col2.metric("📄 Documents", documents)
    col3.metric("🖼️ Images", images)
    col4.metric("📂 Others", others)

    col5, col6, col7 = st.columns(3)

    col5.metric("🎬 Videos", videos)
    col6.metric("🎵 Audio", audio)
    col7.metric("📊 Spreadsheets", spreadsheets)

    st.divider()

    # Display classified files
    st.subheader("📂 Organised Files")

    for category, files in organised_files.items():

        with st.expander(f"{category} ({len(files)} files)"):

            for file in files:
                st.write("📄", file.name)

    # Create ZIP file
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

    # Download button
    st.divider()

    st.download_button(
        label="📦 Download Organised Files",
        data=zip_buffer.getvalue(),
        file_name="SORTIFY_Organised_Files.zip",
        mime="application/zip"
    )

else:

    st.info("Please upload files to start organising!")

 
