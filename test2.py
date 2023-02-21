import os

# Folder name
folder_name = r'C:\Users\14088\Videos\ValoClips'

# List to hold the file names
file_names = []

# Loop through the files in the folder
for file_name in os.listdir(folder_name):
    # Check if the file is a regular file (not a directory)
    if os.path.isfile(os.path.join(folder_name, file_name)):
        # Add the file name to the list
        file_names.append(file_name)

# Print the list of file names
print(file_names)