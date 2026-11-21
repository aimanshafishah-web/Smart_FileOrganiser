import os
import shutil
file_types = {
    "Documents": [".pdf", ".docx", ".txt"],
    "Images": [".jpg", ".jpeg", ".png"],
    "Spreadsheets": [".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"]
}
def get_category(file_name):

    extension = os.path.splitext(file_name)[1].lower()

    for category, extensions in file_types.items():

        if extension in extensions:
            return category

    return "Others"
def organise_files(source_folder):

    for file_name in os.listdir(source_folder):

        file_path = os.path.join(source_folder, file_name)

        if os.path.isfile(file_path):

            category = get_category(file_name)

            destination_folder = os.path.join(
                source_folder, category
            )

            os.makedirs(destination_folder, exist_ok=True)

            destination_path = os.path.join(
                destination_folder, file_name
            )

            if os.path.exists(destination_path):
                print(f"Skipped duplicate: {file_name}")
                continue

            shutil.move(file_path, destination_path)

            print(f"Moved {file_name} to {category}")
folder_path = input("Enter folder path: ")

if os.path.isdir(folder_path):

    organise_files(folder_path)

    print("Files organised successfully!")

else:
    print("Invalid folder path!")
