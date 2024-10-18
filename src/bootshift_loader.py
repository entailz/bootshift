#!/usr/bin/env python3

import os
import subprocess
import re
import textwrap
import configparser

BOOT_ENTRY_PATH = "/boot/loader/entries"


def get_user_home():
    user = os.getenv("SUDO_USER")
    if user:
        return os.path.expanduser(f"/home/{user}")
    else:
        return os.path.expanduser("~")


CONFIG_PATH = os.path.join(get_user_home(), ".config/bootshift/config.ini")


def sanitize_filename(snapshot_name):
    return re.sub(r'[<>:"/\\|?*]', "_", snapshot_name)


def list_snapshots():
    try:
        result = subprocess.run(
            ["sudo", "btrfs", "subvolume", "list", "/"],
            capture_output=True,
            text=True,
            check=True,
        )
        return parse_snapshots(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running Btrfs command: {e}")
        return []


def parse_snapshots(output):
    snapshots = []
    lines = output.splitlines()
    snapshot_regex = re.compile(
        r"^\s*ID\s+\d+\s+gen\s+\d+\s+top\s+level\s+5\s+path\s+(timeshift-btrfs/snapshots/[^/]+)/@"
    )
    for line in lines:
        match = snapshot_regex.search(line)
        if match:
            snapshot_name = match.group(1).split("/")[-1]
            snapshots.append(snapshot_name)
    return snapshots


def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
        return config
    else:
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")


def create_boot_entry(snapshot, partuuid, boot_config):
    sanitized_name = sanitize_filename(snapshot)
    formatted_name = sanitized_name.replace("_", "-").replace(" ", "_")
    entry_filename = f"arch-snapshot-{formatted_name}.conf"
    entry_file_path = os.path.join(BOOT_ENTRY_PATH, entry_filename)

    if os.path.exists(entry_file_path):
        print(f"Entry for snapshot '{snapshot}' already exists.")
        return

    title = boot_config["boot"]["title"].format(snapshot=snapshot)
    linux = boot_config["boot"]["linux"]
    initrd = boot_config["boot"]["initrd"]
    options = f"root=PARTUUID={partuuid} rootflags=subvol=/timeshift-btrfs/snapshots/{snapshot}/@ {boot_config['boot']['options']}"

    boot_entry_content = textwrap.dedent(f"""
        title    {title}
        linux    {linux}
        initrd   {initrd}
        options  {options}
    """)

    try:
        with open(entry_file_path, "w") as f:
            f.write(boot_entry_content.strip())
        print(f"Created boot entry for snapshot: {snapshot}")
    except Exception as e:
        print(f"Failed to create boot entry for snapshot {snapshot}: {e}")


def main():
    snapshots = list_snapshots()
    if not snapshots:
        print("No snapshots found.")
        return

    try:
        config = load_config()
        partuuid = config["partuuid"]["partuuid"]
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: {e}")
        return

    for snapshot in snapshots:
        create_boot_entry(snapshot, partuuid, config)


if __name__ == "__main__":
    main()
