import urllib2


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]


class Tag:
    """
    This is a data type that we use for all of our interest tags.
    """
    def __init__(self, tag):
        """
        Initialze the tag.
        Takes on argument of type String
        """
        self.tag = tag.lower()

    def similarityTo(self, otherTag):
        """
        Calculates whether or not a tag matches with another tag. We could
        potentially do a multiple depth search, but for now we are keeping it
        at a depth of 1 to keep testing things quick and simple.
        Takes one argument of type Tag
        """
        try:
            if(self.tag == otherTag.tag): return True
            htmlBody1, htmlBody2 = WikipediaArticle(self.tag.replace(' ', '_').lower()).htmlBody, WikipediaArticle(otherTag.tag.replace(' ', '_').lower()).htmlBody
            bool1, bool2 = False, False
            for line in htmlBody1:
                line = line.strip()
                if self.tag in line:
                    bool1 = True
                    break
            if(not bool1): return False
            for line in htmlBody2:
                line = line.strip()
                if otherTag.tag in line:
                    bool2 = True
                    break
            return bool1 and bool2
        except Exception as e:
            return self.tag == otherTag.tag


class WikipediaArticle:
    def __init__(self, keyword):
        self.keyword = keyword
    @property
    def htmlBody(self):
        infile = opener.open('http://en.wikipedia.org/w/index.php?title=' +\
                        self.keyword + '&printable=yes')
        return infile
