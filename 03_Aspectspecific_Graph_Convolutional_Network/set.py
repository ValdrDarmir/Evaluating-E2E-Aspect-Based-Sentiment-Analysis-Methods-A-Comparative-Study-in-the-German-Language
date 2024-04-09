
train_set = './datasets/mobasa/mobasa_test.raw'

f = open(train_set, 'r', encoding='utf-8', newline='\n', errors='ignore')
print(len(f.readlines()))