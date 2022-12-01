### About
#### Here is listed the requirements for buerokratt and how to build your infrastructure in Riigipilv

Database VirtualMachine (VM that runs postgres databases)
```
2vCPU, 4GB RAM, min 10-15GB HDD
```
BOT VirtualMachine (VM that runs bot)
```
4vCPU, 4GB RAM, min 10-15 GB HDD
```
BOT-TRAIN VirtualMachine (VM that runs bot train)
```
4vCPU, 4-8GB RAM, min 10-15GB HDD
```
BYKSTACK VirtualMachine (VM that runs buerokratt core services)
```
4-8vCPU, 8-10GB RAM, min 5-10HDD
```

#### URL requirements
Production enviorment  
Customer-service - admin.buerokratt.YOURDOMAIN.ee  
TIM - tim.buerokratt.YOURDOMAIN.ee  
Public ruuter - ruuter.buerokratt.YOURDOMAIN.ee   
Private ruuter - priv-ruuter.buerokratt.YOURDOMAIN.ee  
Chat widget - buerokratt.YOURDOMAIN.ee  
Monitoring - seire.buerokratt.YOURDOMAIN.ee  
Analytics - analyytika.buerokratt.YOURDOMAIN.ee  


Test enviorment  
Customer-service - admin.test.buerokratt.YOURDOMAIN.ee  
TIM - tim.test.buerokratt.YOURDOMAIN.ee  
Public ruuter - ruuter.test.buerokratt.YOURDOMAIN.ee  
Private ruuter - priv-ruuter.test.buerokratt.YOURDOMAIN.ee  
Chat widget - buerokratt.test.YOURDOMAIN.ee  
Monitoring - seire.test.buerokratt.YOURDOMAIN.ee  
Analytics - analyytika.test.buerokratt.YOURDOMAIN.ee 

### Riigipilv infrastructure building for buerokratt
After ordering the VM's in RPLV follow these steps in Riigpiv (RPLV)  
- build the required VM's using the correct flavors (this automatically adds the required vcpu, ssd/hdd, ram) and choose Ubuntu 20.04 as OS (make sure to add extra ssh keys if necessary (alternatively you an add them under .ssh/authorized_keys)
- add new networking security group to open required ports for buerokratt; add this security group to your existing VM's; make sure that you have also added web and ssh security groups
- assign a floating IP to your bykstack VM
- 




#### VirtualMachine hosts file  
vm-databases (for Database vm)  
vm-bot (for Bot VM)  
vm-trainingbot (for Bot train)  
vm-bykstack (for buerokratt core services)  
These addresses must be inserted into your VM's `/etc/hosts` file accompanied by their respected internal IP  

for example:
 ```
 
ubuntu@client-bykstack:~$ nano /etc/hosts
127.0.0.1 localhost
192.168.11.1	 vm-Bykstack
192.168.11.2	 vm-Databases
192.168.11.3	 vm-Bot 
192.168.11.4   vm-TrainingBot


# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
```
 
