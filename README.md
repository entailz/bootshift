# bootshift

Bootshift is a portmanteau of "systemd-boot" and "timeshift".

## Installation

Always read the install.sh before installing, it is extremely simple. You will need to install the dependencies with your package manager of choice (see dependencies section).

```sh
./install.sh install
```

## Usage

Run bootshift just as you would run timeshift, it is simply a wrapper that first runs timeshift then runs the python script which will create corresponding boot entries in the /boot/loader/entries directory.


[!IMPORTANT]

- this script must be run as root as it will modify the /boot/loader/entries directory.
- bootshift will ignore top level 256


## Configuration

- You will need to create a directory called bootshift in ~/.config/ and create a file called config.ini inside of bootshift, use example_config.ini as a reference.
- config.ini is essentially a template entry for your snapshots in ini format.
- It is important that you replace the partuuid with the partuuid of the partition that contains your timeshift-btrfs snapshot directory.


## Requirements

- python
- btrfs
- timeshift
- systemd-boot

## License

MIT
