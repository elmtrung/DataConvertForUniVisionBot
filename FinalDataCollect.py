import json
import random
import string
import os
import binascii
from datetime import datetime
from fuzzywuzzy import fuzz
import re

# Đọc nội dung từ file
file_path = 'YDN.json'
file_name = os.path.splitext(os.path.basename(file_path))[0]
with open('.\\Data\\source\\' + file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
with open('.\\Data\\source\\' + file_name + '2.json', 'r', encoding='utf-8') as file2:
    data2 = json.load(file2)
with open('\\Data\\source\\Major\\nganh.json', 'r', encoding='utf-8') as nganh_file:
    nganh_data = json.load(nganh_file)

# Tạo danh sách để lưu trữ kết quả tìm kiếm
major_list_raw = []
not_found = []

# Hàm loại bỏ nội dung trong dấu ngoặc đơn
def remove_parentheses_content(s):
    return re.sub(r'\(.*?\)', '', s).strip()
# Hàm chuyển đổi chuỗi thành 24 ký tự
def encode_to_24_chars(input_string):
    # Chuyển đổi chuỗi thành bytes
    input_string = input_string + file_name
    clean_str = input_string.replace('.', '0')
    byte_string = clean_str.encode('utf-8')
    # Sử dụng binascii.hexlify để chuyển đổi bytes thành chuỗi hex
    hex_string = binascii.hexlify(byte_string).decode('utf-8')
    # Đảm bảo chuỗi hex có độ dài 24 ký tự
    if len(hex_string) < 24:
        hex_string = hex_string.ljust(24, '0')
    elif len(hex_string) > 24:
        hex_string = hex_string[:24]
    return hex_string

# Hàm chuyển đổi chuỗi thành mảng
def convert_string_to_array(input_string):
    # Sử dụng phương thức split để tách chuỗi thành các phần tử dựa trên dấu ;
    array = [item.strip() for item in input_string.split(';')]
    return array

# Duyệt qua từng ngành trong DTT.json
for item in data:
    name = item['Tên ngành']
    found = False
    # Duyệt qua từng ngành con trong nganh.json
    for nganh_item in nganh_data:
        for sub_major in nganh_item['sub_majors']:
            # Sử dụng fuzzywuzzy để tìm kiếm giá trị gần giống
            if fuzz.ratio(sub_major['name'], remove_parentheses_content(name)) > 80:
                result_item = {
                    "DDT_name": name,
                    "Major_id": sub_major['id'],
                    "Major_name": sub_major['name'],
                    "Faculty_id": nganh_item['id'],
                    "Faculty_name": nganh_item['name'],
                    "subject_combinations": item.get('Tổ hợp môn', ''),
                    "entry_score_record": item.get('Điểm chuẩn', ''),
                    "notes": item.get('Ghi chú', ''),
                    "major_code": item.get('Mã ngành', '')
                }
                for ddt2_item in data2:
                    if fuzz.ratio(ddt2_item['Tên ngành'], name) > 80:
                        result_item["entry_score_exam"] = ddt2_item.get('Điểm chuẩn', '')
                        break
                    else:
                        result_item["entry_score_exam"] = ''
                major_list_raw.append(result_item)
                found = True
                break
        if found:
            break
    if not found:
        not_found.append(name)
# In ra cac ngành không tìm thấy
print(file_name)
print("Các ngành không tìm thấy:")


for name in not_found:
    print(name)
# Tạo tập hợp để lưu trữ các Faculty_id và Faculty_name duy nhất
faculty_set = set()

# Duyệt qua từng mục trong major_list_raw
for item in major_list_raw:
    faculty_id = item['Faculty_id']
    faculty_name = item['Faculty_name']
    faculty_set.add((faculty_id, faculty_name))

# Chuyển tập hợp thành danh sách
faculty_list_raw = [{"Faculty_id": fid, "Faculty_name": fname} for fid, fname in faculty_set]

# Sắp xếp danh sách theo Faculty_id
faculty_list_raw = sorted(faculty_list_raw, key=lambda x: x['Faculty_id'])

# Tạo danh sách để lưu trữ kết quả
faculty_list = []

uni_id = encode_to_24_chars(file_name)
# Duyệt qua từng mục trong kq2.json và mã hóa Faculty_id
for faculty in faculty_list_raw:
    encoded_faculty_id = encode_to_24_chars(faculty['Faculty_id'])
    new_faculty = {
        "_id": {
            "$oid": encoded_faculty_id
        },
        "university_id": {
            "$oid": uni_id  # Example university_id, replace with actual data
        },
        "name": faculty['Faculty_name'],
        "created_at": {
            "$date": "2023-01-01T00:00:00.000Z"
        }
    }
    faculty_list.append(new_faculty)

# Ghi danh sách đã mã hóa vào file
output_file = file_name + 'Faculty.json'
with open('.\\Data\\OutPut\\Faculty\\' + output_file, 'w', encoding='utf-8') as kq2_encoded_file:
    json.dump(faculty_list, kq2_encoded_file, ensure_ascii=False, indent=4)


major_list = []

# Duyệt qua từng mục trong kq1.json và chuyển đổi sang định dạng mới
for item in major_list_raw:
    Major_id = encode_to_24_chars(item["Major_id"])
    Faculty_id = encode_to_24_chars(item["Faculty_id"])
    major = {
         "_id": {
            "$oid": Major_id
        },
        "faculty_id": {
            "$oid": Faculty_id
        },
        "career_ids": 
            {
                "$oid": "64b7f9a2f9a2a7b1c7b8b8b5"  # Example career ID, replace with actual data
            },
        "name": item["Major_name"],
        "description": "",  # Example description, replace with actual data
        "level": "Bachelor's",  # Example level, replace with actual data
        "duration": 4,  # Example duration, replace with actual data
        "major_code": item["major_code"],  # Example major code, replace with actual data
        "subject_combinations": convert_string_to_array(item["subject_combinations"]),
        "entry_score_exam": {
            "2024": item["entry_score_exam"],  # Example score, replace with actual data
        },
        "entry_score_record": {
            "2024": item["entry_score_record"]
        },
        "tuition_fee": 3200,  # Example tuition fee, replace with actual data
        "notes": item["notes"],  # Example notes, replace with actual data
        "created_at": {
            "$date": datetime.now().isoformat() + "Z"
        }
    }
    major_list.append(major)

# Ghi kết quả vào file Major.json
output_file = file_name + 'Major.json'
with open('.\\Data\\OutPut\\Major\\' +output_file, 'w', encoding='utf-8') as major_file:
    json.dump(major_list, major_file, ensure_ascii=False, indent=4)
