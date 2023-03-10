import os
import re
import yaml
import json
from bs4 import BeautifulSoup

def find_normative_tables(html_file, output_file):
    """
    Find normative tables in an HTML file and save the IDs of the greatgrandparent elements to a YAML file.

    Args:
        html_file (str): Path to the HTML file to search.
        output_file (str): Path to the YAML file to save the list of normative IDs.

    Returns:
        None
    """
    # Load the HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all <a> elements that meet the criteria
    normative_links = soup.find_all("a", href="versions.html#std-process", title="Standards Status = Normative")

    # Create a list to store the IDs of normative tables
    normative_ids = []

    # Loop over the normative links
    for link in normative_links:
        # Find the greatgrandparent element that contains the <a>
        greatgrandparent = link.find_parent().find_parent().find_parent()
        # Check if the greatgrandparent element is a table
        if greatgrandparent.name == "table":
            # Get the ID of the greatgrandparent element and add it to the list
            normative_ids.append(greatgrandparent.get("id"))
        else:
            # Print an error message if the greatgrandparent element is not a table
            print(f"Error: Element with ID {greatgrandparent.get('id')} is not a table.")

    # Save the list of normative table IDs as a YAML file
    with open(output_file, "w") as f:
        yaml.dump(normative_ids, f)
        return normative_ids


def find_normative_docs(html_file, output_file):
    """
    Find normative documents in an HTML file and save the list of document names to a YAML file.

    Args:
        html_file (str): Path to the HTML file to search.
        output_file (str): Path to the YAML file to save the list of document names.

    Returns:
        None
    """
    # Load the HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all <a> elements that have href="versions.html#std-process" and title="Normative Content"
    normative_links = soup.find_all("a", href="versions.html#std-process", title="Normative Content")

    # Create a list to store the document names
    normative_docs = []

    # Loop over the normative links
    for link in normative_links:
        # Find the preceding <a> element in the same <li>
        prev_link = link.find_previous_sibling("a")
        # Check if the preceding <a> element exists
        if prev_link:
            # Get the text of the preceding <a> element and add it to the list of document names
            normative_docs.append(prev_link.get_text(strip=True))

    # Save the list of document names as a YAML file
    with open(output_file, "w") as f:
        yaml.dump(normative_docs, f)
        return normative_docs




def find_normatives_in_reslist(html_file, output_file):
    """
    Find normative resources in an HTML file and save the list of resource names to a YAML file.

    Args:
        html_file (str): Path to the HTML file to search.
        output_file (str): Path to the YAML file to save the list of resource names.

    Returns:
        None
    """
    # Load the HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all <a> elements that have href="versions.html#std-process" and title="Normative Content"
    normative_links = soup.find_all("a", href="versions.html#std-process", title="Normative Content")

    # Create a list to store the resource names
    normative_resources = []

    # Loop over the normative links
    for link in normative_links:
        # Find the parent <a> element
        parent_link = link.previous_element.previous_element
        # Check if the parent <a> element exists
        if parent_link:
            # Get the text of the parent <a> element and add it to the list of resource names
            normative_resources.append(parent_link.text.strip().split()[0])

    # Save the list of resource names as a YAML file
    with open(output_file, "w") as f:
        yaml.dump(normative_resources, f)
        return normative_resources



# with open("normative.yaml", "w") as f:
#     f.write("")  # Clear the file if it exists
# find_normative_tables("pages/datatypes.html", "normativedatatypes")
# find_normative_docs("pages/documentation.html", "normativesindocumentation")
# find_normative_resources("pages/resourcelist.html", "normativesinreslist")

# # Load the results from the YAML file and print them
# with open("normative.yaml", "r") as f:
#     normative_data = yaml.safe_load(f)
#     print(normative_data)




