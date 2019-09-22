# CRC Records for Cores and Collections to ScienceBase
This project explores a couple of the concepts we are pursuing for the next generation of the National Digital Catalog by using the USGS Core Research Center (CRC) as an example use case. The CRC manages collections of rock cores and cuttings at the USGS facility in Lakewood. The CRC has had a databased inventory for decades, the "CRC Well Catalog," that has been through several different generations of technology. This situation is generally typical across many of the other institutions managing geoscience collections (or other scientific collections for that matter). The CRC inventory management system consists of the following major technical components:

* A highly normalized (e.g., 64 tables) relational database in PostgreSQL
* A custom web application for managing the database, accessed internally by CRC staff
* An ArcGIS MapServer [service](https://my.usgs.gov/arcgis/rest/services/crcwc/crcwc/MapServer) that provides feature services for the cores and cuttings collections along with supporting layers
* A custom [web application](https://my.usgs.gov/crcwc/) for public search and browse

One of the principles that we are pursuing for the next gen catalog is to try and make maximum use of whatever exists as operational infrastructure from NDC contributors. We want to move from a "push to" to a "draw from" modality. In the draw from mode, we are talking about software that is able to read whatever is available online and integrate the information into the NDC. So, the fundamental question is, how well does the CRC present its inventory to the world in a way that a software algorithm can read it and digest the information for use? We are examining this in terms of two main categories of data integration problem solving: syntactic and semantic.

So far, the CRC has only been represented in the NDC with a one-time data dump to CSV files of a small subset of its inventory. These records were organized into two collections in ScienceBase ([Cuttings](https://www.sciencebase.gov/catalog/item/4f4e49d8e4b07f02db5df2d2) and [Cores](https://www.sciencebase.gov/catalog/item/4f4e49dae4b07f02db5e0486)). In the process I lay out here, I removed the existing items and then replaced them with a new structure for the full set of items.

All in all, this process achieves what I set out to do - build out 62K items of new information in the NDC. However, there are a number of pretty major pitfalls encountered here that I discuss in the notes below. As the CRC Well Catalog continues to be developed, this process could be run again to refresh the collections represented in ScienceBase and the NDC. However, it has enough steps against enough variety in source material that it is really not a viable solution to operationally source the NDC as it stands today.

## Multiple Sources of Source Data
The ArcGIS MapServer layers present what should be the most reasonable way to have a software tool that regularly checks for new or updated records and brings them into the NDC. However, there are some issues with how the MapServer layers are formatted and presented for use. Behind the scenes, the MapServer is configured to work against two database views created for this purpose in the underlying PostGIS database. These views do not have any particular logic applied to them in terms of naming properties in a way that makes better sense as a point of distribution for the data. Rather, like a lot of GIS services, these were set up expressly for the purpose of driving a single [web map application](https://my.usgs.gov/crcwc/map). So, when you look at the raw output from the MapServer, it shows records that are not really built to be used in any other context.

The CRC web site also provides a [text search interface](https://my.usgs.gov/crcwc/query) that presents a different view of cores and cuttings and provides download options that were used to build our "raw" data. This view has been harmonized at the application layer to present property names that are mostly in common between the cores and cuttings tables. It also incorporates an internal relationship between tables in the underlying database to include interval information where it exists.

Included in the properties are boolean indicators of whether or not a given core/cutting record has related photos, "analysis" files, and/or thin sections. Each of these related artifacts are quite valuable and somewhat untapped digital aspects of the CRC that we would like to make sure are included when someone discovers cores/cuttings through ScienceBase, the NDC, or some other web system. The photos of core and thin section scans are often of high enough quality and resolution to support some degree of analysis. The "analysis" documents consist of a variety of material related to the cores/cuttings in some way, but do contain some number of digital files from geochemical and other analyses that were returned to the CRC under agreement with companies who were given access to subsample or borrow samples over time.

Unfortunately, the records about these artifacts are currently only included on the rendered web pages for each CRC core or cutting. This sets us up to potentially scrape the information from the web pages. However, those web pages are accessed via an internal numeric identifier that is included in the MapServer layers but not included in the download option. The links to individual "report" pages are included in the web page rendering of a text search result but not the download.

Ultimately, in this case, this means we have to put together three distinct sets of information and then stitch them all together to get to reasonably complete records for each core and cutting record in the inventory.

* Download of the most presentable and complete inventory information with records duplicated by interval that needs to be regrouped on "Lib Num" to produce the items we want in the catalog
* MapServer layer query to return "raw" data for the collections, the internal id value we need to build links to web pages, and potentially a better form of what is inherently valid geometry
* Web pages that can be scraped to retrieve a table of thin sections (including links to scans), links to high resolution photos of boxes of core, and links to documents/files associated with records in the inventory

This is a not uncommon situation with situations like this. Different investments have been made over time into various ways of managing an active collection or inventorying an archive collection. Demand has sometimes driven investment in building some type of online exposure of the information, usually built with a combination of custom code and perhaps some type of off the shelf tools like ArcGIS server. The web app has really been the point in these endeavors with a particular group of stakeholders in mind, and it has not been a priority to build a generalized API for data access and distribution.

In these situations, some type of display logic is built into the application level of the system. This is actually a level of improving semantic interoperability in the data, but it only benefits a relatively narrow audience. To make sense of it in some other context, multiple methods of interface to the information often need to be stitched together like we're doing here.

Another approach to this situation for the CRC and others may be to leverage the more recent developments coming from the semantic web and linked data world. Web pages that present information for humans (aka meatware) can be tweaked to incorporate the extra structure that makes them conducive to understanding by machines (aka software). I did take a quick look at how the CRC web app is indexed in public search to see if anything could be leveraged there. A [site-limiting search](https://www.google.com/search?q=site%3Amy.usgs.gov%2Fcrcwc) in Google (almost always my first rough look) turned up 276 results, far short of proven public exposure for the thousands of records. The site does not provide any type of sitemap approach or other method to help search engines index its "core findable units" (landing pages for each core and cutting record). The search results include [pages](https://my.usgs.gov/crcwc/core/report/80145) that are likely added to public indexes via serendipity when they are linked to from some other place that is more optimized for public search. A quick look at the landing pages themselves reveals that they do not present any structured metadata (schema.org or otherwise) to the web.

## Data Enrichment
A final step in this experiment involved developing a process to reach out and retrieve related information from a third party source that can be used to enrich the CRC records. In this case, I leveraged the work that the Macrostrat team has done to assemble geologic mapping data from multiple sources and resolutions and provide it for geologic context. This is ultimately one of a number of "enhancers" that we may want to put in place for the entire National Digital Catalog to continuously monitor associated data systems for new information and then run to bring value back to the NDC itself. As an experiment here where I could tee up specific properties as tags in the resulting ScienceBase Items, I used one of the simpler, high level APIs from Macrostrat to retrieve information on each unique point coordinate in the CRC Well Catalog and incorporate rock types, geologic map units, geologic age (surface), and stratigraphic unit information as tags. We can now examine these together with related tags created from the CRC source data for discussions on where to take this engineering in future.

## Data Assembly
Once all source data are brought together and enhancements generated and cached, I wrote a process to assemble everything into new ScienceBase Items, replacing the older items in the two collections. This makes the ~62K items immediately available in what is the live National Digital Catalog today. While the ScienceBase instantiation of the NDC has a number of limitations in terms of the specialized searches that are of interest to the geoscience community, it does a reasonable job of bringing everything together for at least some limited search and discovery functionality. Working within the constraints of the ScienceBase Item model in the way that I have with this project also sets up further discussion about both syntactic and semantic data integration challenges and potential responses.

## Recommendations
Ultimately, we want every source for the NDC to have some kind of logical starting point, the origin of registration for each collection being shared that exposes the full slate of collection information for the NDC (or any other online system) to pick up and work with. Users should be able to discover collection items in specialized NDC searches (through APIs and web tools), through public search engines, and through any other tool that someone wants to build against these public data. Alternatively, the NDC itself could be the tool that provides all of that functionality while dealing with all of the backend messy work of putting things together like this project has demonstrated. However, each case like this takes a certain degree of time to build out and make operational. Any time anything changes on the back end, the process breaks and has to be revisited. All in all, that is likely not a sustainable or scalable aproach. In the case of the CRC, specifically, there are a couple of logical steps that would markedly improve the situation.

### Syntactic Integration Recommendations
1. Improve the properties ArcGIS MapServer layers in the same way that the text search app does, employing property names that are more clear, easy to use, harmonized across the collections, and documented with metadata.
2. Incorporate properties in the MapServer layers to include the related artifacts - photos, thin sections, analysis files. While most expressions of GeoJSON properties are simple key/value pairs like the current CRC layers, the [RFC7946](https://tools.ietf.org/html/rfc7946) specification indicates that properties can be any type of valid JSON, including properties that are objects or arrays similar to what this project resulted in for the cores and cuttings structures that built the ScienceBase Items. It is not known whether or not the ArcGIS Server implementation will support this approach, but it should be explored.
3. As an alternative or in addition to the ArcGIS Server approach, consider embedding schema.org metadata as JSON-LD in the CRC Well Catalog web site landing pages for each item in the collections and providing a sitemap to help search engines and indexers hone in on the key indexable pages. This could serve as a different type of primary source for the NDC and would have the added benefit of optimizing public search. While there is no specific schema.org schema set up for things like rock cores and cuttings, they are certainly [Things](https://schema.org/Thing) and the digital records describing these physical artifacts could loosely be interpreted as [CreativeWork](https://schema.org/CreativeWork). Put together with digital artifacts like many of the items in these collections, it would not be unreasonable to base the schema on [Dataset](https://schema.org/Dataset) and put together into a [DataCatalog](https://schema.org/DataCatalog) or [Collection](https://schema.org/Collection) level. In addition, related schemas such as [Person](https://schema.org/Person), [Organization](https://schema.org/Organization), [Place](https://schema.org/Place) and others can be used to inform how the metadata elements are tagged for expression on the web and knowledge graphs.

### Semantic Integration Recommendations
1. Examine key properties in the data, particularly geologic formation and age at depth, against established vocabularies to determine alignment and record applicable identifiers to those vocabularies in the data. Expose term identifiers and accepted name strings in services intended for distribution of the data so values can be compared effectively with other data systems.
2. It may be necessary to improve depth information for intervals with additional details on how these were determined from underlying data (e.g., depth from top of well head or from surface) and any known uncertainty quantification to go along with interpreting and using semantically aligned geologic formation and age information.
3. Examine other fields of information to determine if internal harmonization can be achieved. For instance, lease, well name, operator, and other string values are currently seen with multiple spelling forms and other relatively simple issues that still require additional steps at the point of integration before they can be used effectively as more than labels.