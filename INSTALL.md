# Installation

### Step 1: Get the firmware file that you want to modify

First you need to have an official firmware update file, here's how to get one.

- **Recommended:** Get the latest OP-1 firmware update file from the TE website: https://teenage.engineering/downloads
- *Experimental:* If you want you can try older firmware files from the archive: https://github.com/op1hacks/op1-fw-archive

- I recomend saving a copy of your firmware file in the "fw" folder located in "assets" 

- This tool is currently compatible with OP-1 fimrwares up to the latest version, 246.

### Step 2: Setup! 
- op1REpacker GUI works on macOS and Windows 10/11 follow the steps bellow for your specific platform 


macOS (ARM) M1-M4 based devices 

- 1. Download or pull a copy of the respoisitory from Github. (If you are reading this you have probably done this already)

- 2. Install Python from python.org - (https://www.python.org/downloads/macos/)

- 3. open a terminal in the root of the op1REpackerGUI directory. You can do this easliy by opening finder, then in the menu bar select "view" then select "Show Path Bar". right or two finger click the op1REpackerGUi directory and select "open in terminal" 
 
- 4. run './install.sh' and follow the prompts to setup op1REpackerGUI. See 'Install script info' section for more information on what this script is doing. 

- 5. select yes to run or run the install script again after setup to launch the application 

- Congrats the program is setup! Read bellow for other ways to start the program 

- 5.5 if the install.sh script does not work after setup, in a terminal window opened in the op1REpackerGUi directory, run "source .vrepacker/bin/activate"

- 6. Then run "python3 main.py" to start the application 


Windows 10/11 

Windows10/11 ( run setup with add python.exe to path and use admin privileges when installing )

- 1. Download or pull a copy of the repository from Github. (If you are reading this you have probably done this already)

- 2. ensure python3 is installed from python.org - (https://www.python.org/downloads/windows/) Make sure to select "add python.exe to PATH" and select "use admin privileges when installing" during setup. 

- 3. install GTK3 runtime using the latest installer - (https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer) use recomended defaults when installing

- 4. open a CMD window in the op1REpackerGUI directory. You can do this easily by typing 'cmd' in the filebrowser path at the top of file browser

- 5. run "pip install -r winrequirements.txt",then run "winget install FFmpeg" in the CMD window. (You do not have to install FFmpeg but opie uses it to make rips.)

- 6. run the program with "python main.py" 


### Step 3: Using op1REpackerGUI to create your custom firmware!

Now your folder should have the file ```op1_246-REpacked.op1```. Run the normal OP-1 firmware update process by holding down COM on power on. This will take you to the OP-1 bootloader. Press 1 to upload your firmware, upload the repacked file you created then eject the op-1. The fimrware update process should start. After this process completes the mods/theme will be installed on your OP-1.
**Enjoy!**

### Troubleshooting


