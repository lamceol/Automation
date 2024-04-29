# Script to pull name and email details from an HTML file and save them to a spreadsheet

from bs4 import BeautifulSoup
import pandas as pd

def extract_psychiatrist_details_to_spreadsheet(html_file_path):
    # Load the HTML content from a file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'lxml')

    # List to hold all entries
    entries = []

    # Find all psychiatrist entries based on a common container class or identifier
    psychiatrist_entries = soup.find_all('div', class_='s-psychresults__item')

    # Loop through each entry and extract details
    for entry in psychiatrist_entries:
        name_tag = entry.find('span', class_='s-psychresults__item__name')
        if name_tag:
            full_name = name_tag.get_text(strip=True).split()
            first_name = full_name[1] if len(full_name) > 1 else 'No first name provided'
            last_name = name_tag.find('span', class_='s-psychresults__item__nb-block').get_text(strip=True) if name_tag.find('span') else 'No last name provided'
            email_tag = entry.find('a', href=lambda href: href and "mailto:" in href)
            email = email_tag.get_text(strip=True) if email_tag else 'No email provided'
            entries.append({"First Name": first_name, "Last Name": last_name, "Email": email})

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(entries)
    
    # Save the DataFrame to an Excel file
    df.to_excel("psychiatrists_contact_list.xlsx", index=False)
    
    # Print completion message
    print(f"Total number of psychiatrist entries processed and saved: {len(entries)}")

# Specify the path to your HTML file
html_file_path = 'Results _ Your Health in Mind.html'
extract_psychiatrist_details_to_spreadsheet(html_file_path)
