# Edit file with Vim
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