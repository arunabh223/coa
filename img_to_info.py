import base64
from openai import OpenAI
import os
import pandas as pd
import csv
import re
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API key is missing. Please add it to the .env file.")
client = OpenAI(api_key=openai_api_key)

with open("llama/ext_images/page_1.png", "rb") as f:
    bin_content = f.read()

b64_content = base64.b64encode(bin_content).decode()

prompt = "From this image extract the following information - batch no, mfg date. There is a table having headers 'test items', 'standard' and 'test results'. Give me all the information in that table."


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64_content}"
                    },
                },
            ],
        }
    ],
)

identified_item = response.choices[0].message.content
#print(identified_item)

# Extract Batch no and Mfg date
batch_no_match = re.search(r"Batch no: (\w+)", identified_item)
mfg_date_match = re.search(r"Manufacture date: ([\w\-]+)", identified_item)
batch_no = batch_no_match.group(1) if batch_no_match else "N/A"
mfg_date = mfg_date_match.group(1) if mfg_date_match else "N/A"

# Parse the markdown table and convert it to a list of lists
table_lines = identified_item.split('\n')
table_data = []
for line in table_lines:
    if '|' in line:
        table_data.append([cell.strip() for cell in line.split('|') if cell.strip()])

# Extract headers and table data
headers = table_data[0]
table_data = table_data[2:]  # Skip the header and separator lines

# Add Batch no and Mfg date as separate rows
final_data = [
    ["Batch no", batch_no],
    ["Mfg date", mfg_date],
    [],
    headers,
] + table_data

# Save to CSV
csv_file_path = "output.csv"
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in final_data:
        writer.writerow(row)