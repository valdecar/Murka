from tkinter import Tk, Frame, Label, Button, Entry, Listbox, Text, Checkbutton, Menu
from tkinter import filedialog
from tkinter import StringVar, END, NORMAL, EXTENDED, VERTICAL, HORIZONTAL, INSERT, N, S, E, W
from tkinter import messagebox
from tkinter import ttk
import time
import test
import parsers
import storage
import os
import pathsAndTypes as pathes
import settingsAgent
'''
! system settings
! thems
! buttons order
'''


class Tool(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid(row=0, column=0)
        
        # on window close
        ##self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.focus_set()

        def key(event):
            if test.pause:
                test.pause = False
                self.play()
            else:
                test.pause = True
                
            print("pressed %s" % repr(event.char))
            
        self.bind("<space>", key)
        
        # book pathes and storage controller
        self.bookAgent = pathes.BookNamesAgent()

        # engine
        self.engine = test.start_engine()

        # for selection during speech
        self.textInsertBusy = False
    
        # settings
        self.settingsDict = settingsAgent.load_settings()

        # menu
        self.menubar = Menu(self)
        # self['menu'] = self.menubar

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Open New Book", command=self.open_file)
        menu.add_command(label="Choice book from history",
                         command=self.choice_book)
        menu.add_command(label="Save current",
                         command=self.bookAgent.save_book_opend)
        menu.add_command(label="Save current as new book",
                         command=self.choice_name_for_book)
        
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Settings", menu=menu)
        menu.add_command(label="Voice settings",
                         command=self.choice_language)
        menu.add_command(label="Text color settings",
                         command=self.choice_colors)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Bookmarks", menu=menu)
        menu.add_command(label="bookmarks",
                         command=self.open_bookmarks)
        menu.add_command(label="save bookmark from cursor",
                         command=self.save_bookmark)

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)

        # description
        self.desc = "book storing"
        self.labelDesc = Label(self, text=self.desc)
        self.labelDesc.grid(row=0, column=1)

        # choice book
        self.buttonChoiceBook = Button(self, text='choice book',
                                       command=self.choice_book)
        self.buttonChoiceBook.grid(row=1, column=0)
        
        # save book
        self.buttonSaveBook = Button(self, text='save current book',
                                     command=self.bookAgent.save_book_opend)
        self.buttonSaveBook.grid(row=1, column=1)
        
        # save as new book
        self.buttonSaveAsNew = Button(self, text="save as new",
                                      command=self.choice_name_for_book)
        self.buttonSaveAsNew.grid(row=1, column=2)
        
        # description
        self.labelDesc = Label(self, text="book editing")
        self.labelDesc.grid(row=2, column=1)

        # reset i button
        self.buttonResetI = Button(self, text='reset i', command=self.reset_i_refill)
        self.buttonResetI.grid(row=3, column=0)

        self.labelPlayDesc = Label(self, text="book plaing")
        self.labelPlayDesc.grid(row=4, column=1)
        
        # play from cursore button
        self.buttonPlayFromCursore = Button(self, text="play from cursore",
                                            command=self.play_from_cursore)
        self.buttonPlayFromCursore.grid(row=5, column=2)
        
        # play button
        self.buttonPlay = Button(self, text="play", command=self.play)
        self.buttonPlay.grid(row=5, column=0)
        
        # pause button
        self.buttonPause = Button(self, text="pause", command=self.pause)
        self.buttonPause.grid(row=5, column=1)
        # self.labelPauseDesc = Label(self, text="pause book")
        # self.labelPauseDesc.grid(row=3, column=1)
        

        # narrator settings
        # self.buttonChoiceLanguage = Button(self, text="choice language",
        #                                    command=self.choice_language)
        # self.buttonChoiceLanguage.grid(row=1, column=2)
        
        # self.labelDer = Label(self, text="*************")
        # self.labelDer.grid(row=4, column=0)
                
        # open file
        # self.buttonOpenFile = Button(self, text="open file",
        #                              command=self.open_file)
        # self.buttonOpenFile.grid(row=5, column=0)
        # self.labelOpenFileDesc = Label(self, text="open file")
        # self.labelOpenFileDesc.grid(row=5, column=1)
        
        
        # for autoscrolling
        self.aScrollI = test.i
        self.aScrollDelta = 1

        # for autosaving
        self.aSaveI = test.i
        self.aSaveDelta = 10

        # check autoscrolling flag
        self.autoscrolling = StringVar()
        self.autoscrolling.set('True')
        self.checkAutoscroll = Checkbutton(self, text='autoscrolling',
                                           variable=self.autoscrolling,
                                           onvalue='True', offvalue='False')
        self.checkAutoscroll.grid(row=6, column=0)
        
        # bookmarks
        # self.buttonOpenBookmarks = Button(self, text='bookmarks',
        #                                  command=self.open_bookmarks)
        # self.buttonOpenBookmarks.grid(row=6, column=1)
        # self.buttonSaveBookmark = Button(self, text='save bookmark',
        #                                 command=self.save_bookmark)
        # self.buttonSaveBookmark.grid(row=6, column=2)

        # BEGIN OF text:

        # width = root.winfo_screenwidth()
        # height = root.winfo_screenheight()
        self.textFrame = Text(self, width=700, height=100)  # 700 30
        # frame take 3 column
        self.textFrame.grid(row=8, column=0,
                            columnspan=3)  # , sticky=(N, S, E, W)

        # scroollbar for text frame
        self.scrollTextFrame = ttk.Scrollbar(self, orient=VERTICAL,
                                             command=self.textFrame.yview)
        self.scrollTextFrame.grid(row=8, column=3, sticky=(N, S))
        self.textFrame['yscrollcommand'] = self.scrollTextFrame.set
        
        # adding tag to text
        self.textFrame.tag_add('myFontTag', '1.0', 'end')

        # tags for default and selected text
        self.myFontTagDeffault = (200, 200, 200)
        self.myFontTagSelectedDeffault = (70, 70, 70)
        self.myFontTagSelectedCurrentlyDeffault = (90, 90, 90)
        
        # load user's tags settings
        self.myFontTagNew = self.settingsDict['myFontTag']
        self.myFontTagSelectedNew = self.settingsDict['myFontTagSelected']
        self.myFontTagSelectedCurrentlyNew = self.settingsDict['myFontTagSelectedCurrently']

        self.textFrame.tag_configure('myFontTag',
                                     font='helvetica 24 bold',
                                     background="#%02x%02x%02x"
                                     % self.myFontTagNew,
                                     relief='raised')
        self.textFrame.tag_configure('myFontTagRead',
                                     font='helvetica 24 bold',
                                     background="#%02x%02x%02x"
                                     % (100, 100, 100),
                                     relief='raised')
        self.textFrame.tag_configure('myFontTagSelected',
                                     font='helvetica 24 bold',
                                     background="#%02x%02x%02x"
                                     % self.myFontTagSelectedNew,
                                     relief='raised')
        self.textFrame.tag_configure('myFontTagChanged',
                                     font='helvetica 24 bold',
                                     background="#%02x%02x%02x"
                                     % (50, 50, 100),
                                     relief='raised')
        # tag for currently readed text
        self.textFrame.tag_configure('myFontTagSelectedCurrently',
                                     font='helvetica 24 bold',
                                     background="#%02x%02x%02x"
                                     % self.myFontTagSelectedCurrentlyNew,
                                     relief='raised')
        # update text
        self.buttonUpdateText = Button(self, text='update',
                                       command=self.text_update)
        self.buttonUpdateText.grid(row=3, column=2)

        # clear text
        self.buttonClearText = Button(self, text='clear',
                                      command=self.clear_text)
        self.buttonClearText.grid(row=3, column=1)

        # END OF: text.
        
        # BEGIN OF bind events:

        # other aproach to handle events
        # found in:
        # http://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
        
        # rename textFrame id (for tcl) (otherwise it not show frame)
        self.textFrame._orig = self.textFrame._w + "_orig"
        # print(self.textFrame._w)
        self.tk.call("rename", self.textFrame._w, self.textFrame._orig)

        # register callback for any modified text event
        self.tk.createcommand(self.textFrame._w, self._proxy)
        # print(self.textFrame._w)

        # END OF bind events.

        # BEGIN OF scale:

        # adding scale to text
        self.scaleTextFrame = ttk.Scale(self, orient=HORIZONTAL, length=200,
                                        from_=10.0, to=50.0,
                                        command=self.scale_command)
        self.scaleTextFrame.grid(row=7, column=1,
                                 columnspan=2, sticky=(N, S, W, E))
        # label for scale
        self.labelScale = Label(self, text='Scale text',)
        self.labelScale.grid(row=7, column=0, sticky=(E))
        
        # END OF scale.
        
        # label for status
        # self.varForStatus = StringVar()
        self.labelStatus = Label(self, text='status', textvariable="status")
        self.labelStatus.grid(row=9, column=0, sticky=(W))
        # self.varForStatus.set("Redy")
        
        # resize behavior
        self.parent.columnconfigure(0, weight=1)
        for i in range(3):
            self.columnconfigure(i, weight=1, minsize=30)
        self.parent.rowconfigure(0, weight=1)
        self.rowconfigure(8, weight=1, minsize=10)

        # load last book
        if self.bookAgent.db.last is not None:
            try:
                # open book and set test.i
                text = self.bookAgent.open_book_stored(self.bookAgent.db.last)
                self.reset_i_save()
                self.reset_i_scroll()
                self.import_text_to_frame(text)
                
                # scale to current cursor position
                self.textFrame.yview('%d' % (test.i))
            except:
                print("open_book: error open book")
        else:
            print('Warning: loading last fail')

    def choice_colors(self):
        root = Tk()
        child1 = ChoiceColors(root, self)
        h = 400
        w = 400
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (w, h, x/2-30, y/2-30))

    def choice_name_for_book(self):
        '''
        DESCRIPTION:
        Choice name for new book.
        '''
        root = Tk()
        child1 = SetBookName(root, self)
        h = 400
        w = 400
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (w, h, x/2-30, y/2-30))

    def open_bookmarks(self):
        '''
        DESCRIPTION:
        Load bokmarks and
        open bookmarks windows.
        '''
        bookmarksDict = self.bookAgent.get_bookmarks()
        bookmarks = list(bookmarksDict.keys())
        root = Tk()
        child1 = ChoiceBookmark(root, self, bookmarks)
        h = 400
        w = 400
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (w, h, x/2-30, y/2-30))
        root.wm_title("bookmarks list")
        
    def save_bookmark(self):
        '''
        DESCRIPTION:
        Save current cursor position to db
        as bookmark.
        '''
        lineId = self.textFrame.index(INSERT).split('.')[0]

        if self.bookAgent.set_bookmark(lineId) == 1:
            print("open book first")

    def choice_book(self):
        '''
        DESCRIPTION:
        Choice book from history.
        '''
        books = self.bookAgent.db.select_all_books_names()
        booksNames = [book[0] for book in books]
        # self.bookmarksDict = [book[2] for book in books]
        root = Tk()
        child1 = ChoiceBook(root, self, booksNames)
        h = 400
        w = 400
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (w, h, x/2-30, y/2-30))
        root.wm_title("Choice book")

    def reset_i_refill(self):
        self.reset_i()
        self.import_text_to_frame(self.bookAgent.text)

    def reset_i(self, _to=0):
        '''
        DESCRIPTION:
        Set test i ether 0 or _to.
        Also set aScrollI to 0 for scrolling.
        Also set aSaveI to 0.
        '''
        self.bookAgent.reset_i(_to)
        self.reset_i_scroll()
        self.reset_i_save()

    def reset_i_save(self):
        self.aSaveI = test.i

    def reset_i_scroll(self):
        self.aScrollI = test.i

    def set_scroll(self):
        # scroll to current
        if test.i > 2:
            print("scroling work")
            print(test.i)
            self.textFrame.yview('%d' % (test.i-2))

    def text_update(self):
        '''
        DESCRIPTION:
        Update text from textFrame to test.text for engine
        '''
        print(self.textFrame.index(INSERT))
        self.bookAgent.text = []

        textStr = ""
        # count = self.textFrame.count('1.0', 'end', 'lines')[0]
        # print(count)
        
        # for python3.2 bag
        count = self.tk.call(self.textFrame._w, 'count',
                              *('-lines', '1.0', 'end' ))
        print(count)
        for i in range(count+1)[1:]:
            line = self.textFrame.get('%d.0' % i, '%d.end' % i)
            if len(line) > 0:
                textStr = textStr + line
        textStr = textStr +"\n" +'end of text'
        
        # parse book and import to frame
        self.bookAgent.text = parsers.parse_book_from_str(textStr)
        self.clear_text(clearI=False)
        self.import_text_to_frame(self.bookAgent.text)
 
        # chek textChanged indicator
        self.bookAgent.textChanged = True

        print("len from text_update: %d" % len(self.bookAgent.text))

    def on_text_modified(self, *args):
        '''
        DESCRIPTION:
        When some modified hapend show count of 
        text and reset event flag
        '''
        print(self.textFrame.count('1.0', 'end', 'lines'))
        
        # reset modified flag
        # self.tk.call(self.textFrame._w, 'edit', 'modified', False)
        # reset modified flag
        self.textFrame.edit_modified(False)

    def _proxy(self, command, *args):
        '''
        DESCRIPTION:
        this is other aproach for catching modified of text event
        
        Change tag of inserted text.
        '''
        # print(args)
        cmd = (self.textFrame._orig, command) + args
        # print(cmd)
        if command in ("insert", "delete", "replace", "edit"):
            # lineId = int(self.textFrame.index(INSERT).split('.')[0])
            # lineFrameText = self.textFrame.get('%d.0' % lineId,
            #                                    '%d.end' % lineId)
            # charId = int(self.textFrame.index(INSERT).split('.')[1])
            # lineForInsert = lineFrameText[:charId]+args[1]+lineFrameText[charId:]
            # lineForDelete = lineFrameText[:charId-1]+lineFrameText[charId:]
            # elif self.changedTextLines[lineId] == lineForInsert:
            # elif self.changedTextLines[lineId] == lineForDelete:
            # print(cmd)

            if command in ("insert"):
                # print(self.textFrame.index(INSERT))
                # 'if' for some bag with doublication
                if 'myFontTag' not in cmd:
                    # check if selection during speech
                    if not self.textInsertBusy:
                        # add tag to inserted text
                        cmd = cmd + ('myFontTagChanged',)
            
        # because we oweride modified text event we should
        # return something insted (i.e. modified text manualy)
        # (if not, nothing happend)
        result = self.tk.call(cmd)
        
        if command in ("insert"):
                # print(self.textFrame.index(INSERT))
                # 'if' for some bag with doublication
                if 'myFontTag' not in cmd:
                    # check if selection during speech
                    if not self.textInsertBusy:
                        if len(cmd[-2]) > 100:
                            self.textFrame.yview('end')
                            print("scale to end")
                            # print(cmd)
                        
            
        return(result)

    def clear_text(self, clearI=True, clearText=False):
        if clearI:
            self.reset_i()
        if clearText:
            self.bookAgent.text = []
        
        # python3.2 bag # print(self.textFrame.count('1.0', 'end', 'lines'))
        self.textFrame.delete('1.0', 'end')

    def _call(self, t=None):
        '''
        DESCRIPTION
        for recolored text interactively
        '''
        # i = test.i if test.i > 0 else 1
        i = test.i
        if i > 0 and not test.pause:
            # recolored text
            self.textInsertBusy = True
            lineText = self.textFrame.get('%d.0' % i, '%d.end' % i)
            self.textFrame.delete('%d.0' % i, '%d.end' % i)
            self.textFrame.insert('%d.0' % i, lineText, ('myFontTagSelected'))

            # currently readed text
            lineText = self.textFrame.get('%d.0' % (i+1), '%d.end' % (i+1))
            self.textFrame.delete('%d.0' % (i+1), '%d.end' % (i+1))
            self.textFrame.insert('%d.0' % (i+1), lineText,
                                  ('myFontTagSelectedCurrently'))

            self.textInsertBusy = False

        # autoscrolling
        if test.i > self.aScrollI+self.aScrollDelta:
            self.aScrollI = self.aScrollI + self.aScrollDelta
            if self.autoscrolling.get() == 'True':
                self.textFrame.yview('%d' % (test.i-1))

        # autosaving
        if test.i > self.aSaveI+self.aSaveDelta:
            self.aSaveI = self.aSaveI + self.aSaveDelta
            self.bookAgent.set_bookmark_current()
            print("autosaving done")
            
        # for selecting text samolteniusly with reading
        self.parent.after(100, self._call)

    def scale_command(self, value):
        '''
        DESCRIPTION:
        change font of text while scaling
        using tag 'myFontTag'
        '''
        # print(self.textFrame.index(INSERT))
        # print(value)
        self.textFrame.tag_configure('myFontTag',
                                     font='helvetica %s bold'
                                     % value.split('.')[0])
        self.textFrame.tag_configure('myFontTagSelected',
                                     font='helvetica %s bold'
                                     % value.split('.')[0])

    def on_closing(self):
        '''
        DESCRIPTION:
        Show ask messagebox and play exiting frase
        '''
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.engine.say("exiting murka")
            time.sleep(1.0)
            test.stop_engine(self.engine)
            time.sleep(0.3)
            self.parent.destroy()

    def open_file(self):
        '''
        DESCRIPTION
        Open file and parse it,
        then plaice it itro textFrame
        line by line.
        Add entry to database.
        Save text to "booksData/books"
        as "bookName.txt" file.
        Save as last.
        '''

        # open dialog for choicing file
        bookPathAndFile = filedialog.askopenfilename(parent=self)
        print("bookPathAndFile=%s" % bookPathAndFile)
       
        # set book names
        self.bookAgent.set_book_name_from_full(bookPathAndFile)

        # importing text to frame
        text = self.bookAgent.import_text_new(bookPathAndFile)
        self.reset_i()
        self.reset_i_save()
        self.reset_i_scroll()
        self.import_text_to_frame(text)
        
        # save text
        self.bookAgent.save_book_new()
        
        # save as last
        # bookName = os.path.basename(bookFileName)
        # self.db.set_last_book(bookName)

        # print("5="+self.textFrame.get('5.0', '5.end'))
        # print("5 actual = "+self.text[5])
        # print(self.textFrame.index('end-1 line'))
        print("len from open_file: %d " % len(self.bookAgent.text))
        # print("2="+self.textFrame.get('2.0', 'end'))
        
    def import_text_to_frame(self, _text):
        '''
        DESCRIPTION:
        Load text from _text to textFrame.
        '''
        self.clear_text(False)
        
        # insert text into textFrame
        self.textInsertBusy = True
        for i in range(len(_text)+1)[1:]:
            # adding end to any line (for textFrame.insert)
            if '\n' not in _text[i-1]:
                backspace = '\n'
            else:
                backspace = ''
            if i < test.i:
                self.textFrame.insert('end', _text[i-1]+backspace,
                                      ('myFontTagSelected'))
            else:
                self.textFrame.insert('end', _text[i-1]+backspace,
                                      ('myFontTag'))
        self.textInsertBusy = False
        # self.textFrame.yview_moveto('0.5')
        # self.textFrame.yview('5')
       
    def play_from_cursore(self):
        '''
        DESCRIPTION:
        Play from current cursore.
        '''
        lineId = self.textFrame.index(INSERT).split('.')[0]
        print(lineId)
        # test.i = int(lineId)
        self.reset_i(int(lineId)-1)
        test.pause = True
        self.play()

    def play(self):
        '''
        DESCRIPTION:
        Play text line by line 
        from self.bookAgent.text.
        '''
        print(test.i)
        if test.pause:
            test.pause = False
        if self.bookAgent.text is not None:
            # print('text')
            # print(self.bookAgent.text)
            test.say_text(self.engine, self.bookAgent.text)  # , self.textFrame
        else:
            print("test is none")

    def pause(self):
        test.pause = True
        print(self.aScrollI)
        print(self.bookAgent.get_i())
        print(self.autoscrolling.get())

    def choice_language(self):
        '''
        DESCRIPTION:
        Choice engine settings.
        '''
        voices = self.engine.getProperty("voices")
        print([voice.languages for voice in voices])
        try:
            voicesNames = [voice.languages[0] for voice in voices]
        except:
            voicesNames = [voice.name for voice in voices]
        root = Tk()
        child1 = ChoiceLanguage(root, self, voicesNames)
        h = 400
        w = 400
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (w, h, x/2-30, y/2-30))
        root.wm_title("Voice settings")


