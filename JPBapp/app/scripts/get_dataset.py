import zipfile
import os

def zip_folder(folder_path, output_zip_path):
    # Create a ZIP file for writing
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all the files and subdirectories in the folder
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add the file to the ZIP archive with a relative path
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

def get_dataset_zip():
    folder_to_zip = os.getcwd()+'/app/scripts/data'
    output_zip_file = os.getcwd()+'/app/scripts/data.zip'
    zip_folder(folder_to_zip, output_zip_file)

    return '/static/scripts/data.zip'