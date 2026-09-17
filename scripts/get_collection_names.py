# Get all Earthdata collection names
#
# 9/16/2026 Cole K
# Uses the earthaccess to make a table of collection shortnames, conceptIDs, etc.

# Import Packages
import earthaccess
import pandas as pd

# Query CMR for all collections
cloud_collections = earthaccess.search_datasets(cloud_hosted=True, has_granules=True, count=-1)
other_collections = earthaccess.search_datasets(cloud_hosted=False, has_granules=True, count=-1)
collections = cloud_collections + other_collections

# Loop through and collect info from all collections
rows = []
for c in collections:
    try:
        file_format = c["umm"]["ArchiveAndDistributionInformation"]["FileArchiveInformation"][0][
            "Format"
        ]
    except Exception as e:
        file_size = "unknown"
        print(f"Something went wrong: {e}")

    try:
        file_size = c["umm"]["ArchiveAndDistributionInformation"]["FileArchiveInformation"][0][
            "AverageFileSize"
        ]

    except Exception as e:
        file_size = "unknown"
        print(f"Something went wrong: {e}")

    rows.append(
        {
            "DAAC": c["meta"]["provider-id"],
            "Variables": c["meta"]["has-variables"],
            "Concept_ID": c["meta"]["concept-id"],
            "Shortname": c["umm"]["ShortName"] + "." + c["umm"]["Version"],
            "Longname": c["umm"]["EntryTitle"],
            "File Format": file_format,
            "File Size": file_size,
        }
    )

df = pd.DataFrame(rows)

df.to_csv("./data/earthdata_collections_2.csv", index=False)
