import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.text_cleaning import remove_text_between_angle_brackets, clean_text


def download_patent_text(patent_url: str) -> pd.DataFrame | None:
    # Send a GET request to the patent URL
    response = requests.get(patent_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        description_paragraphs = soup.find_all(
            "div", {"class": "description-paragraph"}
        )
        if description_paragraphs:
            patent_df = pd.DataFrame({"description_paragraphs": description_paragraphs})
            patent_df["clean_paragraphs"] = patent_df.description_paragraphs.astype(
                str
            ).apply(lambda x: remove_text_between_angle_brackets(clean_text(x)))
            return patent_df
        else:
            print("Could not find patent text on the page.")
    else:
        print(f"Failed to fetch the patent page. Status code: {response.status_code}")
