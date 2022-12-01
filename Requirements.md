### About
#### Here is listed the requirements for buerokratt when depolying it

Database VitualMachine (VM that runs postgres databases)
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
#### VirtualMachine names for ssh traffic  
vm-databases (for Database vm)  
vm-bot (for Bot VM)  
vm-trainingbot (for Bot train)  
vm-bykstack (for buerokratt core services)  
These addresses must be inserted into your VM's `/etc/hosts` file accompanied by their respected internal IP  


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
