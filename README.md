# TikTok Scraper
Get TikTok videos from a hashtag feed. This scraper is based on TikAPI, and requires an API key to operate.

CLI implemented using [Typer](https://typer.tiangolo.com/).

## Usage
Help can be accessed by running `python main --help` and `python clean --help`.

### Scraping
1. Set up virtual environment and install `requirements.txt`
1. Add your API key in a `.env` file. The default name for this variable is `TIKAPI_KEY`.
1. Enter your hashtags each on a new line in `hashtags.txt`. You can include the hashtag symbol or not.
1. Run `main.py`

You'll find your results at `./data/results.csv`.

### Cleaning
Run `python clean` to clean your results. By default, this command drops unneeded columns from `results.csv`, renames the remaining columns, and saves them to `results_clean.csv`. There are two options to alter this behavior:
1. `python clean --narrow [N]` - Narrow down the results to only the top N most viewed videos.
1. `python clean --narrow [N] --by-hashtag` - Narrow down to the top N videos, but the narrowing down is scoped to each hashtag, so you'll end up with a maximum of (N * number of hashtags) videos.

## To Do
- [x] Data cleaning functionality to remove unwanted columns
- [x] Data cleaning functionality to narrow down videos to most viewed and remove duplicates