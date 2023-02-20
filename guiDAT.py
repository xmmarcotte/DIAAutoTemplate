import smartsheet
from geopy.geocoders import Nominatim
import usaddress
import sys
import tkinter
from tkinter import *
import win32gui
import win32con
import re

if sys.stdin.isatty():
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide, win32con.SW_HIDE)


def exitProg():
    sys.exit()


def splash():
    splash_win = Tk()
    splash_win.title('DIA Auto Template')
    splash_win.iconbitmap('terminal.ico')
    w = 588
    h = 290
    ws = splash_win.winfo_screenwidth()
    hs = splash_win.winfo_screenheight()
    x = ws / 2 - w / 2
    y = hs / 2 - h / 2
    splash_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    img = PhotoImage(file='cooltext422597314654859.png')
    splashLogo = tkinter.Label(splash_win, image=img)
    splashLogo.pack()
    greeting = tkinter.Label(text='Author: Mikey Marcotte')
    greeting.pack()
    splash_win.after(3000, lambda: splash_win.destroy())
    splash_win.protocol("WM_DELETE_WINDOW", exitProg)
    splash_win.mainloop()


def main():
    def printValue(event):
        global tkt
        tkt = ticket.get()
        main.destroy()

    def printValue2():
        global tkt
        tkt = ticket.get()
        main.destroy()

    main = Tk()
    main.title('DIA Auto Template')
    main.iconbitmap('terminal.ico')
    w = 300
    h = 100
    ws = main.winfo_screenwidth()
    hs = main.winfo_screenheight()
    x = ws / 2 - w / 2
    y = hs / 2 - h / 2
    main.geometry('%dx%d+%d+%d' % (w, h, x, y))
    greeting = tkinter.Label(text='Please enter the ticket number: ')
    greeting.pack(pady=10)
    ticket = Entry(main)
    ticket.pack(pady=5)
    main.bind('<Return>', printValue)
    Button(main,
           text='Submit',
           padx=0,
           pady=0,
           command=printValue2).pack()
    main.protocol("WM_DELETE_WINDOW", exitProg)
    main.mainloop()


def tryAgain():
    def printValue(event):
        global tkt
        tkt = ticket.get()
        ta.destroy()

    def printValue2():
        global tkt
        tkt = ticket.get()
        ta.destroy()

    ta = Tk()
    ta.title('DIA Auto Template')
    ta.iconbitmap('terminal.ico')
    w = 300
    h = 100
    ws = ta.winfo_screenwidth()
    hs = ta.winfo_screenheight()
    x = ws / 2 - w / 2
    y = hs / 2 - h / 2
    ta.geometry('%dx%d+%d+%d' % (w, h, x, y))
    greeting = tkinter.Label(text='Ticket not found. Please re-enter the ticket number: ')
    greeting.pack(pady=10)
    ticket = Entry(ta)
    ticket.pack(pady=5)
    ta.bind('<Return>', printValue)
    Button(ta,
           text='Submit',
           padx=0,
           pady=0,
           command=printValue2).pack()
    ta.bind('<Return>', printValue)
    ta.protocol("WM_DELETE_WINDOW", exitProg)
    ta.mainloop()


def popUp():
    win = Tk()
    win.title('DIA Auto Template')
    win.iconbitmap('terminal.ico')
    w = 700
    h = 450
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = ws / 2 - w / 2
    y = hs / 2 - h / 2
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    v = Scrollbar(win, orient='vertical')
    v.pack(side=RIGHT, fill='y')
    text = Text(win, font=('Consolas', '12'), yscrollcommand=v.set)
    text.insert(END, write)
    v.config(command=text.yview)
    text.pack()
    win.protocol("WM_DELETE_WINDOW", exitProg)
    win.mainloop()


geolocator = Nominatim(user_agent='geoapiExercises')
SMARTSHEET_ACCESS_TOKEN = 'vrwMoy8Wy9APWHRxhWvWkoo0k0GuYs4npJ2Kw'
smart = smartsheet.Smartsheet(SMARTSHEET_ACCESS_TOKEN)
smart.errors_as_exceptions(True)
sheet_id = 8499987391768452
sheet = smart.Sheets.get_sheet(sheet_id)
column_map = {}
for column in sheet.columns:
    column_map[column.title] = column.id
row_map = {}


def get_cell_by_column_name(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)


i = 0
for rows in sheet.rows:
    row_map[i] = rows.id
    i = i + 1


