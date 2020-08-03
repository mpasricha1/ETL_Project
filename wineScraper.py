from splinter import Browser 
from bs4 import BeautifulSoup 
import pandas as pd

# Create browser object for navigating through pages
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://www.winespectator.com/vintage-charts/region/united-states"
browser.visit(url)

# Create a soup object for the first page
html = browser.html 
soup = BeautifulSoup(html, "html.parser")

# Find each link on the page
wineTypes = soup.find_all("h3", class_="m-0")

wineList = []

for wine in range(len(wineTypes)):
# Click the button
	browser.find_by_css("h3.m-0 a")[wine].click()

# Create a new a new soup object for the new page 
	html = browser.html 
	soup = BeautifulSoup(html, "html.parser")

# Find the wine type for the current page
	header = soup.find("div", class_="md:text-lg")
	
# This section contains two loops the outer loop controls looping through each table row
# The inner loop controls looping through each column of each row 
# The if in the innner loop checks for duplicate description rows and skips if found
# 	by checking for an h5 tag with class mt-0 d-md-none
# Each row a dictionary is created and the header for each column is used as the key 

	for row in soup.select("tbody tr"):
		wineDict = {}
		hText = header.h1.find(text=True, recursive=False)
		wineDict["type"] = hText
		for col in row.select("td[valign=top]"):
			if col.find("h5", class_="mt-0 d-md-none"):
				pass
			else:
				key = col.find("h5").text
				try:
					if col.find(text=True, recursive=False) == None:
						if col.find("a"): 
							value = col.find("a").text
							wineDict[f"{key}"] = value
						else:
							value = col.find("span").text
							wineDict[f"{key}"] = value
					else:
						value = col.find(text=True, recursive=False)
						wineDict[f"{key}"] = value
				except: 
					print("skipping")
			wineList.append(wineDict)

	browser.back()

# Create DataFrame and export to csv
browser.quit()
wine_df = pd.DataFrame(wineList)
wine_df.to_csv("wine_data.csv")
print(wine_df)
