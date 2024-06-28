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

with open("/Users/arunabhbora/Downloads/Code/coa/ext_images/page_1.png", "rb") as f:
    bin_content = f.read()

b64_content = base64.b64encode(bin_content).decode()

prompt = "From this image extract the following information - product name, product batch number. There is a table below analysis results having headers 'Item(s)', 'Method(s)', 'Result(s)' and 'Limit'. Give me all the information in that table."


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
print(identified_item)

#Showing this result in the form of a table

# Extract Batch no and Mfg date
product_name_match = re.search(r".*Product Name (\w+)", identified_item)
batch_no_match = re.search(r".*Manufacture date: ([\w\-]+)", identified_item)
name = product_name_match.group(1) if product_name_match else "N/A"
batch_no = batch_no_match.group(1) if batch_no_match else "N/A"

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
    ["Product name", name],
    ["Batch no", batch_no],
    [],
    headers,
] + table_data

# Save to CSV
csv_file_path = "output.csv"
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in final_data:
        writer.writerow(row)

