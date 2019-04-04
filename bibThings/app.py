#!/usr/bin/env python
# -*- coding: utf-8 -*-

#To clean DB, do : "python manage.py flush"

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
from django.conf import settings

from bibBot.models import Verse
from createDB_and_qText import createVerseDB, createTextfilesWithoutSpace, createWholeVersesWithoutSpace
from matchQuery import match_verse, match_verses, match_chapter, match_words

#
# Initialize DB
# Clean up text files, and then create one big bible verse text where all texts are without spaces
#

def init_DB_and_qText():
    RECORDS_COUNT = Verse.objects.count()

    # If there is a DB, delete all entries in the DB (resetting DB)
    if RECORDS_COUNT > 0:
        #print(str(RECORDS_COUNT) + " verse records are deleted.")
        Verse.objects.all().delete()

    # Create a bible verse DB
    createVerseDB()
    print("New DB size: " + str(Verse.objects.count()))

    # Remove all spaces from initial text file
    print("Create text files with no spaces")
    createTextfilesWithoutSpace()

    # From bible text files with no spaces, create one big file
    print("Create a single text file with all verses")
    createWholeVersesWithoutSpace()

# Check if 'inputString' contains numbers
def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))


########################################

need_init = input("\nIf need to initialize, enter 'yes', otherwise type any key:").lower()
if need_init in ["yes", "y"]: init_DB_and_qText()

########################################
#
# Regular expressions
#

# Matching single verse
# 요 3:16
# 요 3 16
q_re_1 = '^(?P<bookName>[a-zA-Z가-힣1-9]+)\ ?(?P<chapterNo>\d+)[\: \ ]+(?P<verseNoBegin>\d*)$'

# Matching verses
# 요 3:16-20
# 요 3 16-20
# 요 3 16 20
q_re_2 = '^(?P<bookName>[a-zA-Z가-힣1-9]+)\ ?(?P<chapterNo>\d+)[\: \ ]+(?P<verseNoBegin>\d*)\ ?\-?\ ?(?P<verseNoEnd>\d+)$'

# Matching a chapter
# 요 3
q_re_3 = '^(?P<bookName>[a-zA-Z가-힣1-9]+)\ ?(?P<chapterNo>\d+)$'


p_query_1 = re.compile(q_re_1)
p_query_2 = re.compile(q_re_2)
p_query_3 = re.compile(q_re_3)


# Iterate while user wants to input more queries

while True :

    q = input("Enter the query: ")

    if hasNumbers(q):
        match_1 = p_query_1.search(q)
        match_2 = p_query_2.search(q)
        match_3 = p_query_3.search(q)

        #print("Type 1: {}".format(match_1))
        #print("Type 2: {}".format(match_2))
        #print("Type 3: {}".format(match_3))

        if match_1:
            match_verse(match_1)
        elif match_2:
            match_verses(match_2)
        elif match_3:
            match_chapter(match_3)
        else:
            print("No matches")

    else:
        match_words(q)

    ask_more = input("\nIf want to stop, enter 'no' or '0'. Otherwise type any key:" ).lower()

    if ask_more in ["no", "n", "0"]: break





