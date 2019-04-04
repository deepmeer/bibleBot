#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To clean DB : "python manage.py flush"

# set the default Django settings module

from django.conf import settings

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "bibThings.settings")
# Setup django project
django.setup()

import codecs
import re

from django.db import models
from django.db.models import Q

from bibBot.models import Verse


# Create verse database

def createVerseDB():

    re_reading_bibText = "^(?P<bookName>[가-힣]+)\ ?(?P<chapterNo>[0-9]+)\:(?P<verseNo>[0-9]+)\ +(?P<verseText>.+)$"
    p = re.compile(re_reading_bibText)

    database_count = Verse.objects.count()

    if database_count == 0 or not 0:
        print("DB Count: " + str(database_count))

        for book_name in settings.BOOK_ABBR_LIST:

            f_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/KSV_woSectionTitle/' + book_name + '.txt'

            with codecs.open(f_path, 'r', encoding='euc-kr') as f:

                line = f.readline()

                while line:
                    #print("Line {}: {}".format(cnt, line.strip()))

                    match = p.search(line) #.groupdict()
                    if match:
                        chapterNo = int(match.group('chapterNo'))
                        verseNo = int(match.group('verseNo'))

                        v = Verse(version=settings.VERSION,
                                  book=book_name.lower(),
                                  bookOrder=1,
                                  chapter=chapterNo,
                                  verse=verseNo,
                                  verseText=match.group('verseText')
                                  )

                        v.save()
                        #print("BookName:" + v.book + " " + str(v.chapter) + ":" + str(v.verse) + " " + v.verseText)

                    #else:
                    #    print("Irregular verse: ", line)

                    line = f.readline()


            f.close()
        #print("database_count: " + str(Verse.objects.count()))

# End of reading bibText and creating DB

# Create new text files after removing spaces from Bible text files
def createTextfilesWithoutSpace():

    ppp_re = '^(?P<bookName>[가-힣]+)(?P<chapterNo>[0-9]+)\:(?P<verseNo>[0-9]+)\ *(?P<verseText>.+)$'

    ppp = re.compile(ppp_re)

    for book_name in settings.NUMBERED_BOOK_ABBR_LIST:
        f_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/KSV_woSectionTitle_numbered/' + book_name + '.txt'
        w_noSpace_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/KSV_woSectionTitle_woSpace/' + book_name + '.txt'

        with open(w_noSpace_path, 'w', encoding='euc-kr') as wf:
            with codecs.open(f_path, 'r', encoding='euc-kr') as rf:

                line = rf.readline()

                while line:

                    match = ppp.search(line)
                    # print(line)

                    if match:
                        verse = match.group('verseText')
                        wf.write(match.group('bookName') + " " + match.group('chapterNo') + " " +
                                 match.group('verseNo') + " " + verse.replace(" ", "") + '\n')
                    else:
                        print("Wrong line " + line)

                    line = rf.readline()

            rf.close()

        wf.close()

# Create a big single Bible text file
def createWholeVersesWithoutSpace():

    from_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/KSV_woSectionTitle_woSpace/'

    fromfilelist = sorted(os.listdir(from_path))
    with open('/Users/hosoolee/Desktop/bibleBot/BibleText/bible.txt', "w", encoding="euc-kr") as outfile:

        for eachfile in fromfilelist:
            if eachfile.endswith('.txt'):
                fpath = from_path + eachfile
                with open(fpath, 'r', encoding="euc-kr") as readfile:
                    outfile.write(readfile.read() + "\n")
                    readfile.close()

        outfile.close()

