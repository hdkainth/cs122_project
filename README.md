# CS 122 Project
Project Title: SJSU Parking Tracker

Authors: Hardeep Kainth, Ynha Nguyen

# Project Description
- For our project, we will create a parking tracker for the four parking garages at San Jose State University. Utilizing SJSU’s parking tracker website, which contains information about each garage’s percentage capacity (sjsuparkingstatus.sjsu.edu), we will be able to scrape the data at every refresh. Over time, as more data is gathered, we will be able to visualize trends across times of day and days of the week to come to conclusions on the activity of parking garages and what times are best for each garage to find parking. This project will be created primarily through Python, and the GUI will be created using Python’s Tkinter library. 

# Project Outline and Plan

## Interface Plan
- For our interface, we will be using a GUI using Python’s Tkinter library. Our home screen will include various widgets, including 3 buttons for fetching data, viewing the data analysis, and visualizing the data. The data can be viewed through another pop up window. We will also include a drop down window to filter through specific parking garages and time ranges.

## Data Collection and Storage Plan
- Data Collection: Our data will be collected using two Python libraries, “requests” and “BeautifulSoup.” The requests library will send a ping to the website to gather the information, and BeautifulSoup will be used as an HTML parser to find our desired numbers and write them as a file.

- Data Storage: Our data will be stored using .csv files gathered from the aforementioned HTML parsing. CSV files are extremely useful and versatile, as they can be used in conjunction with libraries like NumPy or Pandas to generate tables, which can be used with modules like Matplotlib to easily generate graphical representations of our data.

## Data Analysis and Visualization Plan
- Data Analysis: To analyze our data, we will calculate trends using Python’s Pandas library. Because this library is ideal for handling data in CSV files, we can use Pandas to read through our data and analyze it by calculating various statistics, such as parking availability averages and trends throughout the day. Pandas also works well with Matplotlib which will make visualizing and plotting our data more efficient.

- Data Visualization: Our visualization component will plot the data for parking availability depending on the time and parking garage. Using Matplotlib, we will make a times series plot to visualize parking availability throughout the day and a bar chart to visualize the parking availability based on each garage.  
