import socket
import time
import vs2020
import sys
from optparse import OptionParser

class TcpClient(object):

  def __init__(self, options):
    super().__init__()
    self.options = options
    self.buffer_size = 4096
    host = options.tcp_host
    port = options.tcp_port
    timeout = float(options.timeout)/1000
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.settimeout(timeout)
    self.sock.connect((host, port))

  def command(self, cmd):
    self.sock.send(bytes(cmd + "\r\n",'utf-8'))
    r = self.sock.recv(self.buffer_size)
    return r.decode().rstrip()

  def close(self):
    self.sock.close()

if __name__ == '__main__':
  config = vs2020.config()
  parser = OptionParser("""usage: %prog [options]
SYNOPSIS AND USAGE
  %prog [options]

DESCRIPTION
    TCP client for stage-view app. This program
    communicates with stage controller.
    Note that this program reads `~/.vs2020rc' for configuration.

    If you see timeout error, set `timeout'
    line on the configration file as below and raise the
    value.  Default setting is 5000 mseconds.

    timeout: 5000  

EXAMPLE

SEE ALSO
  http://dream.misasa.okayama-u.ac.jp
  https://github.com/misasa/vs2020/blob/master/vs2020/tcp_client.py

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014-2022 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  January 26, 2022: Add Program
""")
  parser.add_option("-v","--verbose",action="store_true",dest="verbose",default=False,help="make lots of noise")
  parser.add_option("--tcp-host",action="store",type="string",dest="tcp_host",default=config['tcp_host'],help="set the address of the Stage controller (default: %default) which the program will connect to.")
  parser.add_option("--tcp-port",action="store",type="int",dest="tcp_port",default=config['tcp_port'],help="set the port of the Stage controller (default: %default) which the program will connect to.")
  # parser.add_option("--tls-path",action="store",type="string",dest="tls_path", default=config['tls_path'],help="set the tls file path of the MQTT broker (default: %default) which the program will connect to.")
  parser.add_option("--timeout",action="store",type="int",dest="timeout",default=config['timeout'],help="set timeout in msec (default: %default)")
  parser.add_option("-l","--log_level",dest="log_level",default="INFO",help="set log level")

  (options, args) = parser.parse_args()

  c = TcpClient(options)
  while True:
    try:
      inp = input("YOU>")
      r = c.command(inp)
      print(r)
      time.sleep(1)
    except socket.timeout:
      print("timed out!!!")      
    except Exception as e:
      print(e, file=sys.stderr)
