AOL (Assembly Oriented Language) by Phoenix Studios
Overview
Welcome to AOL (Assembly Oriented Language), a programming language developed by Phoenix Studios. AOL aims to simplify the process of writing assembly code, making operating system development more accessible. AOL combines the syntax of ASM, C, Python, and C# to provide an intuitive yet powerful coding experience.

Versions
AOL is available in two versions:

Python Module Version: This version runs purely from Python and PACI.
.exe Version: This is the full-featured version of AOL.
Purpose
AOL's primary goal is to make assembly programming easier, thereby facilitating the development of operating systems.

Usage
Python Module Version
To use the Python module version, you'll need to install the AOL module and optionally pcd_py for terminal use.

Installation
bash
Copy code
pip install aol
pip install pcd_py  # Optional but recommended for terminal use
Commands
You can run AOL commands through pcd_py:

To convert an AOL file to assembly:

bash
Copy code
aol ./file.aol
To parse an AOL file:

bash
Copy code
aol ./file.aol --parse
.exe Version
Simply download and run the executable file for the full version of AOL.

Setting Up AOL Icon in VS Code
VS Code is a great IDE for developing with AOL, and you can add a custom AOL icon for better file recognition.

Steps
Locate User Settings Folder

Windows: %appdata%/Code/User
Linux: /home/<your_user>/.config/<Code Folder>/User/
Mac: /Users/<your_user>/Library/Application Support/<Code Folder>/User/
Create Custom Icons Folder

Create a folder named vsicons-custom-icons in the user settings folder.
Copy AOL Icon

Copy the files from the assets folder in the AOL directory to the vsicons-custom-icons folder.
Configure VS Code

Open VS Code and navigate to:
File -> Preferences -> Settings -> Extensions -> VS Icons Configuration
Add the path to the parent folder of the vsicons-custom-icons folder.
Update Settings

Open the settings.json file in the parent folder of vsicons-custom-icons and add the following lines:

json
Copy code
"vsicons.associations.files": [
    {
        "icon": "aol-icon",
        "extensions": [
            "aol"
        ],
        "filename": false,
        "format": "svg"
    },
    {
        "icon": "aol-vardict-icon",
        "extensions": [
            "aolvd"
        ],
        "filename": false,
        "format": "svg"
    },
    {
        "icon": "aol-objdict-icon",
        "extensions": [
            "aolobjd"
        ],
        "filename": false,
        "format": "svg"
    },
    {
        "icon": "aol-metadata-icon",
        "extensions": [
            "aolMd",
            "aolMetaData",
            "aol_metadata"
        ],
        "filename": false,
        "format": "svg"
    }
]
Save and Apply

Save the settings.json file. The AOL icon should now appear for .aol files in VS Code.
Notes
The Python module version of AOL can be installed via pip.
Installing pcd_py is optional but recommended for terminal use.
Contact
For more information and support, please contact Phoenix Studios (pheonix.community.mail@gmail.com).

Enjoy using AOL and happy coding!