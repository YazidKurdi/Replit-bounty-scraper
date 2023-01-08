import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from to_csv import csv_to_json

def scrape_bounties():

    # Make a request to the website
    response = requests.get('https://replit.com/bounties?order=creationDateDescending')

    # HTMLFileToBeOpened = open("bounty_html.html", "r")

    # Reading the file and storing in a variable
    # contents = HTMLFileToBeOpened.read()

    # soup = BeautifulSoup(contents, 'html.parser')

    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div that contains the data you want to scrape
    div_matches = soup.find_all(role="article")

    if os.path.exists("bounties.csv"):
        df = pd.read_csv("bounties.csv",index_col=0)
    else:
        df = pd.DataFrame(columns=['price', 'due_days', 'title', 'description', 'author', 'posted_time', 'link'])  # create a new file if it doesn't exist

    for div in div_matches[::-1]:

        price = div.find('span', {'class': 'css-1vcini8'}).text
        due_days = div.find('div', {'class': 'css-1pwjctj'}).find('span').text if div.find('div', {'class': 'css-1pwjctj'}) else 'closed'
        title = div.find('h3').text
        description = div.find('span', {'class': 'css-o4584k'}).text
        author = div.find('a', {'class': 'css-4sa1ap'}).text
        posted_time = div.find_all('span', {'class': 'css-4zs3mz'})[1].text
        link = f"https://replit.com{div.find('a', {'class': 'css-79kc9w'})['href']}"

        # Create a new data frame with the extracted data
        new_row = pd.DataFrame(
            {'price': price, 'due_days': due_days, 'title': title, 'description': description, 'author': author,
             'posted_time': posted_time, 'link': link}, index=[0])

        # new_link = new_row["link"].iloc[0]

        # Append the new row to the data frame using pd.concat
        # df = pd.concat([df, new_row],ignore_index=True)\
        #     .drop_duplicates(subset=["link"],ignore_index=True)

        # Check if the new row is already present in the DataFrame based on the "link" column
        if new_row["link"].isin(df["link"]).any():
        # Update the "due date" and "posted date" columns in the existing DataFrame
            df.loc[df['link'] == link, ['due_days', 'posted_time']] = [due_days,posted_time]
        else:
        #     # Concatenate the new row to the existing DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv('bounties.csv',index = True,index_label="index")
    csv_to_json("bounties.csv","bounties.json")
