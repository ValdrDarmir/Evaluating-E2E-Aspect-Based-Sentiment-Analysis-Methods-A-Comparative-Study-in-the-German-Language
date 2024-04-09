import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import sys
import os

"""
This Python script processes an XML file containing opinion-related data. It performs several operations to clean and standardize the XML structure:

1. Remove No Relevance: Removes <Document> elements with a <relevance> value of "false".
2. Remove No Opinions: Removes <Document> elements without any <Opinion> elements or with a <target> value of "NULL".
3. Remove Star Targets: Removes <Document> elements containing <Opinion> elements with a <target> attribute containing an asterisk '*'.
4. Save XML File: Writes the modified XML structure to an output file.
5. Split File: Divides the XML file into multiple sub-files.

Source: this summary was made by ChatGPT 3.5
"""


# remove entries from the xml file without relevance
def removeNoRelevance(fileName):
    if os.path.exists(f"input/{fileName}"):
        tree = ET.parse(f"input/{fileName}")
        root = tree.getroot()
        for document in root.findall("Document"):
            relevance = document.find("relevance").text
            if relevance == "false":
                root.remove(document)
        return root


# remove entries without a target (target = "NULL")
def removeNoOpinions(xml_file):
    for document in xml_file.findall("Document"):
        opinions = document.find('Opinions')
        if opinions is not None:
            for opinion in opinions.findall('Opinion'):
                # print(ET.tostring(opinion))
                target = opinion.get('target')
                if target == "NULL":
                    xml_file.remove(document)
    return xml_file


# removes opinions with a * contained in the target value; Necessary for the Graph-based approaches and easier prediction
def removeStarTargets(xml_file):
    for document in xml_file.findall("Document"):
        opinions = document.find('Opinions')
        if opinions is not None:
            for opinion in opinions.findall('Opinion'):
                # print(ET.tostring(opinion))
                target = opinion.get('target')

                def has_asterisk(string):
                    return '*' in string

                if has_asterisk(target):
                    print(target)
                    xml_file.remove(document)
                    break

    return xml_file


# save the new xml file, encoding for german chars
def saveXMLFile(xml_file, new_file_name):
    tree = ElementTree(xml_file)
    tree.write(f"output/{new_file_name}", encoding="utf-8", xml_declaration=True)


# split the files in 10 subsets
def splitFile(file_name, splits):

    if os.path.exists(f"output/{file_name}"):
        tree = ET.parse(f"output/{file_name}")
        root = tree.getroot()
        num_elements = len(root)
        elements_per_subfile = num_elements // splits

        # this code is based on an answer from ChatGPT
        for i in range(splits):
            start_index = i * elements_per_subfile
            end_index = (i + 1) * elements_per_subfile if i < splits - 1 else num_elements
            sub_root = ET.Element(root.tag)
            sub_root.extend(root[start_index:end_index])
            sub_tree = ET.ElementTree(sub_root)
            file_name = file_name.replace(".xml", "")
            sub_tree.write(f"output/{file_name}_{i+1}.xml", encoding="utf-8", xml_declaration=True)


# Count the amount of documents
def countOriginal():
    file_name = "GermEval_Test.xml"
    count = 0
    if os.path.exists(f"input/{file_name}"):
        tree = ET.parse(f"input/{file_name}")
        root = tree.getroot()
        for document in root.findall("Document"):
            count += 1
    print(count)


# change file_name for different datasets
def main():
    file_name = "MobASA_Test.xml"
    new_file_name = "MobASA_Test_Clean.xml"
    make_splits = True

    xml_file = removeNoRelevance(file_name)
    xml_file = removeNoOpinions(xml_file)
    # remove function for MobASA
    # xmlFile = removeStarTargets(xmlFile)
    saveXMLFile(xml_file, new_file_name)

    if make_splits is True:
        splitFile(new_file_name, 10)


if __name__ == '__main__':
    sys.exit(main())
