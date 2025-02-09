import httpx
import lxml.etree
from tqdm.auto import tqdm
import pandas as pd

params = {
    "verb": "ListRecords",
    "metadataPrefix": "edm",
}

namespaces = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "edm": "http://www.europeana.eu/schemas/edm/",
    "svcs": "http://rdfs.org/sioc/services/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
}

csv_header_written = False  # Flag to track if header has been written

with httpx.Client() as client:
    response = client.get("https://data.rijksmuseum.nl/oai", params=params)

    tree = lxml.etree.fromstring(response.content)

    total_records = int(
        tree.xpath(".//oai:resumptionToken/@completeListSize", namespaces=namespaces)[0]
    )

    with tqdm(total=total_records) as pbar:
        while True:
            tree = lxml.etree.fromstring(response.content)

            batch = tree.xpath(".//oai:record", namespaces=namespaces)
            records = []

            for i, record in enumerate(batch):
                object_id = record.xpath(
                    ".//oai:identifier/text()", namespaces=namespaces
                ) or [None]
                title = record.xpath(".//dc:title/text()", namespaces=namespaces) or [
                    None
                ]
                description = record.xpath(
                    ".//dc:description/text()", namespaces=namespaces
                ) or [None]
                image_url = (
                    record.xpath(
                        ".//edm:object/edm:WebResource/@rdf:about",
                        namespaces=namespaces,
                    )
                    or record.xpath(
                        ".//edm:object/@rdf:resource", namespaces=namespaces
                    )
                    or [None]
                )
                artist = record.xpath(
                    ".//dc:creator/@rdf:resource", namespaces=namespaces
                ) or [None]

                records.append(
                    dict(  # Append to batch list
                        original_id=object_id[0],
                        image_url=image_url[0],
                        long_title=title[0],
                        description=description[0],
                        artist=artist[0],
                    )
                )

            df_batch = pd.DataFrame(records)
            df_batch.to_csv(
                "../data/records.csv",
                mode="a",
                header=not csv_header_written,
                index=False,
            )
            csv_header_written = True

            pbar.update(len(batch))

            resumption_token_list = tree.xpath(
                ".//oai:resumptionToken/text()", namespaces=namespaces
            )
            if resumption_token_list:
                params = {
                    "verb": "ListRecords",
                    "resumptionToken": resumption_token_list[0],
                }
                response = client.get("https://data.rijksmuseum.nl/oai", params=params)
            else:
                break
