# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "datasets",
#     "pandas",
# ]
# ///
from datasets import Dataset
import pandas as pd

url = (
    "https://github.com/MuseumofModernArt/collection/raw/refs/heads/main/Artworks.json"
)
df = pd.read_json(url)
ds = Dataset.from_pandas(df)
print(ds)
ds.push_to_hub(repo_id="vincentmin/moma")