def compare_normatives_and_sds(normatives_file, sds_file, output_file):
    """
    Compare the entries in two YAML files and create a new YAML file with three lists:
    - Entries that can be found in both files
    - Entries that can be found in the normatives file but not in the SDs file
    - Entries that can be found in the SDs file but not in the normatives file

    Args:
        normatives_file (str): Path to the normatives YAML file.
        sds_file (str): Path to the normative_SDs YAML file.
        output_file (str): Path to the output YAML file.

    Returns:
        None
    """
    # Load the normatives file
    with open(normatives_file, "r") as f:
        normatives_data = yaml.safe_load(f)

    # Remove duplicates from normatives_data
    for section_name, section_data in normatives_data.items():
        normatives_data[section_name] = list(set(section_data))

    # Load the SDs file
    with open(sds_file, "r") as f:
        sds_data = yaml.safe_load(f)

    # Create three lists to store the results
    both_lists = []
    normatives_only = []
    sds_only = []

    # Find entries that can be found in both files
    for section_name, section_data in normatives_data.items():
        if isinstance(sds_data, list):
            both_entries = list(set(section_data).intersection(set(sds_data)))
        else:
            both_entries = list(set(section_data).intersection(set(sds_data[section_name])))
        both_lists.extend(both_entries)

    # Find entries that can be found in the normatives file but not in the SDs file
    for section_name, section_data in normatives_data.items():
        if isinstance(sds_data, list):
            normatives_only.extend(list(set(section_data).difference(set(sds_data))))
        elif section_name not in sds_data:
            normatives_only.extend(section_data)
        else:
            normatives_only.extend(list(set(section_data).difference(set(sds_data[section_name]))))

    # Find entries that can be found in the SDs file but not in the normatives file
    if isinstance(sds_data, list):
        sds_only = list(set(sds_data).difference(set(both_lists)))
    else:
        for section_name, section_data in sds_data.items():
            if section_name not in normatives_data:
                sds_only.extend(section_data)
            else:
                sds_only.extend(list(set(section_data).difference(set(normatives_data[section_name]))))

    # Save the results to a new YAML file
    with open(output_file, "w") as f:
        yaml.dump({"Both": both_lists, "Normatives in pages only": normatives_only, "SDs Only": sds_only}, f)








def find_normative_resources(package_folder, output_file):

    # List to store the normative SDs
    normative_sds = []

    # Loop over all the files in the package folder
    for file_name in os.listdir(package_folder):
        # Check if the file is a JSON file and starts with "StructureDefinition-"
        if file_name.endswith(".json") and file_name.startswith("StructureDefinition-"):
            # Load the JSON file
            with open(os.path.join(package_folder, file_name), "r", encoding="utf-8") as f:
                sd = json.load(f)
                print(file_name)
            # Check if the SD has the desired value for "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status"
            if "extension" in sd and any(ext.get("url") == "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status" and ext.get("valueCode") == "normative" for ext in sd["extension"]):
                # Add the SD to the list of normative SDs
                normative_sds.append(sd["id"])

    # Save the list of normative SDs as a YAML file
    with open(output_file, "w") as f:
        yaml.dump(normative_sds, f)



