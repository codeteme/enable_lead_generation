# Scrape website https://www.talabat.com/qatar/restaurants
# and save data to csv file

from bs4 import BeautifulSoup
import requests
import csv
import time
import pandas as pd


# Define a function tha scrape data from website
def talabat_scrape_data(url: str):
    """
    Get the name and the tags of all restaurants in Talabat's website
    Args: url (str): url of the website to scrape
    Returns: two lists: names and tags
    """
    # Get the html content of the website
    response = requests.get(url)
    # Parse the html content
    soup = BeautifulSoup(response.text, "html.parser")
    # get divs in all-restaurantsstyles__AllVendorsContainer-sc-1x4w8ei-0 QqCUl
    restaurants = soup.find_all(
        "div", class_="all-restaurantsstyles__AllVendorsContainer-sc-1x4w8ei-0 QqCUl"
    )
    # vendorstyles__VendorContainer-sc-eu6e2y-0 bPwOAu mx-2 mb-4
    vendors = restaurants[0].find_all(
        "div", class_="vendorstyles__VendorContainer-sc-eu6e2y-0 bPwOAu mx-2 mb-4"
    )
    # Get p with class h5 f-14 m-0 text-nowrap
    names = [
        vendor.find("p", class_="h5 f-14 m-0 text-nowrap").text for vendor in vendors
    ]
    # Get tags for each vendor h5 f-14 muted m-0 text-nowrap
    tags = [
        vendor.find("p", class_="h5 f-14 muted m-0 text-nowrap").text
        for vendor in vendors
    ]
    # Split each elemnt in tags and create a list of lists
    tags = [tag.split(",") for tag in tags]
    # Get text
    return names, tags


def talabat_save_csv(names_all, tags_all):
    # Write data to csv file
    with open("data/raw/talabat.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Tags"])
        for i in range(len(names_all)):
            writer.writerow([names_all[i], tags_all[i]])


def talabat_main():
    names_all = []
    tags_all = []
    # Go through the following URLs https://www.talabat.com/qatar/restaurants?page=1,2,3,...,111
    for i in range(1, 120):
        url = "https://www.talabat.com/qatar/restaurants?page=" + str(i)
        names, tags = talabat_scrape_data(url)
        print("Scraped page " + str(i))
        print("----------------------------------------------------")
        # Append the names to the list
        names_all.extend(names)
        # Append the tags to the list
        tags_all.extend(tags)
        # Wait for 1 second to avoid being blocked
        time.sleep(1)
    talabat_save_csv(names_all, tags_all)


talabat_main()


def mybookqatar_scrape_data(url: str):
    """
    Get the name and the tags of all restaurants in Urbanpoints's website
    Args: url (str): url of the website to scrape
    Returns: two lists: names and tags
    """
    # Get the html content of the website
    response = requests.get(url)
    # Parse the html content
    soup = BeautifulSoup(response.text, "html.parser")
    # Get div with class container position-relative
    restaurants = soup.find_all("div", class_="container position-relative")
    # Get div with class mb-search-list
    vendors = restaurants[0].find_all("div", class_="mb-search-list")
    # Get ul with class ShowCat
    names = [vendor.find("ul", class_="ShowCat").text for vendor in vendors]
    # Split elements by \n and create a differnt list with elements
    names = [name.split("\n") for name in names]

    return names[0]


def mybookqatar_save_csv(names):
    # put each element in the list in a separate row
    with open("data/raw/mybookqatar.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name"])
        for i in range(len(names)):
            writer.writerow([names[i]])


def mybookqatar_main():
    url = "https://www.mybookqatar.com/our-merchants/"
    names = mybookqatar_scrape_data(url)
    mybookqatar_save_csv(names)


# mybookqatar_main()


