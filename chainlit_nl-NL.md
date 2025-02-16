# Welkom bij Artie!

Ontdek de kunstwereld samen met Artie.
Met elk gesprek zal Artie je meenemen op een reis naar een nieuw kunstwerk van het Rijks, MoMA of Tate museum.
Praat over de geschiedenis van een object, bespreek de gebeurtenissen die de kunstenaar er toe hebben aangezet om dit schilderij te maken, of vraag Artie wat hij denkt van een aspect van de afbeelding.
Artie is hier om samen met jou de kunstwereld te verkennen.

## Over Artie

Ik vind het leuk kunst op mezelf te observeren. Maar wanneer ik een werk ervaar samen met mijn vrienden of familie, dan zie ik dingen die ik nooit in mijn eentje zou hebben gezien. Mijn vader, die zelf ook een kunstenaar was, die nam me vaak mee naar musea en vertelde me van alles over de achtergrond, geschiedenis en context achter de kunstwerken. Ik had het voorrecht om zo'n kennisrijke gids bij me te hebben. Met Artie hoop ik zo'n ervaring iets dichter bij iedereen te brengen.

## Technologieën

Je kan de code hier vinden: https://github.com/vincentmin/artie
Ik heb gebruik gemaakt van de volgende uitstekende technologieën om Artie te bouwen:

- [Rijks Museum OAI-PMH API](https://data.rijksmuseum.nl/docs/): De kunstwerken van het Rijks Museum heb ik verkregen via de Rijks Museum data API. Veel dank aan het Rijks Museum om deze data zo vrij beschikbaar te maken!
- [MoMA](https://github.com/MuseumofModernArt/collection): De kunstwerken van het MoMA heb ik verkregen via deze github link. Zeer gebruiksvriendelijk en het word regelmatig geupdate; bedankt MoMA!
- [Tate](https://github.com/tategallery/collection): De kunstwerken van het Tate museum heb ik verkregen via deze github link. Zeer gebruiksvriendelijk! Helaas wordt de dataset niet meer geupdate, dus de nieuwste kunstwerken zullen niet beschikbaar zijn. Bedankt Tate!
- [Google Gemini](https://deepmind.google/technologies/gemini/flash/): Google's Gemini Flash 2.0 model is het Large Language Model dat Artie ondersteund. We gebruiken de multi-modal mogelijkheden van het model om Artie de kunstwerken echt te laten zien, zodat hij met je mee kan kijken. Daarnaast gebruiken we de ruimtelijk begrip (spatial understanding) mogelijkheden van het model om Artie specifieke delen van de kunstwerken te laten tonen. Deze feature is nog niet helemaal perfect, maar het creëert een leuke ervaring. En ook gebruiken we Google Search om het model dingen op te laten zoeken indien dat nodig is.
- [Micr.io](http://micr.io/): De afbeeldingen van het Rijks Museum worden gehost op Micr.io. Deze biedt een bijzonder handige API om plaatjes te schalen, bijsnijden etc. Dit gebruiken we samen met de spatial understanding van Gemini om Artie specifieke delen van afbeeldinge te laten tonen. Dit is helaas niet beschikbaar voor MoMA en Tate.
- [Hugging Face Datasets](https://huggingface.co/datasets): We gebruiken de fantastische streaming features van Hugging Face Datasets om met weinig latency en geheugen kunstwerken aan de gebruikers te tonen.
- [Chainlit](https://github.com/Chainlit/chainlit): Dit feature-rijke package is gebruikt om de frontend van Artie te bouwen.
