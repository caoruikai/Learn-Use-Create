## Mail

### When used as a command

1. `mail`: list all mail in `/var/spool/mail/$USERNAME`
2. Type index: View content of email
    - `Enter`: next page
    - `q`: quit viewing the email
3. `delete`: delete the oldest email
4. `q`+`Enter`: quit `mail`

## Redirect

`tee /dev/stdout /dev/stderr` 

## SSH

### ProxyJump

There are two ways to proxyjump:

1. `ssh -J <user@bastion:port> <user@remote:port>`

2. In `~/.ssh/config`:

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

### Keep SSH alive

Add the following to `~/.ssh/config`:

```
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 10
```

## alias

### Alias for long path

1. In `.bashrc`, add a line like this: `my_alias='cd <path>'`.
2. `source .bashrc` or start a new session.
3. Type `my_alias` will `cd` to that path.