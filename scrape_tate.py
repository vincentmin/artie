# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "datasets",
#     "pandas",
# ]
# ///
import pandas as pd
from datasets import Dataset

url = "https://github.com/tategallery/collection/raw/refs/heads/master/artwork_data.csv"
df = pd.read_csv("data/tate.csv", low_memory=False, dtype={"year": str})
df.thumbnailUrl = df.thumbnailUrl.str.replace(
    "www.tate.org.uk", "media.tate.org.uk"
).str.replace("_8.jpg", "_10.jpg")
ds = Dataset.from_pandas(df)
print(ds)
ds.push_to_hub(repo_id="vincentmin/tate")
