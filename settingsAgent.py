def load_settings():
    try:
        with open('settings.txt') as f:
            settings = f.read()
        settings = eval(settings)
    except:
        print('ERROR: load_settings')
        settings = {'myFontTag': (200, 200, 200),
                    'myFontTagSelected': (70, 70, 70),
                    'myFontTagSelectedCurrently': (90, 90, 90)}

    return(settings)
        

def save_settings(settingsDict):
    settings = load_settings()
    for key in settingsDict.keys():
        settings[key] = settingsDict[key]

    f = open('settings.txt', 'x')
    f.write(str(settings))
    f.close()