def find_normative_valuesets(package_folder, output_file):
    # create an empty dictionary to store the valuesets and their corresponding StructureDef ids
    valuesets = []

    # loop through all files in the package folder
    for filename in os.listdir(package_folder):
        if filename.endswith(".json"):
            # open the file and load the JSON data
            with open(os.path.join(package_folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)

            # check if the StructureDef has the standards-status extension set to "normative"
            if ("resourceType" in data) and (data["resourceType"]=="StructureDefinition") and ("extension" in data) and any(
                ext.get("url") == "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status"
                and ext.get("valueCode") == "normative"
                for ext in data["extension"]
            ):
                # loop through the snapshot elements and find any that have a binding value set
                for element in data["snapshot"]["element"]:
                    if "binding" in element:
                        binding = element["binding"]
                        # check if the binding has a valueSet and extract the valueset id from the URL
                        if "valueSet" in binding:
                            valueset_url = binding["valueSet"]
                            valueset_id = valueset_url.split("/")[-1].split("|")[0]
                            valueset_path = os.path.join(package_folder, f"ValueSet-{valueset_id}.json")
                            # check if the valueset file exists and load the JSON data
                            if os.path.exists(valueset_path):
                                with open(valueset_path, "r", encoding="utf-8") as f:
                                    valueset_data = json.load(f)
                                # extract the vs status from the "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status" extension
                                vs_status = None
                                if "extension" in valueset_data:
                                    for ext in valueset_data["extension"]:
                                        if ext.get("url") == "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status":
                                            vs_status = ext.get("valueCode")
                                            break
                                valuesets.append({"resourceId":data["id"],"valueset": valueset_id, "status": vs_status})

    # save the valuesets dictionary as a YAML file
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(valuesets, f, default_flow_style=False)






def find_unreferenced_normative_valuesets(package_folder, valuesets_file, output_file):
    # Load the list of referenced normative valuesets from the valuesets_file
    with open(valuesets_file, "r", encoding="utf-8") as f:
        referenced_valuesets = yaml.safe_load(f)
    referenced_valueset_ids = [vs["valueset"] for vs in referenced_valuesets if vs.get("status") == "normative"]

    # Create an empty list to store the unreferenced normative valuesets
    unreferenced_valuesets = []

    # Loop through all files in the package folder
    for filename in os.listdir(package_folder):
        if filename.startswith("ValueSet-") and filename.endswith(".json"):
            # Open the file and load the JSON data
            with open(os.path.join(package_folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check if the ValueSet has the standards-status extension set to "normative"
            if ("resourceType" in data) and (data["resourceType"]=="ValueSet") and ("extension" in data) and any(
                ext.get("url") == "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status"
                and ext.get("valueCode") == "normative"
                for ext in data["extension"]
            ):
                # Check if the ValueSet is not in the referenced normative valuesets list
                valueset_id = data.get("id")
                if valueset_id and valueset_id not in referenced_valueset_ids:
                    unreferenced_valuesets.append(valueset_id)

    # Save the unreferenced normative valuesets as a YAML file
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(unreferenced_valuesets, f, default_flow_style=False)



def find_normatives_in_pages(pagesfolder,outputfile):

    normative_data ={}



#   Check for <a> that have href="versions.html#std-process", title="Standards Status = Normative"
#   Get the id of the table (greatgrandparent of the <a> element)
#   => output/t1-normativedatatypes.yaml
    normative_data["normativedatatypes"]=find_normative_tables(os.path.join(pagesfolder,"datatypes.html"), "output/t1-normativedatatypes.yaml")



#   Check for all <a> that have href="versions.html#std-process", title="Normative Content")
#   Get the content of the preceding <a> element
#   => output/t2-normativesindocumentation.yaml
    normative_data["normativesindocumentation"]=find_normative_docs(os.path.join(pagesfolder,"documentation.html"), "output/t2-normativesindocumentation.yaml")



#   Check for all <a> that have href="versions.html#std-process", title="Normative Content"), 
#   Get the text of the parent <a> element - and remove the extra stuff because the <a>s are nested here.
#   => output/t3-normativesinreslist.yaml
    normative_data["normativesinresourcelist"]=find_normatives_in_reslist(os.path.join(pagesfolder,"resourcelist.html"), "output/t3-normativesinreslist.yaml")

    with open(outputfile, "w") as f:
        f.write("")  # Clear the file if it exists
        yaml.dump(normative_data, f)


# 4. Put those all together
#   => 1-NormativesInPages.yaml
find_normatives_in_pages("pages","output/1-NormativesInPages.yaml")





# 5. Find the Normative resources:
#   Go through the package JSONs, identify the SDs with Normative status
#   => output/2-normativeSDs.yaml
find_normative_resources("package", "output/2-normativeSDs.yaml")





# 6. Compare the entries in the two lists (normative SDs and normatives found in docs) and create a new YAML file with three lists:
#   Entries that can be found in both files
#   Entries that can be found in the pages but not in the SDs
#   Entries that can be found in the SDs but not in the pages
#   => output/R3-comparison.yaml
compare_normatives_and_sds("output/1-NormativesInPages.yaml", "output/2-normativeSDs.yaml", "output/R3-comparison.yaml")


# 7. Find ValueSets that should not be normative
#   Go through the StructureDefs that have Normative status, 
#   For all valueset bindings, get the normative status from the corresponding ValueSet JSON
#   => output/2-Normative_sd_valuesets.yaml
find_normative_valuesets("package", "output/4-normative_sd_valuesets.yaml")        


# 8. List valuesets that need not be normative
#   Go through all the ValueSet JSONs that are Normative (from 1)
#   List those that are not referenced in the normative resources
find_unreferenced_normative_valuesets("package", "output/4-normative_sd_valuesets.yaml", "output/5-unexpected_normative_valuesets.yaml")



