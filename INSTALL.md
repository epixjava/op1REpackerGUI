# Installation

#TODO: Add windows specific install steps, add troubleshooting section 

### Step 1: Get the firmware file that you want to modify

First you need to have an official firmware update file, here's how to get one.

- **Recommended:** Get the latest OP-1 firmware update file from the TE website: https://teenage.engineering/downloads
- *Experimental:* If you want you can try older firmware files from the archive: https://github.com/op1hacks/op1-fw-archive

- I recomend saving a copy of your firmware file in the "fw" folder located in "assets" 

- This tool is currently compatible with OP-1 fimrwares up to the latest version, 246.

### Step 2: Get into the terminal

In this step we'll need to make sure  **python3**  is installed since Python 3 is the programming
language that **op1REpackerGUI** uses. 

First we'll need to open the terminal:
- Open the Terminal App on your system (more info about Terminal here: https://macpaw.com/how-to/use-terminal-on-mac) 
- If on windows open a command prompt or powershell window. 
- Next lets see if python3 is installed.
  In the terminal type the following command and press enter:
```python3 --version``` 
or 
``` which python```
  If the output looks something like `Python 3.X.X` or '/usr/bin/python3' then you have python3 and can continue to step #3. 

If you get an error from the command above (something like `command not found: python3`) you'll need to install Python 3.  I would recommend checking out one of the following guides for installing it:
 - https://www.saintlad.com/install-python-3-on-mac/
 - https://docs.python-guide.org/starting/install3/osx/




### Step 2.5 Windows Specific instructions 

-  When running this tool on Windows, you must install GTK for The Glitter Theme Engine to run correctly. Download and install GTK from this link here: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer 

- GTK does not need any additional setup. After the install completes you can proceed to step #3. 

### Step 3: Running op1REpacker 

- Download the source code from this repository. 
- Open a terminal/command prompt window targeting the main folder for op1REpackerGUI. The terminal should say username@MacBookPro op1REpackerGUI % or (FILLIN WITH WINDOWS FILE PATH) if on windows 
- Run " Python3 main.py" to start op1REpackerGUI 
- Use the file browser to select your .op1 firmware file, SVG file or the folder of your unpacked firmware file. 

### Step 4: Create your custom firmware!

Now your folder should have the file ```op1_246-REpacked.op1```. Run the normal OP-1 firmware update process by holding down COM on power on. This will take you to the OP-1 bootloader. Press 1 to upload your firmware, upload the repacked file you created then eject the op-1. The fimrware update process should start. After this process completes the mods/theme will be installed on your OP-1.
**Enjoy!**

### Troubleshooting

