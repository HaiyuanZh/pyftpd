#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import sys
import tkinter as tk
import tkinter.font as tkFont
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer   ##多线程
# from pyftpdlib.servers import MultiprocessFTPServer  ##多进程
# from pyftpdlib.servers import FTPServer

class MyHandler(FTPHandler):

    def set_label(self, label):
        self.label = label
        pass

    def on_connect(self):
        self.remote_ip_str = self.remote_ip.split(':')[-1]
        str = "%s connected" % self.remote_ip_str
        self.label.config(text = str)
        pass

    def on_disconnect(self):
        str = "%s disconnected" % self.remote_ip_str
        # do something when client disconnects
        self.label.config(text = str)
        pass

    def on_login(self, username):
        # do something when user login
        self.label.config(text="%s %s用户登入" % (self.remote_ip_str, username))
        pass

    def on_logout(self, username):
        self.label.config(text="%s 用户%s登出" % (self.remote_ip_str, username))
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        self.label.config(text="%s 文件发送" % self.remote_ip_str)
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        self.label.config(text="%s 文件收到" % self.remote_ip_str)
        pass

    def on_incomplete_file_sent(self, file):
        self.label.config(text="%s 完成文件发送" % self.remote_ip_str)
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        self.label.config(text="%s 完成文件接收" % self.remote_ip_str)
        # remove partially uploaded files
        import os
        os.remove(file)

def ftpd(showlabel):
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    # authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    # authorizer.add_anonymous(os.getcwd())
    authorizer.add_anonymous("/Users/Haiyuan/vmshare", perm='elradfmwMT')

    # Instantiate FTP handler class
    handler = MyHandler
    handler.set_label(handler, showlabel)
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)
    # 外部公网地址
    # handler.masquerade_address = '183.220.1.161'
    # 需要在外网路由器设置端口映射
    # handler.passive_ports = range(60000, 61000)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 2121)
    # server = FTPServer(address, handler)
    server = ThreadedFTPServer(address, handler)
    # server = MultiprocessFTPServer(address, handler)
    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    # server.serve_forever()
    srv = threading.Thread(target=server.serve_forever)
    srv.daemon = True
    srv.start()

def btnExit():
    sys.exit()


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry("900x600")
    root.title("Awooa出品的自用ftp服务端工具")
    label = tk.Label(root, text='提供ftp服务给外部系统',
                     fg='#0000CD',
                     pady=200,
                     font=tkFont.Font(size=40))

    ftpd(label)
    label.pack()

    pixelVirtual = tk.PhotoImage(width=1, height=1)
    tk.Button(root, text='退 出',font=tkFont.Font(size=30),
              foreground='green',
              background='black',
              image=pixelVirtual,
              width=200,
              height=80,
              compound=tk.CENTER,
              command=btnExit).pack()
    tk.mainloop()

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         master.geometry("640x480")
#         master.columnconfigure(0, weight = 0)
#         master.rowconfigure(2, weight = 0)
#         self.master = master
#         self.pack()
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.hi_there = tk.Button(self, bg="blue")
#         self.hi_there["text"] = "启动ftpd"
#         self.hi_there["command"] = self.onclick
#         # self.hi_there.configure(width=100,height=50)
#         self.hi_there.pack(side="top")
#         # self.hi_there.grid(row=0,column =0)
#
#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         # self.quit.grid(row = 1, column = 0)
#         # self.quit.configure(width=100,height=50)
#         self.quit.pack(side="bottom")
#         # self.quit.grid(row=1,column=0)
#
#     def onclick(self):
#         self.hi_there["state"] = "disabled"
#         ftpd()
#
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = Application(master=root)
#     app.mainloop()