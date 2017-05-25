import xml.parsers.expat
from functools import reduce
import sys
import os
#sys.setrecursionlimit(10000)


def parse_book_from_str(textStr):
    parser = ParserTXT()
    return(parser.parse_book_from_str(textStr))


def save_book(dataList, _fileName):
    
    # change type
    # _fileName = _fileName+'.'+bookType
    # print(_fileName)
    # convert list to string
    data = reduce(lambda x, y: x+'\n'+y, dataList, '')
    f = open(_fileName, 'w')
    f.write(data)
    f.close()


def import_text(_fileName, useLinesSep=False):
    
    # change type
    # bookType = _fileName.split('.')[-1]
    # if bookType != 'txt':
    #     _fileNameTXT = _fileName.replace('.'+bookType, '.txt')
    
    textType = os.path.basename(_fileName).split('.')[-1]
    print(_fileName)
    print(textType)
    if textType == 'fb2':
        parser = ParserFB2()
        parser.parse_book(bookName=_fileName)
    elif(textType == 'txt'):
        parser = ParserTXT()
        parser.parse_book(bookName=_fileName, useLinesSep=useLinesSep)
    return(parser.out)


class ParserFB2():
    '''
    DESCRIPTION:
    '''

    def __init__(self):
        self.bookNameDefault = "Cook Glen - And Dragons in the Sky - 1972.fb2"
        self.dataStr = None
        self.dataList = []
        self.out = []

    def parse_book(self, bookName=None):
        self.open_fb2_book(bookName)
        self.parse_fb2()
        self.data_correct()
        self.split_str_to_lines()
        # return(self.out)
    
    def split_str_to_lines(self):
        if self.dataList is None:
            print('split_str_to_lines: self.dataList is None')
            return(1)

        text = []
        text.extend(sum([t.split("\n") for t in self.dataList], []))
        text1 = []
        text1.extend(sum([t.replace('.', '.\n').split("\n") for t in text], []))
        text2 = []
        text2.extend(sum([t.replace('!', '!\n').split("\n") for t in text1], []))
        text3 = []
        text3.extend(sum([t.replace('?', '?\n').split("\n") for t in text1], []))
        self.out = list(filter(lambda x: x != '', text3))

    def open_fb2_book(self, bookName=None):
        if bookName is None:
            bookName = self.bookNameDefault

        with open(bookName, encoding='cp1251') as f:
            self.dataStr = f.read()

    def data_correct(self):
        '''
        DESCRIPTION:
        correct parsed data from book
        '''
        if self.dataList is None:
            print('data_correct: self.dataList is None')
            return(1)
        data = self.dataList[:]

        # remove '\\n'
        data = [d if len(d) > 3 else '\n' for d in data]

        # remove long and unsence strings
        def filter_test(seq):
            if '\n' in seq:
                return(True)
            elif(len(seq) <= 6):
                return(True)
            elif(len(seq.split()) > 1):
                return(True)
            else:
                return(False)

        data = list(filter(filter_test, data))
        # return(data)
        self.dataList = data[:]

    def parse_fb2(self):
        '''
        DESCRIPTION:
        parse data from string data
        for now it just place all tags data to list
        '''
        
        data = self.dataStr
        if data is None:
            print('parse_fb2: self.data is none')
            return(1)

        p = xml.parsers.expat.ParserCreate()

        dataList = []

        '''
        def start_element(name, attrs):                                        
            print('Start element:', name, attrs)
            tagsList.append(Tag(name, attrs)

        def end_element(name):            
            print('End element:', name)
            tagsList[-1].close()
        '''

        def char_data(data):
            # print('Character data:', repr(data))
            # tagsList[-1].add_data(repr(data))
            dataList.append(data)  # repr(data)

        # p.StartElementHandler = start_element                                  
        # p.EndElementHandler = end_element       
        p.CharacterDataHandler = char_data

        p.Parse(data)
        # return([(tag.name, tag.data) for tag in tagsList])
        self.dataList = dataList


class ParserTXT():
    
    def __init__(self):
        self.bookNameDefault = ""
        self.dataStr = None
        self.dataList = None
        self.out = None

    def parse_book(self, bookName, useLinesSep=False):
        self.open_txt_book(bookName=bookName)
        # self.dataList = self.dataStr.split('.')
        # self.out = self.parse_txt(inputList=self.dataList, outList=[])
        self.split_str_to_lines(useLinesSep)
        
    def parse_book_from_str(self, dataStr):
        self.dataStr = dataStr
        self.split_str_to_lines()
        return(self.out)
    
    def split_str_to_lines(self, useLinesSep=False):
        if self.dataStr is None:
            print('split_str_to_lines: self.dataStr is None')
            return(1)

        if not useLinesSep:
            self.dataStr = self.dataStr.replace('\n', ' ')

        self.dataList = self.dataStr.replace('.', '.\n').split('\n')
        self.out = list(filter(lambda x: x not in ['', ' '], self.dataList))

    def open_txt_book(self, bookName=None):
        if bookName is None:
            bookName = self.bookNameDefault
            
        with open(bookName) as f:
            data = f.read()
        self.dataStr = data
    
    def parse_txt(self, inputList, outList):
        '''
        DESCRIPTION:
        Replace too long sequences 
        '''
        if len(outList) == 0:
            inputList
        
        # dataList = self.dataStr.split('.')
        if len(inputList) == 0:
            return(outList)

        seq, rest = inputList[0], inputList[1:]

        wordsList = seq.split()
        if len(wordsList) > 7:
            if '\n' in seq:
                lineBef, lineAft = seq.split('\n', 1)
                outList.append(lineBef)  # !
                rest.insert(0, lineAft)
            else:
                # find midle word and split at it
                head, sep, tail = seq.partition(' '+wordsList[4]+' ')
                outList.append(head+sep)  # !
                rest.insert(0, tail)
        else:
            if '\n' in seq:
                outList.append(seq.replace('\n', ' '))
            else:
                outList.append(seq)
        return(self.parse_txt(inputList=rest, outList=outList))
            

