"""
Contains optional data cleaning functions.
"""
import sys

import pandas as pd
import typer

from lib.cleaning import narrow_down, narrow_down_by_hashtag, clean_columns


RAW_RESULTS_PATH = './data/results.csv'
CLEAN_RESULTS_PATH = './data/results_clean.csv'


def main(
    narrow: int = typer.Option(None, 
        help="Narrow down to a certain number of results"),
    by_hashtag: bool = typer.Option(False, 
        help="Perform narrowing down on a by-hashtag basis instead of overall"),
) -> None:
    df = pd.read_csv(RAW_RESULTS_PATH)

    if narrow is not None:
        if by_hashtag:
            df = narrow_down_by_hashtag(df, n=narrow)
        else:
            df = narrow_down(df, n=narrow)
    
    df = clean_columns(df)
    df.to_csv(CLEAN_RESULTS_PATH, index=False)


if __name__ == "__main__":
    typer.run(main)
