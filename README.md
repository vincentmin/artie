# open-data-chatbot

A chatbot on open data. I have not yet decided which open data source to use yet.
Options:
- https://docs.irail.be/ [for example](https://api.irail.be/v1/liveboard/?id=BE.NMBS.008892007&station=Gent-Sint-Pieters&date=070225&time=1230&arrdep=departure&lang=en&format=json&alerts=false)
- https://www.ns.nl/reisinformatie/ns-api


## Getting started

First, [get a Google API key](https://aistudio.google.com/apikey) and store it in `.env` with the name `GOOGLE_API_KEY`.
Then run
```bash
pip install .
chainlit run src/main.py
```
A chatbot should now be running at http://localhost:8000.
