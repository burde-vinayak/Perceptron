import os
import sys
import pickle
import random

class perceptron_avg():
    bias=0
    word_weight={}
    word_avg_weight={}
    files={}
    c=1
    beta=0
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
                                self.word_avg_weight[word]=0
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
                                self.word_avg_weight[word] = 0
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
                                self.word_avg_weight[key]=self.word_avg_weight.get(key)+(y*self.c*values[0].get(key))
                            self.bias=self.bias+y
                            self.beta=self.beta+(y*self.c)
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
                                self.word_avg_weight[key] = self.word_avg_weight.get(key) + (y * self.c * values[0].get(key))
                            self.bias = self.bias + y
                            self.beta = self.beta + (y * self.c)

                            #print(str(self.bias))
                    self.c=self.c+1
        for words in self.word_avg_weight.keys():
            self.word_avg_weight[words]=self.word_weight.get(words)-((1/self.c)*self.word_avg_weight.get(words))
        self.beta=self.bias-((1/self.c)*self.beta)







obj=perceptron_avg();

path=sys.argv[1]
iter=30

obj.weight_initialize(path)
obj.percep(iter)
#print(str(obj.beta))
fopen=open('per_model.txt','wb')
#fopen.write(str(obj.totalspamfiles)+'   '+str(obj.totalhamfiles)+'\n'+ str(obj.ham_words_probab) + '\n' + str(obj.spam_words_probab))
data={'bias_beta':obj.beta,
      "word_weights_and_avg":obj.word_avg_weight
       }
#
pickle.dump(data,fopen)
#print(len(obj.vocabulary))
fopen.close()

