# Installation guide

### Step 1: Get the firmware file that you want to modify
- First you need to have an official firmware update file, here's how to get one.

- **Recommended:** Get the latest OP-1 firmware update file from the TE website: https://teenage.engineering/downloads

- *Alternative:* If you want you can try older firmware files from the archive: https://github.com/op1hacks/op1-fw-archive

- I recomend saving a copy of your firmware file in the 'fw' folder located in 'op1REpackerGUI/assets/fw'

- This tool is currently compatible with OP-1 fimrwares up to the latest version, 246.

### Step 2: Setup! 
- op1REpacker GUI works on macOS and Windows 10/11 follow the steps bellow for your specific platform 


macOS (ARM) M1-M4 based devices 

- 1. Download or pull a copy of the respoisitory from Github. (If you are reading this you have probably done this already)

- 2. Install Python from python.org - (https://www.python.org/downloads/macos/)

- 3. open a terminal in the root of the op1REpackerGUI directory. You can do this easliy by opening finder, then in the menu bar select "view" then select "Show Path Bar". right or two finger click the op1REpackerGUi directory and select "open in terminal" 
 
- 4. run './install.sh' and follow the prompts to setup op1REpackerGUI. 
See the 'Install script info' section at the bottom for more information on what this script is doing. 

- 5. select yes to run or run the install script again after setup to launch the application 

- Congrats the program is setup! Read bellow for other ways to start the program 

- 5.5 if the install.sh script does not work after setup, in a terminal window opened in the op1REpackerGUi directory, run "source .vrepacker/bin/activate"

- 6. Then run "python3 main.py" to start the application 


Windows 10/11 

Windows10/11 

- 1. Download or pull a copy of the repository from Github. (If you are reading this you have probably done this already)

- 2. ensure python3 is installed from python.org - (https://www.python.org/downloads/windows/) Make sure to select "add python.exe to PATH" and select "use admin privileges when installing" during setup. 

- 3. install GTK3 runtime using the latest installer - (https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer) use recomended defaults when installing

- 4. open a CMD window in the op1REpackerGUI directory. You can do this easily by typing 'cmd' in the filebrowser path at the top of file browser

- 5. run "pip install -r winrequirements.txt",then run "winget install FFmpeg" in the CMD window. (You do not have to install FFmpeg but opie uses it to make rips.)

- 6. run the program with "python main.py" 


### Step 3: Using op1REpackerGUI to create your custom firmware!
- To start go to the 'Browse' button at the bottom and select a valid .op1 firmware file. The broswer will ask you what type of file you are selecting. 

- Click 'Unpack' to unpack the directory and create a folder in the same directory as the firmware file. 

- Go to browse and select 'Firmware Directory' and then select your unpacked firmware directory. TIP: Unless it has been moved, remove .op1 from the browser path. This will be the location of the unpacked directory. This can save you a few clicks. 

- Lets enable some mods! With your unpacked firmware directory selected, check the boxes next to the mods you want to apply. Once the mods you want have been selected, click 'Modify' to modify the firmware. NOTE: Do not apply multiple mods to the same firmware directory. If you are changing the CWO graphic for instance only choose one of the CWO mods to apply. 

- After the mods have been applied you can select 'Repack' to make your modified firmware. Please make sure you apply any themes from the Glitter Theme Engine before you repack the firmware. 

- Now your 'fw' folder should have the file `op1_246-REpacked.op1`. Run the normal OP-1 firmware update process by holding down COM when switching on the device. This will take you to the OP-1 bootloader. Press 1 to upload your firmware, upload the repacked file you created then eject the op-1. The fimrware update process should start. After this process completes the mods/theme will be installed on your OP-1. NOTE: If your OP-1 was running moddified firmware before this step, please install a clean firmware before installing the REpacked.op1 firmware. Wipeing user data is not enough and applying multiple hacked firmware ontop of one another will cause issues. 


**Enjoy!**

### Troubleshooting

Issue: My OP-1 makes wierd beeps and pops. Sound does not function right. 

Fix: Reinstall a clean OP-1 firmware file. You must restore, a factory reset will not fix the issue. After the stock firmware has been applied, try to re install 
the REpacked.op1 firmware file again. If you are still having the issue try to recreate your firmware file and try the steps again. 

Issue: On macOS/Windows, op1REpackerGUi will not start says it can not find libcairo2.dll. 

Fix: This issue occurs because cairo has not been setup correctly. Typically if it is installed, the location of the .dll has not been saved to PATH. The install.sh script sets these locations in PATH by default. You can try to run the script again or link the PATH's yourself if you have a special setup. If you are seeing this error on windows, check your GTK+ installation or re install.

Issue: Opie toolkit crashes with error. 'No backend found' or 'needs pywin32 installed'

Fix: Typically this happens because a dependency is missing. If on macOS make sure the right version of libusb and pyusb are installed. This could also be a PATH issue and libusb needs to be linked to PATH. The install.sh script should add homebrew to your PATH so the program can find the library. If this crash is happening on Windows make sure pywin32 is installed. Pywin32 should be installed via winrequirements.txt so it could be an issue with your enviroment.  

Issue: op1REpackerGUi is unresponsive while running opie. 

Fix: None: this is expected behavior. Once you are finished with the command you are running, opie should release its hold on op1REpackerGUi and you will be able to interact with the program again

Issue: on macOS, When running ./install.sh I get the error 'accsess is denied' 

Fix: make the script executable by typing 'chmod +x install.sh' in the terminal window and try running the install script again. 

### Install script info 

I want you to know what the install script is doing instead of you just running something because I told you to. The install.sh script does a few things. 

Initially it checks if the setup has already been completed and if it has been comepleted then it will start op1REpackerGUI. If the setup has not been completed it will begin the setup process. It checks if setup is comepleted by looking at installed dependacies and if the virtual enviroment has been created. 

The setup process is thus: 

1. Prompt user to install python3 

2. Install Homebrew and set homebrew paths to user PATH in .zprofile 

3. Installs 4 brew packages, libusb, cairo, python-tk and ffmpeg. 

4. Sets PKG_CONFIG_PATH and DYLD_LIBRARY_PATH to PATH. This allows the tool to find some of the system level packages installed in the prior step. 

5. Creates then activates a virtual python environment named vrepacker in the op1REpackerGUI folder. 

6. Installs python dependancies to the vrepacker environment via requirements.txt 

7. Asks the user if they wish to start the program. 


