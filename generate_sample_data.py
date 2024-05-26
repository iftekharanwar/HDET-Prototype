import pandas as pd
import random
import xml.etree.ElementTree as ET

# Function to generate random IP address
def generate_ip():
    return f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to generate random DHCP options
def generate_dhcp_options():
    options = ["option1", "option2", "option3", "option4", "option5"]
    return random.choice(options)

# Generate sample data
data = []
for i in range(1, 151):
    data.append({
        "id": i,
        "ip_address": generate_ip(),
        "dhcp_options": generate_dhcp_options()
    })

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel file
df.to_excel("sample_data.xlsx", index=False)

# Convert to XML format
root = ET.Element("HardwareData")
for index, row in df.iterrows():
    entry = ET.SubElement(root, "Entry")
    ET.SubElement(entry, "ID").text = str(row["id"])
    ET.SubElement(entry, "IPAddress").text = row["ip_address"]
    ET.SubElement(entry, "DHCPOptions").text = row["dhcp_options"]

# Save to XML file
tree = ET.ElementTree(root)
tree.write("sample_data.xml")

print("Sample data generated successfully: sample_data.xlsx, sample_data.xml")
