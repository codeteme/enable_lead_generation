import pandas as pd

# import ../data/raw/talabat.csv first column is string, second column is list
talabat = pd.read_csv("data/raw/talabat.csv")


def remove_duplicates_talabat(data: pd.DataFrame):
    """
    Removes duplicates from the talabat data.
    Args: data - a pandas dataframe of the talabat data
    """
    # Remove duplicates
    data = data.drop_duplicates()
    return data


def get_talabat_tag_count(data: pd.DataFrame):
    """
    Returns a dictionary of the number of times each tag occurs in the talabat data.
    Args: data - a pandas dataframe of the talabat data
    """
    # Remove the brackers and quotatoin marks from the tags column
    data["Tags"] = data["Tags"].str.replace("[", "")
    data["Tags"] = data["Tags"].str.replace("]", "")

    # Get the unique tags
    tags = data["Tags"].unique()
    # Split each element by comma and create a different list with elements
    tags = [tag.split(",") for tag in tags]
    # Flatten the list
    tags = [item for sublist in tags for item in sublist]
    # Remove the whitepaces
    tags = [tag.strip() for tag in tags]
    # Remove single quotes
    tags = [tag.replace("'", "") for tag in tags]
    # Remove duplicates
    tags = list(set(tags))
    # Sort the list
    tags.sort()

    # Count the number of restaurants with each tag
    # Create a dictinary with the tag as key and the number of restaurants with that tag as value
    tag_count = {}
    for tag in tags:
        tag_count[tag] = str(data["Tags"].str.contains(tag).sum())

    return tag_count


def tag_count_to_csv(tag_count: dict):
    """
    Creates a csv file with the tag count data.
    Args: tag_count - a dictionary of the tag count data
    """

    # Create a dataframe with the tag_count dictionary
    tag_count_df = pd.DataFrame.from_dict(tag_count, orient="index")
    tag_count_df.columns = ["Count"]
    # Sort the dataframe by the count column
    tag_count_df = tag_count_df.sort_values(by="Count", ascending=False)
    # Save the dataframe to a csv file
    tag_count_df.to_csv("data/processed/talabat_tag_count.csv")

    return None


def get_food_vendors_talabat(data: pd.DataFrame, tags: list):
    """
    Returns a dataframe of the restaurants with the tags in the tags list.
    Args: data - a pandas dataframe of the talabat data
          tags - a list of tags
    """
    # Create a dataframe of the restaurants with the tags in the tags list
    food_vendors = data[~data["Tags"].str.contains("|".join(tags))]
    return food_vendors


# tag_count = get_talabat_tag_count(talabat)
# tag_count_to_csv(tag_count)

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

print("============================================================")
print("Shape before removing duplicates: " + str(talabat.shape))
print("Removing duplicates...")
talabat_unique = remove_duplicates_talabat(talabat)
print("Done!")
print("Shape after removing duplicates: " + str(talabat_unique.shape))
print("============================================================")
print("Shape before removing non-food tags: " + str(talabat_unique.shape))
tag_count = get_talabat_tag_count(talabat_unique)

# Assert that all non-food tags are in the tag_count dictionary
for tag in NON_FOOD_TAGS_TALABAT:
    assert tag in tag_count.keys()

# Filter the talabat dataframe to only include restaurants with none of the non-food tags
talabat_food = get_food_vendors_talabat(talabat_unique, NON_FOOD_TAGS_TALABAT)
print("Shape after removing non-food tags: " + str(talabat_food.shape))
print("============================================================")

talabat_food.to_csv("data/processed/talabat_food.csv")
