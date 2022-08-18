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

give_ownership = """ https://stackoverflow.com/questions/55072221/deploying-postgresql-docker-with-ssl-certificate-and-key-with-volumes """

directories = ["customer-support", "ruuter", "dmapper", "chat-widget", "tim", "resql"]
dbDirectories = ["users-db", "tim-db"]
 
for directory in directories:
    os.chdir(directory)
    subprocess.check_output(create_cert, shell=True, executable='/bin/bash')
    os.chdir("..")

for dir in dbDirectories:
    os.chdir(directory)
    subprocess.check_output(create_cert, shell=True, executable='/bin/bash')
    subprocess.check_output(give_ownership)
    os.chdir("..")