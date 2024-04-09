'''
Biaffine Dependency parser from AllenNLP
'''
import argparse
import json
import os
import re
import sys
   
import re

from allennlp.predictors.predictor import Predictor
from allennlp_models import pretrained
from allennlp.data.dataset_readers import dataset_reader
from lxml import etree
from nltk.tokenize import TreebankWordTokenizer
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument('--data_path', type=str, default='./data/mobasa',
                        help='Directory of where mobasa data held.')
    return parser.parse_args()


def xml2txt(file_path):
    '''
    Read the original xml file of semeval data and extract the text that have aspect terms.
    Store them in txt file.
    '''
    output = file_path.replace('.xml', '_text.txt')
    sent_list = []
    with open(file_path, 'rb') as f:
        raw = f.read()
        root = etree.fromstring(raw)
        for sentence in root:
            sent = sentence.find('text').text
            terms = sentence.find('Opinions')
            
            if sentence.find('relevance').text == 'false':
                continue
            if terms.find('Opinion') is None:
                continue    
            #print(terms.find('Opinion').attrib['target'])
            if terms.find('Opinion').attrib['target'] == 'NULL':
                continue
            if terms:
                sent_list.append(sent)
    with open(output, 'w') as f:
        for s in sent_list:
            f.write(s+'\n')
    print('processed', len(sent_list), 'of', file_path)


def text2docs(file_path, predictor):
    '''
    Annotate the sentences from extracted txt file using AllenNLP's predictor.
    '''
    with open(file_path, 'r') as f:
        sentences = f.readlines()
    docs = []
    print('Predicting dependency information...')
    for i in tqdm(range(len(sentences))):
        docs.append(predictor.predict(sentence=sentences[i]))

    return docs


def dependencies2format(doc):  # doc.sentences[i]
    '''
    Format annotation: sentence of keys
                                - tokens
                                - tags
                                - predicted_dependencies
                                - predicted_heads
                                - dependencies
    '''
    sentence = {}
    sentence['tokens'] = doc['words']
    sentence['tags'] = doc['pos']
    # sentence['energy'] = doc['energy']
    predicted_dependencies = doc['predicted_dependencies']
    predicted_heads = doc['predicted_heads']
    sentence['predicted_dependencies'] = doc['predicted_dependencies']
    sentence['predicted_heads'] = doc['predicted_heads']
    sentence['dependencies'] = []
    for idx, item in enumerate(predicted_dependencies):
        dep_tag = item
        frm = predicted_heads[idx]
        to = idx + 1
        sentence['dependencies'].append([dep_tag, frm, to])

    return sentence


def get_dependencies(file_path, predictor):
    docs = text2docs(file_path, predictor)
    sentences = [dependencies2format(doc) for doc in docs]
    return sentences


def syntaxInfo2json(sentences, origin_file):
    json_data = []
    tk = TreebankWordTokenizer()
    mismatch_counter = 0
    idx = 0
    with open(origin_file, 'rb') as fopen:
        raw = fopen.read()
        root = etree.fromstring(raw)
        for sentence in root:
            example = dict()
            example["sentence"] = sentence.find('text').text
            if sentence.find('relevance').text == 'false':
                continue
            terms = sentence.find('Opinions')    
            if terms.find('Opinion') is None:
                continue        
            # for RAN
            
            if terms.find('Opinion').attrib['target'] == 'NULL':
                continue
            
            example['tokens'] = sentences[idx]['tokens'] 
            example['tags'] = sentences[idx]['tags']
            example['predicted_dependencies'] = sentences[idx]['predicted_dependencies']
            example['predicted_heads'] = sentences[idx]['predicted_heads']
            example['dependencies'] = sentences[idx]['dependencies']
            # example['energy'] = sentences[idx]['energy']
            
            example["aspect_sentiment"] = []
            example['from_to'] = [] #left and right offset of the target word 

            for c in terms:
                if c.attrib['polarity'] == 'conflict':
                    continue
                target = c.attrib['target']
                example["aspect_sentiment"].append((target, c.attrib['polarity']))
                
                # index in strings, we want index in tokens
                left_index = int(c.attrib['from'])
                right_index = int(c.attrib['to'])
                example_ohne_at = re.sub(r'[;@#$%&]', ' ', example['sentence'])
                left_word_offset = len(tk.tokenize(example_ohne_at[:right_index]))
                to_word_offset = len(tk.tokenize(example_ohne_at[:right_index]))

                
                example['from_to'].append((left_word_offset,to_word_offset))
            if len(example['aspect_sentiment'])==0:
                idx += 1
                continue
            json_data.append(example)
            idx+=1
    extended_filename = origin_file.replace('.xml', '_biaffine_depparsed.json')
    with open(extended_filename, 'w') as f:
        json.dump(json_data, f)
    print('done', len(json_data))
    print(idx)


def main():
    args = parse_args()
    
    
    predictor = pretrained.load_predictor("structured-prediction-biaffine-parser")#Predictor(pretrained, dataset_reader)
    
    train_file='MobASA_Train_Clean.xml'
    test_file='MobASA_Test_Clean.xml'
    
        # xml -> txt
    xml2txt(os.path.join(args.data_path, train_file))
    xml2txt(os.path.join(args.data_path, test_file))

        # txt -> json
    train_sentences = get_dependencies(os.path.join(args.data_path, train_file.replace('.xml', '_text.txt')), predictor)
    syntaxInfo2json(train_sentences, os.path.join(args.data_path, train_file))
        
    test_sentences = get_dependencies(os.path.join(args.data_path, test_file.replace('.xml', '_text.txt')), predictor)
    syntaxInfo2json(test_sentences, os.path.join(args.data_path, test_file))

    print(len(train_sentences), len(test_sentences))
if __name__ == "__main__":
    main()
