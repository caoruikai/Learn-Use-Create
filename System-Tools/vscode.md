# Notes on Visual Studio Code



# VSCode on Windows
- Change newline character to "\n" before writing anything

## Start terminal using some arbitrary program

1. Search "terminal shell" in setting
2. Find `Terminal > Integrated > Automation Shell > OS (Windows/Osx/Linux)`
3. Click `Edit in settings.json`
4. Update the value for `terminal.integrated.shell.windows` to the path of your program.



# Connect to server using sftp

1. Install extension `sftp` in vscode.

2. Create a server folder `mkdir <name-your-server>`

3. In vscode, press `Shift+Control+P`, type in `sftp`, press `sftp:config`

4. Fill in the config file.

5. Create a project folder inside server folder.

6. Syncing can be done using right click on the folder panel.



# Keyboard Shortcuts
- Reference: https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf

## Interface
- Command Palette: `command`+`shift`+`f`
- Shift to next opened file/tab: `ctrl`+`tab`
- Toggle terminal: `ctrl`+`` ` ``

## Editor
- Undo: `command`+`z`
- Redo: `shift`+`command`+`z`
- Delete all text of the line after cursor (deletes the next line break if the cursor is at line end): `command`+`del`
- Delete all text of the line before cursor (deletes the previous line break if the cursor is at line start): `command`+`back`
- Delete current line: `shift`+`command`+`k`
- Move cursor to doc start/end: `command`+`up`/`down`
- Move cursor to line start/end: `home`/`end` or `command`+`<-`/`->`
- Move cursor to previous/next word: `option`+`<-`/`->`
- Select from cursor to doc start/end: `shift`+`command`+`up`/`down` or `shift`+`home`/`end`
- Select from cursor to line start/end: `shift`+`command`+`<-`/`->`
- Select from cursor to previous/next word end: `shift`+`option`+`<-`/`->`
- Select current/next same word (including line break): `command`+`d`
- Cut line up/down: `option`+`up`/`down`
- Copy line up/down: `shift`+`option`+`up`/`down`
- Cut current line (no need to select first): `command`+`x`
- Copy current line (no need to select first): `command`+`c`