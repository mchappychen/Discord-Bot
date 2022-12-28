#This file is used to relay messages between my discord python bot, and a web-browser script

# How it works:
# 1. start http_server.py
# 2. chatgpt sends request to server every second to see if disc_message isn't empty
# 3. discord sends request to server (from human) to set disc_message
# 4. chatgpt gets disc_message, reset it, and process it
# 5. discord checks every second to see if chatgpt_message isn't empty
# 6. server returns data to discord

from http.server import HTTPServer, BaseHTTPRequestHandler
import json,time, requests, threading
from urllib.parse import urlparse
from socketserver import ThreadingMixIn

#Colors
class c:
   violet = '\033[95m'
   pink = '\033[94m'
   blue = '\033[96m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   end = '\033[0m'
   bold = '\033[1m'


disc_message = ''
chatgpt_message = ''

class Serv(BaseHTTPRequestHandler):
   def do_POST(self):
      global disc_message,chatgpt_message

      self.send_response(200)
      self.end_headers()
      #{from:discord/chatgpt , msg:blah blah blah}
      content = json.loads(self.rfile.read(int(self.headers.get('Content-Length'))))
      print(f"{c.blue}Connection from:{content['from']}, Data:{content['msg']}{c.end}")

      #If the message is from discord bot
      if content['from'] == 'discord':

         #set disc_message
         disc_message = content['msg']

         #wait until chatgpt_message isn't empty, check every 1s?
         while chatgpt_message == '':
            time.sleep(1)

         #send the chatgpt_message back to discord
         self.wfile.write(bytes(chatgpt_message,'utf-8'))
         
         #clear chatgpt_message
         chatgpt_message = ''

      #If the message is from chatgpt webpage
      elif content['from'] == 'chatgpt':

         #Find a way to check if the message should be sent to discord
         if content['msg'] != 'ready':
            chatgpt_message = content['msg']

         #wait until disc_message isn't empty, check every 1s?
         while disc_message == '':
            time.sleep(1)

         #send the disc_message back to chatgpt page
         self.wfile.write(bytes(disc_message,'utf-8'))

         #clear disc_message
         disc_message = ''

      #the response data is sent at the end of this method
      return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
   """I dont know what this does"""

httpd = ThreadedHTTPServer(('localhost',8080),Serv)
print("Server is up. Don't forget to refresh chatgpt webpage")
httpd.serve_forever()



