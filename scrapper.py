import requests
from bs4 import BeautifulSoup
import mysql.connector

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'scrapper'
}

# Create a connection to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heading TEXT,
    description TEXT,
    link TEXT
)
""")

# Send a request to the BBC News website
bbc_r1 = requests.get('https://www.bbc.com/')
coverpage_bbc = bbc_r1.content

# Parse the content with BeautifulSoup
soup_bbc = BeautifulSoup(coverpage_bbc, 'html5lib')

# Find all news cards
news_cards = soup_bbc.findAll('div', {"data-testid": "card-text-wrapper"})

# Iterate through each card and extract the heading, description, and link
for card in news_cards:
    heading_tag = card.find('h2', {"data-testid": "card-headline"})
    description_tag = card.find('p', {"data-testid": "card-description"})
    link_tag = card.find_parent('a', {"data-testid": "internal-link"})
    
    # Extract text and href attribute
    heading = heading_tag.get_text() if heading_tag else 'No heading'
    description = description_tag.get_text() if description_tag else 'No description'
    link = 'https://www.bbc.com' + link_tag['href'] if link_tag else 'No link'
    
    # Print the extracted information
    print(f"Heading: {heading}")
    print(f"Description: {description}")
    print(f"Link: {link}")
    print("-" * 80)
    
    # Insert data into MySQL table
    cursor.execute("""
        INSERT INTO news (heading, description, link)
        VALUES (%s, %s, %s)
    """, (heading, description, link))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
