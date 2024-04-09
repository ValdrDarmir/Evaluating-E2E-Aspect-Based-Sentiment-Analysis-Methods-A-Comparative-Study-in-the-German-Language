import xml.etree.ElementTree as ET
import sys
import os

"""
This Python script performs various tasks related to processing XML data:

1. amountEntries(name): Counts the number of entries in an XML file by checking for the presence of "id" attributes in all elements.
2. amountOpinions(name): Counts the total number of opinions in an XML file by summing the counts of <Opinion> elements within <Document> elements.
3. amountSentiment(name, polarityValue): Counts the number of opinions with a specific polarity value (positive, negative, or neutral) in an XML file.
4. storeInformation(): Stores information about the corpus including the total number of entries, total opinions, and counts of positive, negative, and neutral opinions in a text file.
5. sentenceLengthSem(): Computes the average sentence length for different corpora defined in the 'nameList' variable.
6. sentenceLength(): Computes the average sentence length for specific XML files and calls sentenceLengthSem() for additional corpora.

Source: This summary was made by ChatGPT 3.5
"""


# count the amount of entries in a xml file
def amountEntries(name):
    count = 0
    if os.path.exists(f"output/{name}"):
        tree = ET.parse(f"output/{name}")
        root = tree.getroot()
        for element in root.iter():
            if "id" in element.attrib:
                count += 1
        print(f"Amount entries: {count}")
        return count


# count the amount of opinions in the file
def amountOpinions(name):
    count = 0
    if os.path.exists(f"output/{name}"):
        tree = ET.parse(f"output/{name}")
        root = tree.getroot()
        for entry in root.findall("Document"):
            opinions = entry.find('Opinions')
            if opinions is not None:
                count += len(opinions.findall('Opinion'))
        print(f"Amount of opinions in the file: {count}")
        return count


# count the amount of sentiments in the file
def amountSentiment(name, polarityValue):
    count = 0
    if os.path.exists(f"output/{name}"):
        tree = ET.parse(f"output/{name}")
        root = tree.getroot()
        for entry in root.findall("Document"):
            opinions = entry.find('Opinions')
            if opinions is not None:
                for opinion in opinions.findall('Opinion'):
                    # print(ET.tostring(opinion))
                    polarity = opinion.get('polarity')
                    if polarity is not None:
                        if polarity == polarityValue:
                            count += 1
        return count


# store the information in a file
def storeInformation():
    # name = "GermEval_Test_Clean.xml"
    # name = "GermEval_Train_Clean.xml"
    # name = "MobASA_Test_Clean.xml"
    name = "MobASA_Train_Clean.xml"
    name = "StudyCheck.xml"
    entries = amountEntries(name)
    opinions = amountOpinions(name)
    amount_negativ = amountSentiment(name, "negative")
    amount_positiv = amountSentiment(name, "positive")
    amount_neutral = amountSentiment(name, "neutral")

    file_name = name.rsplit("_", 1)[0] + str("_analysis")
    message = f"Corpus: {name} \nTotal Entries: {entries} \nTotal Opinions: {opinions} \nTotal positive opinions: {
        amount_positiv} \nTotal negative opinions: {amount_negativ} \nTotal neutral opinions: {amount_neutral}"
    with open(f"output/{file_name}.txt", "w") as file:
        file.write(message)


# get the sentence length of the SemEval corpus for the different subsets, Needed in discussion/limitations compare with GermEval length
def sentenceLengthSem():
    name_list = ["Laptop_Train_v2.xml", "Laptops_Test_Gold.xml",
                 "Restaurants_Test_Gold.xml", "Restaurants_Train_v2.xml"]
    total_words = 0
    total_documents = 0
    for name in name_list:
        if os.path.exists(f"input/{name}"):
            tree = ET.parse(f"input/{name}")
            root = tree.getroot()

            amount_documents = 0
            word_count = 0
            for entry in root.findall("sentence"):
                amount_documents += 1
                text = entry.find('text').text
                words = text.split()

                word_count += len(words)
            total_words += word_count
            total_documents += amount_documents
            average_subset = word_count/amount_documents
            print(f"Corpus: {name}\nAverage : {average_subset}")

    total_average = total_words/total_documents
    print(f"All:\nAverage : {total_average}")


# get the sentence length of the GermEval/MobASA corpus for the different subsets, Needed in discussion/limitations compare with SemEval length
def sentenceLength():
    name_list = ["MobASA_Train_Clean.xml", "MobASA_Test_Clean.xml",
                 "GermEval_Train_Clean.xml", "GermEval_Test_Clean.xml"]
    total_words = 0
    total_documents = 0
    for name in name_list:
        if os.path.exists(f"output/{name}"):
            tree = ET.parse(f"output/{name}")
            root = tree.getroot()

            amount_documents = 0
            word_count = 0
            for entry in root.findall("Document"):
                amount_documents += 1
                text = entry.find('text').text
                words = text.split()

                word_count += len(words)
            total_words += word_count
            total_documents += amount_documents
            average_subset = word_count/amount_documents
            print(f"Corpus: {name}\nAverage : {average_subset}")
    total_average = total_words/total_documents
    print(f"All:\nAverage : {total_average}")
    sentenceLengthSem()


def main():
    storeInformation()


if __name__ == '__main__':
    sys.exit(main())