def getInfo():
    global exists, account, configType, hostname, lanSubnet, lanGateway, cktId, wanSubnet, wanGateway, lanIp, wanIp, carrier, speed, address, password, city, state
    exists = False
    for row in sheet.rows:
        if tkt == get_cell_by_column_name(row, 'Equipment Ticket/PWO').display_value:
            exists = True
            account = get_cell_by_column_name(row, 'Account').display_value
            configType = get_cell_by_column_name(row, 'config script template type').display_value
            hostname = get_cell_by_column_name(row, 'Hostname').display_value
            lanSubnet = get_cell_by_column_name(row, 'LAN subnet mask').display_value
            lanGateway = get_cell_by_column_name(row, 'LAN gateway').display_value
            cktId = get_cell_by_column_name(row, 'circuit ID').display_value
            wanSubnet = get_cell_by_column_name(row, 'WAN subnet mask').display_value
            wanGateway = get_cell_by_column_name(row, 'WAN gateway.').display_value
            lanIp = get_cell_by_column_name(row, 'LAN IP (LAN Network IP)').display_value
            wanIp = get_cell_by_column_name(row, 'WAN IP address (WAN Usable)').display_value
            carrier = get_cell_by_column_name(row, 'Carrier').display_value
            speed = get_cell_by_column_name(row, 'Speed').display_value
            speed = re.sub('\D', '', speed)
            address = get_cell_by_column_name(row, "Customer Location").display_value
            address = usaddress.parse(address)
            address = dict(address)
            address = dict((v, k) for k, v in address.items())
            password = address['PlaceName'].replace(',', '') + speed
            city = address['PlaceName'].replace(',', '')
            state = address['StateName']


splash()
main()
try:
    getInfo()
except Exception as e:
    write = e
while not exists:
    tryAgain()
    getInfo()
if configType == '4K series RJ45':
    write = f"""hostname {hostname}
enable secret Granite1!
username GraniteNOC secret Gran1te0ff
username ADSOffnet secret {password}
username TempTech secret Password123

service password-encryption



ip domain name granitenet.com


crypto key generate rsa modulus 1024

ip ssh version 2
banner motd #
WARNING: To protect the system from unauthorized use and to ensure
that the system is functioning properly, activities on this system are
monitored and recorded and subject to audit.  Use of this system is
expressed consent to such monitoring and recording.  Any unauthorized
access or use of this Automated Information System is prohibited and
could be subject to criminal and civil penalties.
#

interface GigabitEthernet0/0/0
description To {carrier} WAN CID {cktId} // {account}
ip address {wanIp} {wanSubnet}
no negotiation auto
media-type  RJ45
speed 100
no shutdown
exit


interface GigabitEthernet0/0/1
description To LAN
ip address {lanGateway} {lanSubnet}
negotiation auto
no shutdown

ip route 0.0.0.0 0.0.0.0 {wanGateway}
ip ssh version 2


line con 0
login local
no ip access-list standard CPEAccess
ip access-list standard CPEAccess
permit 172.16.0.0 0.15.255.255
permit 10.0.0.0 0.255.255.255
permit 192.168.0.0 0.0.255.255
permit 198.18.0.0 0.1.255.255
permit 198.51.100.0 0.0.0.255
permit host 65.202.145.2
permit host 72.46.171.2
permit host 172.85.135.238
permit host 162.223.83.42
permit host 162.223.83.38
deny   any

ip access-list standard GRANITESNMP
permit 162.223.83.38
permit 162.223.86.38
permit 172.85.135.238
permit 198.19.0.33
permit 198.19.0.32
deny   any log
!

SNMP-Server view SNMPv3View 1.3.6 included
SNMP-Server group SNMPv3Group v3 priv Read SNMPv3View Write SNMPv3View
SNMP-Server user SNMPv3User SNMPv3Group v3 auth md5 $$w1n$t@R!$$ priv des $$w1n$t@R!$$ access GRANITESNMP

archive
log config
logging enable
logging size 150
notify syslog contenttype plaintext
hidekeys

cts logging verbose

no aaa new-model
clock timezone EDT -5 0
clock summer-time EDT recurring 2 Sun Mar 3:00 1 Sun Nov 3:00

line con 0
exec-timeout 15 0
logging synchronous
stopbits 1
line aux 0
stopbits 1
line vty 0 4
access-class CPEAccess in
exec-timeout 15 0
logging synchronous
transport input ssh
line vty 5 15
access-class CPEAccess in
exec-timeout 5 0
logging synchronous
transport input ssh

no ip nat service sip udp port 5060
ip forward-protocol nd
no ip http server
no ip http secure-server


end

copy run start

copy run start


POWER CYCLE ROUTER

conf t

aaa new-model

ip tacacs source-interface GigabitEthernet0/0/0

aaa authentication login default group tacacs+ local
aaa authentication enable default group tacacs+ enable
aaa authorization console
aaa authorization exec default group tacacs+ local 
aaa authorization commands 1 default group tacacs+ local 
aaa authorization commands 15 default group tacacs+ local 
aaa authorization network default group tacacs+ local 
aaa accounting exec default start-stop group tacacs+
aaa accounting commands 1 default start-stop group tacacs+
aaa accounting commands 15 default start-stop group tacacs+
aaa accounting network default start-stop group tacacs+
aaa accounting connection default start-stop group tacacs+
aaa accounting system default start-stop group tacacs+

tacacs server EXTERNAL_ACS
address ipv4 172.85.135.235 
timeout 1 
key V#38fe;5K[

tacacs-server directed-request

line con 0
exec-timeout 15 0
logging synchronous
line vty 0 15
logging synchronous
transport input ssh
end


copy run start
copy run start

sh ver

sh run
"""

