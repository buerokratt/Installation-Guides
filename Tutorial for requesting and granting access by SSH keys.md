### About
#### Tutorial on how to create and add ssh keys to a VM in Riigipilv enviorment  

##### SSH key generating: Linux and MacOSX

##### Create the key
```
cd ~/.ssh
ssh-keygen -t rsa -C "your_email@example.com"
# Check your generated key
cat id_rsa.pub
```
##### Copy the key
In the Riigipilv GUI go to your user's dashboard and select SSH link.
ADD the SSH key into your inventory

##### Open terminal into your VM
You should be asked preferred method of authentication, type "YES"

Connection to your VM using terminal, has been established.
