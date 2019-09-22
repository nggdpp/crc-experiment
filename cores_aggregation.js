db.getCollection("cores_raw").aggregate(

	// Pipeline
	[
		// Stage 1
		{
			$group: {
			    "_id": "$Lib Num",
			    "intervals": {"$push": "$$ROOT"}
			}
		},

		// Stage 2
		{
			$project: {
			    "_id": 0,
			    "Lib Num": "$_id",
			    "API Num": {"$arrayElemAt": [ "$intervals.API Num", 0 ]},
			    "Operator": {"$arrayElemAt": [ "$intervals.Operator", 0 ]},
			    "Well Name": {"$arrayElemAt": [ "$intervals.Well Name", 0 ]},
			    "Field": {"$arrayElemAt": [ "$intervals.Field", 0 ]},
			    "State": {"$arrayElemAt": ["$intervals.State", 0]},
			    "County": {"$arrayElemAt": ["$intervals.County", 0]},
			    "Type": {"$arrayElemAt": ["$intervals.Type", 0]},
			    "Photos": {"$arrayElemAt": ["$intervals.Photos", 0]},
			    "Thin Sec": {"$arrayElemAt": ["$intervals.Thin Sec", 0]},
			    "Analysis": {"$arrayElemAt": ["$intervals.Analysis", 0]},
			    "Latitude": {"$arrayElemAt": ["$intervals.Latitude", 0]},
			    "Longitude": {"$arrayElemAt": ["$intervals.Longitude", 0]},
			    "coordinates_geohash": {"$arrayElemAt": ["$intervals.coordinates_geohash", 0]},
			    "Source": {"$arrayElemAt": ["$intervals.Source", 0]},
			    "Security Flag": {"$arrayElemAt": ["$intervals.Security Flag", 0]},
			    "crc_collection_name" : {"$arrayElemAt": ["$intervals.crc_collection_name", 0]},
			    "sb_parent_id" : {"$arrayElemAt": ["$intervals.sb_parent_id", 0]},
			    "intervals": { 
			            "$map": { 
			                "input": "$intervals", 
			                "as": "m", 
			                "in": { 
			                    "Formation": "$$m.Formation", 
			                    "Age": "$$m.Age",
			                    "Min Depth": "$$m.Min Depth",
			                    "Max Depth": "$$m.Max Depth"
			                } 
			            } 
			        }
			}
		},

		// Stage 3
		{
			$lookup: // Equality Match
			{
			    from: "cores_from_mapserver",
			    localField: "Lib Num",
			    foreignField: "properties.libno",
			    as: "mapserver_data"
			}
		},

		// Stage 4
		{
			$project: {
			    "Lib Num": 1,
			    "API Num": 1,
			    "Operator": 1,
			    "Well Name": 1,
			    "Field": 1,
			    "State": 1,
			    "County": 1,
			    "Type": 1,
			    "Photos": 1,
			    "Thin Sec": 1,
			    "Analysis": 1,
			    "Latitude": 1,
			    "Longitude": 1,
			    "coordinates_geohash": 1,
			    "Source": 1,
			    "Security Flag": 1,
			    "crc_collection_name" : 1, 
			    "sb_parent_id" : 1,
			    "intervals": 1,
			    "crcwc_url": {$concat: ["https://my.usgs.gov/crcwc/core/report/", {$toString: {"$arrayElemAt": ["$mapserver_data.id", 0]}}]}
			}
		},

		// Stage 5
		{
			$lookup: // Equality Match
			{
			    from: "scraped_web_pages",
			    localField: "crcwc_url",
			    foreignField: "source",
			    as: "scrape"
			}
		},

		// Stage 6
		{
			$project: {
			    "Lib Num": 1,
			    "API Num": 1,
			    "Operator": 1,
			    "Well Name": 1,
			    "Field": 1,
			    "State": 1,
			    "County": 1,
			    "Type": 1,
			    "Photos": 1,
			    "Thin Sec": 1,
			    "Analysis": 1,
			    "Latitude": 1,
			    "Longitude": 1,
			    "coordinates_geohash": 1,
			    "Source": 1,
			    "Security Flag": 1,
			    "crc_collection_name" : 1, 
			    "sb_parent_id" : 1,
			    "intervals": 1,
			    "crcwc_url": 1,
			    "documents": {"$arrayElemAt": ["$scrape.documents", 0]},
			    "photos": {"$arrayElemAt": ["$scrape.photos", 0]},
			    "thin_sections": {"$arrayElemAt": ["$scrape.thin_sections", 0]}
			}
		},

		// Stage 7
		{
			$lookup: // Equality Match
			{
			    from: "gmu_context",
			    localField: "coordinates_geohash",
			    foreignField: "coordinates_geohash",
			    as: "gmu_context"
			}
		},

		// Stage 8
		{
			$project: {
			    "Lib Num": 1,
			    "API Num": 1,
			    "Operator": 1,
			    "Well Name": 1,
			    "Field": 1,
			    "State": 1,
			    "County": 1,
			    "Type": 1,
			    "Photos": 1,
			    "Thin Sec": 1,
			    "Analysis": 1,
			    "Latitude": 1,
			    "Longitude": 1,
			    "coordinates_geohash": 1,
			    "Source": 1,
			    "Security Flag": 1,
			    "crc_collection_name" : 1, 
			    "sb_parent_id" : 1,
			    "intervals": 1,
			    "crcwc_url": 1,
			    "documents": 1,
			    "photos": 1,
			    "thin_sections": 1,
			    "surface_rocktype": {"$arrayElemAt": ["$gmu_context.data.rocktype", 0]},
			    "surface_age": {"$arrayElemAt": ["$gmu_context.data.age", 0]},
			    "gmu_name": {"$arrayElemAt": ["$gmu_context.data.name", 0]},
			    "strat_unit": {"$arrayElemAt": ["$gmu_context.data.strat_unit", 0]},
			    "gmu_ref": {"$arrayElemAt": ["$gmu_context.data.map_ref.url", 0]}
			}
		},

		// Stage 9
		{
			$match: {
			
			}
		},

		// Stage 10
		{
			$out: "cores"
		},
	],

	// Options
	{
		allowDiskUse: true
	}

	// Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

);
