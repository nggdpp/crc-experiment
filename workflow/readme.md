# Environment

Use the environment.yml file in the root of this project to build a Conda environment with the necessary Python dependencies. Or refer to those dependencies if you want to build a virtual environment in some other way.

# Docker MongoDB

The methods in this workflow use a local instance of a out of the box MongoDB instance run in Docker. I used the expedience of:

``docker run -d -p 27017:27107 -v ~/data/crc-experiment:/data/db mongo``

Replace "~/data/crc-experiment" with whatever local path you want to persist your data in, or run the Docker container purely with no persistence at all. Note that this creates a non-production, wide open MongoDB instance running on whatever machine you run Docker on. It's not meant for anything other than standing in as a temporary data store for the data in motion within this workflow. You don't even need to persist the data here unless you are going to come back to this and want to leave things intact. I used MongoDB because if it's ease of use for JSON-based documents and the power of it's aggregation system, which I take advantage of at several points and note in my documentation.

All of the references to create a MongoClient in the code rely on accessing a local instance on port 27017 with no authentication requirement. Alternatively, you could spin up an account on the free [MLab service](https://mlab.com/) or access any other MongoDB instance you might have access to. You will then need to adjust the calls to open up a MongoClient to include the necessary access and authentication information in whatever way you choose.

# Binder View

If you want to run these notebooks in Binder, you can do that via the following:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/nggdpp/crc-experiment/master)

The environment.yml should solve all the necessary dependencies when it launches other than the MongoDB instance. Any code that runs against the CRC web site, ScienceBase, Macrostrat, or other open and public access points should execute, and you can fiddle with where and how the resulting data is processed in memory or persisted. See the notes above if you want to solve or change the MongoDB dependency.

# Workflow Sequence
The overall process for this experiment is described in the main readme at the root. This readme lists the specific workflow steps as links to the Jupyter Notebooks containing their code and discussion. These steps do need to be run in sequence at first or otherwise have their data dependencies met.

1. [Prep Raw Data.ipynb](Prep&#32;Raw&#32;Data.ipynb) - Pulls the data downloads from the CRC Well Catalog web app, adds values for later processing, and loads them as collections in MongoDB
2. [Pull MapServer Information.ipynb](Pull&#32;MapServer&#32;Information.ipynb) - Pages through queries of the MapServer layer query services for the two collections and caches the features with linked identifiers in MongoDB for later processing
3. [Scrape CRC Web Pages.ipynb](Scrape&#32;CRC&#32;Web&#32;Pages.ipynb) - Uses the assembled identifiers from the MapServer layers to create URLs to landing pages, sets these up in a collection for processing, scrapes data structures from the pages, and caches the results in MongoDB for later processing
4. [Geologic Map Unit Context.ipynb](Geologic&#32;Map&#32;Unit&#32;Context.ipynb) - Prepares a collection of unique geohashed coordinates, runs queries against a Macrostrat API, and caches the results in the collection for later processing
5. [cores_aggregation.js](cores_aggregation.js) and [cuttings_aggregation.js](cuttings_aggregation.js) - Used via a MongoDB console connection to generate "cores" and "cuttings" collections containing combination of properties from raw data, scraped data, and GMU contextual data
6. [Build SB Items.ipynb](Build SB Items.ipynb) - uses the final collections for cores and cuttings with functions from [sbitem_from_crcrecord.py](sbitem_from_crcrecord.py) to build ScienceBase Items and loads them to ScienceBase

At the end of this processing, all collections from MongoDB were exported using MongoDB functions to a collection of JSON document arrays and gzipped for inclusion in the project. These datasets are considered intermediaries and not really the point of this project, but they are included for reference and can be read by anything capable of consuming JSON arrayed documents. The actual final product from these processing steps are the collection items in the following two ScienceBase Collections of the National Digital Catalog.

* [USGS Core Research Center (CRC) Collection of Core](https://www.sciencebase.gov/catalog/item/4f4e49dae4b07f02db5e0486)
* [USGS Core Research Center (CRC) Collection of Cuttings](https://www.sciencebase.gov/catalog/item/4f4e49d8e4b07f02db5df2d2)