class Choice(Frame):
    '''
    DESCRIPTION:
    Base class, used for choicing.
    Contain Listbox and done button.
    Constructor get list of items for choicing from.
    '''
    def __init__(self, parent, parentWindow, itemsList):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid(row=0, column=0)

        self.parentWindow = parentWindow
        self.items = itemsList

        # create list with items
        self.listBox = Listbox(self, selectmode=EXTENDED)
        self.listBox.grid(row=1, column=1)
        # insert items to listBox
        for item in self.items:
            self.listBox.insert(END, item)
        
        self.buttonDone = Button(self, text="choice", command=self.done)
        self.buttonDone.grid(row=3, column=0)

    def done(self):
        lb = self.listBox
        items = list(map(int, lb.curselection()))
        print(items)
        self.parent.destroy()


class ChoiceBook(Choice):
    def __init__(self, parent, parentWindow, itemsList):
        # supr(createSets,self).__init__(parent)
        Choice.__init__(self, parent, parentWindow, itemsList)

        self.buttonDeliteBook = Button(self, text="delete",
                                           command=self.delete_book)
        self.buttonDeliteBook.grid(row=0, column=0)
    
    def delete_book(self):
        '''
        DESCRIPTION:
        Delete book from list, from self.items,
        from db, from books directorys.
        '''
        # get selected items
        lb = self.listBox
        items = list(map(int, lb.curselection()))
        
        # get values from listbox
        keys = lb.get('0', 'end')
        print(keys)
        print(self.items)

        booksNames = []

        for item in items:

            booksNames.append(keys[item])

            # delete from listBox
            self.listBox.delete(item)

            # delete from items
            self.items.pop(self.items.index(keys[item]))
        
        # rewrite entry in db
        self.parentWindow.bookAgent.delete_books(booksNames)
        print(booksNames)
        print(items)
    
    def done(self):
        '''
        DESCRIPTION:
        Load data from db.
        Use it for current textFrame and test.i.
        '''
        lb = self.listBox
        items = list(map(int, lb.curselection()))
        print(items)
        currentBookName = self.items[items[0]]
        print(currentBookName)

        # open book and save it as last
        self.parentWindow.bookAgent.open_book_stored(currentBookName)
        
        self.parentWindow.bookAgent.db.set_last_book(currentBookName)
        text = self.parentWindow.bookAgent.text
        self.parentWindow.import_text_to_frame(text)
        self.parentWindow.reset_i_save()
        self.parentWindow.reset_i_scroll()
        self.parentWindow.textFrame.yview('%d' % (test.i))
        self.parent.destroy()


