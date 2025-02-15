# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "datasets",
#     "requests",
# ]
# ///
from datasets import Dataset
import tempfile
from pathlib import Path
import requests

url = (
    "https://github.com/MuseumofModernArt/collection/raw/refs/heads/main/Artworks.json"
)

with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir) / "Artworks.json"

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(temp_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    ds = Dataset.from_json(str(temp_path))
    print(ds)
    ds.push_to_hub(repo_id="vincentmin/moma")
