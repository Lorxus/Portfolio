# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid: str, title: str, description: str, link: str, pubdate: datetime):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
    
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate
    

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase) -> None:
        super().__init__()
        self.phrase = phrase.lower()

    def is_phrase_in(self, text: str) -> bool:
        cleantext = text
        cleantext = cleantext.lower()

        for char in list(string.punctuation):  # remove all punctuation, replace it with spaces
            cleantext = cleantext.replace(char, ' ')

        wordlist = cleantext.split() # turn everything into lists to enforce word boundaries
        phraselist = self.phrase.split()
        phrase_l = len(phraselist)

        # print(wordlist)
        # print(phraselist)

        if phraselist[0] not in wordlist:  # preoptimization: is the first word of the phrase even present?
            return False
        else:
            for idx in range(len(wordlist)):
                if wordlist[idx:idx+phrase_l] == phraselist:  # 'is the sublist of wordlist of length len(phraselist) the same as phraselist?' 
                    return True
        
        return False
    
    def evaluate(self, story):
        return self.is_phrase_in(story)


# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase) -> None:
        super().__init__(phrase)

    def evaluate(self, story):
        # print(story)
        # print(type(story))
        # print(story.get_title())
        return super().evaluate(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase) -> None:
        super().__init__(phrase)

    def evaluate(self, story):
        # print(story)
        # print(type(story))
        # print(story.get_title())
        return super().evaluate(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, timestring) -> None:
        super().__init__()
        pubdate = datetime.strptime(timestring, '%d %b %Y %H:%M:%S')
        pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        self.pubdate = pubdate
        
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, timestring) -> None:
        super().__init__(timestring)
    
    def evaluate(self, story):
        return story.get_pubdate() < self.pubdate 

class AfterTrigger(TimeTrigger):
    def __init__(self, timestring) -> None:
        super().__init__(timestring)

    def evaluate(self, story):
        return story.get_pubdate() > self.pubdate


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(object):
    def __init__(self, trigger: Trigger) -> None:
        self.trigger = trigger
    
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(object):
    def __init__(self, trigger1: Trigger, trigger2: Trigger) -> None:
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
class OrTrigger(object):
    def __init__(self, trigger1: Trigger, trigger2: Trigger) -> None:
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # Problem 10
    storylist = []
    for s in stories:
        tempflag = False
        for t in triggerlist:
            if t.evaluate(s):
                tempflag = True
        if tempflag:
            storylist.append(s)
    
    return storylist

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    configged_triggers = {}

    triggerlist = []
    
    for l in lines:
        command = l.split(',')

        if command[0] != 'ADD':
            if command[1] == 'TITLE':
                newtrigger = TitleTrigger(command[2])
            elif command[1] == 'DESCRIPTION':
                newtrigger = DescriptionTrigger(command[2])
            elif command[1] == 'BEFORE':
                newtrigger = BeforeTrigger(command[2])
            elif command[1] == 'AFTER':
                newtrigger = AfterTrigger(command[2])
            elif command[1] == 'NOT':
                newtrigger = NotTrigger(command[2])
            elif command[1] == 'AND':
                newtrigger = AndTrigger(command[2], command[3])
            elif command[1] == 'OR':
                newtrigger = OrTrigger(command[2], command[3])
            
            configged_triggers[command[0]] = newtrigger  # this runs every non-ADD loop regardless

        else:  # command[0] == ADD    
            addlength = len(command)
            for idx in range(1, addlength):
                triggerlist.append(configged_triggers[command[idx]])  # append to triggerlist the configged-trigger whose name is the n+1st entry in the ADD command 
    
    return triggerlist




SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Gaetz")
        t2 = DescriptionTrigger("Ukraine")
        t3 = DescriptionTrigger("Clinton")
        t4 = OrTrigger(t2, t3)
        t5 = DescriptionTrigger("Anthropic")
        triggerlist = [t1, t4, t5]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))
            # Yahoo's RSS feed no longer has descriptions included

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

