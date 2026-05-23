import random as r
import string as s
str = input("enter a message: ") 
words = str.split()
coding = input("Enter 1 for coding and 0 for decoding: ")
coding = True if(coding=='1') else False
if coding:
    list = []
    for word in words:
        if len(word) >=3:
            character1 = "".join(r.choices(s.ascii_letters,k=3))
            character2 = "".join(r.choices(s.ascii_letters,k=3))
            nword = character1 + word[1:] + word[0] + character2
            list.append(nword)
        else:
            list.append(word[::-1])
    print(" ".join(list))
else:
    list = []
    for word in words:
        if len(word) >=3:
            nword = word[-4] + word[3:-4]
            list.append(nword)
        else:
            list.append(word[::-1])
    print(" ".join(list))