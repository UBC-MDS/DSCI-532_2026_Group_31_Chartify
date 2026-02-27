import pandas as pd 
import kagglehub
from kagglehub import KaggleDatasetAdapter
import unicodedata


def get_data():
    # Create a function to normalize Artist Names that have special characters to their closes ASCII equivalents
    # Function created with assistance by Claude AI
    def normalize_text(text):
        if isinstance(text, str):
            # Decompose special characters, the encode to ASCII 
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

    # Use KaggleDatasetAdapter to download the dataset programatically
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "sanjanchaudhari/spotify-dataset/versions/1",
        "cleaned_dataset.csv",
        )
    
    # Apply normalization of characters to Artist, Song and Album Names
    df['Artist'] = df['Artist'].apply(normalize_text)
    df['Album'] = df['Album'].apply(normalize_text)
    df['Track'] = df['Track'].apply(normalize_text)
    df['Title'] = df['Title'].apply(normalize_text)
    
    return df 