from bs4 import BeautifulSoup
import re
import urllib2

sites = [
#        ('http://en.wikipedia.org/wiki/16th_century', False),
#        ('http://en.wikipedia.org/wiki/17th_century', False),
#        ('http://en.wikipedia.org/wiki/18th_century', False),
#        ('http://en.wikipedia.org/wiki/19th_century', False),
        ('http://en.wikipedia.org/wiki/Timeline_of_modern_history', True),
]

event_regex = re.compile('^ *([0-9]{4})[^:]*: (.+)$')

def scrape_events(site, sentence_per_event):
   soup = BeautifulSoup(urllib2.urlopen(site).read())
   text = soup.get_text()
   for line in text.splitlines():
       match = event_regex.match(line)
       if match:
            year = match.group(1)
            text = match.group(2)
            if not sentence_per_event:
               yield (text, int(year))
            else:
                cur = [] 
                for event in text.split('. '):
                    if event:
                        if not event[-1].isupper() and event[-3:] != ' St':
                            yield ('. '.join(cur + [event]) + ('.' if event[-1] != '.' else ''), int(year))
                            cur = []
                        else:
                            cur += [event]
                if cur:
                    yield ('. '.join(cur) + ('.' if event[-1] != '.' else ''), int(year))


if __name__ == '__main__':
    print('HISTORY = ['+',\n'.join([repr(event) for site, sentence_per_event in sites for event in scrape_events(site, sentence_per_event) if len(event[0]) <= 50])+']')
