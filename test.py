import pyttsx as pyttsx
import time


class Translator():
    def __init__(self):
        self.line = 0
        self.listeners = []
        
    def __add__(self, k):
        self.line = self.line + k
        for listener in self.listeners:
            listener._call()#textFrame.event_generate('<<myEvent>>')

    def add_listener(self, listener):
        self.listeners.append(listener)


pause = False
i = 0

# textObj = Translator()


def start_engine(engine=None):
    if engine is None:
        engine = pyttsx.init()
    engine.setProperty("rate", 170)
    if not engine._inLoop:
        engine.startLoop(False)
    engine.say("Ready")
    engine.iterate()
    # engine.endLoop()
    return(engine)


def say_text(engine, text):
    '''
    for seq in text:
        if not pause:
            engine.say(seq)
            time.sleep(3)
        else:
            print("pause")
            return(0)
    return(0)
    '''
    global i
    
    #i = 0
    def onEnd(name, completed):                
        #print(("finishing",name,engine.isBusy()))
        global i
        global pause
        #global textObj

        i = i+1
        #print(i)
        
        if i < len(text) and not pause:
            #textObj+1
            try:
                engine.say(text[i])
            except:
                print("exception i")
        else:
            engine.disconnect(cn)
            
            # if not pause then text ended
            if not pause:
                i = 0
            else:
                # play from one sequence back
                if i>0:
                    i = i-1
            print("disconnected first")

    cn = engine.connect("finished-utterance", onEnd)
    engine.say(text[i])


def stop_engine(engine):
    engine.endLoop()
    engine.stop()


#def test():
#    engine.proxy.startLoop(True)

#engine.proxy._driver.__init__(engine.proxy)    
