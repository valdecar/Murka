import sqlite3
import os


class BooksStorage():
    def __init__(self):
        self.conn = sqlite3.connect('storage.db')
        self.cursor = self.conn.cursor()
        self.last = self.get_last_bookName()
    
    def delete_book(self, bookName):
        '''
        DESCRIPTION:
        Delete book from db.
        '''
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM books WHERE bookName = ?", (bookName,))
        self.conn.commit()

    def set_changedText(self, bookName):
        '''
        DESCRIPTION:
        Set that book was changed
        i.e. text was saved to 
        "booksData/changedText".
        '''
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE books SET textChanged = 1 WHERE bookName = ?", (bookName,))
        self.conn.commit()
    
    def get_changedText(self, bookName):
        '''
        DESCRIPTION:
        Check if book was changed.
        '''
        books = self.cursor.execute("SELECT textChanged FROM books WHERE bookName = ?", (bookName, ))
        try:
            books = [book for book in books]
            if int(books[0][0]) == 0:
                return(False)
            else:
                return(True)
        except:
            print('get_bookmarks: error')
            return(False)

    def set_last_book(self, bookName):
        '''
        DESCRIPTION:
        set book with bookName as last opend.
        '''
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE books SET last = 0 WHERE last = 1")
        self.conn.commit()
        self.cursor.execute("UPDATE books SET last = 1 WHERE bookName = ?", (bookName, ))
        self.conn.commit()

    def get_last_bookName(self):
        '''
        DESCRIPTION:
        Get last opened book. 
        '''
        self.cursor = self.conn.cursor()
        books = self.cursor.execute("SELECT bookName FROM books WHERE last = 1")
        try:
            books = [book for book in books]
            return(books[0][0])
        except:
            print('get_last_bookName: error')
            return(None)
        
    def get_bookmarks(self, bookName):
        '''
        DESCRIPTION:
        Get all bookmarks for book.
        '''
        self.cursor = self.conn.cursor()
        
        books = self.cursor.execute("SELECT bookmarks FROM books WHERE bookName = ?", (bookName, ))
        try:
            books = [book for book in books]
        except:
            print('get_bookmarks: error')
            return({})
        return(eval(books[0][0]))

    def set_bookmarks(self, bookName, bookmarksDict):
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE books SET bookmarks = ? WHERE bookName = ?",
                            (str(bookmarksDict), bookName,))
        self.conn.commit()
    
    def get_pathAndFile_of_book(self, bookName):
        '''
        DESCRIPTION:
        STATUS:
        Unused.
        '''
        self.cursor = self.conn.cursor()
        books = self.cursor.execute("SELECT bookPath FROM books WHERE bookName = ?", (bookName, ))
        try:
            books = [book for book in books]
            pathAndFile = os.path.join(books[0][0], bookName)
        except:
            print('get_pathAndFile_of_book: error')
            return('')
        return(pathAndFile)

    def add_or_change_book(self, bookName, bookmarksDict, last=1, textChanged=0):
        '''
        DESCRIPTION:
        Add book, rewrite if needed and set
        as last to db.
        '''
        self.cursor = self.conn.cursor()
        # booksList = self.cursor.execute("SELECT bookName, bookmarks FROM books")
        # if bookName in [book[0] for book in booksList]:
        
        # bookName = os.path.basename(bookPathAndFile)
        # bookPath = os.path.dirname(bookPathAndFile)

        self.cursor.execute("DELETE FROM books WHERE bookName = ?", (bookName,))
        self.conn.commit()
        # textChanged = 0
        # print((last, bookName, bookmarksDict, textChanged))
        self.cursor.execute("INSERT INTO books VALUES (?,?,?,?)",
                            (last, bookName, str(bookmarksDict), textChanged,))
        self.conn.commit()
        
        if last == 1:
            self.set_last_book(bookName)
        
    def select_all_books_names(self):
        '''
        DESCRIPTION:
        Select all books names from db.
        STATUS:
        Used for choicing book window. 
        '''
        self.cursor = self.conn.cursor()
        books = self.cursor.execute("SELECT bookName FROM books")
        booksList = [book for book in books]
        return(booksList)

    def select_all_books(self):
        '''
        DESCRIPTION:
        STATUS:
        Unused.
        '''
        self.cursor = self.conn.cursor()
        books = self.cursor.execute("SELECT * FROM books")
        booksList = [book for book in books]
        return(booksList)

    def close_connection(self):
        self.conn.close()
    
    def open_connection(self):
        self.conn = sqlite3.connect('storage.db')

    
