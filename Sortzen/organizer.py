import os
import shutil

def organize_files(source_folder):

    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".doc", ".txt"],
        "Videos": [".mp4", ".mkv", ".mov"],
        "Audio": [".mp3", ".wav"],
        "Archives": [".zip", ".rar"],
        "Python Files": [".py"]
    }

    organized_count = 0

    for filename in os.listdir(source_folder):

        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):

            extension = os.path.splitext(filename)[1].lower()

            category = "Others"

            for folder, extensions in file_types.items():
                if extension in extensions:
                    category = folder
                    break

            destination_folder = os.path.join(source_folder, category)

            os.makedirs(destination_folder, exist_ok=True)

            destination_path = os.path.join(destination_folder, filename)

            shutil.move(file_path, destination_path)

            organized_count += 1

    return organized_count