elif configType == '4K series with SFP':
    write = f"""hostname {hostname}
enable secret Granite1!
username GraniteNOC secret Gran1te0ff
username ADSOffnet secret {password}
username TempTech secret Password123


service password-encryption


ip domain name granitenet.com


crypto key generate rsa modulus 1024




ip ssh version 2
banner motd #
WARNING: To protect the system from unauthorized use and to ensure
that the system is functioning properly, activities on this system are
monitored and recorded and subject to audit.  Use of this system is
expressed consent to such monitoring and recording.  Any unauthorized
access or use of this Automated Information System is prohibited and
could be subject to criminal and civil penalties.
#

interface GigabitEthernet0/0/0
description To {carrier} WAN CID {cktId} // {account}
ip address {wanIp} {wanSubnet}
no negotiation auto
media-type  sfp
no shutdown
exit


interface GigabitEthernet0/0/1
description To LAN
ip address {lanGateway} {lanSubnet}
negotiation auto
no shutdown

ip route 0.0.0.0 0.0.0.0 {wanGateway}
ip ssh version 2


line con 0
login local
no ip access-list standard CPEAccess
ip access-list standard CPEAccess
permit 172.16.0.0 0.15.255.255
permit 10.0.0.0 0.255.255.255
permit 192.168.0.0 0.0.255.255
permit 198.18.0.0 0.1.255.255
permit 198.51.100.0 0.0.0.255
permit host 65.202.145.2
permit host 72.46.171.2
permit host 172.85.135.238
permit host 162.223.83.42
permit host 162.223.83.38
deny   any

ip access-list standard GRANITESNMP
permit 162.223.83.38
permit 162.223.86.38
permit 172.85.135.238
permit 198.19.0.33
permit 198.19.0.32
deny   any log
!

SNMP-Server view SNMPv3View 1.3.6 included
SNMP-Server group SNMPv3Group v3 priv Read SNMPv3View Write SNMPv3View
SNMP-Server user SNMPv3User SNMPv3Group v3 auth md5 $$w1n$t@R!$$ priv des $$w1n$t@R!$$ access GRANITESNMP

archive
log config
logging enable
logging size 150
notify syslog contenttype plaintext
hidekeys

cts logging verbose

no aaa new-model
clock timezone EDT -5 0
clock summer-time EDT recurring 2 Sun Mar 3:00 1 Sun Nov 3:00

line con 0
exec-timeout 15 0
logging synchronous
stopbits 1
line aux 0
stopbits 1
line vty 0 4
access-class CPEAccess in
exec-timeout 15 0
logging synchronous
transport input ssh
line vty 5 15
access-class CPEAccess in
exec-timeout 5 0
logging synchronous
transport input ssh

no ip nat service sip udp port 5060
ip forward-protocol nd
no ip http server
no ip http secure-server


end

copy run start

copy run start


POWER CYCLE ROUTER

conf t

aaa new-model

ip tacacs source-interface GigabitEthernet0/0/0

aaa authentication login default group tacacs+ local
aaa authentication enable default group tacacs+ enable
aaa authorization console
aaa authorization exec default group tacacs+ local 
aaa authorization commands 1 default group tacacs+ local 
aaa authorization commands 15 default group tacacs+ local 
aaa authorization network default group tacacs+ local 
aaa accounting exec default start-stop group tacacs+
aaa accounting commands 1 default start-stop group tacacs+
aaa accounting commands 15 default start-stop group tacacs+
aaa accounting network default start-stop group tacacs+
aaa accounting connection default start-stop group tacacs+
aaa accounting system default start-stop group tacacs+

tacacs server EXTERNAL_ACS
address ipv4 172.85.135.235 
timeout 1 
key V#38fe;5K[

tacacs-server directed-request

line con 0
exec-timeout 15 0
logging synchronous
line vty 0 15
logging synchronous
transport input ssh
end


copy run start
copy run start

sh ver

sh run
"""

