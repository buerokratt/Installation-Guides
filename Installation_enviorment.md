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
Add user to docker group
```
sudo usermod -aG docker ${USER}
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
ssh-keygen -t rsa -m PEM "your_email@example.com"
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
