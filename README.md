# Welcome to Artie!

Have a chat with Artie and explore the art world together.
With each conversation, Artie will take you on a journey into a random art piece from the Rijks Museum.
Talk about the history that lies behind an object, discuss the events that led the artist to create this painting, or ask Artie what he thinks about a particular feature of the image.
Artie is here to discover the Rijks Museum together with you.

Try it out here: [artie.vincentmin.com](https://artie.vincentmin.com/)

## About

Observing art by myself can be nice, but experiencing a piece with friends or family often makes me see things that I would never have spotted by myself. My father, who was an artist himself, would take me to musea and tell me about the background, history and context of art pieces. I was fortunate to have such a knowledgeable guide to explore art with. With Artie, I tried to make such an experience accessible to anyone.

## Technologies

Find the code here: https://github.com/vincentmin/artie
I used the following excellent technologies to build this experience:

- [Rijks Museum OAI-PMH API](https://data.rijksmuseum.nl/docs/) The art pieces that you can discover with Artie originate from the Rijks Museum data API. Thanks so much to the Rijks Museum for making this so freely accessible!
- [MoMA](https://github.com/MuseumofModernArt/collection): The art pieces from the MoMA were obtained through this github repository. The json format is very easy to use and they regularly update the dataset. Thanks MoMA!
- [Tate](https://github.com/tategallery/collection): The art pieces from the Tate were obtained through this github repository. The csv format is very easy to use. Sadly, the dataset is no longer updated, so the newest art pieces will not be available on Artie. Thanks for making this available Tate!
- [Google Gemini](https://deepmind.google/technologies/gemini/flash/): Google's Gemini Flash 2.0 model is the LLM that powers Artie. We use the model's multi-modal capabilities to let Gemini see the image of the art piece. Furthermore, we use the spatial understanding capabilities to present specific regions of the image to the user. Finally, the model can also use Google Search to look up any information that it may need.
- [Micr.io](http://micr.io/): The images from the Rijks Museum are hosted on micr.io. They provide an excellent API to crop and scale images. We use this together with Gemini's spatial understanding feature to let Artie show specific regions of the art pieces to users. Sadly this is not available for MoMA or Tate.
- [Hugging Face Datasets](https://huggingface.co/datasets): We use the fantastic streaming features of Hugging Face Datasets to show art pieces to the users with low latency.
- [Chainlit](https://github.com/Chainlit/chainlit): This feature-rich package was used to build the frontend to the application.