elif configType == 'Offnet_ASR-920_Copper_LAN':
    write = f"""!
version 15.6
no service pad
service timestamps debug datetime msec
service timestamps log datetime msec
service password-encryption
no platform punt-keepalive disable-kernel-core
platform bfd-debug-trace 1
platform xconnect load-balance-hash-algo mac-ip-instanceid
platform tcam-parity-error enable
platform tcam-threshold alarm-frequency 1
!
hostname {hostname}
!
boot-start-marker
boot-end-marker
!
!
vrf definition Mgmt-intf
!
address-family ipv4
exit-address-family
!
address-family ipv6
exit-address-family
!
logging buffered 51200 warnings
!
aaa new-model
!
!
aaa group server tacacs+ management
server-private 172.85.135.235 timeout 1 key 7 122F46444A0D095F7F001F
ip tacacs source-interface BDI100
!
aaa authentication login default group management local
aaa authentication enable default group management enable
aaa authorization console
aaa authorization exec default group management local 
aaa authorization commands 1 default group management local 
aaa authorization commands 15 default group management local 
aaa authorization network default group management local 
aaa accounting exec default start-stop group management
aaa accounting commands 1 default start-stop group management
aaa accounting commands 15 default start-stop group management
aaa accounting network default start-stop group management
aaa accounting connection default start-stop group management
aaa accounting system default start-stop group management
!
!
!
!
!
aaa session-id common
clock timezone EST -5 0
clock summer-time EDT recurring 2 Sun Mar 3:00 1 Sun Nov 3:00
facility-alarm critical exceed-action shutdown
!
!
!
!
!
!
!
!
!

no ip domain lookup
ip domain name granitempls.com
!
ip dhcp pool Mgmt-intf
network 172.16.0.0 255.255.255.0
!
!
!
!
login block-for 300 attempts 4 within 120
login delay 2
login on-failure log
login on-success log
!
!
!         
!
!
!
!
!
!
multilink bundle-name authenticated
!
!
!
sdm prefer default 
!
username NOCAdmin privilege 15 secret 5 $1$QxBT$i0o24EYUorGW8MGdm8.gE1
username turnup-temp privilege 15 secret 5 $1$Mk4X$0a44f6jFsUke7lwozYCt5/
username granitenoc secret 5 $1$J.jq$fKW6pxUQp.gCyuCxGz/lf0
!
redundancy
bridge-domain 100 
!
!
!         
!
!
transceiver type all
monitoring
!
! 
!
crypto key generate rsa modulus 1024
!
!
!
!
!
!
!
!
interface GigabitEthernet0/0/0
description  {cktId} {account}
no ip address
media-type rj45
speed 1000
no negotiation auto
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
!
!
interface GigabitEthernet0/0/1
description CUSTOMER LAN
ip address {lanGateway} {lanSubnet}
media-type rj45
negotiation auto
!
interface TenGigabitEthernet0/0/2
description {cktId} {account}
no ip address
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
!
!
interface TenGigabitEthernet0/0/3
description OPTICAL CUSTOMER LAN
no ip address
!
interface TenGigabitEthernet0/0/4
no ip address
!
interface TenGigabitEthernet0/0/5
no ip address
!
interface GigabitEthernet0
vrf forwarding Mgmt-intf
ip address 172.16.0.1 255.255.255.0
negotiation auto
!
interface BDI100
ip address  {wanIp} {wanSubnet}
no shut
!
ip forward-protocol nd
!
ip bgp-community new-format
no ip http server
no ip http secure-server
ip tftp source-interface GigabitEthernet0
ip tacacs source-interface BDI100
ip ssh time-out 60
ip ssh authentication-retries 2
ip ssh version 2
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip route 0.0.0.0 0.0.0.0 {wanGateway}
!
ip access-list standard CPEAccess
permit 162.223.83.42
permit 162.223.83.38
permit 65.202.145.2
permit 134.204.10.2
permit 134.204.11.2
permit 172.85.135.238
permit 172.85.180.240
permit 72.46.171.2
permit 172.16.0.0 0.15.255.255
permit 10.0.0.0 0.255.255.255
permit 192.168.0.0 0.0.255.255
permit 198.18.0.0 0.1.255.255
permit 198.51.100.0 0.0.0.255
permit 100.64.1.0 0.0.0.255
permit 100.64.2.0 0.0.0.255
deny   any
ip access-list standard GRANITESNMP
permit 162.223.83.42
permit 162.223.83.38
permit 162.223.86.38
permit 172.85.135.238
permit 172.85.180.240
permit 198.19.0.33
permit 198.19.0.32
permit 198.19.127.0 0.0.0.31
deny   any log
ip access-list standard GraniteNTP
permit 162.223.83.36
permit 162.223.86.36
permit 198.18.0.0 0.1.255.255
deny   any
!
!
!
snmp-server group SNMPv3Group v3 priv read SNMPv3View write SNMPv3View 
snmp-server view SNMPv3View dod included
SNMP-Server user SNMPv3User SNMPv3Group v3 auth md5 $$w1n$t@R!$$ priv des $$w1n$t@R!$$ access GRANITESNMP
snmp-server community yNLQ14xxH4mgV RO GRANITESNMP
snmp-server trap-source BDI100
snmp-server location {city}, {state}
snmp-server chassis-id {hostname}
snmp-server enable traps bfd
snmp-server enable traps config-copy
snmp-server enable traps config
snmp-server enable traps event-manager
snmp-server enable traps cpu threshold
snmp-server enable traps ethernet evc status create delete
snmp-server enable traps alarms informational
snmp-server enable traps ethernet cfm alarm
snmp-server enable traps transceiver all

snmp ifmib ifindex persist
!
tacacs-server directed-request
!
!
!
control-plane
!
banner motd ^CCCCC

WARNING: To protect the system from unauthorized use and to ensure
that the system is functioning properly, activities on this system are
monitored and recorded and subject to audit.  Use of this system is
expressed consent to such monitoring and recording.  Any unauthorized
access or use of this Automated Information System is prohibited and
could be subject to criminal and civil penalties.

^C
!
line con 0
exec-timeout 15 0
logging synchronous
stopbits 1
line aux 0
stopbits 1
line vty 0 4
access-class CPEAccess in vrf-also
logging synchronous
transport input ssh
line vty 5 15
access-class CPEAccess in vrf-also
logging synchronous
transport input ssh
!         
exception crashinfo file bootflash:crashinfo
ntp source BDI100
ntp access-group peer GraniteNTP
ntp server 162.223.83.36 prefer
ntp server 162.223.86.36
!
!
end

"""

