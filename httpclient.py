#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, Phousanak Han, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    # def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        data_list = data.split("\r\n")
        code_message = data_list[0]
        code_number = code_message.split(' ')[1]
        return int(code_number)

    def get_headers(self, data):
        headers = data.split("\r\n")
        return headers

    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        host, port, path = self.urlHandler(url)
        self.connect(host, port)
        request = "GET " + path + " HTTP/1.1\r\n"
        request += "Host: " + host + "\r\n"
        request += "Accept: */*\r\n"  # any MIME type
        request += "Connection: close\r\n"
        request += "\r\n"
        self.sendall(request)

        data = self.recvall(self.socket)
        body = self.get_body(data)
        code = self.get_code(data)
        #print("------CODE IN GET------")
        print(code)
        # print("-----------END---------")
        #print("------BODY IN GET------")
        print(body)
        # print("-----------END---------")
        self.close()
        return HTTPResponse(code, body)

    def urlHandler(self, url):
        urllib_parse = urllib.parse.urlparse(url)
        url_hostname = urllib_parse.hostname
        url_path = urllib_parse.path
        url_port = urllib_parse.port

        if url_port == None:
            url_port = 80
        if len(url_path) == 0:
            url_path += "/"
        return url_hostname, url_port, url_path

    def POST(self, url, args=None):
        if args == None:
            args = ""
        else:
            args = urllib.parse.urlencode(args)
        host, port, path = self.urlHandler(url)
        self.connect(host, port)
        request = "POST " + path + " HTTP/1.1\r\n"
        request += "Host: " + host + "\r\n"
        request += "Content-Type: application/x-www-form-urlencoded\r\n"
        request += "Content-Length: " + str(len(args)) + "\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"
        request += args
        self.sendall(request)
        data = self.recvall(self.socket)
        body = self.get_body(data)
        code = self.get_code(data)
        #print("------CODE IN POST------")
        print(code)
        # print("-----------END---------")
        #print("------BODY IN POST------")
        print(body)
        # print("-----------END---------")
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
