import xml.sax
import os

class Exception_ParserXML():
    def __call__(self, message):
        raise xml.sax.SAXException(message)


class handlerXML(xml.sax.ContentHandler, xml.sax.SAXException):
    def __init__(self, path, show=False, delete=False, add=False):
        self.Ex = Exception_ParserXML()
        self.symbol_ban = {".":".00",  "!":".01",  "@":".02",  "#":".03",  "$":".04",  "%":".05",  "^":".06",
                           "&":".07",  "*":".08",  "+":".09", "\n":".10", "\t":".11", "\"":".12", "\'":".13",
                           "/":".14",  "<":".15",  ">":".16",  '`':".17", '\\':".19",  " ":".20",  "=":".21"}

        types = [j[1] if j[1] in ("dir", "file") else self.Ex(1)    for j in path]
        names = ["a_"+"".join([j if (j not in self.symbol_ban) else self.symbol_ban[j] for j in i[0]])   for i in path]
        new_path = map((lambda x, y: [x, y]), names, types)

        self.show, self.delete, self.add = show, delete, add

        if add or delete:
           self.path, self.data, self.rec = new_path[0:-1], new_path[-1], True
           for type_element in self.path:
              if not type_element[1] == "dir": self.Ex(3)
        elif show:
           self.path, self.rec = new_path, False

        self.length_path = len(self.path) #for searching element
        self.i = 0                        #
        self.count = 0                    #for add element
        self.inside = False               #
        self.show_data = []               #for show element
        self.xml_new = []                 #for new xml document


    def startElement(self, name, att):
        depth = int(att.get("depth"))
        if (self.i != self.length_path and self.path[self.i][0] == name and self.path[self.i][1] == att.get("type") and self.i == depth):
           self.i += 1

        if self.i == self.length_path and self.count >= 0:
           if self.delete:
              if (name == self.data[0] and att.get("type") == self.data[1] and depth == self.length_path):
                 self.inside = True
                 self.rec = False
           elif self.add:
              self.inside = True
              if self.count == 1:
                 self.show_data.append([name, att.get("type")])
              if (name == self.data[0] and att.get("type") == self.data[1] and depth == self.length_path):
                 self.Ex(2)
           elif self.show:
              self.inside = True
              if self.count == 1:
                 self.show_data.append([name, att.get("type")])
                 
        if self.inside:
           self.count += 1
        if self.rec:
           self.xml_new.append('<%s type="%s" depth="%s">\n' % (name, att.get("type"), depth))


    def endElement(self, name):
        if self.inside:
           self.count -= 1
           if self.count == 0:
              self.inside = False
              self.count = -1
              if self.add:
                 self.xml_new.append('<%s type="%s" depth="%s">\n</%s>\n' %
                    (self.data[0], self.data[1], self.length_path, self.data[0]))

        if self.rec:
           self.xml_new.append('</%s>\n' % (name))
        if self.count == -1 and self.delete: 
           self.rec = True


    def finish(self):
        if self.add or self.delete:
           self.show_data.append(self.data)
           try:
              new_xml_file = open("user/f_structure.xml", "w")
              new_xml_file.writelines(self.xml_new)
           finally:
              new_xml_file.close()

        first = []
        for i in (name[0][2:] for name in self.show_data):
           for key in self.symbol_ban: i = i.replace(self.symbol_ban[key], key)
           first.append(i)

        return map((lambda x, y: [x, y]), first, [types[1] for types in self.show_data])


if __name__ == "__main__":
   path = [["root", "dir"]]
   x = xml.sax.make_parser()
   request = handlerXML(path, show=True)
   x.setContentHandler(request)
   x.parse("user"+os.sep+"f_structure.xml")
   show_data = request.finish()
   print (show_data)