elif configType == 'Offnet_ASR-920_Fiber_LAN':
    write = f"""hostname {hostname}

boot-start-marker	
boot-end-marker


vrf definition Mgmt-intf

address-family ipv4
exit-address-family

address-family ipv6
exit-address-family

logging buffered 51200 warnings

aaa new-model


aaa group server tacacs+ management
server-private 172.85.135.235 timeout 1 key 7 122F46444A0D095F7F001F
ip tacacs source-interface BDI100

aaa authentication login default group management local
aaa authentication enable default group management enable
aaa authorization console
aaa authorization exec default group management local 
aaa authorization commands 1 default group management local 
aaa authorization commands 15 default group management local 
aaa authorization network default group management local 
aaa accounting exec default start-stop group management
aaa accounting commands 1 default start-stop group management
aaa accounting commands 15 default start-stop group management
aaa accounting network default start-stop group management
aaa accounting connection default start-stop group management
aaa accounting system default start-stop group management





aaa session-id common
facility-alarm critical exceed-action shutdown











no ip domain lookup
ip domain name granitempls.com












multilink bundle-name authenticated


license boot level metroipaccess

sdm prefer default 



username NOCAdmin privilege 15 secret 5 $1$QxBT$i0o24EYUorGW8MGdm8.gE1
username turnup-temp privilege 15 secret 5 $1$Mk4X$0a44f6jFsUke7lwozYCt5/
username granitenoc secret 5 $1$J.jq$fKW6pxUQp.gCyuCxGz/lf0

redundancy
bridge-domain 100 





transceiver type all
monitoring







crypto key generate rsa modulus 1024	  


ip dhcp pool Mgmt-intf
network 172.16.0.0 255.255.255.0          

interface GigabitEthernet0/0/0
description {cktId} {account}
no ip address
media-type rj45
negotiation auto
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
no shutdown



interface GigabitEthernet0/0/1
description // CUSTOMER_PUBLIC_LAN //
media-type rj45
negotiation auto
no shutdown


interface TenGigabitEthernet0/0/2
description {cktId} {account}
no ip address
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
no shutdown


interface TenGigabitEthernet0/0/3
description // CUSTOMER_PUBLIC_LAN_Fiber//
ip address  {lanIp} {lanSubnet}
negotiation auto
no shutdown

interface TenGigabitEthernet0/0/4
no ip address

interface TenGigabitEthernet0/0/5
no ip address

interface GigabitEthernet0
vrf forwarding Mgmt-intf
no ip address
negotiation auto

interface BDI100
ip address  {wanIp} {wanSubnet}

no shutdown

ip forward-protocol nd

ip bgp-community new-format
no ip http server
no ip http secure-server
ip tftp source-interface GigabitEthernet0
ip ssh time-out 60
ip ssh authentication-retries 2
ip ssh version 2
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip route 0.0.0.0 0.0.0.0 {wanGateway}



ip access-list standard GRANITESNMP
permit 162.223.83.42
permit 162.223.83.38
permit 162.223.86.38
permit 172.85.135.238
permit 172.85.180.240
permit 198.19.0.33
permit 198.19.0.32
permit 198.19.127.0 0.0.0.31
deny   any log
ip access-list standard GraniteNTP
permit 162.223.83.36
permit 162.223.86.36
permit 198.18.0.0 0.1.255.255
deny   any


ip access-list extended VTY
permit ip host 162.223.83.42 any
permit ip host 162.223.83.38 any
permit ip host 65.202.145.2 any
permit ip host 172.85.135.238 any
permit ip host 198.19.127.2 any
permit ip host 198.19.0.21 any
permit ip host 172.85.228.254 any
permit ip host 134.204.10.2 any
permit ip host 134.204.11.2 any
permit ip host 72.46.171.2 any
permit ip 172.16.0.0 0.15.255.255 any
permit ip 10.0.0.0 0.255.255.255 any
permit ip 192.168.0.0 0.0.255.255 any
permit ip 198.18.0.0 0.1.255.255 any
permit ip 100.64.1.0 0.0.0.255 any
permit ip 198.51.100.0 0.0.0.255 any
permit ip 100.64.2.0 0.0.0.255 any


snmp-server group SNMPv3Group v3 priv read SNMPv3View write SNMPv3View 
snmp-server view SNMPv3View dod included
SNMP-Server user SNMPv3User SNMPv3Group v3 auth md5 $$w1n$t@R $$ priv des $$w1n$t@R $$ access GRANITESNMP
snmp-server trap-source BDI100
snmp-server location {city}, {state}
snmp-server chassis-id {hostname}
snmp-server enable traps bfd
snmp-server enable traps config-copy
snmp-server enable traps config
snmp-server enable traps event-manager
snmp-server enable traps cpu threshold
snmp-server enable traps ethernet evc status create delete
snmp-server enable traps alarms informational
snmp-server enable traps ethernet cfm alarm
snmp-server enable traps transceiver all
snmp ifmib ifindex persist

tacacs-server directed-request





control-plane

banner motd ^CCCCCC

WARNING: To protect the system from unauthorized use and to ensure
that the system is functioning properly, activities on this system are
monitored and recorded and subject to audit.  Use of this system is
expressed consent to such monitoring and recording.  Any unauthorized
access or use of this Automated Information System is prohibited and
could be subject to criminal and civil penalties.

^C

line con 0
exec-timeout 15 0
logging synchronous
stopbits 1
line aux 0
stopbits 1
line vty 0 4
access-class VTY in vrf-also
logging synchronous
transport input ssh
line vty 5 15
access-class VTY in vrf-also
logging synchronous
transport input ssh

exception crashinfo file bootflash:crashinfo

ntp source BDI100
ntp access-group peer GraniteNTP
ntp server 162.223.83.36 prefer
ntp server 162.223.86.36



end
"""

