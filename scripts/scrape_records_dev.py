import httpx
import lxml.etree
from tqdm.auto import tqdm
import pandas as pd

params = {
    "verb": "ListIdentifiers",
    "metadataPrefix": "edm",
}

namespaces = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    # "dc": "http://purl.org/dc/elements/1.1/",
    # "dcterms": "http://purl.org/dc/terms/",
    # "edm": "http://www.europeana.eu/schemas/edm/",
    # "svcs": "http://rdfs.org/sioc/services/",
    # "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
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

            batch = tree.xpath(".//oai:header", namespaces=namespaces)
            records = []

            for i, record in enumerate(batch):
                object_id = record.xpath(
                    ".//oai:identifier/text()", namespaces=namespaces
                ) or [None]
                datestamp = record.xpath(
                    ".//oai:datestamp/text()", namespaces=namespaces
                ) or [None]
                set_spec = record.xpath(".//oai:setSpec/text()", namespaces=namespaces)

                records.append(
                    dict(
                        object_id=object_id[0],
                        datestamp=datestamp[0],
                        set_spec=set_spec,
                    )
                )

            df_batch = pd.DataFrame(records)
            df_batch.to_csv(
                "data/bare_records.csv",
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
                    "verb": "ListIdentifiers",
                    "resumptionToken": resumption_token_list[0],
                }
                response = client.get("https://data.rijksmuseum.nl/oai", params=params)
            else:
                break