class ChoiceBookmark(Choice):
    def __init__(self, parent, parentWindow, itemsList):
        # supr(createSets,self).__init__(parent)
        Choice.__init__(self, parent, parentWindow, itemsList)

        self.buttonDeliteBookmark = Button(self, text="delete",
                                           command=self.delete_bookmark)
        self.buttonDeliteBookmark.grid(row=0, column=0)
    
    def delete_bookmark(self):
        '''
        DESCRIPTION:
        Delete bookmarks from list, from self.items,
        from db.
        '''
        # get selected items
        lb = self.listBox
        items = list(map(int, lb.curselection()))
        
        # get dictionary for current book from db
        bookmarksDict = self.parentWindow.bookAgent.db.get_bookmarks()
        print(bookmarksDict)
        print(items)

        # get values from listbox
        keys = lb.get('0', 'end')
        print(keys)
        print(self.items)

        for item in items:
            # delete from dictinacy
            bookmarksDict.pop(keys[item])
            # delete from listBox
            self.listBox.delete(item)
            # delete from items
            self.items.pop(self.items.index(keys[item]))
        
        # rewrite entry in db
        self.parentWindow.bookAgent.rewrite_bookmarks(bookmarksDict)
        print(bookmarksDict)
        print(items)
    
    def done(self):
        '''
        DESCRIPTION:
        Get selected bookmark and use it for test.i. 
        '''
        # get selected items
        lb = self.listBox
        items = list(map(int, lb.curselection()))
        bookmarkId = self.listBox.get(items[0])
        print(items)
        
        # get bookmark from db
        bookmarksDict = self.parentWindow.bookAgent.get_bookmarks()
        print(bookmarksDict)
        print(bookmarkId)
        
        # change test.i
        currentBookmark = bookmarksDict[str(bookmarkId)]
        self.parentWindow.reset_i(_to=int(currentBookmark))

        self.parent.destroy()


