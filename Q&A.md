#### About
##### Here are listed issues we have witnesed during installation and how to solve them

###### Issue 
Library "TEEMAD" does not load.
Description - After logging in as admin into backoffice GUI, the library "TEEMAD" will not load and you can see the loading circle non-stop.
Cause - It is caused by non-functioning ssh private key. When using `kygen` command you create a key in OPENSH format, that java does not undersand.
        Looking at `private-ruuter` logs, you should see following example lines: 
        ``` Caused by: com.jcraft.jsch.JSchException: invalid privatekey: [B@67ca1612 ```
        and
        ``` Unable to call function getBlacklistedIntents
            java.lang.reflect.InvocationTargetException: null ```
        This is caused by your RSA SSH key wrong format. When using `keygen` the defalt format is OPENSSH but it should be RSA
Solution - After you have created your SSH private key, use the command 
        ```ssh-keygen -p -f /home/ubuntu/.ssh/id_rsa -m pem ```
        This ill change your key into RSA format.

