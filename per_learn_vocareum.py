import os
import sys
import pickle
import random

class perceptron():
    bias=0
    word_weight={}
    files={}

    def weight_initialize(self,path):
        i=0
        for dirName, subdirList, fileList in os.walk(path, topdown=True):
            #print('Found directory: %s' % dirName)

            for fname in fileList:
                if "spam" in dirName:
                    #print('\t%s' % fname)
                    spam_words = {}
                    i+=1
                    fopen=open(os.path.join(dirName,fname), "r", encoding="latin1")
                    for line in fopen:
                        for word in line.split():
                            if spam_words.get(word):
                                spam_words[word] += 1
                            else:
                                spam_words[word] = 1
                            if word not in self.word_weight:
                                self.word_weight[word]=0
                    self.files[i] = (spam_words, "spam")


                elif "ham" in dirName:

                    i+=1
                    ham_words={}
                    fopen = open(os.path.join(dirName,fname), "r", encoding="latin1")
                    for line in fopen:
                        for word in line.split():
                            if ham_words.get(word):
                                ham_words[word] += 1
                            else:
                                ham_words[word] = 1
                            if word not in self.word_weight:
                                self.word_weight[word] = 0
                    self.files[i] = (ham_words, "ham")
        #print(self.files)

    def percep(self,iter):

        for i in range(iter):
            keys=list(self.files.keys());
            random.shuffle(keys);
            for key in keys:
                # print('Found directory: %s' % dirName
                    values=self.files.get(key);
                    # print (values[0]+' '+values[1])
                    if values[1]=="spam":
                        # print('\t%s' % fname)
                        y=1
                        alpha=0

                        for key in values[0].keys():
                            alpha=alpha+(self.word_weight.get(key)*values[0].get(key))
                        alpha=alpha+self.bias

                        if (y*alpha)<=0:
                            for key in values[0].keys():
                                self.word_weight[key]=self.word_weight.get(key)+(y*values[0].get(key))
                            self.bias=self.bias+y
                            #print(str(self.bias))


                    elif values[1]=="ham":
                        y=-1

                        alpha=0


                        for key in values[0].keys():
                            alpha = alpha + (self.word_weight.get(key) * values[0].get(key))
                        alpha = alpha + self.bias

                        if (y * alpha) <= 0:
                            for key in values[0].keys():
                                self.word_weight[key] = self.word_weight.get(key) + (y * values[0].get(key))
                            self.bias = self.bias + y
                            #print(str(self.bias))









obj=perceptron();

path=sys.argv[1]
iter=20

obj.weight_initialize(path)
obj.percep(iter)
#print(str(obj.bias))
fopen=open('per_model.txt','wb')
#fopen.write(str(obj.totalspamfiles)+'   '+str(obj.totalhamfiles)+'\n'+ str(obj.ham_words_probab) + '\n' + str(obj.spam_words_probab))
data={'bias_beta':obj.bias,
      "word_weights_and_avg":obj.word_weight
       }
#
pickle.dump(data,fopen)
#print(len(obj.vocabulary))
fopen.close()

