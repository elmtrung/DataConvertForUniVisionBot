import json
import os

def merge_json_files(file_list, output_file):
    merged_data = []

    for file in file_list:
        with open('.//OutPut//Major//'+ file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                merged_data.extend(data)
            else:
                merged_data.append(data)

    with open('.//Merged//' + output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

# Example usage
file_list = ['YDNMajor.json', 'DADMajor.json', 'DDFMajor.json', 'DDKMajor.json', 'DDQMajor.json', 
    'DDTMajor.json', 'DDYMajor.json', 'DSKMajor.json', 'KTDMajor.json', 'TTDMajor.json', 
    'VKUMajor.json', 'XDNMajor.json']
output_file = 'mergedMajor.json'
merge_json_files(file_list, output_file)