import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(table):
    """
    Scrape data from a single table and return a DataFrame.

    Parameters:
    table (BeautifulSoup): The BeautifulSoup object representing the table.

    Returns:
    pandas.DataFrame: A DataFrame containing the scraped data.
    """
    # Initialize lists to store data
    polish_names = []
    latin_names = []

    # Collecting data
    for row in table.tbody.find_all('tr')[1:]:
        # Find all data for each column
        columns = row.find_all('td')

        if len(columns) >= 2:  # Ensure there are at least two columns
            polish_name = columns[0].text.strip()
            latin_name = columns[1].text.strip()

            polish_names.append(polish_name)
            latin_names.append(latin_name)

    # Create a DataFrame
    birds_df = pd.DataFrame({"Polish Name": polish_names, "Latin Name": latin_names})
    return birds_df

def scrape_multiple_tables(url):
    """
    Scrape data from multiple tables on a webpage and return a combined DataFrame.

    Parameters:
    url (str): The URL of the webpage containing the tables.

    Returns:
    pandas.DataFrame: A DataFrame containing the scraped data from all tables.
    """
    data = requests.get(url).text  # send a GET request to fetch the page content
    soup = BeautifulSoup(data, "html.parser")  # parse the HTML content using BeautifulSoup

    # Find all tables of the desired class
    tables = soup.find_all('table', class_='wikitable')

    all_birds_df = pd.DataFrame()  # Initialize DataFrame to store all scraped data

    # Scrape data from each table and concatenate DataFrames
    for table in tables:
        birds_df = scrape_table(table)
        all_birds_df = pd.concat([all_birds_df, birds_df], ignore_index=True)

    return all_birds_df

if __name__ == "__main__":
    url = "https://pl.wikipedia.org/wiki/Ptaki_Polski"
    birds_data = scrape_multiple_tables(url)

    # Export DataFrame to a text file without header and index
    with open("lista_ptakow_polski.txt", "w", encoding="utf-8") as file:
        for index, row in birds_data.iterrows():
            file.write(f"{row['Polish Name']} ({row['Latin Name']})\n")

    # Export DataFrame to a CSV file
    # birds_data.to_csv("birds.csv", index=False, encoding="utf-8")

    # print("Data exported to birds.csv successfully.")

    print("Data exported to lista_ptakow_polski.txt successfully.")
