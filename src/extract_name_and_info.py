from bs4 import BeautifulSoup
import csv

# Path to your file
file_path = '../confidential_files/people_dir_html.txt'

# Read the HTML content from the file
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all person details wrappers
people = soup.find_all("div", class_="oist-pl-teaser__wrapper oist-pl-department__teaser__wrapper")

# Prepare a list to hold the extracted information
members_info = []

# Iterate through each person and extract the relevant information
for person in people:
    name = person.find("div", class_="oist-pl-department__person-name-en")
    
    # Correcting the email extraction by specifically looking for the mailto link
    email_link = person.find("a", href=lambda href: href and "mailto:" in href)
    
    # Extracting the position name
    position = person.find("div", class_="oist-pl-department__position__name-en")
    if position is None:
        position_text = ""  # In case there is no position found
    else:
        position_text = position.text.strip()
    
    if name and email_link:
        # Extract the text for the name and the email address from the 'href' attribute
        member_name = name.text.strip()
        member_email = email_link['href'].replace("mailto:", "").strip()
        
        # Add the extracted information to our list (now including the position)
        members_info.append((member_name, member_email, position_text))

# Specify the file you want to write to
output_file_path = '../confidential_files/members_info.csv'

# Writing to the CSV file
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(['Name', 'Email', 'Position'])
    # Write the member information
    for member in members_info:
        writer.writerow(member)

print(f"Information successfully saved to {output_file_path}.")
