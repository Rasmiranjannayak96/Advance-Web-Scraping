'''Imports: We import necessary libraries, including selenium for web scraping and time for handling delays.

Setting up WebDriver: The Chrome WebDriver is initialized using the path to chromedriver.exe, which allows Selenium to control the Chrome browser.'''

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Initialize the Chrome WebDriver with the path to the chromedriver executable
s = Service('C:/Users/RasmiranjanN/OneDrive - Kensium Solutions Pvt Ltd/Desktop/Serp Scraping/chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Open the Flipkart mobiles page
driver.get('https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&page=2')

# Function to extract the HTML source code of the mobile phones container on the current page
def html_source():
    # Locate the container element that holds the mobile phones data
    phone_container = driver.find_element(By.CSS_SELECTOR, "#container > div > div.nt6sNV.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div:nth-child(2)")
    
    # Get the outer HTML of the located container element
    container_html = phone_container.get_attribute('outerHTML')
    
    # Save the extracted HTML source code to a file named 'Flipcart.html'
    # The file is opened in append mode ('a') so that new data is added at the end of the file
    with open('Flipcart.html', 'a', encoding='utf-8') as f:
        f.write(container_html + '\n')
    
    return container_html  # Return the HTML for further processing

# Start from the first page
page_number = 1

# Initialize empty lists to store the extracted data
name = []
price = []
rating = []
memory = []
display = []
camera = []
battery = []
processor = []
warranty = []

# Loop through all pages to extract the HTML source and data
while True:
    # Call the function to extract and save the HTML source code
    html = html_source()
    
    # Parse the saved HTML file with BeautifulSoup using the 'lxml' parser
    soup = BeautifulSoup(html, 'lxml')
    
    # Find all containers that hold individual phone details based on the CSS class
    containers = soup.find_all('div', {'class': 'tUxRFH'})

    # Loop through each container to extract the relevant data
    for i in containers:
        # Find all the list items within the container's unordered list (ul) with the class 'G4BRas'
        x = i.find('ul', {'class': 'G4BRas'}).find_all('li')
        
        # Try to extract the phone name and append it to the 'name' list; if not found, append NaN
        try:
            name.append(i.find('div', {'class': 'KzDlHZ'}).text)
        except:
            name.append(np.nan)
        
        # Try to extract the phone price and append it to the 'price' list; if not found, append NaN
        try:
            price.append(i.find('div', {'class': 'Nx9bqj _4b5DiR'}).text)
        except:
            price.append(np.nan)
        
        # Try to extract the phone rating and append it to the 'rating' list; if not found, append NaN
        try:
            rating.append(i.find('div', {'class': 'XQDdHH'}).text)
        except:
            rating.append(np.nan)
        
        # Try to extract the phone memory details from the first list item and append to 'memory' list; if not found, append NaN
        try:
            memory.append(x[0].text)
        except:
            memory.append(np.nan)
        
        # Try to extract the phone display details from the second list item and append to 'display' list; if not found, append NaN
        try:
            display.append(x[1].text)
        except:
            display.append(np.nan)
        
        # Try to extract the phone camera details from the third list item and append to 'camera' list; if not found, append NaN
        try:
            camera.append(x[2].text)
        except:
            camera.append(np.nan)
        
        # Try to extract the phone battery details from the fourth list item and append to 'battery' list; if not found, append NaN
        try:
            battery.append(x[3].text)
        except:
            battery.append(np.nan)
        
        # Try to extract the phone processor details from the fifth list item and append to 'processor' list; if not found, append NaN
        try:
            processor.append(x[4].text)
        except:
            processor.append(np.nan)
        
        # Try to extract the phone warranty details from the sixth list item and append to 'warranty' list; if not found, append NaN
        try:
            warranty.append(x[5].text)
        except:
            warranty.append(np.nan)
    
    # Try to locate the "Next" button to go to the next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a:nth-child(12)")
        
        # Click the "Next" button to navigate to the next page
        next_button.click()
        
        # Increment the page number
        page_number += 1
        
        # Pause for 5 seconds to allow the next page to load completely
        time.sleep(5)
    
    except:
        # If the "Next" button is not found (e.g., end of pages), break the loop
        break

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame({
    'Brand': name,
    'Price': price,
    'Rating': rating,
    'Memory': memory,
    'Display': display,
    'Camera': camera,
    'Battery': battery,
    'Processor': processor,
    'Warranty': warranty
})

# Optional: Save the DataFrame to a CSV file for further analysis or sharing
df.to_csv('Flipkart_Mobiles.csv', index=False)

