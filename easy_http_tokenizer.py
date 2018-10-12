import http.server
import socketserver
import threading
import argparse
import re
import cgi
import json
from cutkum.tokenizer import Cutkum
import sys
import time

def tokenize(string):
        start_time = time.time()
        #print(Cutkum().tokenize(string))
        #print("--- %s seconds ---" % (time.time() - start_time))
        return Cutkum().tokenize(string)

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):   

  def do_POST(self):
    
    if None != re.search('/tokenizer', self.path):

      length = int(self.headers.get('content-length'))

      data = self.rfile.read(length)

      self.send_response(200)
      
      self.send_header('Content-Type', 'text/html')
      

      decoded_data = data.decode('utf-8')

      tokenized_data = tokenize(decoded_data)

      str_tokenized_data = '|'.join(tokenized_data)

      self.end_headers()

      self.wfile.write(str_tokenized_data.encode("utf-8"))
    return


  def do_GET(self):
    
    if None != re.search('/', self.path):

      self.send_response(200, 'test')

      self.send_header('Content-Type', 'text/html')

      #print("hello")

      self.end_headers()

      self.wfile.write("WELCOME TO CUTKUM TOKENIZER, USE POST at /tokenizer AND WRITE INPUT INTO RAW OF BODY.".encode("utf-8"))
    return

class ThreadedHTTPServer(socketserver.ThreadingMixIn,http.server. HTTPServer):
  allow_reuse_address = True

  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)

class SimpleHttpServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)

  def start(self):
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True
    self.server_thread.start()

  def waitForThread(self):
    self.server_thread.join()

  # def addRecord(self, recordID, jsonEncodedRecord):
  #  LocalData.records[recordID] = jsonEncodedRecord

  def stop(self):
    self.server.shutdown()
    self.waitForThread()

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='HTTP Server')
  parser.add_argument('port', type=int, help='Listening port for HTTP Server')
  parser.add_argument('ip', help='HTTP Server IP')
  args = parser.parse_args()

  server = SimpleHttpServer(args.ip, args.port)
  print ('HTTP Server Running...........')
  server.start()
  server.waitForThread()

