<p align="center">
  <a href="https://git.vanenter.nl/bkrflo/NAS_docker-compose">
    <img src="https://git.vanenter.nl/repo-avatars/1-b3c2388c15b628a3faf3b2ea5a1dceb5" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">NAS docker-compose</h3>

  <p align="center">
    My working repository of docker-compose on the Synology NAS. https://stolp.liefdelaan.nl
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#traefik">Traefik</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- About the project -->
## About the project

Finally I started to work with docker on the synology. At first it did not work because I bound myself to the GUI side of docker provided by the DSM of Synology. When I started to play with the terminal I in the end got it. Before I was just clicking and now with typing the commands I really needed to understand what I did. To save it all I built myself this repo so I can look back at old settings and code.

### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Docker](https://www.docker.com)
* [Docker-compose](https://docs.docker.com/compose/)
* [Docker hub](https://hub.docker.com)


<!-- GETTING STARTED -->
## Getting Started

To use this repository, please install docker, docker-compose, put the files from this repository in a folder, create a .env file for each sub-folder and than run docker-compose for apps and servers. Please be aware that you uncomment the following line during testing so you do not exceed the rate limit of Letsencrypt.
```sh
  - --certificatesResolvers.myresolver.acme.caServer=https://acme-staging-v02.api.letsencrypt.org/directory
```
### Prerequisites

This is an overview of how to install the prerequisites for this project. Please be aware that it is written for the Synology Os and that you need to  things you need to use the software and how to install them.
#### docker
Install docker via the GUI.
1. Open the NAS DSM
2. Open Package Center
3. Search docker and install the package
4. You can copy this repo anywhere on the nas

_For more information, please refer to the [Synology Docker Installation Docs](https://www.synology.com/en-us/dsm/feature/docker)_

#### docker-compose
1. Move old docker-compose version to back-up file.
   ```sh
   sudo su
   cd /var/packages/Docker/target/usr/bin/
   mv docker-compose docker-compose_bak
   ```
2. Download the latest docker-compose
   ```sh
   curl -L https://github.com/docker/compose/releases/download/X.XX.X/docker-compose-`uname -s`-`uname -m` -o docker-compose
   ```
Be sure to replace the X.XX.X with the [latest docker compose release number from here](https://github.com/docker/compose/releases) (1.28.2 at this time).

3. Make sure docker-compose is executable
```sh
chmod +x docker-compose
```
_For more information, please refer to the [Docker-Compose Installation Docs](https://docs.docker.com/compose/install/)_

### Installation

All the commando's are ran as if you start from the root of the project.

1. Clone the repo
   ```sh
   git clone https://git.vanenter.nl/bkrflo/NAS_docker-compose.git
   ```
2. Create missing folders for all the docker services in the docker-compose files.
    a. apps/*
    b. servers/*
3. Make sure the let's encrypt request is in staging mode, check servers/docker-compose.yml, search for:
    ```sh
      - --certificatesResolvers.myresolver.acme.caServer=https://acme-staging-v02.api.letsencrypt.org/directory 
    ```
4. Copy archive/apps.example.env to apps/.env and fill in the necessary values
5. Copy archive/servers.example.env to servers/.env and fill in the necessary values
   ```sh
     cp ./archive/apps.example.env ./apps/.env
     cp ./archive/servers.example.env ./servers/.env
     nano ./apps/.env
     nano ./servers/.env
   ```
   You can find the PUID and GUID by entering:
   ```sh
   id [USER]
   ```
   Where [USER] is the username under which all the processes need to run (an admin)
6. Install necessary networks. We have: 
    a. frontend which is direct connected to the internet
    b. backend which is connected for backend purposes (frontend server to backend mysql server)
    c. appnet which is completely different, not connected to any other network.
   I choose for a 172.20.0.0/16 network divided in 24 bit networks. You can choose whatever works. 
   ```sh
   docker network create --driver=bridge --subnet=172.20.99.0/24 --gateway=172.20.99.1 --attachable frontend
   docker network create --driver=bridge --subnet=172.20.10.0/24 --gateway=172.20.99.1 --attachable backend
   docker network create --driver=bridge --subnet=172.20.20.0/24 --gateway=172.20.99.1 --attachable appnet
   ```
7. Run docker-compose
   ```sh
   cd ./apps
   docker-compose up -d
   cd ../servers
   docker-compose up -d
   ```
8. Restart traefik container
   ```sh
   docker restart traefik
   ```
9. Test if all the front facing docker containers have the correct fake certificates.
10. If succesfull remove the acme.json file in the letsencrypt folder
    ```sh
    rm ./servers/traefik/letsencrypt/acme.json
    ```
11. comment the line with:
    ```sh
      - --certificatesResolvers.myresolver.acme.caServer=https://acme-staging-v02.api.letsencrypt.org/directory
    ```
12. Recreate Traefik
    ```sh
    docker rm traefik --force
    cd ./servers
    docker-compose up -d
    ```
13. After creation of Troefik reboot traefik container for the last time.
    ```sh
    docker restart traefik
    ```
14. Back acme.json file with all the current certificates.
    ```sh
    cp ./servers/traefik/letsencrypt/acme.json ./servers/traefik/letsencrypt/acme.backup.json
    ```

<!-- USAGE EXAMPLES -->
## Usage

#### Changes
If you change anything in the docker-compose file you can apply the changes by running the docker-compose command again.
```sh
cd ./servers
docker-compose up -d
cd ../apps
docker-compose up -d
```
#### Updates
To update the containers I am not running an extra service. Every week I run the following command to pull the latest image:
```sh
cd ./servers
docker-compose pull
cd ../apps
docker-compose pull
```
And I apply the new image by re-running docker-compose.
```sh
cd ./servers
docker-compose up -d
cd ../apps
docker-compose up -d
```
Rollback is easy because the old image remain in docker. If you want to cleanup these unused images you can run:
```sh
docker image prune --all
```

_For more examples and ideas, please refer to the [Docker Documentation](https://docs.docker.com)_



<!-- TRAEFIK -->
## Traefik

In our project we use Traefik as a reverse proxy. You can also use the built-in reverse proxy of Synology but the containerized Traefik provides some extra futures. It is portable like docker intended and you can use docker to have some settings applied by docker itself.

### Overview
I forward the ports 80, 443, 22 from my external ip-address to the synology NAS on the router. And these ports are received by Traefik. Depending on the domain name the traffic is routed to specific containers. 

To prevent unauthorized access some routes are blocked (see red block in image) by Authelia. All these routes are first routed to authelia to authenicate the user. If the user is authenticated, the traffic is rerouted to the container. If there is no valid authentication the traffic stops at authelia.

Traefik can be configured by using Docker or via files. I have used both. The NAS DSM and Home Assistant (HA) is not in docker, so it is routed by file-configuration.

<img src="https://entermi.nl/wp-content/uploads/2021/02/IMG_0084.jpg">

_For an explanation of the Traefik architecture, please read this [Traefik Concepts](https://doc.traefik.io/traefik/getting-started/concepts/)_

### Docker configuration
You can configure Traefik and it's rules via labels on the docker container in the docker-compose file. Here you configure each container as a 'client' of the Traefik container. The Traefik container can be a 'client' of itself. The settings below are already set in the docker-compose files. For better understanding I will highlight a few.
#### Traefik container
With the labels you configure the other containers. Some main settings need to be entered directly in Traefik via commands. Like which entrypoints does Traefik need to listen to. These are defined for html as follows:
--entrypoint.[NAME ENTRYPOINT].address=[IP (optional)]:[PORT]
So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)

```sh
    - --entryPoints.web.address=:80
    - --entryPoints.websecure.address=:443
```
_For more information about entrypoints, please read this [Traefik Entrypoints]https://doc.traefik.io/traefik/routing/entrypoints/)_

Another important setting is allowing docker & file configuration.
```sh
    - --providers.docker=true
    - --providers.file.directory=/rules
```
This enables the providers docker & file and defines where the files can be found.

_For more information about providers, please read this [Traefik Providers Docker](https://doc.traefik.io/traefik/routing/providers/docker/)_

#### All 'client' containers
Configure a router for the container, define which entrypoint is needed:
traefik.http.routers.[ROUTER_NAME].entrypoints=[ENTRYPOINT_NAME]

So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
```sh
    - traefik.http.routers.sonarr-rtr.entrypoints=web
```

Specify a domain to listen to filter the traffic on:
traefik.http.routers.[ROUTER_NAME].rule=HostHeader(`[EXTERNAL_DOMAIN_OF_APP]`)

So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
```sh
    - traefik.http.routers.sonarr-rtrs.rule=HostHeader(`$URL_SONARR`)
```

Define the service name, which is the docker service name if you use the docker provider.
traefik.http.routers.[ROUTER_NAME].service=[DOCKER_SERVICE_NAME]

So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
```sh
    - traefik.http.routers.stolpweb-rtrs.service=stolpweb
```

### Let's Encrypt & SSL
All websites need to be secured by an certificate. if you do not the browsers will issue a security warning. Traefik is able to communicate with let's encrypt. This way it requests and renews certificates for your services. To enable this you need to do a few things.

#### As a Traefik command
1. Define a certificate resolver and method. Here we use a http challenger.
    --certificatesResolvers.[RESOLVER_NAME].acme.httpChallenge=true

    So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)

    ```sh
        - --certificatesResolvers.myresolver.acme.httpChallenge=true
    ```

2. Make sure we use a staging server of Let's Encrypt to perform all the requests as a test.

    So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
    ```sh
        - --certificatesResolvers.myresolver.acme.caServer=https://acme-staging-v02.api.letsencrypt.org/directory
    ```

3. Specify which entrypoint needs to be used for the http challenge. We use the entrypoints, port 80, named web.
    --certificatesResolvers.[RESOLVER_NAME].acme.httpChallenge.entryPoint=web

    So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
    ```sh
        - --certificatesResolvers.myresolver.acme.httpChallenge.entryPoint=[ENTRYPOINT_NAME]
    ```

4. Specify e-mail address. Not obligatory, but it is nice to provide to a free service. It can contact you and sends a heads-up when your certificates are close to expiring.
    --certificatesResolvers.myresolver.acme.email=[EMAIL_ADDRESS]

    So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
    ```sh
        - --certificatesResolvers.[RESOLVER_NAME].acme.email=floris@vanenter.nl
    ```

5. The certificates needs to be saved somewhere. We choose to save it in a json file. This file will be used every time you spin up a container.

    So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
    ```sh
        - --certificatesResolvers.myresolver.acme.storage=/letsencrypt/acme.json
    ```

#### As a Docker label on a container
1. Define the domain where the certificate needs to be requested for. It can retrieve it from the router-rules, but I want to be sure it is correct. Since I use a variable, it is not double administration.
    * traefik.http.routers.[ROUTER_NAME].tls.domains[0].main=[EXTERNAL_DOMAIN_OF_APP]
    * traefik.http.routers.[ROUTER_NAME].tls=true
    * traefik.http.routers.[ROUTER_NAME].tls.certresolver=[RESOLVER_NAME]

    So you can find it in [servers/docker-compose](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/servers/docker-compose.yml)
    ```sh
        - traefik.http.routers.stolpweb-rtrs.tls.domains[0].main=$URL_STOLPWEB
        - traefik.http.routers.stolpweb-rtrs.tls=true
        - traefik.http.routers.stolpweb-rtrs.tls.certresolver=myresolver
    ```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the Creative Commons License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Floris van Enter - [EnterMI](https://entermi.nl) - floris@entermi.nl

Project Link: [https://github.com/beakerflo/nas_synology_docker-compose](https://github.com/beakerflo/nas_synology_docker-compose)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Readme page](https://github.com/beakerflo/nas_synology_docker-compose/blob/master/README.md)
* [Synology Docker Media Server with Traefik, Docker Compose, and Cloudflare](https://www.smarthomebeginner.com/synology-docker-media-server/)
