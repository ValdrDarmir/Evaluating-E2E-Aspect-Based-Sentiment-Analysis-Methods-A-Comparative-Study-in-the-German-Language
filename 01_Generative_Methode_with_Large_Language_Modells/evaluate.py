import sys
import os
import xml.etree.ElementTree as ET
import json
import numpy as np
import datetime


# get all aspect tuples (target + sentiment) from the corpus.xml and store the tuples in a list (for entries with multiple)
# aspect tuples and save all in a dict (id + aspect tuples)
def extractOpinionsXML(name):
    corpus_dict = {}
    if os.path.exists(f"input/{name}"):

        tree = ET.parse(f"input/{name}")
        root = tree.getroot()

        for entry in root.findall("Document"):
            identifier = entry.get("id")
            opinions = entry.find("Opinions")
            opinion_list = []
            if opinions is not None:
                for opinion in opinions:
                    opinion_dict = {}
                    polarity = opinion.get("polarity")
                    target = opinion.get("target")
                    opinion_dict.update({target: polarity})
                    opinion_list.append(opinion_dict)

            corpus_dict.update({identifier: opinion_list})
    # print(corpus_dict)
    return corpus_dict


# Extract all aspect tuples and store them like the corpus xml file from all prediction json files
def extractOpinionsJSON():
    folder_path = "prediction"
    prediction_dict = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    fill_dict(data, prediction_dict)
                except json.JSONDecodeError:
                    print("Error while Decode")
    # print(prediction_dict)
    return prediction_dict


# adds aspect tuples to a list and return a dict
def fill_dict(data, prediction_dict):
    file_id = data["id"]
    opinion_list = []
    for opinion in data["Aspekte"]:

        opinion_dict = {}
        target = opinion["Term"]
        # polarity = opinion["polarity"]
        if "Polarität" in opinion:
            polarity = opinion["Polarität"]
        elif "Polaritaet" in opinion:
            polarity = opinion["Polaritaet"]
        elif "Polarit\\u00e4t" in opinion:
            polarity = opinion["Polarit\\u00e4t"]
        print(opinion)
        opinion_dict.update({target: polarity})
        opinion_list.append(opinion_dict)
    # print(file_id)

    prediction_dict.update({file_id: opinion_list})
    return prediction_dict


# compare prediction with the corpus values. Counts true positiv, false positiv and false negativ
def compareValues(corpus_dict, prediction_dict):
    tp = 0
    fp = 0
    fn = 0
    for key_corpus in corpus_dict:
        for key_prediction in prediction_dict:
            if key_corpus == key_prediction:
                tp2, fp2, fn2 = comparePrediction(
                    corpus_dict[key_corpus], prediction_dict[key_corpus])

                tp = tp + tp2
                fp = fp + fp2
                fn = fn + fn2
                # print(corpus_dict[key_corpus])
    saveData(tp, fp, fn, prediction_dict)


# compare one entry; saved in a set to compare, return the fp, tp and fn
def comparePrediction(corpus_items, prediction_items):
    # print(corpus_items, prediction_items)
    corpus_set = set()
    prediction_set = set()
    if len(corpus_items) != 0:
        for item_corpus in corpus_items:
            polarity_corpus = next(iter(item_corpus.values()))
            if next(iter(item_corpus.keys())) is not None:
                target_corpus = next(iter(item_corpus.keys())).lower()
            else:
                target_corpus = next(iter(item_corpus.keys()))
            corpus_set.update([(target_corpus, polarity_corpus)])
    if prediction_items is not None:
        for item_prediction in prediction_items:
            polarity_prediction = next(iter(item_prediction.values()))
            if next(iter(item_prediction.keys())) is not None:
                target_prediction = next(iter(item_prediction.keys())).lower()
            else:
                target_prediction = next(iter(item_prediction.keys()))
            prediction_set.update([(target_prediction, polarity_prediction)])
    # print(corpus_set)
    # print(prediction_set)
    tp = len(corpus_set.intersection(prediction_set))
    fp = len(prediction_set.difference(corpus_set))
    fn = len(corpus_set.difference(prediction_set))

    if len(corpus_set) == 0 and len(prediction_set) == 0:
        tp += 1

    # print(tp, fp, fn)
    return tp, fp, fn


# Calculation from:
# Simmering, P. F., & Huoviala, P. (2023).
# Large language models for aspect-based sentiment analysis (arXiv:2310.18025). arXiv. https://doi.org/10.48550/arXiv.2310.18025
def precision(tp, fp):
    precision = np.where((tp + fp) == 0, 0, tp / (tp + fp))
    print(f"Precision: {precision.astype(float)}")
    return precision.astype(float)


def recall(tp, fn):
    recall = np.where((tp + fn) == 0, 0, tp / (tp + fn))
    print(f"Recall: {recall.astype(float)}")
    return recall.astype(float)


def f1_score(tp, fp, fn):
    pre = precision(tp, fp)
    rec = recall(tp, fn)
    f1 = np.where((pre + rec) == 0, 0, 2 * (pre * rec) / (pre + rec))
    print(f"F1: {f1.astype(float)}")
    return f1.astype(float)


def accuracy(tp, fp, fn):
    acc = np.where((tp + fp + fn) == 0, 0, tp / (tp + fp + fn))
    return acc.astype(float)


def saveData(tp, fp, fn, prediction_dict):
    rec = recall(tp, fn)
    pre = precision(tp, fp)
    f1 = f1_score(tp, fp, fn)
    acc = accuracy(tp, fp, fn)
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(current_timestamp)
    fileName = "Metrics_" + str(current_timestamp) + ".txt"
    metrics = f"Precision: {pre} \nRecall: {rec} \nF1-Score: {f1} \nAccuracy: {acc}\n"
    data = f"False Negative: {fn} \nTrue Positive {tp} \nFalse Positive {
        fp} \nAmount Predictions(Only number of text examples not total aspect tuples): {len(prediction_dict)}\n"
    message = metrics + data
    with open(f"output/{fileName}", "w") as file:
        file.write(message)


def main():
    print("Start")
    xml_file_name = "GermEval_Test_Clean.xml"
    # xml_file_name = "MobASA.xml"
    corpus_dict = extractOpinionsXML(xml_file_name)
    prediction_dict = extractOpinionsJSON()
    # how many tuple predictions in both dicts
    t = 0
    for key, value in corpus_dict.items():
        t += len(value)
    d = 0
    for key, value in prediction_dict.items():
        d += len(value)
    print(t, d)
    compareValues(corpus_dict, prediction_dict)


if __name__ == '__main__':
    sys.exit(main())
