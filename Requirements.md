### About
#### Here is listed the requirements for buerokratt and how to build your infrastructure in Riigipilv (RPLV)

Database VirtualMachine (VM that runs postgres databases)
```
2vCPU, 4GB RAM, min 10-15GB SSD/HDD
```
BOT VirtualMachine (VM that runs bot)
```
4vCPU, 4GB RAM, min 10-15 GB SSD/HDD
```
BOT-TRAIN VirtualMachine (VM that runs bot train)
```
4vCPU, 4-8GB RAM, min 10-15GB SSD/HDD
```
BYKSTACK VirtualMachine (VM that runs buerokratt core services)
```
4-8vCPU, 8-10GB RAM, min 5-10 SSD/HDD
```
### Note
Remember to add extra 8 - 10GB SSD/HDD for every VM's system disk.
#### Cooke Domain requirement
Cookie domain level must match between the client domain and domain where buerokratt is installed
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

### RPLV infrastructure building for buerokratt
After ordering the VM's in RPLV follow these steps in RPLV  
- build the required VM's using the correct flavors (this automatically adds the required vcpu, ssd/hdd, ram) and choose Ubuntu 20.04 as OS (make sure to add extra ssh keys if necessary (alternatively you can add them under .ssh/authorized_keys)
- add new networking security group to open required ports for buerokratt; add this security group to your existing VM's; make sure that you have also added web and ssh security groups
- assign a floating IP to your bykstack VM