class ChoiceLanguage(Choice):
    def __init__(self, parent, parentWindow, itemsList):
        # super(createSets,self).__init__(parent)
        Choice.__init__(self, parent, parentWindow, itemsList)

        self.voices = self.parentWindow.engine.getProperty("voices")
        self.defaultVoice = self.parentWindow.engine.getProperty('voice')

        self.buttonChoice = Button(self, text="choice language",
                                   command=self.choice_language)
        self.buttonChoice.grid(row=0, column=0)
    
        self.entry = Entry(self, state=NORMAL)
        # self.entry.focus_set()
        self.entry.insert(0, "170")
        self.entry.grid(row=2, column=0)
        
        self.buttonChangeRate = Button(self, text='change rate',
                                       command=self.change_rate)
        self.buttonChangeRate.grid(row=2, column=1)

        self.buttonDefault = Button(self, text='set default',
                                    command=self.set_default)
        self.buttonDefault.grid(row=3, column=0)

        self.buttonDone = Button(self, text="done", command=self.done)
        self.buttonDone.grid(row=4, column=0)

    def set_default(self):
        self.parentWindow.engine.setProperty('rate', 170)
        self.parentWindow.engine.setProperty('voice', self.defaultVoice)

    def choice_language(self):
        lb = self.listBox
        items = list(map(int, lb.curselection()))
        print(items)
        self.parentWindow.engine.setProperty('voice', self.voices[items[0]].id)

    def change_rate(self):
        rate = int(self.entry.get())
        self.parentWindow.engine.setProperty('rate', rate)

    def done(self):
        # self.parentWindow.childResultList = self.listBox.get(0, END)
        # print(self.listBox.get(0,END))
        self.parent.destroy()


