<p align="center">
  <a href="https://github.com/Justrygh/Final-Project">
  </a>

  <h3 align="center">Enrichment Metadata from DNS over HTTPS Traffic</h3>

  <p align="center">
    Description
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Windows Subsystem for Linux](#how-to-install-windows-subsystem-for-linux)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

About

<!-- GETTING STARTED -->
## Getting Started

#### This project is based on Linux. 
* In order to run the experiment on Windows, You will need to install WSL (Windows Subsystem Linux). 

### How to install Windows Subsystem for Linux
<p>
  If you want to run distros of Linux on Windows 10, you must first enable the Windows Subsystem for Linux feature before you can download and install the flavor of Linux that you want to use.
  </p>

### Enabling Windows Subsystem for Linux using Settings
To install WSL using Setting on Windows 10, use these steps:
1. Open **Settings**.
2. Click on **Apps**.
3. Under the "Related settings" section, click the **Programs and Features** option.
   <img src=https://www.windowscentral.com/sites/wpcentral.com/files/styles/xlarge/public/field/image/2019/12/apps-features-programsfeatures-option.jpg>
4. Click the **Turn Windows features on or off** option from the left pane.
   <img src=https://www.windowscentral.com/sites/wpcentral.com/files/styles/xlarge/public/field/image/2019/12/controlpanel-turn-windows-features-option.jpg>
5. Check the **Windows Subsystem for Linux** option.
   <img src=https://www.windowscentral.com/sites/wpcentral.com/files/styles/xlarge/public/field/image/2019/12/enable-windows-subsystem-linux-windows-10.jpg width="700" height="600">
6. Click the **OK** button.
7. Click the **Restart now** button.

Once you complete the steps, the environment will be configured to download and run the distros of Linux on Windows 10.

### Installing Linux distros using Microsoft Store
To install a distribution of Linux on Windows 10, use these steps:

1. Open **Microsoft Store**.
2. Search for the Linux distribution that you want to install.
   * Ubuntu.
   * Kali Linux.
   * Debian.
3. Select the distro of Linux to install on your device.
   <img src="https://www.windowscentral.com/sites/wpcentral.com/files/styles/xlarge/public/field/image/2019/12/linux-microsoft-store-download.jpg">
4. Click the **Get** (or **Install**) button.
   <img src="https://www.windowscentral.com/sites/wpcentral.com/files/styles/xlarge/public/field/image/2019/12/install-ubuntu-microsoftstore.jpg">
5. Click the **Launch** button.
6. Create a username for the Linux distro and press **Enter**.
7. Specify a password for the distro and press **Enter**.
   <img src="https://www.windowscentral.com/sites/wpcentral.com/files/styles/xlarge/public/field/image/2019/12/setup-ubuntu-wsl-windows10.jpg">
8. Repeat the password and press **Enter** to confirm.

After you complete the steps, you can start using the distro as any other flavor of Linux (without the graphical user interface, of course).



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
Lastly, you will need to install the pip packages listed in src/requirements.txt with the following command:

```
pip3 install -r requirements.txt
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