elif configType == 'Offnet_ASR-920_24Port_Fiber_LAN':
    write = f"""hostname {hostname}

boot-start-marker	
boot-end-marker


vrf definition Mgmt-intf

address-family ipv4
exit-address-family

address-family ipv6
exit-address-family

logging buffered 51200 warnings

aaa new-model


aaa group server tacacs+ management
server-private 172.85.135.235 timeout 1 key 7 122F46444A0D095F7F001F
ip tacacs source-interface BDI100

aaa authentication login default group management local
aaa authentication enable default group management enable
aaa authorization console
aaa authorization exec default group management local 
aaa authorization commands 1 default group management local 
aaa authorization commands 15 default group management local 
aaa authorization network default group management local 
aaa accounting exec default start-stop group management
aaa accounting commands 1 default start-stop group management
aaa accounting commands 15 default start-stop group management
aaa accounting network default start-stop group management
aaa accounting connection default start-stop group management
aaa accounting system default start-stop group management





aaa session-id common
facility-alarm critical exceed-action shutdown











no ip domain lookup
ip domain name granitempls.com












multilink bundle-name authenticated


license boot level metroipaccess

sdm prefer default 



username NOCAdmin privilege 15 secret 5 $1$QxBT$i0o24EYUorGW8MGdm8.gE1
username turnup-temp privilege 15 secret 5 $1$Mk4X$0a44f6jFsUke7lwozYCt5/
username granitenoc secret 5 $1$J.jq$fKW6pxUQp.gCyuCxGz/lf0

redundancy
bridge-domain 100 





transceiver type all
monitoring







crypto key generate rsa modulus 1024	  


ip dhcp pool Mgmt-intf
network 172.16.0.0 255.255.255.0          

interface GigabitEthernet0/0/0
description {cktId} {account}
no ip address
media-type rj45
negotiation auto
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
no shutdown



interface GigabitEthernet0/0/1
description // CUSTOMER_PUBLIC_LAN //
media-type rj45
negotiation auto
no shutdown

interface range GigabitEthernet0/0/2-23
shut

interface TenGigabitEthernet0/0/24
description {cktId} {account}
no ip address
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
no shutdown


interface TenGigabitEthernet0/0/25
description // CUSTOMER_PUBLIC_LAN_Fiber//
ip address  {lanIp} {lanSubnet}
negotiation auto
no shutdown

interface range TenGigabitEthernet0/0/26-27
shut


interface GigabitEthernet0
vrf forwarding Mgmt-intf
no ip address
negotiation auto

interface BDI100
ip address  {wanIp} {wanSubnet}

no shutdown

ip forward-protocol nd

ip bgp-community new-format
no ip http server
no ip http secure-server
ip tftp source-interface GigabitEthernet0
ip ssh time-out 60
ip ssh authentication-retries 2
ip ssh version 2
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip route 0.0.0.0 0.0.0.0 {wanGateway}



ip access-list standard GRANITESNMP
permit 162.223.83.42
permit 162.223.83.38
permit 162.223.86.38
permit 172.85.135.238
permit 172.85.180.240
permit 198.19.0.33
permit 198.19.0.32
permit 198.19.127.0 0.0.0.31
deny   any log
ip access-list standard GraniteNTP
permit 162.223.83.36
permit 162.223.86.36
permit 198.18.0.0 0.1.255.255
deny   any


ip access-list extended VTY
permit ip host 162.223.83.42 any
permit ip host 162.223.83.38 any
permit ip host 65.202.145.2 any
permit ip host 172.85.135.238 any
permit ip host 198.19.127.2 any
permit ip host 198.19.0.21 any
permit ip host 172.85.228.254 any
permit ip host 134.204.10.2 any
permit ip host 134.204.11.2 any
permit ip host 72.46.171.2 any
permit ip 172.16.0.0 0.15.255.255 any
permit ip 10.0.0.0 0.255.255.255 any
permit ip 192.168.0.0 0.0.255.255 any
permit ip 198.18.0.0 0.1.255.255 any
permit ip 100.64.1.0 0.0.0.255 any
permit ip 198.51.100.0 0.0.0.255 any
permit ip 100.64.2.0 0.0.0.255 any


snmp-server group SNMPv3Group v3 priv read SNMPv3View write SNMPv3View 
snmp-server view SNMPv3View dod included
SNMP-Server user SNMPv3User SNMPv3Group v3 auth md5 $$w1n$t@R $$ priv des $$w1n$t@R $$ access GRANITESNMP
snmp-server trap-source BDI100
snmp-server location {city}, {state}
snmp-server chassis-id {hostname}
snmp-server enable traps bfd
snmp-server enable traps config-copy
snmp-server enable traps config
snmp-server enable traps event-manager
snmp-server enable traps cpu threshold
snmp-server enable traps ethernet evc status create delete
snmp-server enable traps alarms informational
snmp-server enable traps ethernet cfm alarm
snmp-server enable traps transceiver all
snmp ifmib ifindex persist

tacacs-server directed-request





control-plane

banner motd ^CCCCCC

WARNING: To protect the system from unauthorized use and to ensure
that the system is functioning properly, activities on this system are
monitored and recorded and subject to audit.  Use of this system is
expressed consent to such monitoring and recording.  Any unauthorized
access or use of this Automated Information System is prohibited and
could be subject to criminal and civil penalties.

^C

line con 0
exec-timeout 15 0
logging synchronous
stopbits 1
line aux 0
stopbits 1
line vty 0 4
access-class VTY in vrf-also
logging synchronous
transport input ssh
line vty 5 15
access-class VTY in vrf-also
logging synchronous
transport input ssh

exception crashinfo file bootflash:crashinfo

ntp source BDI100
ntp access-group peer GraniteNTP
ntp server 162.223.83.36 prefer
ntp server 162.223.86.36



end
"""

