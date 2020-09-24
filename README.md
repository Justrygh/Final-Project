<p align="center">
  <a href="https://github.com/Justrygh/Final-Project">
  </a>

  <h3 align="center">Enrichment Metadata from DNS over HTTPS Traffic</h3>

  <p align="center">
    Classify encrypted traffic by separating WEB and DNS queries over the HTTPS session (port 443), moreover extract as much information as possible. E.g: GET/POST method.
  Therefore, our research suggests improving the end-user security, by trying to filter the malicious domain that queried from the Internet Service Provider server using Machine Learning .

  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Background](#background)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

### Background


<!-- GETTING STARTED -->
## Getting Started

**This project is based on Linux.** 
* In order to run the experiment on Windows, You will need to install WSL (Windows Subsystem Linux). 


### Prerequisites 
Our code was built to run on Linux & Windows. To build the DNS response time measurement tool, You will need to install the following dependencies:
```
libgetdns10
libgetdns-dev
libcurl4-openssl-dev
libssl-dev
libev4, libev-dev
libevent-2.1-7, libevent-core-2.1-7, libevent-openssl-2.1-7, libevent-dev
libuv1
```

To measure page loads, parse the resulting HARs, and insert the HARs into a PostgreSQL database, you will need to install the following dependencies:
```
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
Lastly, you will need to install the pip packages listed in dependencies/requirements.txt with the following command:

```
pip3 install -r requirements.txt
```

For your convenience, you can install **all** the dependencies mentioned above by running **setup.sh** in dependencies with the following command:

```
bash setup.sh
```

### Installation

Once you've installed the dependencies listed above, you need to do a few more things before you can start some measurements:

* Create a PostgreSQL database and user that has write access to the database

* Modify the src/code/database/postgres.ini file to contain your PostgreSQL credentials. For the har_table field, choose the name of the table that you want to store HARs for page load times. For the dns_table field, choose the name of the table that you want to store DNS response times.

* Run the following script to initialize the tables in your database that will store HARs and DNS response times:

```
python3 database.py postgres.ini
```

* Run ```make``` in src/code/dns-timing to create the DNS response time measurement tool


<!-- USAGE EXAMPLES -->
## Usage
Usage

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch 
3. Commit your Changes 
4. Push to the Branch 
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Justrygh/Final-Project](https://github.com/Justrygh/Final-Project)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [https://github.com/noise-lab/dns-measurement-suite](https://github.com/noise-lab/dns-measurement-suite)
* []()
* []()
