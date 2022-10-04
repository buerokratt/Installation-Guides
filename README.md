### About
This document covers installation guides for all of Bürokratt's services.


### Intended target
The intended target of this document is an IT-personnel familiar with [Ubuntu](https://ubuntu.com/), [Linux command line](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview), [Git](https://git-scm.com/) and [Docker](https://www.docker.com/).


### Limitations of this document
This document covers the installation of Bürokratt on [Ubuntu](https://ubuntu.com/) and by using [Linux Terminal](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview).


### Glossary
`Bykstack` - core components of Bürokratt that are essential for services to work

`Backoffice GUI` - graphical user interface as an administrative tool

`Chat Widget` - graphical user interface for End Users to chat via text messages

`Bot` - automated chatbot, responds to End Users without human interference

`Training-bot` - the same as `Bot` but is used only for training purposes

`Terminal` - [Linux command line tool](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview)


### Prerequisites

#### Approximate resource requirements
- `Bykstack` and `Backoffice GUI` total of ~10GB RAM and 7CPU
- `Bot` ~3GB RAM and 4CPU
- `Training-bot` ~3GB RAM and 4CPU

Docker and docker-compose installation:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

#### Docker must be installed
> At least version `20.10.17`
```
docker -v
```

```
Docker version 1.29.2 build 5becea4c
```

#### Docker Compose must be installed
> At least version `2.6.1`
```
docker-compose -v
```

```
Docker Compose version v2.6.1
```


### Installation

#### Prerequisites
- [x] Create a directory on you personal computer or virtual server where to download Bürokratt's source code
- [x] Move to this directory
- [x] While being in this directory, open Terminal
- [x] Clone the source code of Bürokratt
```
git clone https://github.com/buerokratt/Installation-Guides.git
```
- [x] Move to a directory called `Installation-Guides`
```
cd Installation-Guides
```
- [x] Make sure there is a folder called `default-setup`
```
ls | grep default-setup
```

```
default-setup
```

#### Setting up Bykstack and Backoffice GUI

> Continue in folder `Installation-GUides` by using Terminal 

- [x] Move to folder `default-setup`
```
cd default-setup
```
- [x] Make sure there is a folder called `backoffice-and-bykstack`
```
ls | grep backoffice-and-bykstack
```

```
backoffice-and-bykstack
```

- [x] Move to folder `backoffice-and-bykstack`
```
cd backoffice-and-bykstack
```

- [x] Use Docker Compose to set everything up
```
sudo docker-compose up -d
```

- [x] Check if appropriate Docker containers were created
```
sudo docker ps -a | grep byk-
```

```
345045515b2c   riaee/byk-tim:07                      "catalina.sh run"        Up 2 minutes                     8080/tcp, 0.0.0.0:8085->8443/tcp, :::8085->8443/tcp                                     byk-tim
06d0a1e5db93   riaee/byk-chatbot-public-ruuter:03    "catalina.sh run"        Up 2 minutes                     8080/tcp, 0.0.0.0:8080->8443/tcp, :::8080->8443/tcp                                     byk-public-ruuter
4d456da8f574   riaee/byk-dmapper:10                  "catalina.sh run"        Up 2 minutes                     8080/tcp, 0.0.0.0:8081->8443/tcp, :::8081->8443/tcp                                     byk-dmapper
a44d482ae918   riaee/byk-customer-service:17         "/docker-entrypoint.…"   Up 2 minutes                     80/tcp, 0.0.0.0:3001->443/tcp, :::3001->443/tcp                                         byk-customer-service
e1272ee93df0   riaee/byk-chatbot-private-ruuter:03   "catalina.sh run"        Up 2 minutes                     8080/tcp, 0.0.0.0:8443->8443/tcp, :::8443->8443/tcp                                     byk-private-ruuter
d9a02b7de5f4   riaee/byk-chat-widget:14              "/docker-entrypoint.…"   Up 2 minutes                     80/tcp, 0.0.0.0:3000->443/tcp, :::3000->443/tcp                                         byk-widget
1388f20c5613   riaee/byk-resql:11                    "catalina.sh run"        Up 2 minutes                     8080/tcp, 0.0.0.0:8082->8443/tcp, :::8082->8443/tcp                                     byk-resql
bc0dd35d3451   riaee/byk:monitoring-20220802         "/docker-entrypoint.…"   Up 2 minutes                     443/tcp, 0.0.0.0:81->80/tcp, :::81->80/tcp, 0.0.0.0:8444->8443/tcp, :::8444->8443/tcp   byk-monitor
```

- [x] Open Backoffice GUI in browser
Open `https://localhost:3001/` in your browser of choice. You should see Bürokratt's Backoffice GUI.
