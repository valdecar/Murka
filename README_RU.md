
# Мурка
Мурка это программа, читающая текстовые книги вслух. 
Потдерживает форматы текста txt и fb2. 
Работает на Linux, Windows и, наверное, на Mac OS.
Т.е.  кроссплатформенный книжный рассказчик, который может читать вслух текстовые книги в форматах txt и fb2.

### Требования
```
python3.2
espeak на  Linux (протестировано только для Ubuntu 14.04 и Debian Wheezy Sid)

SAPI5 на Windows (протестировано только для Windows 10 )

NSSpeechSynthesizer на Mac OS (не тестировалось)
```
### Установка и запуск
```
1) Распаковать архив
2) Запустить программу:
   Либо 
      Открыть терминал
      перейти в папку Murka
      выполнить:
         python3 gui.py
   или 
      на Linux (работает только на не ntfs файловой системе):
         cd Murka
         chmod +x main.py 
         ./main.py
      on Windows 
         Правой клавишей нажать на main.py 
         выбрать Run as Administrator
 ```
### Предупреждения
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
### Использование
```
You can either play books from file (in that case fb2 and some txt) 
or copy them directly to text frame (after that click update button 
and save as new if needed). 

You can also modify a text in text frame (but not forget the update button).

You can use Space key for play/pause but not forget that pause work not instantly. 
```


 ![alt tag](https://raw.githubusercontent.com/valdecar/Murka/master/screen_overview.png)

### References:
### Благодарности
```
pyttsx: http://pyttsx.readthedocs.io/en/latest/index.html
And, of course, those people, who work at espeak, SAPI5, NSSpeechSynthesizer.
```
