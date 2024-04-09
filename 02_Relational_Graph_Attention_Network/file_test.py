import json


def read_sentence_depparsed(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data

files = ['./data/studycheck/StudyCheck_Test_Clean_biaffine_depparsed.json', './data/studycheck/StudyCheck_Train_Clean_biaffine_depparsed.json']
for file in files:
    file_loaded = read_sentence_depparsed(file)
    #print(file_loaded)
    exit = len(file_loaded)
    for j in range(len(file_loaded)):
        if j >= exit:
            break
        #try:
        if len(file_loaded[j]['tokens']) > 100:
            #print(j)
            #print(file_loaded[j]['sentence'])
            file_loaded.pop(j)
            #print(len(file_loaded))
            exit -= 1
        #except:
           # continue
    '''for j in range(len(file_loaded)):
        if len(file_loaded[j]['tokens']) > 500:
            print(j)
            #print((j['sentence']))
            file_loaded.pop(j)  '''   

    with open(file.replace('.json', '_without_large.json'), "w") as outfile:
        json.dump(file_loaded, outfile)
        
file_high_neg = './GermEval_Train_Clean_biaffine_depparsed_without_large.json'

"""high_neg_loaded = read_sentence_depparsed(file_high_neg)
exit = len(high_neg_loaded)
neg = 0
for i in range(len(high_neg_loaded)):
    if i >= exit:
        break
    try:
        if high_neg_loaded[i]['aspect_sentiment'][0][1] == 'negative' or high_neg_loaded[i]['aspect_sentiment'][1][1] == 'negative':
            print('hä')
            neg += 1  
    except:
        if high_neg_loaded[i]['aspect_sentiment'][0][1] == 'negative':
            print('hä')
            neg += 1 
    if neg == 2:
        high_neg_loaded.pop(i)
        print('popped')
        exit-=1
        neg=0
    elif neg == 1:
        high_neg_loaded.pop(i)
        print('popped')
        exit-=1
with open(file_high_neg, "w") as outfile:
        json.dump(high_neg_loaded, outfile)"""

print('all processed correctly')   
