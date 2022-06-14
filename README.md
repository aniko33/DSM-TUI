<h1 align="center">DSM-TUI Documentation</h1>
<img src="https://user-images.githubusercontent.com/76649588/173510635-e12cfbea-890f-4862-a9c3-2065d11edff6.png">
<div align="center">

[](#)
[](https://github.com/aniko33/DSM-TUI/releases)
[](#)

</div>

### Description

**DSM-TUI** (***Decks Server Manager TUI***) is a **tool** that allows **server 
management** by viewing active services and server status. It is developed
in **Python** with **TUI** (***Terminal User Inteface***)

### Index

- [Compatibility](https://github.com/aniko33/DSM-TUI/blob/main/README.md#compatibility)
  
  - [Platforms](https://github.com/aniko33/DSM-TUI/blob/main/README.md#platforms)
    
  - [Python version](https://github.com/aniko33/DSM-TUI/blob/main/README.md#python-version)
    
- [Download](https://github.com/aniko33/DSM-TUI/blob/main/README.md#download)
  
  - [From source](https://github.com/aniko33/DSM-TUI/blob/main/README.md#from-source)
    
  - [From portable file](https://github.com/aniko33/DSM-TUI/blob/main/README.md#from-portable-file)
    
- [Usage](https://github.com/aniko33/DSM-TUI/blob/main/README.md#usage)
  
- [Notes](https://github.com/aniko33/DSM-TUI/blob/main/README.md#notes)
  
  - [For users](https://github.com/aniko33/DSM-TUI/blob/main/README.md#for-users)
    
  - [For Developers](https://github.com/aniko33/DSM-TUI/blob/main/README.md#for-developers)
    
- [Screenshot](https://github.com/aniko33/DSM-TUI/blob/main/README.md#screenshot)
  
- [Code](https://github.com/aniko33/DSM-TUI/blob/main/README.md#source-code)
  
- [Contributors](https://github.com/aniko33/DSM-TUI/blob/main/README.md#Contributors)
  

## Compatibility

### Platforms

##### Available platform: Linux and Windows.

We made ***Windows compatible*** and ***something in beta could not work***

### Python version

##### it is recommended to use Python with version "*3*" or higher

because of the libraries it is better to ***keep version 3*** or **higher** or the **application may not work**.

## Download

### From source

**Downloading the app from source** could be both a **bad idea** and a **good idea**, the *app could not go because of the **outdated libraries** or the **outdated program** =D*, instead it could be ***useful in case of problems in the code*** or even just to change it.

##### How download from source

###### Linux

```bash
#copy of the repository
git clone https://github.com/aniko33/DSM-TUI.git
#open folder
cd DSM-TUI
#install req...
pip install -r req.txt
#creating the startup file on /bin
chmod +x dsm && sudo mv dsm /bin
echo now you can start DSM with the command: dsm
```

###### Windows

```batch
curl https://github.com/aniko33/DSM-TUI/blob/main/dsm-windows.py --output bsm.py && echo now you can start DSM with the command: python dsm.py 
```

### From portable file

**Downloading from a compiled** file ***could be useful in case the libraries are of poor quality*** or ***just because python no longer allows use***.
The compiled file was compiled with **Pyinstaller**.

##### How download from portable file (only Linux)

```bash
wget https://github.com/aniko33/DSM-TUI/releases/download/v1.0-beta/dsm && chmod +x dsm && sudo mv dsm /bin && echo now you can start DSM with the command: dsm
```

## Usage

Using this tool is very easy just ***run the command***: **on *Linux*** `dsm` **on *Windows***: `python dsm.py`
and an ***interface with various functions*** will be given.

## Notes

### For users

This app ***needs to be connected to an <u>internet network</u>*** and must be able to ***connect to google.com or, in case, change the link***.

### For developers

there is ***no guide on reading the code and using it***, perhaps in the ***next versions there will be a documentation for developers***

# Screenshot

![image](https://user-images.githubusercontent.com/76649588/173388846-7d874fad-008e-4005-abb3-379deccce3c9.png)
![image](https://user-images.githubusercontent.com/76649588/173388920-46ef8cde-72d1-4fa7-bc89-9a6249d458fc.png)

## Source code

#### work in progress

![carbon](https://user-images.githubusercontent.com/76649588/173517936-ba6224a7-437f-47fd-8b29-b353fadb32b7.png)

## Contributors

<a href="https://github.com/aniko33/DMS-TUI/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=aniko33/DMS-TUI" />
</a>
