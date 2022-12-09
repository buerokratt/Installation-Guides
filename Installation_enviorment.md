### About  
Here it will be dscribed, how to prepaire BUEROKRATT installation enviorment in your VM's

- [x] Initial VM preparation
- [x] DATA disk mounting
- [x] Installation of dependancies (docker, docker-compose, PSQL etc.)
- [x] Docker symlink
- [x] SSH key preparation
- [x] Caddy install

##### Initial VM preparation
In Riigipilv GUI, under your tenant's security group management, make sure to allow following ports:
```
    8081 Dmapper
    3000 Chat-widget
    3001 Customer-service
    8082 Resql
    8085 TIM
    8443 Private ruuter
    8080 Public ruuter
```
In terminal to access your VM use following command
```
ssh ubuntu@externalIP
```
After accessing VM in terminal, configure `/etc/hosts` to enable traix between VM's (you have to do it inside every VM you have created.

```
sudo nano /etc/hosts
```
Copy the following lines into the `hosts` file, make sure to change IP's according to what they are in your infrastructure
```
127.0.0.1 localhost
192.168.11.1	 vm-Bykstack
192.168.11.2	 vm-Databases
192.168.11.3	 vm-Bot 
192.168.11.4   vm-TrainingBot
```

##### DATA disk mounting
Check your drives/disks  

```
sudo fdisk -l
```

Create disk, label it, add it to `fstab` and mount
```
sudo parted /dev/vdb
```
```
mklabel gpt
```
```
quit
```
```
sudo mkfs.ext4 /dev/vdb
```
```
sudo nano /etc/fstab
```
```
/dev/vdb    /opt    ext4      defaults        0             0
```
```
sudo mount -a | grep vdb
```

##### Install `docker` and `docker-compose`  
Install docker

```
sudo apt update
```
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
If you are using later version of Ubuntu (22.04 or later) replace `focal` with `jammy`
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```
```
sudo apt install docker-ce
```
```
sudo systemctl status docker
```
Install docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
```
docker-compose --version
```
Version output should be similar to this `docker-compose version 1.29.2, build 5becea4c`

Add user to docker group
```
sudo usermod -aG docker ${USER}
```
##### Install PSQL (Needed in your `DATABASE` VM)
```
sudo apt install postgresql-client-common && sudo apt-get install postgresql-client
```

#### Move docker to `data` disk
```
cd /opt/
```
```
cd /var/lib/
```
```
sudo mv -r docker/ /opt/docker
```
```
sudo ln -s /opt/docker
```

##### SSH preparation

##### Create the key
```
cd ~/.ssh
```
```
ssh-keygen -t rsa -m PEM
```
Check your generated key
```
cat id_rsa.pub
```
Copy the public key into your VM's that need's to be accessed target file - `/home/ubuntu/.ssh/authorized_keys`



##### Install `Caddy`
```
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
```
```
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
```
```
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
```
```
sudo apt update
```
```
sudo apt install caddy
```
#### How to copy files from one VM to another
```
scp /path/to/file.name vm-name:/path/to/folder/
```
