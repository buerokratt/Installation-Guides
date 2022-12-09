### About  
Here it will be dscribed, how to prepaire BUEROKRATT installation enviorment in your VM's

- [x] In Riigipilv GUI, open your tenant and buis VM's. Follow the Riigipilv FAQ (for VM building) and Requirement.md (specs for VM's requirements)
- [x] DATA disk mounting
- [x] Installation of dependancies (docker, docker-compose, PSQL etc.)
- [x] Docker symlink
- [x] SSH key preparation
- [x] Caddy install

#### VM prearation in Riigipilv GUI


#### DATA disk mounting
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

#### Install `docker` and `docker-compose`  
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
#### Install PSQL (Needed in your `DATABASE` VM)
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

#### SSH preparation

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



#### Install `Caddy`
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
