import os

import pandas as pd
import typer
from decouple import config

from lib.helpers import connect_to_tikapi, get_hashtags, clean_temp_files
from lib.Scraper import Scraper


HASHTAGS_FILEPATH = "hashtags.txt"
TEMP_DATA_DIR = "./data/temp"  # to store backup results from each hashtag
OUTPUT_DIR = "./data"

API_KEY = config('TIKAPI_KEY')


def main():
    api = connect_to_tikapi(API_KEY)
    scraper = Scraper(api_obj=api)
    hashtags = get_hashtags(HASHTAGS_FILEPATH)

    hashtag_dfs = []
    temp_filepaths = []
    for hashtag in hashtags:
        print(f"Starting scraping for #{hashtag}")
        df = scraper.get_hashtag_feed(hashtag=hashtag)
        hashtag_dfs.append(df)

        # write out a temporary version of the results as a backup
        output_filepath = os.path.join(TEMP_DATA_DIR, f"results_{hashtag}.csv")
        temp_filepaths.append(output_filepath)
        df.to_csv(output_filepath, index=False)

    print("Writing out final file... ", end="", flush=True)
    big_df = pd.concat(hashtag_dfs)
    output_filepath = os.path.join(OUTPUT_DIR, "results.csv")
    big_df.to_csv(output_filepath, index=False)
    print("finished.")

    print(f">>> Made {scraper.num_calls} API calls for this scrape")

    clean_temp_files(temp_filepaths=temp_filepaths, temp_data_dir=TEMP_DATA_DIR)


if __name__ == "__main__":
    typer.run(main)
