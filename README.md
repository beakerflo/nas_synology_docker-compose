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
    <li><a href="#roadmap">Roadmap</a></li>
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
Be sure to replace the X.XX.X with the latest docker compose release number from here (1.26.2 at this time).

3. Make sure docker-compose is executable
```sh
chmod +x docker-compose
```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
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

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues).



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

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Readme page](https://github.com/othneildrew/Best-README-Template)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png