import pandas as pd
from pymongo import MongoClient
import json

# Connect to MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the database and collections
db = client['UniVisionBot']
Uni = db['University']

# Create a Pandas Excel writer using openpyxl as the engine
with pd.ExcelWriter('universities.xlsx', engine='openpyxl') as writer:
    # Find and process all universities
    universities = Uni.find({}, {'university_code': 1, 'name': 1, '_id': 0})
    for university in universities:
        university_code = university['university_code']
        university_name = university['name']
        
        # Open and process the JSON file
        with open(f'.\\data\\source\\{university_code}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            major_raw = []
            for item in data:
                result_item = {
                    "Tên ngành": item['Tên ngành'],
                    "Tổ hợp môn": item.get('Tổ hợp môn', ''),
                    "Điểm chuẩn": item.get('Điểm chuẩn', ''),
                    "major_code": item.get('Mã ngành', '')
                }
                major_raw.append(result_item)
        
        # Convert the processed data to a DataFrame
        df = pd.DataFrame(major_raw)
        
        # Write the DataFrame to an Excel sheet
        df.to_excel(writer, sheet_name=university_name, index=False)

print("Data exported to universities.xlsx")