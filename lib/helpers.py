import os
from typing import List

from tikapi import TikAPI


def connect_to_tikapi(api_key: str) -> None:
    print("Connecting to TikAPI... ", end="", flush=True)
    api = TikAPI(api_key)
    print("connected.")
    return api


def get_hashtags(filepath) -> List[str]:
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    return [h.strip().replace("#", "") for h in lines]


def clean_temp_files(temp_filepaths: List[str], temp_data_dir: str) -> None:
    """Delete all temp files not created during this run"""
    print("Cleaning temp files... ", end="", flush=True)
    old_files = [
        f for f in os.listdir(temp_data_dir)
        if os.path.isfile(os.path.join(temp_data_dir, f))
            and os.path.join(temp_data_dir, f) not in temp_filepaths
    ]

    for filepath in old_files:
        filepath = os.path.join(temp_data_dir, filepath.strip())
        if os.path.isfile(filepath) and filepath.endswith('.csv'):
            os.remove(filepath)
    print("done.")