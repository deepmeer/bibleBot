#
# Part of this file was from https://github.com/davidwparker/bibleapi-old/blob/master/verses/models.py#L58
#

from django.db import models
from django.http import Http404


class Verse(models.Model):
    version = models.CharField(max_length=100)
    book = models.CharField(max_length=100)
    bookOrder = models.IntegerField()
    chapter = models.IntegerField()
    verse = models.IntegerField()
    verseText = models.TextField('text')

    class Meta:
        db_table = 'verses'
        ordering = ['bookOrder', 'chapter', 'verse']

    # django methods
    def __unicode__(self):
        return self.version + " " + self.book + " " + unicode(self.chapter) + ":" + unicode(self.verse)

    # class methods here down
    #
    # existence
    #

    def verse_exists(self, version, book_name, chapter_number, verse_number):
        return Verse.objects.filter(version__iexact=version, book__iexact=book_name,
                                    chapter=chapter_number, verse=verse_number).exists()

    def chapter_exists(self, version, book_name, chapter_number):
        return Verse.objects.filter(version__iexact=version, book__iexact=book_name,
                                    chapter=chapter_number).exists()

    def book_exists(self, version, book):
        '''Returns whether a book exists'''
        return Verse.objects.filter(version__iexact=version, book__iexact=book).exists()

    """
    def book_exists_or_404(self, version, book):
        '''Raises Http404 if book does not exist'''
        if not Verse().book_exists(version, book):
            raise Http404
    """

    def version_exists(self, version):
        '''Returns whether a version exists'''
        return Verse.objects.filter(version__iexact=version).exists()

    """
    def version_exists_or_404(self, version):
        '''Raises Http404 if version does not exist'''
        if not Verse().version_exists(version):
            raise Http404
    """

    """
    #
    # custom SQL
    #
    def get_array(self, *args, **kwargs):
        '''Returns an array based on the keyword arguments'''
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute(kwargs["query"], kwargs["params"])
        return cursor.fetchall()

    def get_first_col(self, rows):
        results = []
        for row in rows:
            results.append(row[0])
        return results

    def get_book_names_from_abbr(self, version, abbr):
        '''Returns a list of book_names from an abbreviation'''
        abbr = '%' + abbr + '%'
        books = Verse().get_array(params=[version, abbr],
                                  query="SELECT DISTINCT book FROM verses WHERE version = %s AND book LIKE %s ORDER BY bookOrder")
        return Verse().get_first_col(books)

    def get_book_chapters(self, version):
        '''Returns a list of unique book names with their chapters'''
        book_chapters = Verse().get_array(params=[version],
                                          query="SELECT DISTINCT book, chapter FROM verses WHERE version = %s ORDER BY bookOrder, chapter")
        book = None
        chapters = []
        results = []
        for row in book_chapters:
            if book is None:
                book = row[0]
            if book != row[0]:
                results.append({'book': book, 'chapters': chapters})
                book = row[0]
                chapters = []
            chapters.append(row[1])
        return results

    def get_chapter_numbers(self, version, book):
        '''Returns a list of unique chapter numbers'''
        chapters = Verse().get_array(params=[version, book],
                                     query="SELECT DISTINCT chapter FROM verses WHERE version = %s AND book = %s ORDER BY chapter")
        print (chapters)

        return Verse().get_first_col(chapters)
    """

    #
    # filters/lists of objects
    #
    def get_verses_bc(self, version, book, chapter):
        '''Returns a list of verses for a given version, book, and chapter'''
        return Verse.objects.filter(version__iexact=version, book__iexact=book, chapter__iexact=chapter)

    def get_verse(self, version, book, chapter, verse):
        '''Returns an exact verse'''
        return Verse.objects.filter(version__iexact=version, book__iexact=book, chapter__iexact=chapter,
                                    verse__iexact=verse)

    def get_verses(self, version, book, chapter, verse, verse2):
        '''Returns a list of verses or Raises Http404'''
        if verse is None:
            verses = Verse().get_verses_bc(version, book, chapter)
        elif verse2 is None or verse2 < verse:
            verses = Verse().get_verse(version, book, chapter, verse)
        else:
            verses = Verse.objects.filter(version__iexact=version, book__iexact=book, chapter__iexact=chapter,
                                          verse__in=range(int(verse), int(verse2) + 1))

        return verses
