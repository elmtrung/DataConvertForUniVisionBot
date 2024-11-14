import os
import subprocess

# List of file paths to process
file_paths = [
    'YDN.json', 'DAD.json', 'DDF.json', 'DDK.json', 'DDQ.json', 
    'DDT.json', 'DDY.json', 'DSK.json', 'KTD.json', 'TTD.json', 
    'VKU.json', 'XDN.json'
]

# Path to the hyper2.py script
script_path = '.\\data\\hyper2.py'

# Read the content of hyper2.py
with open(script_path, 'r', encoding='utf-8') as file:
    script_content = file.read()

# Iterate over each file path
for file_path in file_paths:
    # Replace the file_path variable in the script content
    modified_script_content = script_content.replace("file_path = 'YDN.json'", f"file_path = '{file_path}'")
    
    # Write the modified script to a temporary file
    temp_script_path = 'temp_hyper2.py'
    with open(temp_script_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(modified_script_content)
    
    # Run the modified script
    subprocess.run(['python', temp_script_path])
    
    # Optionally, remove the temporary script file
    os.remove(temp_script_path)