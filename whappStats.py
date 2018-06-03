#!/usr/bin/env python
#whatsApp statistics 31/05/2018

from os import path
import emoji
import re
from datetime import datetime

d = path.dirname(__file__)

# Read the whole text.
class message(object):
    def __init__(self, date, sender, media, words, emojis):
        super(message, self).__init__()
        self.date = date
        self.sender = sender
        self.media = media
        self.words = words
        self.emojis=emojis

class db(object):
    def __init__(self):
        self.messages=[]
        self.senders=[]
        self.size=0
        self.totalwords=0
        self.totalemojis=0
    def load(self, pathString):
        f= open(path.join(d, pathString))
        for line in f:
            try:
                date=datetime.strptime(line[0:17].rstrip(" "),'%d/%m/%Y, %H:%M')
                self.size+=1
                sender=line[19:].split(":")[0].lstrip(" ")
                if sender not in self.senders:
                    self.senders.append(sender)
                restOfLine="".join(line[20:].split(": ")[1:]).rstrip("\n")
                media = (restOfLine == "<Media omitted>")
                words=0
                emojis=0
                if not media:
                    for word in restOfLine.split():
                        words+=1
                        decode= word.decode('utf-8')
                        for c in decode:
                            if c in emoji.UNICODE_EMOJI:
                                emojis+=1
                self.messages.append(message(date, sender, media, words, emojis))

            except: #messages with \n
                restOfLine=line.rstrip("\n")
                media= False
                for word in restOfLine.split():
                    words+=1
                    decode= word.decode('utf-8')
                    for c in decode:
                        if c in emoji.UNICODE_EMOJI:
                            emojis+=1
                self.messages[-1].words=words
                self.messages[-1].emojis=emojis
            self.totalwords+=words
            self.totalemojis+=emojis

        print self.size, "messages loaded from", self.messages[0].date.strftime('%d/%m/%Y %H:%M'), "to", self.messages[-1].date.strftime('%d/%m/%Y %H:%M')
        print self.senders

    def __str__(self):
        return self.size

    def exportByPerson(self):
        participant=[]
        for sender in self.senders:
            participant.append([0,0,0,0])
        for message in self.messages:
            x=self.senders.index(message.sender)
            participant[x][0]+=1
            if message.media:
                participant[x][1]+=1
            else:
                participant[x][2]+=message.words
                participant[x][3]+=message.emojis
        #message.date.strftime('%d/%m/%Y %H:%M') ,
        print participant

    def exportByWeekDay(self):
        participants=[]
        for sender in self.senders:
            participants.append([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        for message in self.messages:
            x=self.senders.index(message.sender)
            #Monday is 0 and Sunday is 6
            participants[x][message.date.weekday()][0]+=1
            if message.media:
                participants[x][message.date.weekday()][1]+=1
            else:
                participants[x][message.date.weekday()][2]+=message.words
                participants[x][message.date.weekday()][3]+=message.emojis
        #message.date.strftime('%d/%m/%Y %H:%M') ,
        for participant in participants:
            print " ".join(str(val) for val in participant)

myDb=db()
myDb.load('310118.txt')
myDb.exportByPerson()
myDb.exportByWeekDay()

#for eachmessage in myDb.messages:
#    print eachmessage.sender
