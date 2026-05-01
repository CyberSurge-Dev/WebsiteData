Project link on Github: [https://github.com/CyberSurge-Dev/fedora_greeter_wallpaper](https://github.com/CyberSurge-Dev/fedora_greeter_wallpaper)

## What is this?
As a result of having a surplus of free time, I have found myself taking on new hobbies. In this case, I have noticed a distinct lack of purely cosmetic wallpapers on the login screen that you spend less than 30 seconds on. In an effort to fix this incredibly niche issue, at least on my computer, I reverse engineered an existing program to change the GDM greeter wallpaper every time I restart my computer by using a handful of Python scripts and ChatGPT. 

## What's the big deal?
Nothing, really. 

This is an incredibly niche thing that you would think would have a very simple built in solution to Gnome, but dosnt. Although, there is a tool called [GDM Settigns](https://github.com/gdm-settings/gdm-settings) that allows you to change the wallpaper of your Gnome login screen quite easily, along with several other interesting tweaks, the way that these changes are made is complicated. 

Many of the themes and visual tweaks of Gnome are compiled into files known as Gresource files, rather than being being standalone, editable CSS files. This means to make any visual modifications to the operating system (such as changing the login screen wallpaper), you have to extract the css files from these resource files. After you modify the CSS to your liking, you then recompile the resources back into another Gresource file, and replace the existing one. 

Sound simple enough, right? Yes, but this means downloading additional dependencies for something that should be as simple as modifying a CSS file.


## Lets take a look
``` (python3)
image_path = choose_random_image(BKGS)

# Create Backup
subprocess.run([
    "cp", "-r",
    GRESOURCE_P,
    BACKUP
], check=True)


# Extract .gresource File to working directory output
subprocess.run(["./gresource-extract.py", 
GRESOURCE_PATH, "-o", 
WORKDIR+"/output"], check=True)

print("[✓] gresource file: " + 
GRESOURCE_PATH + 
"Extracted Successfully to " 
+ WORKDIR + "/output")

# Copy the background into the directory
subprocess.run([
    "cp",
    image_path, BACKGROUND_PATH
], check=True)
print("[✓] Background " + image_path + " copied to " + BACKGROUND_PATH)

# Re-compile gresource file  
subprocess.run([
    "./gresource-recompile.py",
    WORKDIR + "/output",
    OUTPUT
], check=True)
print("[✓] Recompile Successful")

# Replace original gresource file
subprocess.run([
    "cp",
    OUTPUT,
    GRESOURCE_PATH
], check=True)

print("[✓] .gresource replaced")
```

The code above is a small snip-it from the main script (greeter_wallpaper.py, located in the Github repo attached to this article) for this project. This code segment shows the 5 main steps that need to be done to make any modifications to the login screen.

1. Create a backup of the current theme files (located at ``/usr/share/gnome-shell/``)
2. Extract the contents of ``gnome-shell-theme.gresource`` (this file differs between distrubutions) to the working directory using the ``gresource-extract.py`` script
3. Copy in the new, randomly selected wallpaper, change the name and remove the file extension. Properly modify the CSS files.
4. Using the ``gresource-recompile.py`` script, recompile the working directory into a new Gresource file, and replace the existing one at ``/usr/share/gnome-shell/``

This process can be replicated to modify just about any of the theme CSS files on your Gnome system. Some directories and file names will differ between systems, so it is important to keep that in mind.

## The Install script
This was the fun and annoying part for me, having to learn Bash to make a basic script that just copies and pastes files from one directory to another. So let's take a look.

```
#!/bin/bash
echo "[+] Greeter Wallpaper Installer..."

# Function for updating CSS in theme files
update_css () {
	if grep -q "Greeter Wallpaper" "$1"; then
		echo "[!] css already edited: $1"
	else
		echo "[+] added css to $1"
		cat <<EOF >> "$1"
/* 'Greeter Wallpaper' CSS additions */

.login-dialog { background: transparent; }
#lockDialogGroup {
  background-image: url('resource:///org/gnome/shell/theme/background');
  background-position: center;
  background-size: cover;
}
EOF
	fi
}

echo "[+] Downloading dependencies"
# Dependencies
dnf install glib2-devel

echo "[+] Creating directories for scripts"
mkdir /usr/local/bin/greeter_wallpaper
mkdir /usr/local/bin/greeter_wallpaper/backup
mkdir /usr/local/bin/greeter_wallpaper/wallpapers
mkdir /usr/local/bin/greeter_wallpaper/workdir
mkdir ./output

echo "[+] Copying scripts"
cp -r ./scripts/* /usr/local/bin/greeter_wallpaper/

echo "[+] Copying wallpapers"

rm -r /usr/local/bin/greeter_wallpaper/wallpapers/*
cp -r ./wallpapers/* /usr/local/bin/greeter_wallpaper/wallpapers/

# >> The risky shit <<
echo "[+] Extracting gnome-shell-theme.gresource"
chmod +x "./scripts/gresource-extract.py"
python ./scripts/gresource-extract.py "/usr/share/gnome-shell/gnome-shell-theme.gresource" -o "./output"

if [ -f "./output/org/gnome/shell/theme/gdm.css" ]; then
	update_css "./output/org/gnome/shell/theme/gdm.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell-dark.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell-dark.css"
fi
if [ -f "./output/org/gnome/shell/theme/gdm3.css" ]; then
	update_css "./output/org/gnome/shell/theme/gdm3.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell-high-contrast.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell-high-contrast.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell-light.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell-light.css"
fi

# Re compile .gresource


chmod +x "./scripts/gresource-recompile.py"
python ./scripts/gresource-recompile.py ./output ./gnome-shell-theme.gresource

cp ./gnome-shell-theme.gresource /usr/share/gnome-shell/gnome-shell-theme.gresource

# set up the service
echo "[+] Copying service file to /etc/systemd/system/"
cp ./resources/greeter_wallpaper.service /etc/systemd/system/
echo "[+] Enabling the greeter_wallpaper.service"
systemctl daemon-reload
systemctl enable greeter_wallpaper.service

# Clean up
echo "Cleaning up..."
chmod +x /usr/local/bin/greeter_wallpaper/*
rm -r ./output
rm ./gnome-shell-theme.gresource
echo "[✓] Greeter_wallpaper is installed."
echo "[✓] It is recommended to restart now."
```

The install script is in premise, very simple. The first thing you do is make sure that all the dependencies are installed from the one package manager on your system because you don't care about any other Linux distribution (because they're inferior anyway). 

After that, you create the directories where you intend to install your critical program files into. In this case, I chose to create my program directories in ``/usr/local/bin/`` because that's where Google told me I should put startup programs. Once these directories are created, you can copy in you scripts and resources. 

Before the program can work properly though, you need to make sure the CSS files for all versions of your gnome shell theme are edited (which changes between systems) in your Gresource. This is where the individual extract and recompile scripts from earlier come in useful. Using these scripts we extract the contents of the same ``gnome-shell-theme.gresource`` file from earlier into a local working directory, where we can check if each file has the required CSS, and if it does not, add it.

This is the purpose of the ``update_css`` function, which checks for a specific flag string ("Greeter Wallpaper") to see if the CSS file was already edited by the install script a previous time. If it was, then nothing changes, but if it was not, then it adds a small section of CSS to the bottom of the file.

And in speaking of adding content to the end of a file in bash, did you know there is a difference in functionality between ``cat <<EOF >>`` and ``cat << EOF >>``? Me neither. And if you did know there was a difference, than I'm sorry for your loss.

Lastly in the install process, the script sets up a service on the system, basically a small program that tells the computers program manager (Systemd) to run the scripts every time the computer is powered on.

After this all of this, the program should be ready to work hand free.

## Conclusion
Although this article may serve no purpose to anyone (if anyone) that reads it, I hope you learned at least a little bit about some of the hoops you need to jump through to get seemingly simple things to work on Linux. And although this program may have no reason to exist, it was a good way for me to kill a few hours and learn something new, which is what it's all about.

Project link on Github: [https://github.com/CyberSurge-Dev/fedora_greeter_wallpaper](https://github.com/CyberSurge-Dev/fedora_greeter_wallpaper)