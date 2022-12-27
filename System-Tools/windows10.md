## doskey - Alias setting in Windows

`doskey <alias>=<command>`

## Write a batch file (.bat)

Example:

```shell
doskey ssh-some=ssh user@server.com
sshca.bat
```

## SSH

### If config file was not found

1. Create a `ssh_config` file
2. Open `ssh` using `ssh -F <path-to-ssh_config>`