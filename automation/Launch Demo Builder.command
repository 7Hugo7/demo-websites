#!/bin/bash

# Demo Builder - macOS Double-Click Launcher
# Double-click this file in Finder to launch the app

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Run the start script
./start.sh

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press any key to close..."
    read -n 1
fi