elif configType == 'Offnet_ASR-920_DHCP_LAN_POOL':
    write = f"""!
version 15.6
no service pad
service timestamps debug datetime msec
service timestamps log datetime msec
service password-encryption
no platform punt-keepalive disable-kernel-core
platform bfd-debug-trace 1
platform xconnect load-balance-hash-algo mac-ip-instanceid
platform tcam-parity-error enable
platform tcam-threshold alarm-frequency 1
!
hostname {hostname}
!
boot-start-marker
boot-end-marker
!
!
vrf definition Mgmt-intf
!
address-family ipv4
exit-address-family
!
address-family ipv6
exit-address-family
!
logging buffered 51200 warnings
!
aaa new-model
!
!
aaa group server tacacs+ management
server-private 172.85.135.235 timeout 1 key 7 122F46444A0D095F7F001F
ip tacacs source-interface BDI100
!
aaa authentication login default group management local
aaa authentication enable default group management enable
aaa authorization console
aaa authorization exec default group management local 
aaa authorization commands 1 default group management local 
aaa authorization commands 15 default group management local 
aaa authorization network default group management local 
aaa accounting exec default start-stop group management
aaa accounting commands 1 default start-stop group management
aaa accounting commands 15 default start-stop group management
aaa accounting network default start-stop group management
aaa accounting connection default start-stop group management
aaa accounting system default start-stop group management
!
!
!
!
!
aaa session-id common
clock timezone EST -5 0
clock summer-time EDT recurring 2 Sun Mar 3:00 1 Sun Nov 3:00
facility-alarm critical exceed-action shutdown
!
!
!
!
!
!
!
!
!

no ip domain lookup
ip domain name granitempls.com
ip dhcp excluded-address {lanGateway}
!
ip dhcp pool Mgmt-intf
network 172.16.0.0 255.255.255.0
!
ip dhcp pool PUBLIC
network {lanIp} {lanSubnet}
default-router {lanGateway}
dns-server 8.8.8.8 8.8.4.4 
!
!
!
login block-for 300 attempts 4 within 120
login delay 2
login on-failure log
login on-success log
!
!
!         
!
!
!
!
!
!
multilink bundle-name authenticated
!
!
!
sdm prefer default 
!
username NOCAdmin privilege 15 secret 5 $1$QxBT$i0o24EYUorGW8MGdm8.gE1
username turnup-temp privilege 15 secret 5 $1$Mk4X$0a44f6jFsUke7lwozYCt5/
username granitenoc secret 5 $1$J.jq$fKW6pxUQp.gCyuCxGz/lf0
!
redundancy
bridge-domain 100 
!
!
!         
!
!
transceiver type all
monitoring
!
! 
!
crypto key generate rsa modulus 1024
!
!
!
!
!
!
!
!
interface GigabitEthernet0/0/0
description  {cktId} {account}
no ip address
media-type rj45
speed 1000
no negotiation auto
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
!
!
interface GigabitEthernet0/0/1
description CUSTOMER LAN
ip address {lanGateway} {lanSubnet}
media-type rj45
negotiation auto
!
interface TenGigabitEthernet0/0/2
description {cktId} {account}
no ip address
service instance 100 ethernet
encapsulation untagged
bridge-domain 100
!
!
interface TenGigabitEthernet0/0/3
description OPTICAL CUSTOMER LAN
no ip address
!
interface TenGigabitEthernet0/0/4
no ip address
!
interface TenGigabitEthernet0/0/5
no ip address
!
interface GigabitEthernet0
vrf forwarding Mgmt-intf
ip address 172.16.0.1 255.255.255.0
negotiation auto
!
interface BDI100
ip address  {wanIp} {wanSubnet}
no shut
!
ip forward-protocol nd
!
ip bgp-community new-format
no ip http server
no ip http secure-server
ip tftp source-interface GigabitEthernet0
ip tacacs source-interface BDI100
ip ssh time-out 60
ip ssh authentication-retries 2
ip ssh version 2
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr aes128-cbc aes192-cbc aes256-cbc 3des-cbc
ip route 0.0.0.0 0.0.0.0 {wanGateway}
!
ip access-list standard CPEAccess
permit 162.223.83.42
permit 162.223.83.38
permit 65.202.145.2
permit 134.204.10.2
permit 134.204.11.2
permit 172.85.135.238
permit 172.85.180.240
permit 72.46.171.2
permit 172.16.0.0 0.15.255.255
permit 10.0.0.0 0.255.255.255
permit 192.168.0.0 0.0.255.255
permit 198.18.0.0 0.1.255.255
permit 198.51.100.0 0.0.0.255
permit 100.64.1.0 0.0.0.255
permit 100.64.2.0 0.0.0.255
deny   any
ip access-list standard GRANITESNMP
permit 162.223.83.42
permit 162.223.83.38
permit 162.223.86.38
permit 172.85.135.238
permit 172.85.180.240
permit 198.19.0.33
permit 198.19.0.32
permit 198.19.127.0 0.0.0.31
deny   any log
ip access-list standard GraniteNTP
permit 162.223.83.36
permit 162.223.86.36
permit 198.18.0.0 0.1.255.255
deny   any
!
!
!
snmp-server group SNMPv3Group v3 priv read SNMPv3View write SNMPv3View 
snmp-server view SNMPv3View dod included
SNMP-Server user SNMPv3User SNMPv3Group v3 auth md5 $$w1n$t@R!$$ priv des $$w1n$t@R!$$ access GRANITESNMP
snmp-server community yNLQ14xxH4mgV RO GRANITESNMP
snmp-server trap-source BDI100
snmp-server location {city}, {state}
snmp-server chassis-id {hostname}
snmp-server enable traps bfd
snmp-server enable traps config-copy
snmp-server enable traps config
snmp-server enable traps event-manager
snmp-server enable traps cpu threshold
snmp-server enable traps ethernet evc status create delete
snmp-server enable traps alarms informational
snmp-server enable traps ethernet cfm alarm
snmp-server enable traps transceiver all

snmp ifmib ifindex persist
!
tacacs-server directed-request
!
!
!
control-plane
!
banner motd ^CCCCC

WARNING: To protect the system from unauthorized use and to ensure
that the system is functioning properly, activities on this system are
monitored and recorded and subject to audit.  Use of this system is
expressed consent to such monitoring and recording.  Any unauthorized
access or use of this Automated Information System is prohibited and
could be subject to criminal and civil penalties.

^C
!
line con 0
exec-timeout 15 0
logging synchronous
stopbits 1
line aux 0
stopbits 1
line vty 0 4
access-class CPEAccess in vrf-also
logging synchronous
transport input ssh
line vty 5 15
access-class CPEAccess in vrf-also
logging synchronous
transport input ssh
!         
exception crashinfo file bootflash:crashinfo
ntp source BDI100
ntp access-group peer GraniteNTP
ntp server 162.223.83.36 prefer
ntp server 162.223.86.36
!
!
end
"""
else:
    write = 'Config template not found. Please proceed manually.'
popUp()
