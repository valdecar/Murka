#!/usr/bin/python3
import gui

if __name__ == "__main__":
    root = gui.Tk()
    app = gui.Tool(root)
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
