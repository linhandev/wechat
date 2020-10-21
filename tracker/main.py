# coding=utf-8
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options
import pickle
import util
from influxdb import InfluxDBClient

influx_client = InfluxDBClient("localhost", 8086, "root", "root", "wechat")

define("port", default=8888, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        join_leaves = util.cal_join_leave()
        joins = leaves = 0
        for r in join_leaves.values():
            joins += r[1]
            leaves += r[2]
        self.render(
            "index.html",
            group_num=len(util.get_group_names()),
            group_mbr_num=len(util.get_group_mbrs()),
            unique_group_mbr_num=len(util.get_unique_group_mbrs()),
            joins=joins,
            leaves=leaves,
        )


class GroupHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class PersonHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class AllMessages(tornado.web.RequestHandler):
    """测试用，显示所有消息"""

    def get(self):
        res = influx_client.query("select * from message;")
        self.write(res[0])


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/group", GroupHandler),
            (r"/person", PersonHandler),
            (r"/msg", AllMessages),
        ]
        tornado.web.Application.__init__(
            self,
            handlers,
            template_path=os.path.join(
                os.path.dirname(__file__),
                "template",
            ),
            static_path=os.path.join(os.path.dirname(__file__), "upload"),
        )


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()