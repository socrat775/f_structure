import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpserver
import json, os, xml

from reader import handlerXML


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
           self.redirect("/login/")
           return
        self.render("main.html")


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        self.set_cookie("user", self.get_argument("name"))
        self.redirect("/")


class WebSocketWriter(tornado.websocket.WebSocketHandler):
    def open(self):
        cookie = self.get_cookie("user")
        if not cookie:
           print ("Not Cookie")
        else:
           print ("Connected user:" + cookie)
           self.dictionary_functions = {"DIRECTORY": self.reader_xml}
           self.dictionary_functions["DIRECTORY"]({"show": [["root", "dir"]]})

    def on_message(self, message):
        message = json.loads(message)
        for i in message:
           if i in self.dictionary_functions:
              self.dictionary_functions[i](message[i])
              continue
           else:
              pass

    def reader_xml(self, data):
        x = xml.sax.make_parser()
        result = {}

        try:
           for i in data:
              if i == "show": request = handlerXML(data[i], show=True)
              elif i == "add": request = handlerXML(data[i], add=True)
              elif i == "delete": request = handlerXML(data[i], delete=True)
              else:raise xml.sax.SAXException(4)
           x.setContentHandler(request)
           x.parse("user/f_structure.xml")
           result["SHOW_ELEMENTS"] = request.finish()
        except xml.sax.SAXException as message:
           result["ERROR"] = message.args[0]
        except IOError as message:            #
           result["ERROR"] = message.args[0]  #

        self.write_message(json.dumps(result))

    def on_close(self):
        print("WebSocket close to connect")


if __name__ == "__main__":
    try:
       app = tornado.web.Application(handlers = [ (r'/', MainHandler), (r'/login/', LoginHandler), (r'/websocket/', WebSocketWriter) ],
                                     template_path = (os.path.abspath('..')+os.sep+"client"+os.sep+"template"),
                                     static_path = (os.path.abspath('..')+os.sep+"client"+os.sep+"static"))
       server = tornado.httpserver.HTTPServer(app)
       server.listen(8888)
       tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: print("\n")

