import os
import subprocess

create_cert = """openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3980 \
            -nodes \
            -out cert.crt \
            -keyout key.key \
            -subj "/C=oo/ST=Create/L=your/O=certs/OU=lazy IT Department/CN=default.value"   """

give_ownership = """
sudo chown 999:999 cert.crt 
sudo chmod 0600 cert.crt 
 https://stackoverflow.com/questions/55072221/deploying-postgresql-docker-with-ssl-certificate-and-key-with-volumes """

directories = ["users-db", "tim-db"]
 
for directory in directories:
    os.chdir(directory)
    subprocess.check_output(create_cert, shell=True, executable='/bin/bash')
    #give_ownership
    os.chdir("..")
