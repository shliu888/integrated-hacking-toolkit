import subprocess

def get_monitor_mode_interface(): # get the name of the interface that is in monitor mode
    try:
        # Run iwconfig command and capture output
        iwconfig_output = subprocess.check_output(['iwconfig'], stderr=subprocess.DEVNULL).decode('utf-8')
        
      
        for line in iwconfig_output.split('\n'):
            
            if " Mode:Monitor" in line:
                
                return line.split()[0]
        
        
        return None
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        
        return None
def sniff(interface): # start sniffing on all frequencies
    try:
        
        command = ['airodump-ng', interface, '-abg']
        
        
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running airodump-ng: ",e)
    except FileNotFoundError:
        print("airodump-ng is not installed or not found in the system path.")
    except Exception as e:
        print("An unexpected error occurred: ",e)
        
def monitor_mode(interface):
    try:
        # Run the airmon-ng command to start monitor mode on the specified interface
        subprocess.run(['airmon-ng', 'start', interface], check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to start monitor mode on ",interface,': ',e)
def wirelessAttack():
    while True:
        print('''
    1. Put a wireless card in monitor mode
    2. Packet sniffing
    3. Target packet sniffing
    4. Deauth attack
    5. ARP spoofing attack
    6. Capture WPA/WPA2 handshake
    ''')
        WAchoice=input('Select an option: ')
        if WAchoice=='1':
            check_command = ["airmon-ng", "check"]
    
            try:
                
                check_output = subprocess.run(check_command, capture_output=True, text=True, check=True)
                print("Processes that may interfere with airmon-ng:")
                print(check_output.stdout)
        
                # kills interfering processes
                kill_command = ["airmon-ng", "check", "kill"]
                kill_output = subprocess.run(kill_command, capture_output=True, text=True, check=True)
        
                print("Killed interfering processes:")
                print(kill_output.stdout)
        
            except subprocess.CalledProcessError as e:
                print("An error occurred while executing the command:")
                print(e.stderr)
            monInterface=input('Enter your interface name: ')
            monitor_mode(monInterface)
            monMode = get_monitor_mode_interface()
            print("Successfully started monitor mode on",monMode)
        elif WAchoice=='2':
            monMode = get_monitor_mode_interface()
            sniff(monMode)
        
        
#---------------------------------------
print('''

#######################################
#        Author & Maintainer:         #
#                                     #
#            Shu-Hao Liu              #
#                                     #
#######################################
''')


print('''

1. Wireless Attacks
2. Scanning and Reconnaissance
3. Social Engineering Attacks via TrustedSec's Social-Engineering Toolkit (SET)
4. Payload Generator
5. Password Attacks
''')

choice1= input('Select an option: ')

if choice1=='1':
    wirelessAttack()
elif choice1=='2':
    scanning()
elif choice1=='3':
    socialEngineering()
elif choice1=='4':
    payload()
elif choice1=='5':
    passwdAttacks()
else:
    print('Invalid option')
#-----------------------------------

