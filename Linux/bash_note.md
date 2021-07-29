# Bash Shell Learning Notes
- **Bash**: Bourne Again Shell
- Other shells: zsh, fish, ksh
- Default shell configuraton: last column in `/etc/passwd`
    - Special shell types:
        - `/bin/false`: no shell access for the user, no message.
        - `/usr/sbin/nologin`: no shell access for the user, print a message.



# Builtin v.s. External Commands
- Builtin commands: specific to a certain shell. Behaviors of them can be different for differen shells or versions of the same shell.
- External commands: not specific to a certain shell. Like ones in `usr/bin` or user installed. Behavior of external commands are not impacted by the shell.
- [Builtin commands of bash (for version 5.1)](https://www.gnu.org/software/bash/manual/bash.html#Shell-Builtin-Commands)

## Navigation
- `pwd`: print working directory
- `cd`: change directory
    - `cd -`: return to previous directory
    - `cd ~` or `cd`: go to home directory

## Printing
- `echo`: recommended to be used to print simple strings without special characters because the behavior of `echo` dealing with sepcial characters within `""` varies with distributions and configurations.
- `printf`: with more funcationalities than `echo`. The behavior handling special characters are more consistent.



# Bash History
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



# Useful Key Strokes
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



# Different ways to chain commands
- Piping: `<command1> | <command2>` redirect `stdout` of `command1` as the `stdin` of `command2`.
- AND: `<command1> && <command2>` runs `command1` first and only runs `command2` if the execution of `command1` was successful.
- Semicolon: `<command1>; <command2>` runs both `command1` and `command2` regardless of success.



# Exit code for commands
- `echo $?`: Print exit code for a command after running it.
- `?` is the variable with the exit code of the last run command as the value.



# Alias
- `alias`: shows a list of available aliases in the shell.
- `alias <alias-command>="<actual-command>"`: create an alias command for the actual command. Either single quotes or double quotes work.
- Some useful commands and aliases
    - Top 10 CPU consuming processes: `alias cpu10='ps -L aux | sort -nr -k 3 | head -10'`.
    - Top 10 RAM consuming processes: `alias mem10='ps -L aux | sort -nr -k 4 | head -10'`.
    - View all mounted filesystems in a tabbed layout: `alias lsmount='mount | column -t'`.
- Store aliases in `.bashrc` to reuse them.



# Variables
- Set a variable: `<var-name>=<var-value>`
- `echo`: Print a variable value `echo $<var-name>`
- `env` (external commands): print all variable in the current shell.
- `read <var-name>`: Set a variable value using the prompt.



# Scripting
- Shebang (hash bang) line tells the shell which program to execute the script. Example: `#!/bin/bash`.
- All lines starting with `#` will be ignored except the top line (shebang).
- Make a script executable by its owner: `chmod +x <path-to-script>`
- Run a script by typing its full path `<path-to-script>`
- Run a script in current working directory: `./<script>`



# Streams: stdout, stdin, stderr
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