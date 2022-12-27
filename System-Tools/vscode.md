# Notes on Visual Studio Code

## VSCode on Windows

- Change newline character to "\n" before writing anything

## Connect to server using sftp

1. Install extension `sftp` in vscode.

2. Create a server folder `mkdir <name-your-server>`

3. In vscode, press `Shift+Control+P`, type in `sftp`, press `sftp:config`

4. Fill in the config file.

5. Create a project folder inside server folder.

6. Syncing can be done using right click on the folder panel.

## Start terminal using some arbitrary program

1. Search "terminal shell" in setting
2. Find `Terminal > Integrated > Automation Shell > OS (Windows/Osx/Linux)`
3. Click `Edit in settings.json`
4. Update the value for `terminal.integrated.shell.windows` to the path of your program.