
# Intro 

Welcome to op1REpacker! This is a gui version of the op1repacker command line tool from op1hacks github with some added extras. 

The original tool can be found Here: https://github.com/op1hacks/op1repacker 


## New Features

The opie toolkit has been added to give you even more control over your OP-1. 
features such as: Full device backup, flac A/B side song rips and more.
SVG normalizer and SVG analyzer from the op1hacks repo have been added to aid with SVG creation. 
A simple SVG creation guide. Tips and tricks to make your own graphics and patches.
Mod list with toggles and descriptions for ultimate customization.
Error handeling for troubleshooting messed up files.


# Install required packages

1. pip3 install pipreqs (Or however you manage your packages)
2.in the main folder for op1REpacker open a terminal window and run 
pip install -r requirements.txt
3. Test by running python3 main.py in the same terminal window. op1REpacker should start


# OP-1 REpacker

*Taken from the op1repacker readme* op1repacker is a tool for unpacking and repacking OP-1 synthesizer firmware. It's based on
the collective research we've done at the [op-forums.com custom firmware thread](https://op-forums.com/t/custom-firmware-on-the-op-1/4283/680). 
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
![CWO Wizard](https://raw/githubusercontent.com/epixjava/op1REpacker/op1REpacker/assets/cwo-wizard.png)
![iter LostArt](https://raw/githubusercontent.com/epixjava/op1REpacker/op1REpacker/assets/iter-lostart.png)


## Disclaimer

**Don't use this unless you know exactly what you are doing!**
I take no responsibility for any damage that may result from using
this software. You will void your OP-1 warranty and in extremely unlikely cases, brick your device. 
Use at your own risk! 


## Installation

Ensure you have Python3 installed 

Download a copy of the source code from this repo. 

Open a terminal window pointing to the folder that op1REpacker's  main.py file is located in. 

Install dependancies by running 
'''
pip install -r requirements.txt

'''
I had to use pip3 on macOS so,

'''
pip3 install -r requirements.txt

'''

Run the app using 
'''
python3 main.py

'''


Enjoy using op1REpacker! 

## Features


### Unpack & Repack

To start you need to unpack your firmware. Select the firmware you want to modify in the file browser window. 
The firmware is unpacked to a new folder in the same location as the firmware
file is. If you unpack the firmware file `op1_246.op1` at `/home/user/op1/`
you'll get a folder `/home/user/op1/op1_246/` containing the unpacked files.
The same logic works for repacking, the new firmware file is saved in the same
location, but the name will be `op1_246-repacked.op1`.

REpack after you enable your modifications. 


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
These have been tested on the firmware version 246.
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

  | > Swap the cow in the CWO effect with a super chill wizard

 * gfx-iter-lostart

   > Adds Phytaxil's custom artwork to iter synth. Recreated from 
   > this  image at https://op-forums.com/t/op-1-custom-graphics/17702 
   > since it is unable for download. (Phytaxil, if you still have the 
   > OG file I can use that instead) 
 
 *gfx-seq-deadmau5

   > Adds deadmau5 to the sequencer graphic
   


To enable a mod, first unpack the firmware, select the mods you want 
then click "Modify" op1REpacker will let you know 
when the mods have been applied. Rememeber to repack and upload the 
firmware when complete! 

More modifications will be added later....


## opieREworked
Opie is the desktop frand for the OP-1. 

** Link to Standalone version: https://github.com/epixjava/opietoolkitplus

** Now works on macOS and Windows 10/11!

Rip Sides A and B of your Tape. Rips to FLAC, MP3 or M4a
See storage information of your OP1 
Backup and Restore your OP1
Pretty ASCII art


## usin' it
Run the opie toolkit from the op1REpacker tool. 

Opie will open in the exisiting terminal window

In the terminal window enter one of the following commands; 
"Backup"
"Restore" 
"Rip"
"Storage"
"Eject"
"Exit"

An "opie" folder is created in your users folder. Your backups and rips will be saved here. 


## Issues 
Let me know about em. I have other things going on but I will do my best to take a look at issues. No Promises 

I am always open to Feedback

Please include the type; Bug or Feature Request in your title. Preferably like "Feature Request: Some new feature"

Include whatever you want in your description, photos and error messages help with troubleshooting. 

If you want to contribiute to the project, message me. 


## Credits 
All credit goes to the op1hacks repo, creator of op1repacker, richrd, and creator of opie toolkit, mcginty.

https://github.com/richrd

https://github.com/mcginty

https://github.com/tabascoeye

https://github.com/op1hacks

https://github.com/TomSchimansky for customtkinter 
