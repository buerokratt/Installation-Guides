### Dokumendi eesmärk
Siin on kirjeldatud buerokratti infrastruktuuri nõuded Riipilves (edasipidi RPLV).

Database VM (virtuaal masin mille eesmärgiks on jooksutada postgres andmebaase)
```
2vCPU, 4GB RAM, min 10-15GB SSD/HDD
```
BOT VM (virtuaal masin mille eesmärgiks on jooksutada BOT keskkonda)
```
4vCPU, 4GB RAM, min 10-15 GB SSD/HDD
```
BOT-TRAIN VM (virtuaal masin mille eesmärgiks on jooksutada treenimis keskkonda)
```
4vCPU, 4-8GB RAM, min 10-15GB SSD/HDD
```
BYKSTACK VM (virtuaal masin mille eesmärgiks on jooksutada buerokratti põhiteenuseid)
```
4-8vCPU, 8-10GB RAM, min 5-10 SSD/HDD
```
### Note
Luues RPLV keskkonda, jäta meelde, et lisad iga masina kohta 8-10GB SSD/HDD süsteemi ketta (millel OS) jaoks.

#### URL kirjeldused
Toodangu keskkond  
Customer-service - admin.buerokratt.YOURDOMAIN.ee  
TIM - tim.buerokratt.YOURDOMAIN.ee  
Public ruuter - ruuter.buerokratt.YOURDOMAIN.ee   
Private ruuter - priv-ruuter.buerokratt.YOURDOMAIN.ee  
Chat widget - buerokratt.YOURDOMAIN.ee  
Monitoring - seire.buerokratt.YOURDOMAIN.ee  
Analytics - analyytika.buerokratt.YOURDOMAIN.ee  


Test keskkond  
Customer-service - admin.test.buerokratt.YOURDOMAIN.ee  
TIM - tim.test.buerokratt.YOURDOMAIN.ee  
Public ruuter - ruuter.test.buerokratt.YOURDOMAIN.ee  
Private ruuter - priv-ruuter.test.buerokratt.YOURDOMAIN.ee  
Chat widget - buerokratt.test.YOURDOMAIN.ee  
Monitoring - seire.test.buerokratt.YOURDOMAIN.ee  
Analytics - analyytika.test.buerokratt.YOURDOMAIN.ee 

### RPLV infrastruktuuri ehitus
Peale lepingu sõlmimist ning privaatpilve tellimust, järgi alljärgnevaid samme:
- Määra projekti pilves koguarvn CPU'd, SSD/HDD ning RAM (sellest hakkad hiljem VM'idele resursse küsima)
- Ehita VM'id (OS Ubuntu 20.04 või sarnane
- Määra turvagruppidele pordid kus liiklus peab olema avatud (lisa need näiteks `web` nimelisele turvagrupile) 
- Määra `floating` IP oma bykstack VM'ile