def zomato_scrape_data(file_path: str):
    """
    Get the names of all fine-dining restaurants in Zomato
    Args: file_path (str): file name of the saved html file
    Returns: names
    """
    # Get the html content from a saved html file
    with open(file_path, "r") as f:
        html = f.read()
    # Create a BeautifulSoup object from the html content
    soup = BeautifulSoup(html, "html.parser")

    # Get div with the class sc-1mo3ldo-0 sc-hVbUJp gnbZfT
    restaurants_loaded = soup.find_all("div", class_="sc-1mo3ldo-0 sc-hVbUJp gnbZfT")
    # Remove the first element of the list
    restaurants_loaded.pop(0)
    # Get all divs with class sc-ellAub bZsgnm
    vendors = [
        restaurant.find_all("div", class_="sc-ellAub bZsgnm")
        for restaurant in restaurants_loaded
    ]
    # Get h4 text from vendors[0]
    names_all = []
    for i in range(0, 6, 2):
        names = [vendor[i].find("h4").text for vendor in vendors]
        names_all.extend(names)

    # Get div with the class sc-1mo3ldo-0 sc-hVbUJp gnbZfT
    restaurants_loading = soup.find_all("div", class_="sc-1mo3ldo-0 sc-OxbzP fXHyKw")
    # Get all h4 with class sc-1hp8d8a-0 sc-eetwQk hgMIQY
    names = [
        restaurant.find_all("h4", class_="sc-1hp8d8a-0 sc-eetwQk hgMIQY")
        for restaurant in restaurants_loading
    ]
    # For each name in names get the text
    for name in names:
        names_all.extend([name.text for name in name])

    return names_all


def zomato_save_csv(names: list):
    # Create a dataframe from names_all
    df = pd.DataFrame(names)
    # Change column name to "Name"
    df.columns = ["Name"]
    # Export the dataframe to csv file
    df.to_csv("data/processed/zomato_fine_dining.csv", index=False)


def zomato_main():
    file_path = "data/html/Fine Dining in Doha - Zomato Qatar.html"
    names = zomato_scrape_data(file_path)
    zomato_save_csv(names)


# zomato_main()


def snoonu_scrape_data(file_path: str):
    """
    Get the names of all fine-dining restaurants from Snoonu
    Args: file_path (str): url of the website to scrape
    Returns: names
    """
    # Get the html content from a saved html file
    with open(file_path, "r") as f:
        html = f.read()
    # Create a BeautifulSoup object from the html content
    soup = BeautifulSoup(html, "html.parser")
    # Get div with class container Merchants_wrapper__wg2mn
    restaurants = soup.find_all("div", class_="Merchants_wrapper__wg2mn")
    # Get all p with class Typography_p1__3VqGX MerchantCard_name__XIs7U
    names = [
        restaurant.find_all("p", class_="Typography_p1__3VqGX MerchantCard_name__XIs7U")
        for restaurant in restaurants
    ]
    # Get all p with class MerchantCard_tags__bW4_n
    tags = [
        restaurant.find_all("p", class_="MerchantCard_tags__bW4_n")
        for restaurant in restaurants
    ]
    # For each name in names get the text
    names_all = []
    for name in names:
        names_all.extend([name.text for name in name])
    # For each tag in tags get the text
    tags_all = []
    for tag in tags:
        tags_all.extend([tag.text for tag in tag])
    return names_all, tags_all


def snoonu_save_csv(name: list, tags: list):
    """
    Create a dataframe with Name and Tag columns and save it to csv file
    Args: name (list): names of the restaurants
    Args: tags (list): tags of the restaurants
    """
    # Create a dataframe with Name and Tag columns
    df = pd.DataFrame({"Name": name, "Tag": tags})
    # Export the dataframe to csv file
    df.to_csv("data/processed/snoonu_fine_dining.csv", index=False)


def snoonu_main():
    file_path = "data/html/Food delivery in Doha - Snoonu.html"
    name, tags = snoonu_scrape_data(file_path)
    snoonu_save_csv(name, tags)


# snoonu_main()
