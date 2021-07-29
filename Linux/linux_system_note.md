# Managing Linux System with Ubuntu as an example

## Mainly from "Mastering Ubuntu Server"

**With tips and notes on Linux management from other sources**

**All commands are run using Bash unless declared differently**

- Author: Jay Lacroix
- Edition: 3rd
- Publisher: Packt
- Reading start date: 2021-06-04



# Install Ubuntu Server
1. Download Ubuntu Server ISO.
2. Burn the file into a USB flash disk with Balena Etcher.
3. Install on machine
    - Plug in a ethernet cable if updates are needed.
    - Disk config: LVM group is recommended
4. Post-installation setup
    - Console font size: `sudo dpkg-reconfigure console-setup` and then select a font with larger sizes available.



# Tips
- `Alt+F<n>` will open the nth console session, up to 6.
- When modifying configuration files related to authenticaion (password requirement, sudo access, SSH, etc), it is a good practice to open an extra console session with root access.
- View OS info
    - `cat /etc/os-release`
    - `lsb_release -a`



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
- "read" means reading/listing all the file and sub-directory names.
- "write" means changing the list: adding files/subdirectores, change the names of current files and subdirectories.
- "execute" means the user can `cd` to it.
- Assuming a user has `rxw` access to all files and subdirectories:
    | Permission | ls (show names) | ls -l (show more info) | cd | cat file | ls subdir | update/add filename/subdirname | update file content | 

- "write + execute" means changing the list itself - e.g. removing a file name from the list(directory) and renaming a file (change the list/directory). File level permission is not needed to do above actions.
- "execute" means you can `cd` to it, making it your working directory.
- "execute" without "write" means the files within the directoy cannot be renamed or removed even if one has "write" permission on the file. Because "rename" and "remove" involves updating the directory itself. But the content of the file can be updated if "write" permission of the file was granted.

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



# Packages
- [Ubuntu packages webpage](http://packages.ubuntu.com/)

## Debian packages - `apt`
- Installed binaries are at `/usr/bin/`
- Latest version may not be available until next release
- System packages are also Debian packages and may conflict with user installed packages
- Commands
    - Search: `apt search <keyword1> <keyword2> ...`
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