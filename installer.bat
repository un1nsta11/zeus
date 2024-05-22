@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem SPIDER INSTALLER
@Rem VERSION 1.0.8524
@Rem CREATED 08 MAY 2024
@Rem AUTHOR UN1NSTA11
@Rem ACTIONS REQUIRED: SET TOKEN, SET ID
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Echo Off
SetLocal EnableDelayedExpansion

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem VARIABLES
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Set Token="NA"
Set Id="NA"

Set InstallerDir="C:\spider\"
Set LocalRepo="C:\spider\spider"
Set Application="C:\spider\spider\app.py"
Set UpdaterDir="C:\spider\updater\"
Set UpdaterPath="C:\spider\updater\updater.bat"
Set UpdaterPayload="@echo off && taskkill /F /IM python.exe && cd C:\spider\spider && git pull && git checkout main && git pull && python C:\spider\spider\app.py"

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem CHECK PERMISSIONS
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Echo %Date% %Time% [INFO ] Spyder installer started
Echo %Date% %Time% [INFO ] Checking for permissions
MkDir "%windir%\system32\test" 2>nul
If '%ErrorLevel%' == '0' (
    Echo %Date% %Time% [INFO ] Running as administrator: continue.
    RmDir "%windir%\system32\test" 2>nul
) Else (
    Echo %Date% %Time% [ERROR] Admin permissions required! Please, start the installer under admin.
    Exit /B 1
)

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem PREPARE DIRECTORIES
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Echo %Date% %Time% [INFO ] Create installer directory
If Not Exist %InstallerDir% (
    MkDir %InstallerDir%
    Echo %Date% %Time% [INFO ] Installer directory created: %InstallerDir%
)
Echo %Date% %Time% [INFO ] Create updater directory
If Not Exist %UpdaterDir% (
    MkDir %UpdaterDir%
    Echo %Date% %Time% [INFO ] Updater directory created: %UpdaterDir%
)
Echo %Date% %Time% [INFO ] Create updater script
Echo %UpdaterPayload% > %UpdaterPath%
Echo %Date% %Time% [INFO ] Updater script created, placed into: %UpdaterPath%

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem INSTALL CHOCOLATEY PACKAGE MANAGER
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Set Choco="C:\ProgramData\chocolatey\choco.exe"
powershell Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem INSTALL GIT
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Set Git="C:\Program Files\Git\cmd\git.exe"
If Not Exist %Git% (
    Echo %Date% %Time% [INFO ] Git is installed
) Else (
    Echo %Date% %Time% [INFO ] Git is not installed
    Echo %Date% %Time% [INFO ] Installing git
    %Choco% install git.install -y
    Echo %Date% %Time% [INFO ] Git is installed
)

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem INSTALL PYTHON
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Set Python="C:\Python313\python.exe"
If Exist %Python% (
    Echo %Date% %Time% [INFO ] Python is installed
) Else (
    Echo %Date% %Time% [INFO ] Python is not installed
    Echo %Date% %Time% [INFO ] Installing python
    %Choco% install python3 --pre -y
    Echo %Date% %Time% [INFO ] Python is installed
)

Echo %Date% %Time% [INFO ] Installing required python dependencies and libraries
%Python% -m pip install telebot
Echo %Date% %Time% [INFO ] Installing required python dependencies and libraries: done

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem CLONE SOURCE CODE
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Echo %Date% %Time% [INFO ] Cloning repository
%Git% clone https://github.com/un1nsta11/spider.git %InstallerDir%
Echo %Date% %Time% [INFO ] Repository cloned. Checkout to branch: main
cd %LocalRepo% && git checkout main
Echo %Date% %Time% [INFO ] Repository cloned. Checkout to branch: main: done

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem SET LOCAL APP CONFIGURATION
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Echo %Date% %Time% [INFO ] Make config file
echo {"token": "%Token%"} > %LocalRepo%\config\config.json

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem TEST
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem NOT IMPLEMENTED

@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@Rem AUTORUN & START APPLICATION
@Rem ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Echo %Date% %Time% [INFO ] Adding application into startup
Set StartupFolder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
Echo %Python% %Application% > "%StartupFolder%\spider.bat"
Echo %Date% %Time% [INFO ] Startup added
Echo %Date% %Time% [INFO ] Run application
Start /b "%StartupFolder%\spider.bat"
Echo %Date% %Time% [INFO ] Application started, ErrorLevel: %ErrorLevel%
Exit %ErrorLevel%