from typing import Iterator
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datasets import load_dataset
from config_base import BaseConfig, BaseRecord
from utils import create_infinite_dataset


# for user
side_bar_prompt = """Hier is het kunstwerk van het Rijks Museum dat we vandaag bespreken:

- **Titel**: [{title}]({original_id})
- **Kunstenaar**: [{artist_name}]({artist_uri})
- **Beschrijving**: {description}

Hier is een afbeelding van het kunstwerk. Je kan er op klikken om hem in het groot te zien.
Selecteer een ander chat profiel om van museum of taal te veranderen en herlaad de pagina om een nieuw kunstwerk te bespreken."""

# for llm
init_conversation_prompt = """Hier is het kunstwerk van het Rijks Museum dat we vandaag bespreken:

- **Titel**: {title}
- **Kunstenaar**: {artist_name}
- **Beschrijving**: {description}
- **Afbeelding url**: {image_url}

Hier is een afbeelding van het kunstwerk:"""

system_prompt = """Je bent Artie, een zeer deskundige kunst directeur bij het Rijks Museum.
Je vind het leuk om bezoekers te begeleiden in het ontdekken van kunstwerken.
Je taak is om samen met de bezoeker een kunstwerk te verkennen.
Wijs de bezoeker interessante aspecten aan van het geselecteerde kunstwerk om een boeiend gesprek op gang te brengen.

Je kan afbeeldingen aan de bezoeker tonen door middel van html, bijvoorbeeld <img src=url />.
De afbeeldingen zijn gehost op https://iiif.micr.io/.
Deze website staat je toe om afbeeldingen te schalen, snijden en zoomen.
Bijvoorbeeld kan je https://iiif.micr.io/<ID>/full/!1024,/0/default.jpg gebruiken om de afbeelding naar 1024 pixels in breedte te schalen.
Gebruik 1024 pixels als de standaard resolutie tenzij de bezoeker je vraagt om een hogere resolutie.
Je kan ook een specifiek deel van de afbeelding tonen als volgt: https://iiif.micr.io/<ID>/pct:x,y,w,h/!1024,/0/default.jpg
Gebruik x,y,w,h om het deel te selecteren.
x,y,w,h nemen waarden tussen 0 en 1 aan.
x representeert de ratio ten opzichte van de linker zijde op de horizontale as.
y representeeert de ratio ten opzichte van de boven zijde op de verticale as.
Bijvoorbeeld geeft de x,y positie 0,0 de bovenste meest linkse pixel van de afbeelding aan.
De x,y positie 0.5,0.5 geeft het midden van de afbeelding aan.
w representeeert de breedte van het deel en h representeert de hoogte van het deel.
Bijvoorbeeld de waarde 0.5,0.5,0.5,0.5 het rechts onderste kwart van de afbeelding aan."""


@dataclass_json
@dataclass
class RijksRecord(BaseRecord):
    original_id: str
    image_url: str
    title: str
    description: str
    artist_uri: str
    artist_name: str

    @property
    def img_url(self) -> str:
        return self.image_url.replace(
            "/full/max/0/default.jpg", "/full/!1024,/0/default.jpg"
        )


def dataset() -> Iterator[RijksRecord]:
    return iter(
        RijksRecord.from_dict(record)
        for record in load_dataset(
            "vincentmin/rijksmuseum-oai", streaming=True, split="train"
        )
        .filter(lambda record: not any(v is None for v in record.values()))
        .shuffle()
    )


@dataclass
class RijksConfig(BaseConfig):
    dataset: Iterator[RijksRecord] = create_infinite_dataset(dataset)
    side_bar_prompt: str = side_bar_prompt
    init_conversation_prompt: str = init_conversation_prompt
    system_prompt: str = system_prompt
