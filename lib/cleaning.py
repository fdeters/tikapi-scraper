import ast
from datetime import datetime

import pandas as pd


def narrow_down(dataframe: pd.DataFrame, n: int) -> pd.DataFrame:
    """Narrows down to the top n most viewed videos and removes duplicates"""
    dataframe = dataframe.sort_values(by='stats.playCount', ascending=False)
    dataframe = dataframe.drop_duplicates(subset='id')
    try:
        return dataframe[:n]
    except IndexError:
        return dataframe


def narrow_down_by_hashtag(dataframe: pd.DataFrame, n: int) -> pd.DataFrame:
    """Does the same thing as narrow_down but scopes to each hashtag, so 
    you'll end up with n * (number of hashtags) videos."""
    dataframe = dataframe.sort_values(by='stats.playCount', ascending=False)
    dataframe = dataframe.drop_duplicates(subset='id')
    gb = dataframe.groupby('hashtag_feed')
    groups = [gb.get_group(x) for x in gb.groups]
    results = []
    for group in groups:
        group = group.sort_values(by='stats.playCount', ascending=False)
        try:
            group = group[:n]
        except IndexError:
            pass
        results.append(group)

    return pd.concat(results)    


def clean_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    # drop unwanted columns
    columns_to_keep = list(COLUMNS_TO_KEEP.keys())
    dataframe = dataframe[columns_to_keep]

    # reformat data in some columns
    for c in dataframe.columns:
        try:
            reformat_function = COLUMNS_TO_KEEP[c]["reformat_function"]
        except KeyError:
            reformat_function = None

        if reformat_function:
            dataframe[c] = dataframe[c].apply(reformat_function)

    # rename columns
    column_name_mapper = {
        k: COLUMNS_TO_KEEP[k]['cleaned_name'] 
        for k in COLUMNS_TO_KEEP.keys()
    }
    dataframe = dataframe.rename(columns=column_name_mapper)

    return dataframe


##############################################
## Column cleaning functions

def extract_hashtags(data: str) -> str:
    """Apply to column of dataframe"""
    try:
        challenges = ast.literal_eval(data)
    except ValueError:
        challenges = []
    
    hashtags_list = []
    for c in challenges:
        try:
            hashtags_list.append(c['title'])
        except KeyError:
            pass
    
    try:
        hashtags_str = ', '.join(hashtags_list)
    except Exception:
        hashtags_str = ''
    
    return hashtags_str


def convert_int_to_time(create_time: int) -> str:
    """Apply to column of dataframe"""
    try:
        timestamp = datetime.fromtimestamp(create_time)
        time_string = timestamp.strftime('%m-%d-%Y %H:%M:%S')
    except Exception:
        time_string = ''
    
    return time_string


COLUMNS_TO_KEEP = {
    "challenges": {
        "cleaned_name": "hashtags",
        "reformat_function": extract_hashtags,
    },
    "createTime": {
        "cleaned_name": "created_at",
        "reformat_function": convert_int_to_time,
    },
    "desc": {
        "cleaned_name": "caption",
        "reformat_function": None,
    },
    "id": {
        "cleaned_name": "id",
        "reformat_function": None,
    },
    "author.nickname": {
        "cleaned_name": "author",
        "reformat_function": None,
    },
    "author.verified": {
        "cleaned_name": "author_is_verified",
        "reformat_function": None,
    },
    "music.title": {
        "cleaned_name": "sound_name",
        "reformat_function": None,
    },
    "stats.commentCount": {
        "cleaned_name": "comments",
        "reformat_function": None,
    },
    "stats.diggCount": {
        "cleaned_name": "likes",
        "reformat_function": None,
    },
    "stats.playCount": {
        "cleaned_name": "plays",
        "reformat_function": None,
    },
    "stats.shareCount": {
        "cleaned_name": "shares",
        "reformat_function": None,
    },
    "video.downloadAddr": {
        "cleaned_name": "video_download_link",
        "reformat_function": None,
    },
    "video.duration": {
        "cleaned_name": "video_length",
        "reformat_function": None,
    },
    "hashtag_feed": {
        "cleaned_name": "hashtag_feed",
        "reformat_function": None,
    },
}
