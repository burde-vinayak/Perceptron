import pickle
import os
from math import log10
import sys
fopen=open('per_model.txt','rb')

data=pickle.load(fopen)

path=sys.argv[1]
print(path)
file_actual={}
file_result={}

print (str(data['bias_beta']))
for root,dirs,files in os.walk(path):
    for file in files:
        if 'ham' in file:
            file_actual[file]='ham'
        elif 'spam' in file:
            file_actual[file]='spam'
        if file.endswith('.txt'):
            alpha=0
            fopen = open(os.path.join(root,file), "r", encoding="latin1")
            for line in fopen:
                for word in line.split():
                    if word in data['word_weights_and_avg']:
                      alpha=alpha+data['word_weights_and_avg'].get(word)
            alpha=alpha+data['bias_beta']
            if(alpha>0):
                file_result[file]="spam"
            else:
                file_result[file]="ham"


fopen= open('nboutput.txt','w')
for k,v in file_result.items():
    fopen.write(v+' '+k+'\n')
#print(file_result)
document_count=len(file_actual)
correctly_classified_ham=0
correctly_classified_spam=0
ham_prediction=0
spam_prediction=0
ham_actual=0
spam_actual=0

for file in file_actual.keys():
    if file_actual[file]=='ham':
        ham_actual+=1
    elif file_actual[file]=='spam':
        spam_actual+=1
    if file_actual[file]==file_result[file]:
        if file_actual[file]=='spam':
            correctly_classified_spam+=1
        elif file_actual[file]=='ham':
            correctly_classified_ham+=1
for file in file_result.keys():
    if file_result[file]=='ham':
        ham_prediction+=1
    elif file_result[file]=='spam':
        spam_prediction+=1
#accuracy=(correctly_classified_spam+correctly_classified_ham)/document_count
if ham_actual == 0 or spam_actual == 0 or ham_prediction == 0 or spam_prediction == 0:
        print("Either predicted ham-spam file count is zero or given development ham-spam file count is 0")
else:

    precision_spam=correctly_classified_spam/spam_prediction
    precision_ham=correctly_classified_ham/ham_prediction

    recall_spam=correctly_classified_spam/spam_actual
    recall_ham=correctly_classified_ham/ham_actual

    f1_spam=(2*(precision_spam*recall_spam))/(precision_spam+recall_spam)
    f1_ham=(2*recall_ham*precision_ham)/(precision_ham+recall_ham)

    print("spam Precision: ", precision_spam)
    print("spam Recall: ", recall_spam)
    print("spam F1 Score: ", f1_spam)
    print("ham Precision: ", precision_ham)
    print("ham Recall: ", recall_ham)
    print("ham F1 Score: ", f1_ham)
