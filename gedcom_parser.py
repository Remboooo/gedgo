import re
import codecs
import os

class FilePeeker():
    def __init__(self, f):
        self.f = f
        self.nextline = None

    def peekline(self):
        if not self.nextline:
            self.nextline = self.f.readline()
        return self.nextline

    def readline(self):
        if self.nextline:
            line = self.nextline
            self.nextline = None
            return line
        else:
            return self.f.readline()

class GedcomParser(object):
    """
    File class represents a GEDCOM file.
    Attributes are header, trailer, and entries where header and trailer
    are a single entry each and entries is the dictionary of all entries
    parsed in between.
    """

    line_re = re.compile(
        '^(\d{1,2})' +          # Level
        '(?: @([A-Z\d]+)@)?' +  # Pointer, optional
        ' _?([A-Z\d]{3,})' +    # Tag
        '(?: (.+))?$'           # Value, optional
    )

    def __init__(self, file_name_or_stream):
        if isinstance(file_name_or_stream, basestring):
            bs = min(32, os.path.getsize(file_name_or_stream))
            f = open(file_name_or_stream, 'rb')
            raw = f.read(bs)
            f.close()
            if raw.startswith(codecs.BOM_UTF8):
                encoding = 'utf-8-sig'
                print("UTF8 with BOM")
            else:
                result = chardet.detect(raw)
                encoding = result['encoding']
                print("Not UTF8")
            self.file = codecs.open(file_name_or_stream, mode='r', encoding=encoding, errors='ignore')
        else:
            self.file = file_name_or_stream
        self.file = FilePeeker(self.file)
        self.__parse()

    def __parse(self):
        self.entries = {}

        cont = True

        while cont:
            cont, tag, entry = self.__parse_element()
            if entry and 'pointer' in entry:
                pointer = entry['pointer']
                self.entries[pointer] = entry
            elif tag == 'HEAD':
                self.header = entry
            elif tag == 'TRLR':
                self.trailer = entry

    def __parse_element(self):
        line = self.file.readline()
        if not line:
            return False, None, None
        parsed = self.line_re.match(line.strip())

        if not parsed:
            raise SyntaxError("Bad GEDCOM syntax in line: '%s'" % line)

        level, pointer, tag, value = parsed.groups()

        entry = {
            "tag": tag,
            "pointer": pointer,
            "value": value,
            "children": []
        }

        level = int(level)

        # Consume lines from the file while the level of the next line is
        # deeper than that of the current element, and recurse down.
        while True:
            next_line = self.file.peekline()

            if next_line and int(next_line[0:2]) > level:
                _, _, child_element = self.__parse_element()
                entry['children'].append(child_element)
            else:
                break

        # Keep the entry trimmed down
        for key in entry.keys():
            if not entry[key]:
                del entry[key]

        return True, tag, entry

    def __unicode__(self):
        return "Gedcom file (%s)" % self.file
