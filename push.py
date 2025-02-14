from datasets import Dataset

ds = Dataset.from_json("data/moma_artists.json")
print(ds)
ds.push_to_hub(repo_id="vincentmin/moma")
