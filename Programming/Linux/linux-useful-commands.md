# Useful Linux system related commands

## Ubuntu Specific

### Package Management

- Add a ppa: `sudo add-apt-repository ppa:whatever/ppa`

- Remove a ppa: `sudo add-apt-repository --remove ppa:whatever/ppa`

- Install or upgrade a package `sudo apt install <package-name>`

- Update all packages information: `sudo apt update`

- Upgrade all packages `sudo apt upgrade`

- Find an installed package `dpkg -l <package-name-w/o-wild-card>`

- Uninstall an package but keep all configuration file `sudo apt remove <package-name>`

- Uninstall an package and delete all configuration file `sudo apt purge <package-name>`

- Clean dependencies `sudo apt autoremove`
