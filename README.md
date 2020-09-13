<p align="center">
  <a href="https://github.com/Justrygh/Final-Project">
  </a>

  <h3 align="center">Enrichment Metadata from DNS over HTTPS Traffic</h3>

  <p align="center">
    Description
    <br />
    <a href="https://github.com/Justrygh/Final-Project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Justrygh/Final-Project">View Demo</a>
    ·
    <a href="https://github.com/Justrygh/Final-Project/issues">Report Bug</a>
    ·
    <a href="https://github.com/Justrygh/Final-Project/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
Our code was built to run on Linux & Windows. To build the DNS response time measurement tool, You will need to install the following dependencies:
```sh
libgetdns10
libgetdns-dev
libcurl4-openssl-dev
libssl-dev
libev4, libev-dev
libevent-2.1-7, libevent-core-2.1-7, libevent-openssl-2.1-7, libevent-dev
libuv1
```

To measure page loads, parse the resulting HARs, and insert the HARs into a PostgreSQL database, you will need to install the following dependencies:
```sh
python3, python3-pip, python3-dev
postgresql, postgresql-client
dnsutils
net-tools
autoconf
automake
build-essential
libtool
default-jdk
```
Lastly, you will need to install the pip packages listed in src/requirements.txt with the following command:

pip3 install -r requirements.txt

### Installation

1. Clone the repo
```sh
git clone https://github.com/Justrygh/Final-Project.git
```
2. Once you've installed the dependencies listed above, you need to do a few more things before you can start some measurements:

* Create a PostgreSQL database and user that has write access to the database

* Modify the data/postgres.ini file to contain your PostgreSQL credentials. For the har_table field, choose the name of the table that you want to store HARs for page load times. For the dns_table field, choose the name of the table that you want to store DNS response times.

* Run the following script to initialize the tables in your database that will store HARs and DNS response times:

* python3 database.py postgres.ini

* Run make in src/code/dns-timing to create the DNS response time measurement tool



<!-- USAGE EXAMPLES -->
## Usage



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Justrygh/Final-Project/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch 
3. Commit your Changes 
4. Push to the Branch 
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Justrygh/Final-Project](https://github.com/Justrygh/Final-Project)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=flat-square
[contributors-url]: https://github.com/Justrygh/Final-Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Justrygh/Final-Project.svg?style=flat-square
[forks-url]: https://github.com/Justrygh/Final-Project/network/members
[stars-shield]: https://img.shields.io/github/stars/Justrygh/Final-Project.svg?style=flat-square
[stars-url]: https://github.com/Justrygh/Final-Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/Justrygh/Final-Project.svg?style=flat-square
[issues-url]: https://github.com/Justrygh/Final-Project/issues
[license-shield]: https://img.shields.io/github/license/Justrygh/Final-Project.svg?style=flat-square
[license-url]: https://github.com/Justrygh/Final-Project/blob/master/LICENSE.txt
