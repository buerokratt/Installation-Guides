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

#### Docker must be installed
> At least version `20.10.17`
```
user@ubuntu:~$ docker -v
Docker version 20.10.17, build 100c701
```

#### Docker Compose must be installed
> At least version `2.6.1`
```
user@ubuntu:~$ docker-compose -v
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
user@ubuntu:~$ ls | grep default-setup
```

```
default-setup
```

#### Setting up Bykstack and Backoffice GUI
> Continue in Terminal

- [x] Make sure you are in a folder called `Installation-GUides`
```
user@ubuntu:~$ pwd
/home/Installation-Guides
```
- [x] Move to folder `default-setup`
- [x] Make sure there is a folder called `default-setup`
```
user@ubuntu:~$ ls | grep bykstack-with-backoffice-gui
```

```
bykstack-with-backoffice-gui
```
- [x] Move to folder `bykstack-with-backoffice-gui`
```
user@ubuntu:~$ cd bykstack-with-backoffice-gui
```
- [x] Use Docker Compose to set everything up
