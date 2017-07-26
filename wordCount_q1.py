import getopt
import operator

import sys
'''
Author: Shahrouz Ryan Alimo
Modified: July 2017

'''

class stringItem:
    def __init__(self, sstr, itotal):
        self.Name = sstr
        self.Total = itotal

    def getName(self):
        return (self.Name)

    def getTotal(self):
        return (self.Total)

    def setTotal(self, ntotal):
        self.Total = ntotal

class analizeSentence:
    char_ignores = [".", ",", "-", "{", "}", "[", "]", "(", ")", "\n"]
    word_separator = " "
    sentence_separator = "."

    def __init__(self):
        self.listUniqueWord = []
        self.listWord = []
        self.listSentence = []
        self.strInput = ""
        self.mean_word_in_sentence = 0.0
        self.listPhrasesOfWord = []

    def getListUniqueWord(self):
        return (self.listUniqueWord)

    def getListPhrasesOfWord(self):
        return (self.listPhrasesOfWord)

    def getMeanWordInSentence(self):
        return (self.mean_word_in_sentence)

    def analizeFile(self, filename):
        #open file and read all contents
        fid = open(filename, "r")
        all_string = fid.read()
        fid.close()

        self.analizeWordInString(all_string)
        self.analizeSentenceInString(all_string)

    def analizeWordInString(self, sstr):
        # analize word in string input

        self.strInput = sstr

        # removed selected char
        sstr = self.removeIgnoredChar(sstr)

        # split string by separator
        self.listWord = self.splitSentenceToWord(sstr, self.word_separator)
        n = len(self.listWord)

        # loop over list of word
        for i in range(0, n):
            curItem = stringItem(self.listWord[i], 1)
            self.listUniqueWord = self.add(self.listUniqueWord, curItem)

        #sort list of unique word
        self.listUniqueWord.sort(key=operator.attrgetter('Total'), reverse=True)

    def analizeSentenceInString(self, sstr):
        # analize sentence in string input
        self.strInput = sstr

        self.listSentence = self.strInput.split(self.sentence_separator)
        # remove last sentence if the contents is empty
        if (len(self.listSentence[-1]) == 0):
            del (self.listSentence[-1])

        total_word_in_sentence = 0
        nsentences = len(self.listSentence)
        for i in range(0, nsentences):
            sstr = self.listSentence[i]

            # removed selected char
            sstr = self.removeIgnoredChar(sstr)

            # split string by separator
            arr_sstr = self.splitSentenceToWord(sstr, self.word_separator)

            #create list of phrase using 3 or more words
            self.listPhrasesOfWord = self.createListOfPhrasesWord(self.listPhrasesOfWord, arr_sstr, 3)

            n_arr_sstr = len(arr_sstr)
            total_word_in_sentence = total_word_in_sentence + n_arr_sstr

        # get mean of word in sentence
        self.mean_word_in_sentence = float(total_word_in_sentence)/float(nsentences)

        # sort list of unique phrases of word
        self.listPhrasesOfWord.sort(key=operator.attrgetter('Total'), reverse=True)

    def createListOfPhrasesWord(self, list_saving, list_data, min_word_count):
        n = len(list_data)
        for i in range(0, n-min_word_count):
            for j in range(i+min_word_count, n):
                new_phrases = self.convert_list_to_phrases(list_data, i, j)
                curItem = stringItem(new_phrases, 1)
                list_saving = self.add(list_saving, curItem)
        return (list_saving)

    def convert_list_to_phrases(self, list_data, start_pos, end_pos):
        new_phrases = ""
        for i in range(start_pos, end_pos):
            if(i==end_pos-1):
                new_phrases = new_phrases + list_data[i]
            else:
                new_phrases = new_phrases + list_data[i] + self.word_separator
        return (new_phrases)

    def splitSentenceToWord(self, sstr, separator):
        #convert string to lower
        sstr = sstr.lower()

        #split string by separator
        s_sstr = sstr.split(separator)

        #remove duplicate separator
        for i in range(len(s_sstr)-1, -1, -1):
            if(len(s_sstr[i])==0 or s_sstr[i]==separator):
                del(s_sstr[i])
        return (s_sstr)

    def removeIgnoredChar(self, sstr):
        # replace sentence separator
        for i in range(0, len(self.char_ignores)):
            sstr = sstr.replace(self.char_ignores[i], " ")
        return(sstr)

    def addItem(self, list_data, item):
        # append or add new item in list
        list_data.append(item)
        return (list_data)

    def updateItem(self, list_data, item, idxpos):
        # update item in selected position (idxpos)
        list_data[idxpos] = item
        return(list_data)

    def searchItem(self, list_data, item):
        # search item in existing list
        # return -1 if item not exist
        # return idxpos (item index position) if exist
        idxpos = -1
        n = len(list_data)
        for i in range(0, n): # loop over existing list
            if(item.getName()==list_data[i].getName()):
                idxpos = i
                break
        return (idxpos)

    def add(self, list_data, item):
        # add new item to list

        # search item if exist in list
        idxpos = self.searchItem(list_data, item)
        if(idxpos==-1):
            # add new item
            list_data = self.addItem(list_data, item)
        else:
            # replace item. update total of number item
            item_ori = list_data[idxpos]
            item_ori.setTotal(item_ori.getTotal()+1)
            list_data = self.updateItem(list_data, item_ori, idxpos)
        return (list_data)

    def getSentenceCount(self):
        return(len(self.listSentence))


    def getTotalUniqueWordCount(self):
        return (len(self.listUniqueWord)) #get total of list item

    def getTotalWordCount(self):
        return (len(self.listWord))

    def printItem(self, list_data, last_idx):
        # print list of item

        n = len(list_data)  # get total of list item
        if(last_idx<0):
            last_idx = n

        if(last_idx<=n):
            n = last_idx
        print "-------------------------------------"
        print "No.        Word                Count"
        print "-------------------------------------"
        for i in range(0, n):
            sstr = str(i+1) + ". " + list_data[i].getName() + "    " + str(list_data[i].getTotal())
            print sstr

    def printItemWithMinimumCount(self, list_data, min_count):
        n = len(list_data)  # get total of list item
        print "-------------------------------------"
        print "No.        Word                Count"
        print "-------------------------------------"
        for i in range(0, n):
            if(list_data[i].getTotal()>min_count):
                sstr = str(i + 1) + ". " + list_data[i].getName() + "    " + str(list_data[i].getTotal())
                print sstr
            else:
                break


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print 'wordCount.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'wordCount.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print "Input file is : " + inputfile

    # object initialization
    anSent = analizeSentence()

    #run by process using inputfile
    anSent.analizeFile(inputfile)

    # SC.printItem()
    print "Total Words Count : " + str(anSent.getTotalWordCount())
    print "Total Unique Words Count : " + str(anSent.getTotalUniqueWordCount())
    print "Total Sentences Count : " + str(anSent.getSentenceCount())
    print "Average Sentence Length in Words : %4.2f" % anSent.getMeanWordInSentence()

    print "\n** Show list of words used (descending order) **"
    listUniqueWord = anSent.getListUniqueWord()
    anSent.printItem(listUniqueWord, 5)
    #anSent.printItem(listUniqueWord, -1) #print all data (use -1 for last index parameter)

    print "\n** Show list of words used (descending order) with Total count more than 8 **"
    anSent.printItemWithMinimumCount(listUniqueWord, 8)

    print "\n** Show list of phrases used with three or more words (descending order) **"
    listPhrasesOfWord = anSent.getListPhrasesOfWord()
    anSent.printItem(listPhrasesOfWord, 5)
    #anSent.printItem(listPhrasesOfWord, -1) #print all data (use -1 for last index parameter)

    print "\n** Show list of phrases used with three or more words (descending order) with Total count more than 2 **"
    anSent.printItemWithMinimumCount(listPhrasesOfWord, 2)

if __name__ == "__main__":
    main(sys.argv[1:])

