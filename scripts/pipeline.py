# Data Use Code Snippet generation pipeline
#
# Inputs: list of Earthdata collections
# Outputs: code snippets

# %% Import packages and setup Anthropic API client ---------------------------------------------------

import csv
import json
import subprocess

import earthaccess
from anthropic import Anthropic

print("Using Anthropic's Claude LLM")
client = Anthropic(
    base_url="https://proxy.fast.luna.nasa.gov",
)

N = 1  # set to a small number for debugging (e.g. N=1 stops loop after generating one code snippet)

# %% Run snippet generation workflow ------------------------------------------------------------------

list_of_collections = "./data/earthdata_collections.csv"

with open(list_of_collections) as f:
    # DictReader reads the first line as column headers.
    reader = csv.DictReader(f)

    row_count = 0

    for row in reader:
        # Stop the loop after N collections (since all rows would take too long for testing/development)
        if row_count > N:
            break

        conceptID = row["Concept_ID"]
        fileformat = row["File Format"]
        shortname = row["Shortname"]
        print(fileformat)

        # Get collection metadata ------------------------------------------
        earthaccess.login()
        collections = earthaccess.search_datasets(concept_id=conceptID)
        collection = collections[0]
        umm_metadata = collection["umm"]

        # Print some metadata
        print(f"ShortName: {umm_metadata.get('ShortName')}")
        print(f"Version:   {umm_metadata.get('Version')}")
        print(f"Title:     {umm_metadata.get('EntryTitle')}")

        # Just keep the parts of the collection metadata that could help the LLM generate snippets
        relevant_keys = [
            "EntryTitle",
            "ShortName",
            "Version",
            "Abstract",
            "ProcessingLevel",
            "ScienceKeywords",
            "SpatialExtent",
            "TemporalExtents",
            "Platforms",  # Satellite/Instrument info
            "ArchiveAndDistributionInformation",  # File format (e.g., NetCDF) and average file size
            "DirectDistributionInformation",
            "RelatedUrls",  # Contains links to READMEs, ATBDs, and data access
        ]

        # Create a new dictionary containing only the keys that exist in the metadata
        filtered_metadata = {key: umm_metadata[key] for key in relevant_keys if key in umm_metadata}

        # Convert to a formatted JSON string so it is easier for the LLM to read
        metadata_string = json.dumps(filtered_metadata, indent=2)

        # Generate code snippet ------------------------------------------
        instructions_file = "./specs/SPEC-001-snippets.md"
        with open(instructions_file, encoding="utf-8") as file:
            file_content = file.read()

        # Combine instructions from SPEC*.md with collection metadata from CMR to create a generation prompt for the LLM
        generation_prompt = f"""
            Draft a code access snippet. Here are specs and metadata:
            <specifications>
            {file_content}
            </specifications>
            <metadata>
            {metadata_string}
            </metadata>
        """
        print(generation_prompt)

        # Send prompt to LLM
        api_response = client.messages.create(
            model="claude-4-sonnet",
            max_tokens=1000,
            messages=[{"role": "user", "content": generation_prompt}],
        )

        # Print response text
        code_snippet = api_response.content[0].text
        print(code_snippet)

        # Save outputs ----------------------------------------------------

        output_filename_prompt = f"./output/prompt_{shortname}.md"
        output_filename_snippet = f"./output/snippet_{shortname}.py"

        with open(output_filename_snippet, "w", encoding="utf-8") as file:
            file.write(code_snippet)
        with open(output_filename_prompt, "w", encoding="utf-8") as file:
            file.write(generation_prompt)

        print(f"Successfully saved the generated code to {output_filename_snippet}")

        # Run code snippet ------------------------------------------------

        print(f"Running {output_filename_snippet}...")

        try:
            result = subprocess.run(
                ["python", output_filename_snippet], capture_output=True, text=True, timeout=300
            )

            # 4. Test if it worked
            if result.returncode == 0:
                print(f"✅ SUCCESS for {shortname}!")
                print("--- Output ---")
                print(result.stdout)
                print("--------------")
            else:
                print(f"❌ FAILED for {shortname}!")
                print("--- Error Traceback ---")
                print(result.stderr)
                print("-----------------------")

        except subprocess.TimeoutExpired:
            print(f"⏳ TIMEOUT: The script for {shortname} took too long to run.")
        except Exception as e:
            print(f"⚠️ UNEXPECTED ERROR while trying to execute {shortname}: {e}")

        row_count += 1  # move to the next collection

# Not used ------------------------------------------------------------------------------------

# # OpenAI API call
# from openai import OpenAI
# # Testing OpenAI API access
# print("openAI")
# client = OpenAI(
#     base_url = "https://proxy.fast.luna.nasa.gov"
# )
# api_response = client.chat.completions.create(
#     model = "gpt-4o-mini", # change to sonnet 5.5 if possible (Anthropic)
#     messages = [
#             {
#                 "role":"user",
#                 "content":"Give me three moose facts",
#             }
#         ]
#    )
# print(api_response.choices[0].message.content)

# %%

#  # Lookup data access method based on file format
#         match fileformat:
#             case "NetCDF":
#                 # use NetCDF4 access method
#                 try:
#                     # assumes, for now, all NetCDF files can be accessed the same way
#                     result = acc.access_netcdf(conceptID, umm_metadata)
#                     print(f"Successfully accessed {shortname} / {conceptID} / {fileformat}")
#                     print(
#                         f"Saved access script to {'script_path'}"
#                     )  # need to implement saving, see strawman ducs
#                     print(f"Saved metadata to {'metadata_path'}")

#                 except Exception as e:
#                     print(
#                         f"Error trying to access data for {shortname} / {conceptID} / {fileformat}"
#                     )
#                     print(f"Error details: {e}")

#             case "HDF5":
#                 result = "two"
#             case _:
#                 result = "unknown"
#         print(result)
