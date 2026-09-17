# Data Use Code Snippet generation pipeline
#
# 9/16/2026 JRS
# Inputs: list of Earthdata collections
# Outputs: code snippets

import csv

import access_scripts as acc
import earthaccess

filename = "./data/earthdata_collections.csv"

with open(filename) as file:
    # DictReader reads the first line as column headers.
    reader = csv.DictReader(file)

    row_count = 0

    for row in reader:
        # Stop the loop after 2 collections (since all rows would take too long for testing/development)
        if row_count > 2:
            break

        conceptID = row["Concept_ID"]
        fileformat = row["File Format"]
        shortname = row["Shortname"]
        print(fileformat)

        # Get all collection metadata
        earthaccess.login()
        collections = earthaccess.search_datasets(concept_id=conceptID)
        collection = collections[0]
        umm_metadata = collection["umm"]

        # Print some metadata
        print(f"ShortName: {umm_metadata.get('ShortName')}")
        print(f"Version:   {umm_metadata.get('Version')}")
        print(f"Title:     {umm_metadata.get('EntryTitle')}")

        # Lookup data access method based on file format
        match fileformat:
            case "NetCDF":
                # use NetCDF4 access method
                try:
                    # assumes, for now, all NetCDF files can be accessed the same way
                    result = acc.access_netcdf(conceptID, umm_metadata)
                    print(f"Successfully accessed {shortname} / {conceptID} / {fileformat}")
                    print(
                        f"Saved access script to {'script_path'}"
                    )  # need to implement saving, see strawman ducs
                    print(f"Saved metadata to {'metadata_path'}")

                except Exception as e:
                    print(
                        f"Error trying to access data for {shortname} / {conceptID} / {fileformat}"
                    )
                    print(f"Error details: {e}")

            case "HDF5":
                result = "two"
            case _:
                result = "unknown"
        print(result)

        # Generate code snippet

        # Run code snippet

        # Test if it worked

        # Save outputs

        row_count += 1  # move to the next collection
