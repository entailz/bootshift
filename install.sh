#!/bin/bash

USER_HOME=$(eval echo ~${SUDO_USER})

PYTHON_SCRIPT="src/bootshift_loader.py"
BASH_WRAPPER="src/bootshift"
INSTALL_PATH_BIN="/usr/bin"
INSTALL_PATH_LOCAL_BIN="$USER_HOME/.local/bin"

install_wrapper() {
	echo "Installing Timeshift wrapper script to $INSTALL_PATH_BIN"
	sudo install -m 755 "$BASH_WRAPPER" "$INSTALL_PATH_BIN"
}

install_python() {
	echo "Installing Python script to $INSTALL_PATH_LOCAL_BIN"
	mkdir -p "$INSTALL_PATH_LOCAL_BIN"
	install -m 755 "$PYTHON_SCRIPT" "$INSTALL_PATH_LOCAL_BIN"
}

install() {
	install_wrapper
	install_python
}

uninstall() {
	echo "Uninstalling Timeshift wrapper script from $INSTALL_PATH_BIN"
	sudo rm -f "$INSTALL_PATH_BIN/$BASH_WRAPPER"
	echo "Uninstalling Python script from $INSTALL_PATH_LOCAL_BIN"
	rm -f "$INSTALL_PATH_LOCAL_BIN/$PYTHON_SCRIPT"
}

if [ "$1" == "install" ]; then
	install
elif [ "$1" == "uninstall" ]; then
	uninstall
else
	echo "Usage: $0 {install|uninstall}"
fi
