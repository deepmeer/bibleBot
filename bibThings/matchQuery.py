#!/usr/bin/env python


# set the default Django settings module
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "bibThings.settings")
# Setup django project
django.setup()

import codecs
import re

from django.db import models
from django.db.models import Q

from django.conf import settings
from bibBot.models import Verse

bookName=[]
chapterNo, verseNoBegin, verseNoEnd = 0, 0, 0

def get_bookstat (book_name):
    for book_info in settings.BOOK_STAT:
        if book_info[0] == book_name:
            return book_info
    return False

# Obsolete definition
"""
def Overse_exists (book_name, chapter_number, verse_number):
    book_info = get_bookstat(book_name)

    if (chapter_number <= book_info[1]) and (verse_number <= book_info[chapter_number + 1]):
        return True
    else:
        print("Check Chapter & Verse number [{} {}:{}]".format(book_name, str(chapter_number), str(verse_number)))
        return False
"""

def verses_exist (book_name, chapter_number, verse_number1, verse_number2):
    book_info = get_bookstat(book_name)

    total_verses = book_info[chapter_number + 1]
    if (chapter_number <= book_info[1]) and (verse_number1 < verse_number2) and \
            (verse_number1 <= total_verses) and (verse_number2 <= total_verses):
        return True
    else:
        print("Check Chapter & Verse number [{} {}:{}-{}]".format(book_name, str(chapter_number), str(verse_number1),
                                                                  str(verse_number2)))
        return False

# Obsolete definition
"""
def Ochapter_exists (book_name, chapter_number):
    book_info = get_bookstat(book_name)
    if chapter_number > book_info[1]:
        print("Check Chapter number: " + str(chapter_number))
        return False
    else:
        return True
"""

# Matching a single verse
def match_verse (match):

    initial_bookName = match.group('bookName').lower()
    #print(initial_bookName)
    #print(Verse.book_exists("", settings.VERSION, initial_bookName))

    book_found = False
    for book_aliases in settings.BN_ALIASES:
        if initial_bookName in book_aliases:
            EN_bookName = book_aliases[0]
            KR_bookName = book_aliases[2]
            book_found = True
            break

    if book_found:

        chapterNo = int(match.group('chapterNo'))
        verseNoBegin = int(match.group('verseNoBegin'))

        if Verse.verse_exists("", settings.VERSION, EN_bookName, chapterNo, verseNoBegin):
            verse = Verse.get_verse("", settings.VERSION, EN_bookName, chapterNo, verseNoBegin)
            print("[{} {}:{}] {}".format(KR_bookName, str(chapterNo), str(verseNoBegin), verse[0].verseText))

        else:
            print("Wrong chapter/verse number:{} {}:{}".format(KR_bookName, str(chapterNo), str(verseNoBegin)))

    else:
        print("Wrong Book name: " + initial_bookName)

# Matching multiple contiguous verses
def match_verses (match):

    initial_bookName = match.group('bookName').lower()

    book_found = False
    for book_aliases in settings.BN_ALIASES:
        if initial_bookName in book_aliases:
            EN_bookName = book_aliases[0]
            KR_bookName = book_aliases[2]
            book_found = True
            break

    if book_found:
        chapterNo = int(match.group('chapterNo'))
        verseNoBegin = int(match.group('verseNoBegin'))
        verseNoEnd = int(match.group('verseNoEnd'))

        #print(KR_bookName + " " + str(chapterNo) + ":" + str(verseNoBegin) + "-" + str(verseNoEnd))
        if verses_exist(EN_bookName, chapterNo, verseNoBegin, verseNoEnd):
            verses = Verse.get_verses("", settings.VERSION, EN_bookName, chapterNo, verseNoBegin, verseNoEnd)
            if verses:
                i = verseNoBegin
                print("[{} {}:{}-{}]".format(KR_bookName, str(chapterNo), str(verseNoBegin), str(verseNoEnd)))
                for verse in verses:
                    print("[{}:{}] {}".format(str(chapterNo), str(i), verse.verseText))
                    i += 1
    else:
        print("Wrong Book name: " + initial_bookName)

# Matching q chapter
def match_chapter (match):

    initial_bookName = match.group('bookName').lower()

    book_found = False
    for book_aliases in settings.BN_ALIASES:
        if initial_bookName in book_aliases:
            EN_bookName = book_aliases[0]
            KR_bookName = book_aliases[2]
            book_found = True
            break

    if book_found:
        chapterNo = int(match.group('chapterNo'))

        if Verse.chapter_exists("", settings.VERSION, EN_bookName, chapterNo):

            verses = Verse.get_verses_bc("", settings.VERSION, EN_bookName, chapterNo)  # EN_bookName  "204 Jn"
            if verses:
                i = 1
                print("[{}{}장]".format(KR_bookName, str(chapterNo)))
                for verse in verses:
                    print("[{}:{}] {}".format(str(chapterNo), str(i), verse.verseText))
                    i += 1
            else:
                print("verses of the chapter not found")
        else:
            print("Wrong chapter number: " + str(chapterNo))
    else:
        print("Wrong Book name: " + initial_bookName)

# Matching a query text (allowing space-insensitive)

def match_words(input_q_word):
    bookName=[]
    chapterNo, verseNoBegin, verseNoEnd = 0, 0, 0

    f_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/bible.txt'

    q_word = input_q_word.replace(" ", "")
    re_q_word = re.compile(q_word)

    with codecs.open(f_path, 'r', encoding='euc-kr') as f:
        line = f.readline()
        # print("0" + line)
        visit_count = 0
        count = 0

        while line:
            visit_count += 1
            match = re_q_word.search(line)  # .groupdict()
            if match:
                count += 1

                matched_verse = line.split()
                KR_bookName = matched_verse[0]
                EN_bookName = settings.KR_BN_TO_EN_BN_DICT[KR_bookName].lower()  # 나중에 소문자로 바꿀 것 !
                chapterNo = matched_verse[1]
                verseNo = matched_verse[2]

                verse = Verse.get_verse("", settings.VERSION, EN_bookName, chapterNo, verseNo)

                if verse:
                    print("[{} {}:{}] {}".format(settings.KRBN_ABBR2FULL_DICT[KR_bookName], str(chapterNo), str(verseNo), verse[0].verseText))
                else:
                    #print(verse[0] + str(chapterNo) + ":" + str(verseNo) + "Irregular verses")
                    pass

            line = f.readline()

        print("No of Matches: " + str(count))

