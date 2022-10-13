# Read json file
import json
import pandas as pd

talabat_file_path = "data/html/all-restaurants.json"


def read_json(talabat_file_path: str) -> dict:
    with open(talabat_file_path, "r") as f:
        data = json.load(f)
    return data


def get_keys(data: pd.DataFrame) -> list:
    keys = []
    for key in data["pageProps"]["restaurants"][0]:
        keys.append(key)
    return keys


def get_restaurants_cuisines(data: pd.DataFrame):
    restaurants, cuisines = [], []
    for restaurant in data["pageProps"]["restaurants"]:
        restaurants.append(restaurant["name"])
        cuisines.append(restaurant["cuisines"])
    return restaurants, cuisines


def talabat_to_df(restaurants: list, cuisines: list) -> pd.DataFrame:
    df = pd.DataFrame({"Name": restaurants, "Cuisine": cuisines})
    return df


def talabat_cuisines(df: pd.DataFrame) -> list:
    # For each row, split the cuisines column by a comma and append to a list
    unique_cuisines = df["Cuisine"].apply(lambda x: x.split(","))
    # Flatten the list of lists
    unique_cuisine = [
        cuisine for cuisine_list in unique_cuisines for cuisine in cuisine_list
    ]
    # Remove duplicates
    unique_cuisine = list(set(unique_cuisine))
    return unique_cuisine


def clean_talabat(df: pd.DataFrame) -> pd.DataFrame:
    # Remove rows with no cuisine
    df = df[df["Cuisine"] != ""]
    # Remove rows with no name
    df = df[df["Name"] != ""]
    # Remove rows with no name and cuisine
    df = df[df["Name"] != ""][df["Cuisine"] != ""]
    # Remove duplicates
    df = df.drop_duplicates()
    return df


def get_food_vendors_talabat(data: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe of the restaurants with the tags in the tags list.
    Args: data - a pandas dataframe of the talabat data
    """
    NON_FOOD_TAGS_TALABAT = [
        "Accessories ",
        "Convenience Store",
        "Cosmetics",
        "Hypermarket",
        "Optics",
        "Perfume",
        "Pet Shop",
        "Pharmacy",
        "Poultry",
        "Services",
        "Speciality Store",
        "Specialty Store",
        "Stationary",
        "Supermarket",
        "Toys",
    ]
    # Create a dataframe of the restaurants with the tags in the tags list
    food_vendors = data[~data["Cuisine"].str.contains("|".join(NON_FOOD_TAGS_TALABAT))]
    return food_vendors


if __name__ == "__main__":
    data = read_json(talabat_file_path)
    restaurants, cuisines = get_restaurants_cuisines(data)
    df = talabat_to_df(restaurants, cuisines)
    # unique_cuisine = talabat_cuisines(df)
    print("Shape before cleaning Talabat: ", df.shape)
    df = clean_talabat(df)
    print("Shape after cleaning Talabat: ", df.shape)
    talabat_food = get_food_vendors_talabat(df)
    print("Shape of Talabat food: ", talabat_food.shape)
    talabat_food.to_csv("data/processed/talabat_food_new.csv", index=False)