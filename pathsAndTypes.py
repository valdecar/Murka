import os
import parsers
import storage
import test


class BookNamesAgent():
    '''
    DESCRIPTION:
    This class control names and
    pathes of book.
    It also used for storing books
    itro database.

    For database description see
    storage.py.
    
    Almost all functions needed that
    one of self.set_book_name_* functions
    called previously.
   
    All books save in "txt" formant.

    If book opend first time,
    in that case it's text will be 
    saved to "booksData/books".
    
    If user changed text in textFrame,
    changing text will be saved to
    "booksData/changedText".

    Functions set_book_name used for
    controling name, types of book.
    It needed for correctly save, and
    opend books independently of it status
    (i.e. changed, unchanged).
    '''
    def __init__(self):
        # pathes
        self.pathToBooks = os.path.join(os.getcwd(), "booksData", "books")
        self.pathToBooksChanged = os.path.join(os.getcwd(),
                                               "booksData", "changedTexts")
        # different names of book
        self.bookPathAndFile = None
        self.bookNameWithType = None
        self.bookName = None
        self.bookType = None
        self.bookNameWithTypeNew = None

        self.bookmarksDict = {"current": 0}
        
        self.db = storage.BooksStorage()
        # for text changed indicator
        self.textChanged = False
        self.text = []

    def get_i(self):
        return(test.i)

    def set_book_name_from_name(self, bookName):

        self.bookName = bookName
        self.bookType = 'txt'
        self.bookNameWithTypeNew = self.bookName + '.txt'

    def set_book_name_from_full(self, fullPathAndFile):
        
        self.bookPathAndFile = fullPathAndFile
        self.bookNameWithType = os.path.basename(fullPathAndFile)
        # bookPath = os.path.dirname(bookPathAndFile)
        self.bookName, self.bookType = self.bookNameWithType.split('.')
        self.bookNameWithTypeNew = self.bookName + '.txt'

    def reset_i(self, _to=0):
        '''
        DESCRIPTION:
        Set test i ether 0 or _to.
        '''
        test.i = _to

    def delete_books(self, booksNamesList):
        '''
        DESCRIPTION:
        Delete books from "books" folder
        and from db.
        '''
        for bookName in booksNamesList:
            bookPathAndFile = os.path.join(self.pathToBooks, bookName+'.txt')
            bookCangedPathAndFile = os.path.join(self.pathToBooksChanged,
                                                 bookName+'.txt')
            try:
                # delete from "books" folder
                os.remove(bookPathAndFile)
                os.remove(bookCangedPathAndFile)
            except:
                print("delete_books: error during deleting files")
            self.db.delete_book(bookName)

    def get_bookmarks(self):
        '''
        DESCRIPTION:
        Get all bookmarks from book.
        
        self.set_book_name_from_full or
        self.set_book_name_from_name or
        self.import_text_* or 
        self.open_book_stored
        must be called first.
        '''
        bookName = self.bookName
        if bookName is None:
            print("choice book first")
            return(1)
        self.bookmarksDict = self.db.get_bookmarks(bookName)
        return(self.bookmarksDict)
        
    def set_bookmark(self, lineId):
        '''
        DESCRIPTION:
        Set add bookmark 
        bookmarksDict[lineId]=lineId
        to current book.

        self.set_book_name_from_full or
        self.set_book_name_from_name or
        self.import_text_* or 
        self.open_book_stored
        must be called first.
        '''
        bookName = self.bookName
        if bookName is None:
            print("choice book first")
            return(1)

        bookmarksDict = self.db.get_bookmarks(bookName)
        bookmarksDict[lineId] = lineId
        
        self.db.add_or_change_book(bookName,
                                   bookmarksDict=str(bookmarksDict))
        self.bookmarksDict = bookmarksDict
        return(0)
    
    def set_bookmark_current(self):
        if self.bookName is None:
            # open window for choicing
            print("choice book first")
            return(1)

        bookmarksDict = self.db.get_bookmarks(self.bookName)
        bookmarksDict['current'] = test.i

        self.db.set_bookmarks(self.bookName, bookmarksDict)

    def rewrite_bookmarks(self, bookmarksDict):
        '''
        DESCRIPTION:
        Rewrite bookmarks in db.

        
        self.set_book_name_from_full or
        self.set_book_name_from_name or
        self.import_text_* or 
        self.open_book_stored
        must be called first.
        '''
        self.db.add_or_change_book(self.bookName, 
                                   bookmarksDict=str(bookmarksDict))
        self.bookmarksDict = bookmarksDict
        
    def open_book_stored(self, bookName):
        '''
        DESCRIPTION:
        Open previously opened book
        i.e. it entry stored in db and
             it text stored in booksData.
        Import it's bookmarks.
        '''
        # import bookmarks
        try:
            self.bookmarksDict = self.db.get_bookmarks(bookName)
            print(self.bookmarksDict)
            self.reset_i(_to=int(self.bookmarksDict['current']))
        except:
            self.reset_i()
            print('EX: current extract fail')

        print("test.i = %d" % test.i)
        self.set_book_name_from_name(bookName)
        
        # if changedText exist use it
        pathExist = self.db.get_changedText(bookName)
        print("pathExist?")
        print(pathExist)
        if pathExist:
            try:
                text = self.import_text_from_stored_changed(bookName)
            except:
                print("cannot open changed text")
                print("try to save it again")
                text = self.import_text_from_stored(bookName)
        else:
            text = self.import_text_from_stored(bookName)

        return(text)
    
    def save_book_new(self):
        '''
        DESCRIPTION:
        Save self.text from new book to
        "booksData/books" as "txt" file.
        Add entry to db.
        set current position to 0.

        self.set_book_name_from_full or
        self.set_book_name_from_name or
        self.import_text_* or 
        self.open_book_stored
        must be called first.
        '''
        if self.bookNameWithTypeNew is None:
            print("bookName is None")
            return(1)
        path = os.path.join(self.pathToBooks, self.bookNameWithTypeNew)
        print("path from save_book_new")
        print(path)
        # print(self.text)
        
        parsers.save_book(self.text, path)

        self.bookmarksDict = {"current": 0}
        self.db.add_or_change_book(self.bookName, self.bookmarksDict)
        
    def save_book_opend(self):
        '''
        DESCRIPTION:
        Save text, if it was changed to
        "booksData/changedText".
        Save bookmarks to db.
        Save current position to db.
        
        self.set_book_name_from_full or
        self.set_book_name_from_name or
        self.import_text_* or 
        self.open_book_stored
        must be called first.
        '''

        if self.bookName is None:
            # open window for choicing
            print("choice book first")
            return(1)

        bookmarksDict = self.db.get_bookmarks(self.bookName)
        bookmarksDict['current'] = test.i
        
        # save path if text was changed
        if self.textChanged:

            changedTextPath = os.path.join(self.pathToBooksChanged,
                                           self.bookNameWithTypeNew)
            print("save_book: %s" % changedTextPath)
            print(changedTextPath)
            
            # save changed text
            try:
                parsers.save_book(self.text, changedTextPath)
            except:
                print("ERROR save_book_opend: cannot save text ")
            # self.db.set_changedText(self.bookName)

        self.db.add_or_change_book(self.bookName,
                                   bookmarksDict=str(bookmarksDict),
                                   textChanged=1)
    
    def import_text_from_stored_changed(self, bookName):
        '''
        DESCRIPTION:
        Import previously stored, changed
        text. From "booksData/changedText"
        Also useLinesSep because some lines
        from textFrame not have dots.
        '''
        self.set_book_name_from_name(bookName)
        path = os.path.join(self.pathToBooksChanged, self.bookNameWithTypeNew)
        self.text = parsers.import_text(path, useLinesSep=True)
        return(self.text)

    def import_text_from_stored(self, bookName):
        '''
        DESCRIPTION:
        Import previously stored, unchanged
        text. From "booksData/books"
        Also useLinesSep because some lines
        from textFrame not have dots.
        '''
        self.set_book_name_from_name(bookName)
        path = os.path.join(self.pathToBooks, self.bookNameWithTypeNew)
        print(path)
        self.text = parsers.import_text(path, useLinesSep=True)
        return(self.text)

    def import_text_new(self, pathAndFileName):
        self.set_book_name_from_full(pathAndFileName)
        self.text = parsers.import_text(self.bookPathAndFile)
        return(self.text)



