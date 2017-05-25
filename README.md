# Murka
Murka is an free, cross platform books narrator that can voice text books in txt and fb2 formats.


### requirement
```
python3.2
espeak on Linux (only Ubuntu 14.04 and Debian Wheezy Sid was tested )

SAPI5 on Windows (only Windows 10 was tested)

NSSpeechSynthesizer on Mac OS (not tested at all)
```
### installation and running
```
1) unzip archive 
2) Run program:
   Either
      Open terminal,
      go in Murka folder
      run:
         python3 gui.py
   or 
      on Linux (work only in non ntfs file systems):
         cd Murka
         chmod +x main.py 
         ./main.py
      on Windows 
         right click at main.py 
         choice Run as Administrator button
 ```
### Warnings
```
If something not work try use it like root.
(The reason is that pyttsx send text directly to driver and it's not always permitted). 
If that not help, run 
python3 gui.py 
in terminal and figure out what's wrong.

Some books are very large so wait patiently while it loads.

Remember that pause button works only after sentence will ended
(So not click at it million times, narrator stops when last sentence
will be readed)  
```
### usage
```
You can either play books from text file (in that case .fb2 and some .txt) 
or copy them directly to text frame (after that click update button 
and save as new if needed). 

You can also modify a text in text frame (but not forget the update button).

You can use Space key for play/pause but not forget that pause work not instantly. 
```


 ![alt tag](https://raw.githubusercontent.com/valdecar/Murka/master/screen_overview.png)

### References:
### Acknowledgments
```
pyttsx: http://pyttsx.readthedocs.io/en/latest/index.html
And, of course, those people, who work at espeak, SAPI5, NSSpeechSynthesizer.
```
