import json


def sb_item_from_crcwc(crc_record):
    sb_item = {
        "parentId": crc_record["sb_parent_id"],
        "identifiers": crc_identifiers(crc_record),
        "title": crc_title(crc_record),
        "body": crc_body(crc_record),
        "contacts": crc_contacts(crc_record),
        "provenance": crc_provenance(),
        "browseCategories": ["Physical Item"],
        "webLinks": crc_weblinks(crc_record)
    }
    
    if isinstance(crc_record["Latitude"], str):
        sb_item["spatial"] = crc_location(crc_record)
    
    item_tags = crc_tags(crc_record)
    if item_tags is not None:
        sb_item["tags"] = item_tags
    
    return sb_item


def crc_identifiers(crc_record):
    identifiers = [
        {
            "type": "uniqueKey",
            "scheme": "CRC Well Catalog Database ID",
            "key": crc_record["crcwc_url"].split("/")[-1]
        },
        {
            "type": "uniqueKey",
            "scheme": "CRC Library Number",
            "key": crc_record["Lib Num"]
        }
    ]
    
    if isinstance(crc_record["API Num"], str):
        identifiers.append({
            "type": "uniqueKey",
            "scheme": "American Petroleum Institute Number",
            "key": crc_record["API Num"]
        })
    
    return identifiers


def crc_title(crc_record):
    return f'Core Research Center {crc_record["crc_collection_name"].capitalize()} {crc_record["Lib Num"]}'


def crc_body(crc_record):
    body_string = f'<p>Core Research Center, {crc_record["crc_collection_name"]} {crc_record["Lib Num"]}, from well operated by {crc_record["Operator"]}</p>'
    body_string+=f"<h4>Raw Properties from download, web scrape, MapServer, and Macrostrat API</h4>"

    body_string+="<div>"
    body_string+=json.dumps(crc_record)
    body_string+="</div>"

    return body_string


def crc_contacts(crc_record):
    contacts = [
        {
            "name": "Core Research Center",
            "oldPartyId": 17172,
            "type": "Data Owner",
            "contactType": "organization"
        },
        {
            "name": "Jeannine Honey",
            "oldPartyId": 4685,
            "type": "Data Steward",
            "contactType": "person"
        }
    ]
    
    if crc_record["Operator"] is not None:
        contacts.append(
            {
                "name": crc_record["Operator"],
                "type": "Site Operator",
                "contactType": "organization"
            }
        )
    
    return contacts


def crc_provenance():
    return {"annotation": "Harvested and assembled from: CRC web site download, CRC web site scrape, MapServer layers, Macrostrat API. Data were assembled in an intermediary MongoDB instance, structured with code to product ScienceBase Items, and loaded to ScienceBase collection."}


def crc_weblinks(crc_record):
    web_links = [
        {
            "type": "webLink",
            "typeLabel": "Web Link",
            "uri": crc_record["crcwc_url"],
            "rel": "related",
            "title": "Core Research Center Well Catalog Web Page",
            "hidden": False,
            "itemWebLinkTypeId": "4f4e475de4b07f02db47debf"
        }
    ]
    
    if "documents" in crc_record.keys():
        for doc_link in [d for d in crc_record["documents"] if len(d) > 0]:
            web_links.append(
                {
                    "type": "download",
                    "typeLabel": "Download",
                    "uri": doc_link,
                    "rel": "related",
                    "title": f"Core Research Center Analysis File {doc_link.split('/')[-1]}",
                    "hidden": False,
                    "itemWebLinkTypeId": "4f4e475de4b07f02db47dec0"
                }
            )

    if "photos" in crc_record.keys():
        for doc_link in [p for p in crc_record["photos"] if len(p) > 0]:
            web_links.append(
                {
                    "type": "download",
                    "typeLabel": "Photo",
                    "uri": doc_link,
                    "rel": "related",
                    "title": f"Core Research Center Photo {doc_link.split('/')[-1]}",
                    "hidden": False,
                    "itemWebLinkTypeId": "4f4e475de4b07f02db47dec0"
                }
            )

    if "thin_sections" in crc_record.keys():
        for doc_link in [i["View"] for i in crc_record["thin_sections"] if i["View"] != ""]:
            web_links.append(
                {
                    "type": "download",
                    "typeLabel": "Thin Section",
                    "uri": doc_link,
                    "rel": "related",
                    "title": f"Core Research Center Thin Section {doc_link.split('/')[-1]}",
                    "hidden": False,
                    "itemWebLinkTypeId": "4f4e475de4b07f02db47dec0"
                }
            )

    return web_links


def crc_location(crc_record):
    spatial = {
        "representationalPoint": [
            float(crc_record["Longitude"]), 
            float(crc_record["Latitude"])
        ]
    }
    
    return spatial


def crc_tags(crc_record):
    tags = list()
    
    for interval in crc_record["intervals"]:
        if interval["Formation"] not in [None, "UNKNOWN"]:
            tags.append(
                {
                    "type": "Theme",
                    "scheme": "Geologic Formation at Depth",
                    "name": interval["Formation"]
                }
            )
        if interval["Age"] not in [None, "UNKN"]:
            tags.append(
                {
                    "type": "Theme",
                    "scheme": "Geologic Age at Depth",
                    "name": interval["Age"]
                }
            )
        
    if "surface_rocktype" in crc_record.keys():
        for rock_type in [t for t in crc_record["surface_rocktype"] if t is not None]:
            tags.append(
                {
                    "type": "Theme",
                    "scheme": "Surface Rock Type",
                    "name": rock_type[0:80]
                }
            )

    if "surface_age" in crc_record.keys() and len(crc_record["surface_age"]) > 0:
        tags.append(
            {
                "type": "Theme",
                "scheme": "Surface Geologic Age",
                "name": crc_record["surface_age"][0:80]
            }
        )

    if "gmu_name" in crc_record.keys() and len(crc_record["gmu_name"]) > 0:
        tags.append(
            {
                "type": "Theme",
                "scheme": "Geologic Map Unit Name",
                "name": crc_record["gmu_name"][0:80]
            }
        )
            
    if "strat_unit" in crc_record.keys() and len(crc_record["strat_unit"]) > 0:
        tags.append(
            {
                "type": "Theme",
                "scheme": "Stratigraphic Unit Name",
                "name": crc_record["strat_unit"][0:80]
            }
        )

    if len(tags) == 0:
        return None
    
    return tags
