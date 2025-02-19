
# Intro 

Introducing op1REpackerGUI! This is a gui version of the op1repacker command line tool from op1hacks github with some added extras. 


![OP1REGUI](https://github.com/epixjava/op1REpackerGUI/blob/main/assets/op1REGUI.png)


The original tool can be found here: https://github.com/op1hacks/op1repacker 


## New!!

### Glitter Theme Engine 

Glitter has been added to op1REpackerGUI! The ultimate theme creator for your OP-1. 
Features include: 
Basic mode for easy theme creation by modifying only global colors 
Advanced mode for SVG specific element IDs allowing for deeper customization
Try your theme before applying using the Preview window
Easy editing of community themes
cool colorful boxes


![OP1GLITTER](https://github.com/epixjava/op1REpackerGUI/blob/main/assets/GlitterB.png)

![OP1GLITTERADV](https://github.com/epixjava/op1REpackerGUI/blob/main/assets/GlitterADV.png)



The orginal tool can be found here: https://github.com/Nanobot567/op1-glitter 


I hope you enjoy using this tool as much as I have. Excited to see what you come up with! 

### Opie Toolkit plus 

The opie toolkit has been added to give you even more control over your OP-1. 
features such as: Full device backup, flac A/B side song rips and more.
SVG normalizer and SVG analyzer from the op1hacks repo have been added to aid with SVG creation. 
A simple SVG creation guide. Tips and tricks to make your own graphics and patches.
Mod list with toggles and descriptions for ultimate customization.
Error handeling for troubleshooting messed up files.


# Getting it running 


Ensure you have Python3 installed on your system. 
There are various guides to learn how to do this.
A standard Python3 install will work just fine. Feel free to ask questions if needed! 

1. In the main folder for op1REpackerGUI open a terminal window and run 
```
 pip install -r requirements.txt
```
or if on Mac OS
```
pip3 install -r requirements.txt 


2. Test by running 
```
 python3 main.py 
```
in the same terminal window

op1REpackerGUI should start

!For macOS Arm devices; I had to install libusb with homebrew. This is needed for opie to function correctly. see https://brew.sh for how to install homebrew 

```
 brew install libusb
```

!!For Windows systems, The Glitter Theme Engine requires GTK to run correctly. This is due to an issue with cairosvg on windows 

Install using the latest release found here. No extra setup necessary

```
 https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
```
See the INSTALL.md file for more installation information if you run into trouble with these steps  


#OP-1 REpackerGUI

*Taken from the op1repacker readme* 
op1repacker is a tool for unpacking and repacking OP-1 synthesizer firmware. It's based on
the collective research  done at the [op-forums.com custom firmware thread](https://op-forums.com/t/custom-firmware-on-the-op-1/4283/680). 
This allows you to access and modify the files within the firmware as well as
repacking the files into a valid installable firmware file. Ready made mods
are also included in the tool (see [Modify](#modify)). Lastly it is also
possible to analyze unpacked firmware to get information such as build version,
build time and date, bootloader version etc.

 - Requires Python3
 - Tested on Linux, OS X and Windows 10/11

![Filter Effect](https://raw.githubusercontent.com/op1hacks/op1repacker/master/images/filter.png)
![Custom Iter Graphic](https://raw.githubusercontent.com/op1hacks/op1repacker/master/images/iter-lab.png)
![Tape Invert](https://raw.githubusercontent.com/op1hacks/op1repacker/master/images/tape-invert.png)
![CWO Moose](https://raw.githubusercontent.com/op1hacks/op1repacker/master/images/cwo-moose.png)
![CWO Wizard](https://github.com/epixjava/op1REpackerGUI/blob/main/assets/cwo-wizard.png)
![iter LostArt](https://github.com/epixjava/op1REpackerGUI/blob/main/assets/iter-lostart.png)


## Disclaimer

**Don't use this unless you know exactly what you are doing!**
I take no responsibility for any damage that may result from using
this software. You will void your OP-1 warranty and in extremely unlikely cases, brick your device. 
Use at your own risk! 


## Features


### Unpack & Repack 

To start you need to unpack your firmware. Select the firmware you want to modify in the file browser window. 
The firmware is unpacked to a new folder in the same location that the firmware file is stored
If you unpack the firmware file `op1_246.op1` at `/home/user/op1/`
you'll get a folder `/home/user/op1/op1_246/` containing the unpacked files.
The same logic works for repacking, the new firmware file is saved in the same
location, but the name will be `op1_246-REpacked.op1`.

repack AFTER you enable your modifications and themes 


### Analyze 

After unpacking a firmware file you can analyze the firmware directory.
Make sure the unpacked firmware folder is selected in the file browser window

Example output:

    - FIRMWARE VERSION: R. 00246
    - BUILD VERSION: 00246
    - BUILD DATE: 2022/11/09
    - BUILD TIME: 16:17:00
    - BOOTLOADER VERSION: 2.30
    - OLDEST FILE: 2022/11/09 11:16
    - NEWEST FILE: 2024/10/11 23:52


### Modify

The main reason you are using this program! Here you can select from a list of mods and gfx patches. 

The firmware can be automatically modified with some predefined mods.
These have been tested on the current firmware, version 246.
Currently available mods are:

 * iter

   > Enable the hidden iter synth

 * presets-iter

   > Add community presets from [op1.fun](http://op1.fun) to the iter synth

 * filter

   > Enable the hidden filter effect

 * subtle-fx

   > Lower the default intensity of effects. This allows you to turn effects on
   > without affecting the sound too much. You can then turn them up as you like.
   > This helps with live performances and avoids a sudden change to the sound
   > when an effect is enabled.

 * gfx-iter-lab

   > Add custom lab themed visuals to the iter synth.

 * gfx-tape-invert

   > Move the tracks to the top of the tape screen to make them much 
   easier to see
   > at certain angles.

 * gfx-cwo-moose

   > Swap the cow in the CWO effect with a moose, because why not. 
   
 * gfx-cwo-wizard 

   > Swap the cow in the CWO effect with a super chill wizard

 * gfx-iter-lostart

   > Adds Phytaxil's custom artwork to iter synth. Recreated from 
   > this  image at https://op-forums.com/t/op-1-custom-graphics/17702 
   > since it is unable for download. (Phytaxil, if you still have the 
   > OG file I can use that instead) 
 
   

To enable a mod, first unpack the firmware, select the mods you want 
then click "Modify" op1REpacker will let you know 
when the mods have been applied. Rememeber to repack and upload the 
firmware when complete! 

More modifications will be added later....


## opie toolkit plus

Opie is the desktop frand for the OP-1. 

![opie](https://github.com/epixjava/op1REpackerGUI/blob/main/assets/opie.png)

** Link to Standalone version: https://github.com/epixjava/opietoolkitplus

** Now works on macOS and Windows 10/11!

Rip Sides A and B of your Tape. Rips to FLAC, MP3 or M4a.
See storage information of your OP1. 
Backup and Restore your OP1.
Pretty ASCII art.


## usin' it
Run the opie toolkit from the op1REpackerGUI tool. 

Opie will open in the existing terminal window

In the terminal window enter one of the following commands; 
"Backup"
"Restore" 
"Rip"
"Storage"
"Eject"
"Verify"
"Exit"

An "opie" folder is created in your users folder. Your backups and rips will be saved here. 

Mac os: Macintosh HD\Users\username\opie
Windows: C:\Users\username\opie


## Issues 
Let me know about em. I have other things going on but I will do my best to take a look at issues. No Promises 

I am always open to Feedback

Please include the type; Bug or Feature Request in your title. Preferably like "Feature Request: Some new feature"

Include whatever you want in your description, photos and error messages help with troubleshooting. 

If you want to contribiute to the project, message me. 


## Credits 
All credit goes to the op1hacks repo, creator of op1repacker, richrd, creator of opie toolkit, mcginty and Nanobot567 creator of op-1 glitter. 

https://github.com/richrd

https://github.com/mcginty

https://github.com/tabascoeye

https://github.com/Nanobot567

https://github.com/op1hacks

https://github.com/TomSchimansky for customtkinter 