class SetBookName(Frame):
    def __init__(self, parent, parentWindow):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid(row=0, column=0)

        self.parentWindow = parentWindow
        
        self.entry = Entry(self, state=NORMAL)
        self.entry.focus_set()
        self.entry.insert(0, "newBookName")
        self.entry.grid(row=1, column=0)
    
        
        self.buttonDone = Button(self, text="choice", command=self.done)
        self.buttonDone.grid(row=2, column=0)

    def done(self):
        bookName = self.entry.get()

        # parse text
        self.parentWindow.text_update()
       
        # save text as new book
        self.parentWindow.bookAgent.set_book_name_from_name(bookName)
        self.parentWindow.bookAgent.save_book_new()
        
        self.parent.destroy()


class ChoiceColors(Choice):
    def __init__(self, parent, parentWindow, itemsList=[]):
        # super(createSets,self).__init__(parent)
        Choice.__init__(self, parent, parentWindow, itemsList)
        
        # hide listbox
        self.listBox.grid_forget()

        # change myFontTag
        self.entryMyFontTag = Entry(self, state=NORMAL)
        # self.entry.focus_set()
        self.entryMyFontTag.insert(0, str(self.parentWindow.myFontTagNew))
        self.entryMyFontTag.grid(row=2, column=0)
        self.buttonChangeMyFontTag = Button(self, text='myFontTag',
                                            command=self.change_myFontTag)
        self.buttonChangeMyFontTag.grid(row=2, column=1)
        
        # change myFontTagSelected
        self.entryMyFontTagSelected = Entry(self, state=NORMAL)
        # self.entry.focus_set()
        self.entryMyFontTagSelected.insert(0, 
                                           str(self.parentWindow.myFontTagSelectedNew))
        self.entryMyFontTagSelected.grid(row=3, column=0)
        self.buttonChangeMyFontTagSelected = Button(self, 
                                                    text='myFontTagSelected',
                                                    command=self.change_myFontTagSelected)
        self.buttonChangeMyFontTagSelected.grid(row=3, column=1)
        
        # change myFontTagSelectedCurrently
        self.entryMyFontTagSelectedCurrently = Entry(self, state=NORMAL)
        # self.entry.focus_set()
        self.entryMyFontTagSelectedCurrently.insert(0, 
                                                    str(self.parentWindow.myFontTagSelectedCurrentlyNew))
        self.entryMyFontTagSelectedCurrently.grid(row=4, column=0)
        self.buttonChangeMyFontTagSelectedCurrently = Button(self,
                                                             text='myFontTagSelectedCurrently',
                                                             command=self.change_myFontTagSelectedCurrently)
        self.buttonChangeMyFontTagSelectedCurrently.grid(row=4, column=1)
        
        self.buttonDefault = Button(self, text='set default',
                                    command=self.set_default)
        self.buttonDefault.grid(row=5, column=1)

        self.buttonDone = Button(self, text="done", command=self.done)
        self.buttonDone.grid(row=6, column=0)

    def set_default(self):
        # tags for default and selected text
        self.entryMyFontTag.delete('0', 'end')
        self.entryMyFontTagSelected.delete('0', 'end')
        self.entryMyFontTagSelectedCurrently.delete('0', 'end')
        
        self.parentWindow.myFontTagNew = self.parentWindow.myFontTagDeffault
        self.parentWindow.myFontTagSelectedNew = self.parentWindow.myFontTagSelectedDeffault
        self.parentWindow.myFontTagSelectedCurrentlyNew = self.parentWindow.myFontTagSelectedCurrentlyDeffault
        
        # save settings
        self.parentWindow.settingsDict['myFontTag'] = self.parentWindow.myFontTagDeffault
        self.parentWindow.settingsDict['myFontTagSelected'] = self.parentWindow.myFontTagSelectedDeffault
        self.parentWindow.settingsDict['myFontTagSelectedCurrently'] = self.parentWindow.myFontTagSelectedCurrentlyDeffault
        settingsAgent.save_settings(self.parentWindow.settingsDict)

        self.entryMyFontTag.insert(0, str(self.parentWindow.myFontTagDeffault))
        self.entryMyFontTagSelected.insert(0,
                                           str(self.parentWindow.myFontTagSelectedDeffault))
        self.entryMyFontTagSelectedCurrently.insert(0,
                                                    str(self.parentWindow.myFontTagSelectedCurrentlyDeffault))
        self.parentWindow.textFrame.tag_configure('myFontTag',
                                                  font='helvetica 24 bold',
                                                  background="#%02x%02x%02x"
                                                  % self.parentWindow.myFontTagDeffault,
                                                  relief='raised')
        self.parentWindow.textFrame.tag_configure('myFontTagSelected',
                                                  font='helvetica 24 bold',
                                                  background="#%02x%02x%02x"
                                                  % self.parentWindow.myFontTagSelectedDeffault,
                                                  relief='raised')
        # tag for currently readed text
        self.parentWindow.textFrame.tag_configure('myFontTagSelectedCurrently',
                                                  font='helvetica 24 bold',
                                                  background="#%02x%02x%02x"
                                                  % self.parentWindow.myFontTagSelectedCurrentlyDeffault,
                                                  relief='raised')

    def change_myFontTag(self):
        tag = eval(self.entryMyFontTag.get())
        try:
            self.parentWindow.textFrame.tag_configure('myFontTag',
                                                      font='helvetica 24 bold',
                                                      background="#%02x%02x%02x"
                                                      % tag,
                                                      relief='raised')
            self.parentWindow.myFontTagNew = tag
            
            # save settings 
            self.parentWindow.settingsDict['myFontTag'] = self.parentWindow.myFontTagNew
            settingsAgent.save_settings(self.parentWindow.settingsDict)
        except:
            print('wrong tag = %s' % tag)

    def change_myFontTagSelected(self):
        tag = eval(self.entryMyFontTagSelected.get())
        try:
            self.parentWindow.textFrame.tag_configure('myFontTagSelected',
                                                      font='helvetica 24 bold',
                                                      background="#%02x%02x%02x"
                                                      % tag,
                                                      relief='raised')
            self.parentWindow.myFontTagSelectedNew = tag
            
            # save settings 
            self.parentWindow.settingsDict['myFontTagSelected'] = self.parentWindow.myFontTagSelectedNew
            settingsAgent.save_settings(self.parentWindow.settingsDict)
        except:
            print('wrong tag = %s' % tag)

    def change_myFontTagSelectedCurrently(self):
        tag = eval(self.entryMyFontTagSelectedCurrently.get())
        try:
            self.parentWindow.textFrame.tag_configure('myFontTagSelectedCurrently',
                                                      font='helvetica 24 bold',
                                                      background="#%02x%02x%02x"
                                                      % tag,
                                                      relief='raised')
            self.parentWindow.myFontTagSelectedCurrentlyNew = tag

            # save settings 
            self.parentWindow.settingsDict['myFontTagSelectedCurrently'] = self.parentWindow.myFontTagSelectedCurrentlyNew
            settingsAgent.save_settings(self.parentWindow.settingsDict)
        except:
            print('wrong tag = %s' % tag)

    def done(self):
        # self.parentWindow.childResultList = self.listBox.get(0, END)
        # print(self.listBox.get(0,END))
        self.parent.destroy()


if __name__ == "__main__":
    root = Tk()
    app = Tool(root)
    h = 700  # app.winfo_height()
    w = 730  # app.winfo_width()
    x = root.winfo_screenwidth()
    y = root.winfo_screenheight()
    print('%dx%d+%d+%d' % (w, h, x/2, y/2))
    root.geometry('%dx%d+%d+%d' % (w, h, x/2, y/2))
    root.wm_title("Murka")
    
    # add self to event listener
    # it seems if test given too complicated
    # object (like app) it will not produce
    # events 
    #test.textObj.add_listener(app)
    
    # for text selecting interactively
    root.after(300, app._call)
    root.mainloop()
