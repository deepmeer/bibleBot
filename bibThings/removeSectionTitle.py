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


book_abbr_list1 = ['204 Jn']


def removeSectionTitle():

    ppp = re.compile('^(?P<part1>.*)(?P<sectionTitle>\<.*\>)(?P<part2>.*)$')


    for book_name in settings.NUMBERED_BOOK_ABBR_LIST:
        f_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/KSV_numbered_EN/'+ book_name + '.txt'
        w_path = '/Users/hosoolee/Desktop/bibleBot/BibleText/KSV_woSectionTitle/' + book_name + '.txt'

        with open(w_path, 'w', encoding='euc-kr') as wf:

            with codecs.open(f_path, 'r', encoding='euc-kr') as rf:

                line = rf.readline()
                cnt = 1
                while line:
                    sectionTitle_match = ppp.search(line)

                    if sectionTitle_match:
                        wf.write(sectionTitle_match.group('part1') + sectionTitle_match.group('part2') + '\n')
                    else:
                        wf.write(line)

                    cnt += 1
                    line = rf.readline()

            rf.close()
        wf.close()


removeSectionTitle()


