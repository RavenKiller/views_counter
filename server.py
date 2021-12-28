# views_counter plugin server 
# Developed by Raven, 2021.12.28
# Copyright (c) RavenKiller
# This source code is licensed under the MIT License found in the
# LICENSE file in the root directory of this source tree.

import tornado.ioloop
import tornado.web
import hashlib
import sqlite3
from datetime import datetime as dt
import sys

SQL_CREATE_TABLE = '''CREATE TABLE  IF NOT EXISTS views
        (id         INTEGER PRIMARY KEY,
        site_hash   TEXT    NOT NULL,
        page_hash   TEXT    NOT NULL,
        user_hash   TEXT    NOT NULL,
        time        TEXT    NOT NULL
        );'''
# wildcard: (site_hash, page_hash, user_hash, time)
SQL_INSERT_RECORD = "INSERT INTO views VALUES (NULL, ?, ?, ?, ?);"
# wildcard: (page_hash)
SQL_PAGE_VIEWS = "SELECT COUNT(*) FROM views WHERE page_hash=?;"
# wildcard: (site_hash)
SQL_SITE_VIEWS = "SELECT COUNT(*) FROM views WHERE site_hash=?;"
SQL_PAGE_USERS = "SELECT DISTINCT page_hash, user_hash FROM views;"
SQL_SITE_USERS = "SELECT DISTINCT site_hash, user_hash FROM views;"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("demo.html")

class VCHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def post(self):
        res = {"success":0, "vc_page_views":0, "vc_site_views":0, "vc_page_users":0, "vc_site_users":0}

        # Extract information
        src = self.get_argument("src", "")
        ip = self.request.remote_ip
        user_agent = self.request.headers.get("User-Agent", "")
        origin = self.request.headers.get("Origin", "")
        if not src or  not ip or not user_agent or not origin:
            self.finish(res)

        # Hash
        page_hash = hashlib.md5(src.encode("utf-8")).hexdigest()
        site_hash = hashlib.md5(origin.encode("utf-8")).hexdigest()
        user_hash = hashlib.md5((ip+user_agent).encode("utf-8")).hexdigest()

        # Open DB
        now = dt.now()
        conn = sqlite3.connect('views.db')
        c = conn.cursor()

        try:
            # Insert record
            c.execute(SQL_INSERT_RECORD, (site_hash, page_hash, user_hash, now.strftime("%Y-%m-%d %H:%M:%S")))
            # Page views
            c.execute(SQL_PAGE_VIEWS, (page_hash, ))
            res["vc_page_views"] = c.fetchall()[0][0]
            # Site views
            c.execute(SQL_SITE_VIEWS, (site_hash, ))
            res["vc_site_views"] = c.fetchall()[0][0]
            # Page users
            c.execute(SQL_PAGE_USERS)
            res["vc_page_users"] = len(c.fetchall())
            # Site users
            c.execute(SQL_SITE_USERS)
            res["vc_site_users"] = len(c.fetchall())

            # Close and return
            conn.commit()
            conn.close()
            res["success"] = 1
            self.finish(res)
        except:
            conn.rollback()
            conn.close()
            res["success"] = 0
            self.finish(res)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/views", VCHandler)
    ])

if __name__ == "__main__":
    conn = sqlite3.connect('views.db')
    c = conn.cursor()
    c.execute(SQL_CREATE_TABLE)
    conn.commit()
    conn.close()
    app = make_app()
    app.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.current().start()