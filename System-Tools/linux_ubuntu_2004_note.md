# Managing Linux System (Ubuntu 20.04)
**All commands are run using Bash unless declared differently**

# References
- Mastering Ubuntu Server
    - Author: Jay Lacroix
    - Edition: 3rd
    - Publisher: Packt
    - Reading start date: 2021-06-04
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/html_node/index.html)
- [Ubuntu 20.04 Offical Documentation](https://help.ubuntu.com/20.04/ubuntu-help/index.html)
- [Ubuntu Commnunity Help Wiki](https://help.ubuntu.com/community/CommunityHelpWiki)



# Install Ubuntu Server
1. Download Ubuntu Server ISO.
2. Burn the file into a USB flash disk with Balena Etcher.
3. Install on machine
    - Plug in a ethernet cable if updates are needed.
    - Disk config: LVM group is recommended
4. Post-installation setup
    - Console font size: `sudo dpkg-reconfigure console-setup` and then select a font with larger sizes available.



# Control Tips
- `Alt+F<n>` will open the nth console session, up to 6.
- When modifying configuration files related to authenticaion (password requirement, sudo access, SSH, etc), it is a good practice to open an extra console session with root access.
- View OS info
    - `cat /etc/os-release`
    - `lsb_release -a`
- Suspend the OS (if applicable): `systemctl suspend`; Use ignore option `systemctl suspend -i` to ignore logged in users.
- Suspend the OS via SSH: `echo 'pm-suspend' | sudo at now + 2 minutes` and then disconnect the SSH session.


# Date & Time
- Date & time config file: Symlink `/etc/localtime` to a binary timezone identifier in `/usr/share/zoneinfo` directory.
    -  Show the symlink info: `ls -l /etc/localtime`.
- The timezone is also written to `/etc/timezone` file, thus can be viewed using `cat /etc/timezone`.
- `timedatectl list-timezones` to list all available time zones.
- `sudo timedatectl set-timezone <timezone>` to set timezone.



# Users
- Useful commands: `useradd`, `adduser`, `userdel`, `su`, `usermod`

## Add users
- `useradd`: `sudo useradd -d /home/<username> -m <username>`
    - `-d`: path for home directory for the user
    - `-m`: create the home directory during the process
- `adduser`: `sudo adduser <username>`
- Compare `useradd` and `adduser`:
    - `useradd` is available in more Linux distributions.
    - `adduser` is more user-friendly.
    - `adduser` is a Perl shell script using `useradd`.

## Delete users
- `userdel`: `sudo userdel <username>`
    - `userdel` does NOT remove the home directory.
    - To remove the home directory when deleting an user account, use `-r` option: `sudo userdel -r <user-anme>`

## Switching users
- `su`
    - If password is known: `su - <username>`
    - Switch to root (after root password was set): `su -`
    - Switch to an user with unknown password `sudo su - <username>`

## Modify user accounts
- `usermod [options] LOGIN`
    - Modify group member ship:
        - Primary group: `sudo usermod -g <group-name> <username>`
        - Append to the user list of some groups as the user's secondary groups: `sudo usermod -aG <group-name-1>, <group-name-2> <username>`
    - Modify username: `sudo usermod -l <new-name> <current-name>`
    - Modify home directory: `sudo usermod -d <new-dir> <current-dir> -m`
        - `-m` option: move the current home directory to the new one.

## Default config files for newly added users
- All files in `/etc/skel` will be copied to the home directories of newly added users.
- Can be used to set default configeration of any app (e.g. git, bash).

## Files with user config
- `/etc/passwd`
    - Can be accessed without `sudo`.
    - Format of each line (separated by `:`)
        1. user name
        2. if password was encrypted then 'x' else empty
        3. UID
        4. GID
        5. first name, last name
        6. home directory
        7. default shell
            - default to `/bin/bash` if `adduser` was used
            - default to `/bin/sh` if `useradd` was used
- `/etc/shadow`
    - Can only be accessed with `sudo`
    - Format of each line (separated by `:`)
        1. user name
        2. password hash
        3. number of days between Unix epoch date and last password change
        4. mininum number of days between 2 password changes
        5. maximum number of days between 2 password changes
        6. number of days between warning date and password expiration date
        7. number of days between password expiration date and account disable date
        8. number of days between Unix epoch date and account diable date
        9. unused; reserved for future versions of Linux



# Password
- `passwd`
    - Set up password: `sudo passwd <username>`
    - Lock a user (`-l`): `sudo passwd -l <username>`
        - Users can still SSH to the server. To fully lock a user, diable SSH for them.
         One way is to limit SSH access to a group. When a user is removed from the group, it will not have SSH access.
    - Unlock a user (`-u`): `sudo passwd -u <username>`
    - Show password status (`-S`): `sudo passwd -S <username>`
        - Output format (separated by empty space)
            1. user name
            2. password status: `L` or `P` or `NP`
                - `L`: locked
                - `P`: password set and usable
                - `NP`: does not have a password
            3. date of last password change (mm/dd/yyyy)
            4. minimum dates between 2 password changes
            5. maximum dates between 2 password changes
            6. number of days between warning date and password expiration date
            7. number of days between password expiration date and account disable date
            8. number of days between Unix epoch date and account diable date
- `chage [options] <username>`: change user password expiry information (age)
    - List current info (`-l` option): `sudo chage -l <username>`
    - Force the user to change password when logging in next time (`-d 0`): `sudo chage -d 0 <username>`
    - Update the max and min days between password changes (`-M`, `-m`): `sudo chage -M 90 <username>`, `sudo chage -m 5 <username>`
- Setting a password policy with **Pluggable Authentication Module (PAM)**
    - Install: `sudo apt install libpam-cracklib`
    - Edit the file `/etc/pam.d/common-password` by adding a history requirement
    ```
    password required pam_pwhistory.so
    remember=99 use_authok
    ```



# Groups
- To show the group membership of current logged in user: `groups`
- To show the group membership of any user: `groups <username>`

## File with group config
- `/etc/group`: contains list of groups
    - format of each line (separated by `:`)
        1. group name
        2. if the password was encrypted (`x` means yes)
        3. GID
        4. list of user names that are members (separated by `,`); the user with the same as group are naturally a member and not listed here.
- `/etc/gshadow`: group info with password hashes

## Add & delete a group
- Add a group with `groupadd`: `sudo groupadd <group-name>`
- Delete a group with `groupdel`: `sudo groupdel <group-name>`

## Manage groups of users
- Use user config tool `usermod`
    - `sudo usermod -aG <group-name> <username>`
        - `-a` option: to append the user to the user list of the group, instead of replacing.
        - `-G` option: to modify the secondary group membership, instead of primary.
    - `sudo usermod -g <group-name> <username>`
        - `-g` option: to modify the primary group membership of the group
- Use group config tool `gpasswd`
    - Remove a user from a group: `sudo gpasswd -d <username> <group-name>`
    - Add a user to a (secondary) group: `sudo gpasswd -a <username> <group-name>`



# Relationships between files/directories, users, and groups
- Each file or directory was assigned with only 1 user and 1 group
- To show the user and group of a file/directory: `ls -l`; User and group info was shown after permission info.
- Any user account can be the member of multiple groups.
- In Ubuntu, each user is a member of a group with the same name (primary group); Other distributions may assign all added user to `users` group.
- Primary vs secondary groups of a user: each user has a primary group. A file/directory created by the user will be assigned with the primary group.



# root and sudo

## root
- An user that can do everything
- Locked by default in Ubuntu distribution
    - password hash is `*` in the second postion of `root` line in `etc/shadow`.
- Can be unlocked by setting up a valid password for it: `sudo passwd`.
- After unlocked, can be switched to by `sudo su --login [root]`
- Lock the root account by disable the password: `sudo passwd -l [root]`

## sudo
- A group that can access objects as other users (default root) without logging in
- By default, sudo group has the same access with the root user, but it can be customized.
- To add an user to `sudo` group: `sudo usermod -aG sudo <username>`
- Not all distributions utilize or even install sudo by default.
- Config file that governs sudo access: `/etc/sudoers`.
    - Each line is for a group (with `%`) or user (no `%`).
    - For example
        - `%sudo ALL=(ALL:ALL) ALL`
        - `root ALL=(ALL:ALL) ALL`
    - 1st `ALL`: user or group can use sudo from all terminal.
    - 2nd `ALL`: user or group can use `sudo` to impersonate all other user.
    - 3rd `ALL`: user or group can use `sudo` to impersonate all other group.
    - 4th `ALL`: what commands the user or group can use (all of them if `ALL`).
    - An example without `ALL`: `charlie ubuntu=(dscully:admins) /usr/bin/apt`
- `visudo` should always be used to edit the config file `/etc/sudoers` since it will check errors.



# Inodes - Files, Directories, Links

## inode
- Inode: a data object that contains metadata regarding files within the filesystem.
- `ls -i`: show inode integers of files
- Everything in linux system is actually stored as a inode, or a "file", including files, directories, links, etc.
    - Plain file
    - Directory: a inode with list of filenames and their inodes.
    - Links

## Hard Link
- A hard link was linked to a the inode of a file (cannot be a directory).
- Even if the file was moved to another directory, a hard link to it is still effective.
- The hard link object and the original file share the same data, thus share the same inode integer.
- A hard link cannot be moved to another filesystem since it's based on inodes of a particular filesystem.
- If there is a hard link to a target file and the file was deleted, the inode or actual data was not deleted.
- `ln file1 link1`

## Symbolic Link (symlink, soft link)
- A pointer to a path to a file or directory.
- If the file or directory was moved, the link would not be effective.
- The inodes of the link and the original file/dir are different.

## View the contents of a file
- `cat`: concatenate contents of files and print
- `more`: for long files, use *Enter* to move to the next page.
- `less`: for long files, use *Enter* to move to the next page; use arrow keys to navigate forward and backward.
- `grep <keyword> <filename>`: return the lines containing the keyword. Add argument `-i` to make the keyword case-insensitive.
- `head -n <num>`: print first `<num>` lines of file, `<num>` defaults to 10.
- `tail -n <num>`: print last `<num>` lines of file, `<num>` defaults to 10.
- `tail -f`: live view of a file as it changes; use *Ctrl + c* to quit the live view.

## File & Directory commands
- `ls` (external command): list contents
- `rm`: remove file of directory
- `touch <filename>`
    - If the file does not exist, create an empty file.
    - If the file exists, update the modification time of the file.
- `cp <dir1>/<file1> <dir2>/<file2>`: copy `file1` in `dir1` to `dir2` and rename it as `file2`.
- `cp <dir1>/<file1> <dir2>/<file2> ... <dir>`: copy multiple files to `dir`.
- `cp -r <dir1> <dir2>`: copy `dir1` to `dir2`.
- `mv <dir1>/<file1> <dir2>/<file2>`: move `file1` in `dir1` to `dir2` and rename it as `file2`.
- `mv <dir1>/<file1> <dir2>/<file2> ... <dir>`: move multiple files to `dir`.
- `mv -r <dir1> <dir2>`: move `dir1` to `dir2`.
- For both `cp` and `mv`, if the target file or directory exist, it will be overwritten.



# Permissions

## Permission string
- 1st bit: object type
    - `-` for plain file
    - `d` for directory
    - `l` for link
- 2nd to 4th bits: user permissions
- 5th to 7th bits: group permissions
- 8th to 10th bits: world (other) permissions
- Within user, group, world permissions:
    - 1st bit: `-` for no permission, `r` for read
    - 1st bit: `-` for no permission, `w` for write
    - 1st bit: `-` for no permission, `x` for execute
- For a file
    - `r`: read file
    - `w`: write to file (not renaming, removing, or moving of the file, those are directory permissions)
    - `x`: can be executed as a program
- For a directory
    - `r`: list of content can be viewed (ls)
    - `w`: list of content can be altered
    - `x`: directory can be `cd` to

## Directory should be viewed as a *list* of its objects
- [Reference](https://unix.stackexchange.com/questions/21251/execute-vs-read-bit-how-do-directory-permissions-in-linux-work)
- `---` or `-w-`: no access.
- `r--` or `rw-` gives the access to `ls` the directory. `ls -l` does not show more info than the names.
- `--x` gives the access to `cd` to the directory. The following accesses depend on it:
    - `ls`, `cd` to subdirs
    - View file contents in the directory (`cat file`)
    - Update file contents or the subdir itself.
    - `cp` the files and subdirs to other directories.
    - Execute the files in the directory.
- `r-x` combining the accesses in `r--` and `--x`, and additionally show additional info when `ls -l`.
- `-wx` gives access to all actions in `--x`, and additionally update the directory itself (add/remove file/subdir, `mv` files/subdir, `cp` to the same directory).
- File permissions v.s. dir permissions
    - Permissions to add/remove a file is controlled by the dir permission `-wx`, not the file permission. 
    - If you do not want some users to add/remove files from a directory, set the directory permission to `r-x` for the user.

## Changing Permissions
- `chmod`
    - Using alphabets: `chmod [u|g|o][+|-][rwx] <filename>`
        - For example: `chmod u+rw <filename>`, `chmod g-x <filename>`
        - `u`: user, `g`: group, `o`: others
    - Using octal `chomod <user-octal><group-octal><other-octal> <filename>`
        - Permission: Octal & Binary
            - Read:    4 100
            - Write:   2 010
            - Execute: 1 001
        - To combine permissions is to add octals (binaries)
            - `rwx`: 4+2+1=7 or 100+010+001=111
            - `rw-`: 4+2+0=6 or 100+010+000=110
            - `r-x`: 4+0+1=5 or 100+000+001=101
            - `r--`: 4+0+0=4 or 100+000+000=100
            - `-wx`: 0+2+1=3 or 000+010+001=011
            - `-w-`: 0+2+0=2 or 000+010+000=010
            - `--x`: 0+0+1=1 or 000+000+001=001
            - `---`: 0+0+0=0 or 000+000+000=000
    - Change permission recursively - `-R` option: `chmod 770 -R <dirname>`
    - Change permission based on object types (files v.s. directories)
        - File permissions: `find /path/to/dir/ -type f -exec chmod 644 {} \;`
        - Sub-directory permissions: `find /path/to/dir/ -type d -exec chmod 755 {} \;`
        - Explanation: 
            - `{}` is a placeholder for each object `find` found.
            - `\` is to escape `;`
            - `;` is to end and separate multiple `chmod`, which makes it equivalent to `chmod 644 file1; chmod 644 file2; chmod 644 file3;`
            - Similarly, `+` is to append to the end of the object sequence, which makes it: `chmod 644 file1 file2 file3`.
    - Use `sudo` to change file permission not owned by the current user.

## Changing ownership
- `sudo chown <username> <filename|dirname>`: change the file owner to the user
- `sudo chown -R <username> <dirname>`: change the dir owner recursively
- `sudo chown [-R] <username>:<group-name> <filename|dirname>`: change the owner user and group of the file/dir.
- `sudo chgrp [-R] <group-name> <filename|dirname>`: change owning group of a file/dir.

## Setuid, Setgid, and Sticky bit
- Setuid bit (4): for executable files, if setuid bit was set, then any user has the same permission to execute it as the owner.
    - If setuid bit was set, `ls -l` will show `s` instead of `x` for executable permission bit for the user part. For example `rws` instead of `rwx`.
    - Set setuid bit: `chmod u+s <file>`
    - Unset setuid bit: `chomod u-s <file>`
- Setgid bit (2): 
    - For executable files, if setgid was set, then any group has the same permission to execute it as the owner group.
    - For directories, if setgid was set, then all files/dirs within the directory will have the same group with the directory.
    - If setgid was set, `ls -l` shows `s` instead of `x` for the group part.
    - Set setgid bit: `chmod g+s <file>`
    - Unset setgid bit: `chmod g-s <file>`
- Sticky bit (1): when the sticky bit of a directory was set, then only the file owner, directory owner and root user can add/delete files within it.
    - set sticky bit: `chmod +t <dir>`
    - unset sticky bit: `chmod -t <dir>`
- setuid, setgid, and sticky bit can be set using the summation of the octal values
    - setuid (4), setgid (2), sticky (1)
    - For example, to set both setgid and sticky bit: `chmod 3xxx <dir>`




# Packages
- [Ubuntu packages webpage](http://packages.ubuntu.com/)

## Debian packages - `apt`
- Installed binaries are at `/usr/bin/`
- Latest version may not be available until next release
- System packages are also Debian packages and may conflict with user installed packages
- Commands
    - Search: `apt search <keyword1> <keyword2> ...`
        - Example of search installed packages: `apt search <keyword> | grep installed`.
    - Show info: `apt-cache show <package>`
    - Install: `sudo apt install <package1> <package2> ...`
    - Update package index: `sudo apt update`
    - Upgrade a single package: `sudo apt upgrade <package>`
    - Upgrade all packages: `sudo apt upgrade`
        - No package will be removed in the process
    - Full upgrade: `sudo apt full-upgrade`
        - Packages will be removed if necessary
    - Remove: `sudo apt remove <package1> <package2>`
    - Remove with configuration purged: `sudo apt remove --purge <package>`

## Snap packages (Universal packages) - `snap`
- Installed snap binaries are at `/snap/bin/`
- Commands
    - Search: `snap find <keyword>`
    - Install: `sudo snap install <package>`
    - Remove: `sudo snap remove <package>`
    - Update a package: `sudo snap refresh <package>`
    - Update all packages: `sudo snap refresh`

## Package Repositories
- Concern of adding a package repository
    - Packages may contain backdoors or malwares.
    - Repository may go offline or stop updating.
- Proper way to edit repository list (DO NOT edit the `/etc/apt/sources.list` directly): `sudo apt-add-repository universe`
- Repositories lists
    - `/etc/apt/sources.list`: single file with default repositories.
    - `/etc/apt/sources.list.d/`: `.list` files can be added to this directory.
    - Example of a line: `deb http://us.archive.ubuntu.com/ubuntu focal main restricted`
    - Format of each line
        1. `deb` for binary or `deb-src` for source
        2. url
        3. Codename for Ubuntu release
        4. Component
            - `main`: Canonical supported, open & free
            - `restricted`: Canonical supported, not open or free licence
            - `universe`: supported by community
            - `multiverse`: not supported
- PPA (Personal Package Archives)
    - [Ubuntu PPA webpage](https://launchpad.net/ubuntu/+ppas)
    - Add a PPA: `sudo apt-add-repository ppa:<username>/<package>`
    - Remove a PPA: `sudo apt-add-repository --remove ppa:<username>/<package>`

## Back up & restore Debian packages
- Export list of installed packages: `dpkg --get-selections > packages.list`
- Import from a list and install packages
    ```shell
    sudo apt update
    sudo deselect update
    sudo dpkg --set-selections < packages.list
    sudo apt-get dselect-upgrade
    ```
## Clean up orphaned apt packages
- `apt autoremove`: use with care, especially those `linux-image` packages.

## Hardware enablement updates (HWE)
- Only available for LTS releases.
- Update hardware drivers.
- Can be configured to be on when intall Ubuntu or using this command after installation of Ubuntu: `sudo apt install --install-recommends linux-generic-hwe-18.04`



# File System Layout
- `/`: beginning of filesystem
- `/etc`: system-wide application configuration
- `/home`: user home directories
- `/root`: home directory for user `root`
- `/media`: for removable media, such as flash drives
- `/mnt`: for hard disks
- `/opt`: additional software packages
- `/bin`: essenstial user binaries (ls, cp, etc)
- `/proc`: virtual filesystem for OS-level components
- `/usr/bin`: a majority of user commands
- `/usr/lib`: libraries
- `/var/log`: Log files



# Bash Shell

- **Bash**: Bourne Again Shell
- Other shells: zsh, fish, ksh
- Default shell configuraton: last column in `/etc/passwd`
    - Special shell types:
        - `/bin/false`: no shell access for the user, no message.
        - `/usr/sbin/nologin`: no shell access for the user, print a message.

## Builtin v.s. External Commands
- Builtin commands: specific to a certain shell. Behaviors of them can be different for differen shells or versions of the same shell.
- External commands: not specific to a certain shell. Like ones in `usr/bin` or user installed. Behavior of external commands are not impacted by the shell.
- [Builtin commands of bash (for version 5.1)](https://www.gnu.org/software/bash/manual/bash.html#Shell-Builtin-Commands)
- Common built-in commands for bash (behavior depends on shell):
    - `cd`, `pwd`, `break`, `eval`, `exec`, `exit`, `export`, `alias`, `echo`, `help`, `printf`, `read`, `ualias`.

## Navigation
- `pwd`: print working directory
- `cd`: change directory
    - `cd -`: return to previous directory
    - `cd ~` or `cd`: go to home directory

## Printing
- `echo`: recommended to be used to print simple strings without special characters because the behavior of `echo` dealing with sepcial characters within `""` varies with distributions and configurations.
- `printf`: with more funcationalities than `echo`. The behavior handling special characters are more consistent.

## Bash History
- History is stored at `~/bash_history`.
- Can be access using *up* and *down* arrow keys.
- Command `history` prints the shell histories with the index.
- Historical commands can be run using `!<index>`
- Last commands can be accessed using `!!`, and can be combined within other commands like `sudo !!`
- Remove a command from the history: `history -d <index>`
- Commands with sensative infomation like passwords are stored in the history file unless the command was prefixed with a whitespace (default in Ubuntu 20.04).
- The history behavior can be configured in `~/.bashrc` as `HISTCONTROL=<value>` with possible values as
    - `HISTCONTROL=ignorespace` ignores the command predixed with a whitespace.
    - `HISTCONTROL=ignoredups` ignores the duplicated commands.
    - `HISTCONTROL=ignorespace:ignoredups` or simply `HISTCONTROL=ignoreboth` ignores both cases.
- The histroy can be searched using **Ctrl + r**. See **Useful Key Strokes** for details.

## Useful Key Strokes
- **Tab**
    - Press once: completes path if possible
    - Press twice: shows sugguested path
- **Ctrl + a**: moves the cursor to the beginning of the line.
- **Ctrl + e**: moves the cursor to the end of the line.
- **Ctrl + l**: clears the screen.
- **Ctrl + k**: deletes characters from the cursor to the end of the line.
- **Ctrl + u**: deletes everything you typed on that line.
- **Ctrl + r**: search for the commands history
    1. Press **Ctrl + r**
    2. Type a keyword to search.
    3. The last match shows up.
    4. Press **Ctrl + r** again to move up the history to the previous match.
- **Ctrl + x + e**: edits the current command in the text editor, when saved, the command is executed.

## Different ways to chain commands
- Piping: `<command1> | <command2>` redirect `stdout` of `command1` as the `stdin` of `command2`.
- AND: `<command1> && <command2>` runs `command1` first and only runs `command2` if the execution of `command1` was successful.
- Semicolon: `<command1>; <command2>` runs both `command1` and `command2` regardless of success.

## Exit code for commands
- `echo $?`: Print exit code for a command after running it.
- `?` is the variable with the exit code of the last run command as the value.

## Alias
- `alias`: shows a list of available aliases in the shell.
- `alias <alias-command>="<actual-command>"`: create an alias command for the actual command. Either single quotes or double quotes work.
- Some useful commands and aliases
    - Top 10 CPU consuming processes: `alias cpu10='ps -L aux | sort -nr -k 3 | head -10'`.
    - Top 10 RAM consuming processes: `alias mem10='ps -L aux | sort -nr -k 4 | head -10'`.
    - View all mounted filesystems in a tabbed layout: `alias lsmount='mount | column -t'`.
- Store aliases in `.bashrc` to reuse them.

## Variables
- Set a variable: `<var-name>=<var-value>`
- `echo`: Print a variable value `echo $<var-name>`
- `env` (external commands): print all variable in the current shell.
- `read <var-name>`: Set a variable value using the prompt.

## Scripting
- Shebang (hash bang) line tells the shell which program to execute the script. Example: `#!/bin/bash`.
- All lines starting with `#` will be ignored except the top line (shebang).
- Make a script executable by its owner: `chmod +x <path-to-script>`
- Run a script by typing its full path `<path-to-script>`
- Run a script in current working directory: `./<script>`

## Streams: stdout, stdin, stderr
- File descriptors
    - stdin: 0
    - stdout: 1
    - stderr: 2

## Redirection to a file
- `>` for overwriting; `>>` for appending.
- `>` is equivalent to `1>`. In other words, `stdout` is the default.
- `1>` or `1>>` or simply `>` or `>>`: redirect `stdout` only.
- `2>` or `2>>`: redirect `stderr` only.
- `&>` or `&>>`: redirect both `stdout` and `stderr`.
- `m>&n`: redirect `m` to the current location of `n`
    - Example 1: `ls x y > output.txt 2>&1`. Both `stdout` and `stderr` will be redirected to `output.txt`. 
        - Explanation: `> output.txt` set the current location of `stdout` to `output.txt` and then `2>&1` redirect the `stderr` to the current location of `stdout`, which is already `output.txt`.
    - Example 2: `ls x y 2>&1 > output.txt`. `stdout` will be redirected to `output.txt` and `stderr` will be printed.
        - Explanation: `2>&1` redirect the `stderr` to the current location of `stdout`, which is printing. Then the current location of `stdout` was set to `output.txt`.
- `m> /dev/null`: do not display the `m` stream (delete the stream)
- `1> file1 2> file2`: redirect `stdout` to `file1` and `stderr` to `file2`

## Piping - Redirect stdout of a command as stdin of another command
- `<command1> | <command2>`

## Redirection to both stdout and files: tee command
- `<command> | tee <option> <filename> `
- Append to a file using `-a` option
- Redirect to multiple files: `<command> | tee <file1> <file2>`



# Vim
- *Ctrl + z* bring editor to background.
- `fg` to bring editor to foreground.
- Configuration: `~/.vimrc`
    - Example: Add line `set number` will display line number by default
- Command mode
    - `:q`: quit (when there was no change)
    - `:q!`: force quit (discarding changes)
    - `:wq`: write & quit
    - `:! <shell command>`: run a shell command; Press *Enter* to go back to vim.
    - `:sp` or `:split`: view current file in a horizontally splitted view.
        - `:sp /path/to/file`: view another file in a horizontally splitted view.
        - "RO" means read-only.
        - Holding *Ctrl* and press *w* key twice: switch between the two splits.
        - *Esc*: return to vim.
    - `:vs` or `:vsplit`: vertical version of `:sp`.
    - Example command: `:%s/<keyword1>/<keyword2>/g` - replace all `keyword1` with `keyword2`.
    - Line number: `:set number` to display; `:set nonumber` to disable.
    - Press *x*: delete single character
    - Press *d* twice: delete the whole line and copy it to clipboard
    - Press *p*: paste text in clipboard to where the cursor is.
    - Press *G* (*Shift* + *g*): go to the end of the file.
    - Press *g* twice: go to the top of the file.
- Insert mode
    - In command mode, press *i* or *insert*: go to insert mode.
    - In command mode, press *a*: enter the insert mode one character to the right.
    - In command mode, press *A* (*Shift* + *a*): enter the insert mode with the cursor at the end of the line.
    - *Esc* to quit insert mode.
- Visual mode: select text
    1. Move the cursor to the first character.
    2. Press *v*
    3. Move the cursor to the last character.
    4. Press *y* to disable the hightlight; Now the selected text is copied in clipboard.
    5. Press *p* to paste the copied text to where the cursor is.
    6. Press *u* to undo changes.



# Processes

## Background & Foreground
- **Ctrl+z** to bring a running job background
- `fg` to bring the most recent job ( that was brought background) foreground.
- `jobs` to show all the jobs in background.
- `fg <n>` to bring `n`th job foreground, where `n` is the index shown by the `jobs` command.
- `<command> &` to run a command in background.
- Other ways to run multiple jobs (to avoid background jobs printing output)
    - Open multiple shells
    - Using programs like `tmux` or `screen`.

## `ps` to Manage Processes
- Concepts
    - PID (Process ID): unique ID for the process.
        - `pidof <command>`: return the pid(s) created by the command.
    - TTY (teletypewriter)
        - TTY: usually refer to the processes that is running in the actual server itself (like a shell).
            - Example: `TTY1` to `TTY7` refer to the TTY behind the 7 terminal terminal windows one can open in Ubuntu server 20.04.
        - Pseudu TTY: refer to the processes running in the shell
            - Example: `pts/0`
    - CMD: the command starting the process
    - STAT: the current state of the process. Check the complete list of possible values using `man ps`
    - START: the start time of the command
    - TIME: total CPU time the process has used so far.
    - PRI: priority of the process. Higher the value, higher the priority.
    - NI: niceness of the process. Higher the value, "nicer" the process is to other processes, which means this process is at lower priority.
- `ps`, no option: print basic info for the current user's processes.
    - `ps a`: print more info for the current user's processes
    - `ps au`: print more info for all users
    - `ps aux`: print more info for all user processes and processes that are not tied to a TTY (system level processes).
- Useful examples
    - `ps aux | grep <keword>`: print the processes line containing the keyword.
    - `ps u -C <keword>`, alternative to the above one using `grep`
    - `ps aux --sort=-pcpu | head -n <i>`: sort the processes by CPU usage, only showing top i.
    - `ps aux --sort=-pmem | head -n <i>`: sort the processes by RAM usage, only showing top i.

## Manage Priorities of Processes
- Priorities are managed by setting the "niceness" value.
- Increasing the nice value will lower the priority and descreasing it will boost the priority.
- Possible range of nice value: -20 to 19.
- `nice -n <i> <command>` to start a process with a nice value of `i`.
- `renice -n <i> <PID>` to update the nice value of a process with `i`.
- `sudo` is needed to decrease the nice value of a process.

## Signal
- A signal can be sent to a process by the kernel, another process, or manually with a command.
- Each signal is corresponding to a number.
- `man 7 signal` for help page
- Examples
    - `SIGHUP(1)`: terminal line hangup. Sent to processes when the terminal was closed.
    - `SIGINT(2)`: interrupt program. Sent to processes when *Ctrl + c* was pressed.
    - `SIGKILL(9)`: kill program.
    - `SIGTERM(15)`: software termination signal. Ask a process to terminate cleanly.

## Kill misbehaving processes
- `sudo kill <PID>`
- By default, `SIGTERM(15)` will be sent to the process by `kill`. If successful, the process will free its memory and gracefully close.
- To specify a signal, use `sudo kill -<signal> <PID>`, for example `sudo kill -9 <PID>` to send `SIGKILL(9)` to the process.
- `SIGKILL(9)` should only be used as a last resort because it may cause manages to software or hardware.
- `sudo killall <process-name>`: kill all processes with certain name (command).
- `sudo killall -9 <process-name>`: send `SIGKILL(9)` to all processes with certain name (command).

## System Processes
- Ubunutu 20.04 uses `systemd` to manage system processes.
- "System processes", "services", "daemons" and "units" are interchangable terms.
- `systemctl` is used to manage the units.
- `systemctl` equals `systemctl list-units`, which lists all the units.
- `systemctl | grep <keyword>` is a useful command to search for a unit with a certain keyword.
- `systemctl status <unit-name>`: print the status of a certain unit.
    - Some units may need `sudo` group access to print all information.
    - `systemctl status -l <unit-name>`: print full log entries.
    - Some entries of the output:
        - "Loaded": if the unit will be loaded in the next startup. 
        - "vendor preset": loaded automatically if "enabled".
        - "Acitve": if the unit is currently active.
- `sudo systemctl start <unit-name>`: start a unit.
- `sudo systemctl stop <unit-name>`: stop a unit.
- `sudo systemctl restart <unit-name>`: stop & start a unit.
- `sudo systemctl reload <unit-name>`: reload a unit. Available in some units like Apache. In Apache, reloading it will not close the current web connection, while restarting it will.
- `sudo systemctl enable <unit-name>`: enable a unit. Make the unit start automatically when the server boots.
- `sudo systemctl disable <unit-name>`: disable a unit. Stop the unit from starting automatically when the server boots.
- `sudo systemctl enable --now <unit-name>`: enable & start a unit.
- Stop the *OpenSSH* unit does not close the current ssh connections, only stops new connection.

## Cron - Schedule tasks
- `crontab -l`: list the current user's cron jobs.
- `sudo crontab -u <username> -l`: list a specific user's cron jobs.
- `crontab -e`: edit the cron jobs for the current user.
- `EDITOR=vim crontab -e`: edit the cron jobs with certain editor.
- Format of the cron line: `m h dom mon dow command`
    - `m`: minute
    - `h`: hour in 24-hour format (0~23)
    - `dom`: day of the month
    - `dow`: day of the week (0~6, Sunday~Saturday)
    - `*` in any postion means runing at every minite/hour/dom,/dow
    - `command`: using "fully qualified" or the full path is a good practice.
- The data and time is following the ones set up in the server. It can be checked using `date`.



# System Resources

## Disk Usage
- `df -h`: list the disk usage of all volumns
- `df -i`: list the inode usage of all columns
    - There are limited number of inodes for each volume.
    - Disk usage will also shown as full if inodes are used up. For example, there is an extremely large number of files, which rarely happens.
- `du -hsc *`: list the disk usage of files and directories in the current directory
    - `-h`: human readable
    - `-s`: only files and directories with depth 1 (not recursive)
    - `-c`: display grand total
- `du -hcd i <dir>`: list the disk usage inside the directory.
    - `-d <i>`: go the the `i`th depths of the directory
- `du -h <file>`: list the disk usage of a file.
- `ncdu`: a useful tool to navigate the file system and investigate the disk usage.
    - `sudo apt install ncdu`
    - `ncdu -x`: only scan the local volumns and skipping all network mounts.

## Memory Usage
- `free -[m|g]`: shows the memory usage status.
    - "total": total memory
    - "used": used memory = total - free - buff/cache
    - "free": truly free memory not used by anything
    - "shared": memory used in tmpfs
    - "buff/cache": memory used as kernel buffers and disk cache. Most of it can be used by applications if needed.
    - "available": memory can be used by application if needed.
- Linux will use a big chunk of unused memory as "buff/cache" (disk cache). Most of that amount can be released if needed.

## Swap
- Swap is a disk partition or a file that acts as RAM when the memory is saturated.
- Check the current swap at `/etc/fstab`
- To create and activate a swap file at `/swapfile`
    - Create a file with fixed size: `sudo fallocate -l <size> /swapfile`
    - Permission: `sudo chmod 0600 /swapfile`
    - Make it a swap file: `sudo mkswap /swapfile`
    - Add an entry to `/etc/fstab`: `/swapfile none swap sw 0 0`
    - Activate the swap file: `sudo swapon -a`
    - Deactivate: `sudo swapoff -a`
- Swappiness is used to control how frequently the system starts to use swap.
    - Default value is 60.
    - Larger swappiness value means the system will more likely to use swap.
        - 100 means swap is used whenever possible.
        - 0 means swap is never used.
    - The swappiness value is roughly proportional to the percetage of memory not used.
    - Check the swappiness value: `cat /proc/sys/vm/swappiness`
    - Set the swappiness temporarily (until next reboot): `sudo sysctl vm.swappiness=<value>`
    - To set the swappiness permanentally, edit the line `vm.swappiness = <value>` in the file `/etc/sysctl.conf`.

## CPU - Loading Average
- Loading averages: Average number of tasks that were waiting for the attention from the CPU for a give time period.
- `uptime` shows system up time and loading average over 1 minute, 5 minutes, and 15 minutes.
- Loading average greater than the total number of cores of CPUs meaning over-loaded CPUs.
- Loading average smaller than an usual level might indicate some processes are not running properly.
- It is important to know the baseline of loading average of the server.

## htop - manage resource usage
- Press *u* for user menu, which allows one to select users to filter the processes.
- `htop -d <i>` starts htop with refresh rate of i seconds.
- If *F10* conflicts with the terminal emulator keystroke, *q* can be used to quit `htop`.



# Manage Storage Volumes

## View the current/added disks and partitions
- `sudo fdisk -l`: info on volumes.
- `dmesg --follow`: refreshed after adding a new volume.
- `lsblk`: tree view.
- `blkid`: print attributes like UUIDs and labels of partitions.

## Creating Partition and Format
1. `sudo fdisk <volume>` to start the program. For example, `sudo fdisk /dev/sdb`.
    0. (optional) *m* for the help menu.
    1. *g* or *o*: *g* to create a GUID Partition Table (GPT); *o* to create a Master Boot Record (MBR). GPT is a newer standard.
    2. *n* to create a new partition. If MBR was chosen, primary v.s. extended partition needs to be chosen.
    3. Choose a partition number. Press *Enter* for the default next available number.
    4. Choose the first sector for the partition. Press *Enter* for the default `2048`.
    5. Choose the last sector to use. If pressing *Enter* to accept the default, this partition will consist of all the free space. Type `+<i>G` to make the partition of size i Gigabyte.
2. `sudo mkfs.ext4 /dev/sdb1`: format partition `sdb1` as `ext4` format. 
3. (Optional) Use `e2label /dev/sdb1 <label>` to add a label to the partition.

## Mount and Unmount
- Volumes can only be mounted to an empty directroy.
- By FHS, `/mnt` is used to mount hard drives etc., and `/media` for removable media like flash drives.
- Assuming one would like to mount a formatted partition `/dev/sdb1` to `/mnt/vol`, here are the steps
    1. `df -h` to check the current mounts;
    2. `sudo mkdir /mnt/vol1` to create the directory;
    3. `sudo mount /dev/sdb1 /mnt/vol1` to mount it; A more error-prone alternative is to add the `-t` option with the partition format: `sudo mount /sdb1 -t ext4 /mnt/vol1`;
    4. To unmount it in the future: `sudo umount /mnt/vol`.
- The procedure above only mounts the partition before the next reboot. To make it reboot or manage the property of the mount, use entries in the `/etc/fstab` file.

## /etc/fstab file
- Elements of each line of the file:
    1. The name, label, or UUID (Universally Unique Identifier) of a partition.
        - Example: `/dev/mapper/vgubuntu-root`, `UUID=xxxxxxx`, `LABEL=xxxxx`.
        - Device names are subject to the order of the detection. For example, if hard drives are unplugged and plugged again in different order, same device may end up with different divce names.
        - UUID is a better way to identify the devices, since it is less likely to be changed. The UUID is changed when the partition is formatted.
        - A label of the partition can be added using `e2label /dev/sdb1 <label>`
    2. The directory the partition mounts to.
    3. File system type, e.g. `ext4`.
    4. Mount options separated by commas. Common options:
        - `errors=remount-ro` for root system tells the system to remount the partition as read-only if error occurs.
        - `sw` is swap option.
        - `defaults` implies a group of options:
            - `rw`: partition can be read from and written to.
            - `exec`: files within this partition cab be executable.
            - `auto`: automatically mount the partition at boot time.
            - `nouser`: only `root` is able to mount it.
            - `async`: make the partition operates faster since it will not write everything to it in real-time.
        - `ro`: read-only
        - `noexec`: do not allow executable file.
        - `noauto`: the partition is not auto mounted when `mount -a` is given (for example, at boot time). This option is useful if one would like to mount a partition only when necessary (e.g. a backup drive). After booted, the partition can be mounted manually by using `sudo mount <dir>` without the device name or UUID since the entry is in `/etc/fstab`.
        - `users`: allow users to mount/unmount this partition.
    5. `dump`: 1 for backup, 0 for no backup; Rarely used; Almost always 0; Can be used by a backup utility.
    6. `pass`: order in which `fsck` checks the partitions for failures. Possible values are:
        - 0: never checked;
        - 1: checked first;
        - 2: checked last.
- Recommended steps to update the `/etc/fstab` file:
    1. Run `blkid <device-name>` to get the UUID.
    2. Create a directory the partition will be mounted to.
    3. Open `/etc/fstab` with an editor.
    4. Add a entry to the file with the correct format.
    5. Add a useful comment before the entry starting with `#`.
    6. Save the file with the changes.

## LVM (Logical Volume Manager)
- Volume Group (vg): container containing multiple disks.
- Physical Volume (pv): a physical or virtual hard disk.
- Logical Volume (lv): similar to partition, but is able to span multiple disks.
- Package install:
    - Check if `lvm2` is installed: `apt search lvm2 | grep installed`.
    - Install `lvm2`: `sudo apt install lvm2`.
- Initiate a physical volume: `sudo pvcreate <device-name>`.
- Volume group commands:
    - Create a volume group: `sudo vgcreate <vg-name> <pv-name>`.
    - Display volume groups: `sudo vgdisplay`.
    - Extend a volume group (add extra disks): `sudo vgextend <vg-name> <device-name>`.
    - Remove a volume group: `sudo vgremove <vg-name>`
- Logical Volume commands:    
    - Create a logical volume: `sudo lvcreate -n <lv-name> -L <size>g <vg-name>`.
    - Display logical volumes: `sudo lvdisplay`.
    - Format a logical volume: `sudo mkfs.ext4 /dev/<vg-name>/<lv-name>`
    - Mount a logical volume: `sudo mount /dev/<vg-name>/<lv-name> <dir-to-mount>`.
    - Extend a logical volume to use i% of the free space of the group volume: 
        - `sudo lvextend -n /dev/<vg-name>/<lv-name> -l +<i>%FREE`.
        - `sudo lvextend -L+<i>g /dev/<vg-name>/<lv-name>`.
    - Resize the filesystem to thenew size of logical volume: `sudo resize2fs /dev/mapper/vg--test-<lv-name>`. Note the two hyphens.
    - Remove a logical volume: `sudo lvremove vg-test`. Only a logical volume that is not in use can be removed.

## Concepts Comparison between Traditional and LVM
| Trandition | LVM |
| --- | --- |
| NA | Volume Group (VG) |  
| Device | Physical Volume (PV) |
| Partition | Logical Volume (LV) |
| Format Partition | Format/Extend LV |
| Mount Partition | Mount LV |
| Re-create Partition | Extend/Reduce LV |

## LVM Snapshots
- LVM snapshots captures a logical volume at a certain point in time and preserve it.
- A volume can be rolled back by merging with a snapshot from a previous time.
- LVM snapshots are not backups. They should be used as temporary holding solution for testing new grades, for example.
- Create a LVM snapshot`sudo lvcreate -s -n <snapshot-name> -L <i>g <vg-name>/<lv_name>`
- Roll back a logical volume: `sudo lvconvert --merge <vg-name>/<snapshot-name>`.
- Remove a snapshot: `sudo lvremove <vg-name>/<snapshot-name>`.



# Networks

## Hostname
- View current hostname
    - The prompt shows the hostname by default.
    - `cat /etc/hostname`
- Update the hostname
    1. Update the `/etc/hostname` file by `sudo hostnamectl set-hostname <hostname>` or edit `/etc/hostname` directly.
    2. Update the entry in `/etc/hosts` to match the new hostname.
- `localhost`: a hostname for a server to reach to itself.

## Network Interfaces
- View assigned IP addresses: `ip addr show` or simply `ip a`.
- Interface name: `enp<i>s<j>` or `wlp<i>s<j>`
    - `en` means wired ethernet, `wl` means wireless.
    - `p<i>` means the ith system bus (starting at 0).
    - `s<j>` means the jth PCI slot.
- Bring a interface up or down: `sudo ip link set <interface-name> up/down`.
- Command `ifconfig` is deprecated.

## IP Addresses (IPv4) & Subnet Masks
- IPv4 addresses are 32-bit, separated into four 8-bit segments by dots like `192.168.0.12` (in decimal). Rewriting an address into binaries shows clearly there are four 8-bit numbers.
- The smallest value for each segment is 0, while the largest is 255.
- Local v.s. Global: A global IP address (e.g. `208.67.222.222`) is valid throughout all the internet while a local IP address (e.g. `192.168.0.5`) is only valid with in a local network.
- A (local) network can be splitted into subnets by setting up different CIDR (Classless Inter-Domain Routing). The value of a CIDR means how many bits reprensent the network and the rest for hosts (`192.168.0.3/24`). For example:
    - Class C or `/24`: First 24 bits (3 segments) are defined as a network, and the last 8 bits (last segment) are used to define hosts in the network. Maximum number of hosts: 254.
- Netmask: another way of specifying the subnets setting. `255` means a segment is used for network, `0` means a segment is used for hosts. For example: `255.255.255.0` is equivalent to `/24`.

## Assign a Fixed IP Address
- Preferred method: static lease (DHCP reservation) via the DHCP server.
- Alternative method: Assign a static IP address
    1. Backup the netplan yaml file corresponding to the network interface. For example, `sudo cp /etc/netplan/00-network-manager-all.yaml /etc/netplan/00-network-manager-all.yaml.bak`.
    2. Update the yaml file with a static IP address. 
        - Entries of the yaml file
            - `addresses`: the static IP address assigned to the server.
                - Should be within the scope of local network.
                - Should be out of the scope of DHCP.
                - `/24` indicates that the IP address is part of a 24-bit subnet.
            - `gateway4` address should be the same with the gateway/router.
            - `nameservers`: IP addresses for DNS servers, usually the same with gateway, but can be different.

        - Example:
            ```yaml
            # This is the network config written by 'tsaork'
            network:
            ethernets:
                enp0s25:
                addresses: [192.168.100.50/24]
                gateway4: 192.168.100.1
                nameservers:
                    addresses: [192.168.100.1, 192.168.100.2]
            version: 2
            ```
    3. Double check every entry and get ready if the network stop working.
        - Try not to update the network config remotely, e.g. via SSH.
        - If SSH is the only option, `tmux` is a useful tool. 
            1. Install: `sudo apt install tmux`.
            2. Type `tmux`, then all commands after will be run by `tmux` in the background, even if one disconnect with `tmux` using *Ctrl + b*, release, and then press *d*.
            3. If detached from the `tmux` session, rejoin it using `tumx a`.
    4. `sudo netplan apply` to make the change effective.
    5. Check the updates using `ip a`.

## Linux Name Resolution
- `hosts` entry in the file `/etc/nsswitch.conf` defines the order to check the names.
    - `files` means checking `/etc/hosts`.
- Managing name resolution using `/etc/hosts` is a quick workaround but not convenient since only this server is able to access it, contrasting to a DNS server.
- `systemd-resolve --status | grep DNS\ Servers` will show the current DNS server in use.

## TCP v.s. UDP
- TCP (Transmission Control Protocol) & UDP (User Datagram Protocol) are two protocols to transfer data over internet.
- TCP is more reliable & secure, while UDP is faster.

## Port & Socket
- Like IP addresses are used to distinguish machines, port is used to distinguish services.
- Possible values of a port: 0 to 65535.
- The combination of a IP address, a port, and a protocol (TCP or UDP) is called a socket, and has to be unique for every service in the local network.
- "Well known ports": first 1000 ports reserved for common services, which requires the `sudo` privilege.
- Current port in use can be checked at: `/etc/services`.
- Current port listened to: `sudo ss -tunlp`.

## Port Forwarding & Triggering
- Port forwarding is used to send network traffic to certain service in certain machine within LAN by the gateway.
- Set up in a gateway
    - Inbound port number
    - Inbound external IP address where requests was sent from (can be restricted or all)
    - Internal IP of the receipient machine
    - Internal port number of the receipient machine (can be same with the inbound or not)
- After the gateway receives a request from the external IP addresses with a certain port number, it sends the request to the designated IP address with designated port number.
- Port Triggering
    - More dynamic and flexible than port forwarding.
    - Ranges of IP address and port numbers can be set instead of one-to-one relationship in port forwarding.

## Set up an Ubuntu Server as a DHCP/DNS/Gateway/NTP Server
- Skip for now since it is not needed. Refer to the book itself.

## mail (mailx)
- Listing mode
    1. `mailx`: list all mail in `/var/spool/mail/$USERNAME`
    2. Type index: View content of email
        - `Enter`: next page
        - `q`: quit viewing the email
    3. `delete`: delete the oldest email
    4. `q`+`Enter`: quit `mailx`
- Email mode
    - Write the mail text via stdin: `mailx -s <title> <recipient-email>`. Write `EOT` as the last line to end the stdin.
    - Mail text from a file: `mailx -s <title> <recipient-email> < <path-to-file>`
    - Using pipes: `echo <email-text> | mailx -s <title> <recipient-email`
    - Multiple recipients: `mailx -s <title> <recipient1>, <recipient2>`
    - CC and BCC: `mailx -s <title> <recipient-email> -c <cc-recipient> -b <bcc-recipient>`
    - Attachment: `mailx -s <title> <recipient-email> -a attachment.txt`



# OpenSSH

## Installation & Running
- Check if OpenSSH client was installed: `which ssh`.
- Install client: `sudo apt install openssh-client`.
- Check if OpenSSH daemon (service) was installed: `which sshd`.
- Check the status of OpenSSH service: `systemctl status sshd`.
- Install OpenSSH server: `sudo apt install openssh-server`.
- If the service is not running: `sudo systemctl start ssh`
- If the service is diabled (will not automatically start at the next reboot): `sudo systemctl enable ssh`
- Check the port the service is using: `sudo ss -tunlp | grep ssh`

## Connection from Client
- `ssh <ip>` or `ssh <hostname>`
- Specify the username: `ssh <username>@<ip>` or `ssh <username>@<hostname>`
- Specify port number: `ssh -p <port> <ip>`
- Close the SSH connection: `exit` or press *Ctrl + d*.
- Config file `~/.ssh/config`: save options to connect to different servers and simplify the `ssh` connecting command.
    - Example:
        ```
        Host myserver
            Hostname: 192.168.1.23
            Port 2223
            User tsaork

        Host server2
            Hostname: server2.mynet.org
            Port 2222
            User someuser
        ```
    - With the above example: `ssh myserver` is equivalent to `ssh -p 2223 tsaork@192.168.1.23`
- Config to keep the SSH session alive: add the following to `~/.ssh/config`
    ```
    Host *
        ServerAliveInterval 60
        ServerAliveCountMax 10
    ```

## SSH Key Authentication
- Generating key pairs: `ssh-keygen`
    - Choice of algorithms - `-t` option: `ed25519` is preferred over `rsa`
    - Creates `~/.ssh` directory if not exists.
- Copy the public key to server: `ssh-copy-id -i <path-to-pub-key> <hostname>`
    - Copies the content of the public key to `~/.ssh/authorized_keys` on the server.
- Change passphrase: `ssh-keygen -p`
- SSH agent: use SSH agent to avoid typing the passphrase at every connection (at the current shell).
    - `eval $(ssh-agent)`: add necessary variables in the current shell environment.
    - `ssh-add <path-to-private-key>`

## Secure SSH
- Check authorization log at: `/var/log/auth.log`
- OpenSSH service is configured in the file `/etc/ssh/sshd_config`
- Recommended configuration
    - Change the port SSH uses to some other number than 22.
        - After changing the port number, SSH connections need to be established using the `-p` or `-P` option:
            - `ssh -p <port-number> <hostname>`
            - `scp -P <port-number> <filename> <hostname>:<pathname>`
    - Always use `Protocol 2` instead of `Protocal 1`.
    - Use `AllowUsers` and `AllowGroups` to control acccesses via SSH.
        - `AllowUsers` overrides `AllowGroups`.
        - Add an entry: `AllowUsers <user1> <user2> <user3> ...`.
        - Add an entry: `AllowGroups <group1> <group2> ...`.
        - To create a group and add user to it: `sudo groupadd <ssh-group>`, `sudo usermod -aG <ssh-group> <username>`
        - Disable root user access via SSH: `PermitRootLogin no`.
        - Disable password authenticated SSH connection: `PasswordAuthentication no`.
            - Make sure public key authentication works before disable password connections.
- Restart the service after modifying the config file: `sudo systemctl restart sshd`

## SSH Channeling (Port Forwarding)
- Port forwarding using a SSH connection to a gateway
- Local forwarding is used for a local client to access a socket behind a gateway.
    - `ssh -L <local-port>:<remote-ip>:<remote-port> <ssh-gateway-ip>`
    - If the gateway and the remote are the same machine, use `localhost` for the remote IP: `ssh -L <local-port>:localhost:<remote-port> <ssh-gateway-ip>`
    - It requires the local client has the access to SSH to the gateway.
- Remote forwarding is used for any remote client to access a local server behind a gateway.
    - `ssh -R <remote-port>:localhost:<local-port> <ssh-gateway-ip>`
    - Any remote client having access to SSH to the gateway can send requests to the local socket.
- Both local and remote forwarding command can be summarized as: `ssh -L|R <client-port>:<destination-ip>:<destination-port> <ssh-gateway-ip>`
- IP addresses can be replaced by the hostname if recogonizable by the client.

## ProxyJump
- Temporary: `ssh -J <user@bastion:port> <user@remote:port>`
- Permanent: In `~/.ssh/config`
    ```
    Host bastion
        HostName bastion.server.com
        User tsao
        Port 2222

    Host magic-server
        HostName magic-server.server.com
        User tsao
        ProxyJump bastion
    ```

# File Sharing

## Compare solutions
- Samba: sharing between Linux and Windows machines
- NFS: sharing between Linux machines
- SSHFS: temporary sharing with SSH

## SSHFS
- Installation: `sudo apt install sshfs`
- Mount an external directory to a local one: `sshfs <username>@<remote-ip>:<remote-dir> <local-dir>`
- Unmount
    - If one has root priviledge: `sudo unmount <local-dir>`
    - If one does not have root priviledge: `fusermount -u <local-dir>`
- Add an entry to `/etc/fstab`. 
    - Example: `<username>@<remote-ip>:<remote-dir> <local-dir> fuse.sshfs rw,noauto,users,_netdev 0 0`.
    - Once added, next time to mount it: `/mnt/myfiles`
    - Always use `noauto`




# File Copy / Transfer

## rsync: for complex file syncing jobs
- The most useful archive `-a` option
    - `sudo rsync -a <from-dir> <to_dir>`
    - retains as much metadata including permissions and timestamp
    - `-a` is a shortcut for `-rlptgoD`
- `-r`: sync recursively
- `-v`: verbose mode
- Support SSH: `sudo rsync -av <from-dir> username@192.128.1.3:/<to-dir>`
- `--delete`: delete files in the target dir if they are no longer in the source.
- `-b`: backup mode; outdated files in the target will be moved to `-backup-dir` instead of being updated inplace.
    - Example: `sudo rsync -avb --delete --backup-dir=/backup/$CURDATE /src /target`

## SCP: for simple file copying
- Local to remote: `scp <path-to-file> <username>@<remote-ip/hostname>:<dir>`
- Remote to local: `scp <username>@<remote-ip/hostname>:<path-to-file> <dir>`
- Target paths default to `home` if omitted.
- `-r` for copying directories recursively: `scp -r <src> <target>`
- `-P` for specifying the port number SSH service listens to: `scp -P 1235 <scr> <target>`.
- `-v` for verbose model.
- `scp` recognize configurations in `~/.ssh/config`.



# Python

## Install and create `virtualenv` for Python 3.8 on Ubuntu 20.04
1. Add `universe` apt repository: `sudo apt-add-repository universe` (DO NOT change the `/etc/apt/source.list` file directly).
2. Install `python3.8-venv`: `sudo apt install python3.8-venv`.
3. Create a virtualenv: `python3 -m venv <venv-name>`
4. Activate virtualenv: `source ~/<venv-name>/bin/activate`.
5. Use `pip` to install packages: `python -m pip install -U <packages>`
6. Deactivate the virtualenv: `deactivate`.