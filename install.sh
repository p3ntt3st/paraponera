#!/bin/bash
# Installation of Paraponera

KVER=`uname -a`
ARCH=`uname -m`
DISTRO=''
echo -e "\x1B[01;34m[*]\x1B[0m Installing Paraponera dependencies"

if [[ "$KVER" =~ Debian ]]; then
	
	if [[ "$(cat /etc/debian_version )" =~ Kali  ]]; then
		#NOTHING TO INSTALL
		DISTRO='Kali'
		
	fi
	
	if [[ "$(cat /etc/debian_version )" =~ 7.0  ]]; then
		if [[ ! $( cat /etc/apt/sources.list | grep -i 'unstable' ) ]]; then
			echo deb http://ftp.us.debian.org/debian unstable main contrib >> /etc/apt/sources.list
			apt-get update  > /tmp/parapondera_install.log
		fi
		export DEBIAN_FRONTEND=noninteractive
		apt-get install python-scapy python-glade2 python-webkit xterm python-pexpect ettercap-text-only sslstrip dsniff driftnet apache2 nmap -q -y > /tmp/parapondera_install.log
		head -n -1 /etc/apt/sources.list > sources.list; mv sources.list /etc/apt/sources.list
		DISTRO='Debian'
	fi

elif [[ "$KVER" =~ fc18 ]]; then
	yum install pywebkitgtk sslstrip dsniff driftnet scapy nmap ettercap xterm python-pexpect wget yum -y > /tmp/parapondera_install.log
	
	if [ ! -f /usr/sbin/ettercap ]; then
		ln -sf /usr/bin/ettercap /usr/sbin/ettercap
	fi
	DISTRO='Fedora'

elif [[ "$KVER" =~ buntu ]]; then
	sudo apt-get install python-scapy python-glade2 python-webkit xterm ettercap-text-only sslstrip dsniff driftnet apache2 nmap --force-yes -y > /tmp/paraponera_install.log
	DISTRO='Ubuntu'
fi

if [[ ! $DISTRO ]]; then
    echo -e "\x1B[01;31m[*]\x1B[0m Sorry your system is not supported."
    exit 1
fi

updatedb
ETTERCONF=`locate -n1 etter.conf`

if [ -f "${ETTERCONF}" ]; then
	echo -e "\x1B[01;34m[*]\x1B[0m Changing Ettercap etter.conf file"
	sed -i 's/ec_uid = 65534/ec_uid = 0 /g' ${ETTERCONF}
	sed -i 's/ec_gid = 65534/ec_gid = 0 /g' ${ETTERCONF}
	sed -i 's/#redir_command_on = "iptables -t nat -A PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport"/redir_command_on = "iptables -t nat -A PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport" /g' ${ETTERCONF}
	sed -i 's/#redir_command_off = "iptables -t nat -D PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport"/redir_command_off = "iptables -t nat -D PREROUTING -i %iface -p tcp --dport %port -j REDIRECT --to-port %rport" /g' ${ETTERCONF}
fi


echo -e "\x1B[01;34m[*]\x1B[0m Checking if Metasploit Framework is installed"

MSFC=`locate -n1 msfconsole`

if [ ! -f "${MSFC}" ]; then

	echo -e "\x1B[01;34m[*]\x1B[0m Downloading Metasploit Framework"
	if [ "${ARCH}" == 'x86_64' ]; then
		wget -c http://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run -q
		chmod +x metasploit-latest-linux-x64-installer.run
	        echo -e "\x1B[01;34m[*]\x1B[0m Installing Metasploit Framework"

		./metasploit-latest-linux-x64-installer.run --mode unattended
	else
		wget -c http://downloads.metasploit.com/data/releases/metasploit-latest-linux-installer.run -q
		chmod +x metasploit-latest-linux-installer.run
	        echo -e "\x1B[01;34m[*]\x1B[0m Installing Metasploit Framework"
		./metasploit-latest-linux-installer.run --mode unattended
	fi
else
	echo -e "\x1B[01;34m[*]\x1B[0m Metasploit Framework is installed"
fi


updatedb
MSFC=`locate -n1 msfconsole`

if [ ! -f "${MSFC}" ]; then
    echo -e "\x1B[01;31m[*]\x1B[0m Something went wrong with Metasploit Framework..."
    exit 1
fi	


if [ ! -f /usr/bin/msfconsole ]; then
	echo -e "\x1B[01;34m[*]\x1B[0m Creating symlinks"
	ln -sf ${MSFC} /usr/bin/msfconsole
fi

echo -e "\x1B[01;34m[*]\x1B[0m Cleaning up installation"
if [ -d downloads.metasploit.com ]; then
	rm -Rf downloads.metasploit.com
fi

if [ "${ARCH}" == 'x86_64' ]; then
	if [ -f metasploit-latest-linux-x64-installer.run ]; then
		rm metasploit-latest-linux-x64-installer.run
	fi
else
	if [ -f metasploit-latest-linux-installer.run ]; then	
		rm metasploit-latest-linux-installer.run
	fi
fi	

echo -e "\x1B[01;32m[*]\x1B[0m Installation Complete. Enjoy"

