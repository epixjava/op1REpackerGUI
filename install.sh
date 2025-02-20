#!/bin/bash

#Setup script for op1REpackerGUI created by Epixjava - 2025


print_status() {
    local color=$1
    local message=$2
    case $color in
        "green") echo -e "\033[32m$message\033[0m" ;;
        "red") echo -e "\033[31m$message\033[0m" ;;
        "yellow") echo -e "\033[33m$message\033[0m" ;;
    esac
}


check_success() {
    if [ $? -eq 0 ]; then
        print_status "green" "✓ $1"
    else
        print_status "red" "✗ $1 failed"
        exit 1
    fi
}


# check if setup is complete
check_setup() {
    # required components
    if command -v python3 &> /dev/null && \
       command -v brew &> /dev/null && \
       [ -d ".vrepacker" ] && \
       brew list | grep -q "libusb" && \
       brew list | grep -q "cairo" && \
       brew list | grep -q "python-tk" && \
       brew list | grep -q "ffmpeg" && \
       [ -f "requirements.txt" ]; then
        return 0  # complete
    else
        return 1  # incomplete
    fi
}


# If setup is already complete start venv and run
if check_setup; then
    print_status "green" "Previous setup detected. Starting program..."
    source .vrepacker/bin/activate
    check_success "Virtual environment has been activated"
    print_status "yellow" "Running op1REpackerGUI..."
    python3 main.py
    exit 0
fi

# If we get here, setup is needed
print_status "yellow" "Starting new setup..."


# Check if Python 3 is installed
print_status "yellow" "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_status "red" "Python 3 is not installed."
    print_status "yellow" "Please install Python from the official website:"
    print_status "yellow" "https://www.python.org/downloads/"
    print_status "red" "After installing Python, please run this script again."
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    print_status "green" "✓ Python is installed: $PYTHON_VERSION"
fi


# Install or check Homebrew
print_status "yellow" "Checking Homebrew installation..."
if ! command -v brew &> /dev/null; then
    print_status "yellow" "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    check_success "Homebrew installed successfully"
else
    print_status "green" "✓ Homebrew is already installed"
fi


# Get user's home directory, used for Homebrew paths
USER_HOME=$HOME
print_status "yellow" "Setting up Homebrew in $USER_HOME/.zprofile..."


# Add Homebrew to path in .zprofile
if [ ! -f "$USER_HOME/.zprofile" ] || ! grep -q "brew shellenv" "$USER_HOME/.zprofile"; then
    echo >> "$USER_HOME/.zprofile"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$USER_HOME/.zprofile"
    eval "$(/opt/homebrew/bin/brew shellenv)"
    check_success "Homebrew path setup"
fi


# Install required packages
print_status "yellow" "Installing required packages..."

brew install libusb #needed for op-1 device communications in opietoolkitplus 
check_success "libusb installed"

brew install cairo #needed for cairosvg in GlitterTE
check_success "cairo installed"

brew install python-tk #needed for tkinter support 
check_success "python-tk installed"

brew install ffmpeg #needed for opie rips
check_success "ffmpeg installed"


# Set up environment variables, necessary for cairo to function correctly
print_status "yellow" "Setting up environment variables..."
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"
export DYLD_LIBRARY_PATH="/usr/local/lib:/opt/homebrew/lib:$DYLD_LIBRARY_PATH"


# Check and setup python's virtual environment
print_status "yellow" "Checking Python virtual environment..."
if [ ! -d ".vrepacker" ]; then
    print_status "yellow" "Creating virtual environment '.vrepacker'..."
    python3 -m venv .vrepacker
    check_success "Virtual environment has been created"
fi


# Activate python's virtual environment
print_status "yellow" "Activating virtual environment..."
source .vrepacker/bin/activate
check_success "Virtual environment activated"


# Install python dependencies in python's virtual environment
print_status "yellow" "Installing Python dependencies in virtual environment..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    check_success "Python dependencies installed"
else
    print_status "red" "requirements.txt not found in current directory"
    exit 1
fi
print_status "green" "Setup completed successfully!"


# Ask user if they want to start the program
read -p "Would you like to start op1REpackerGUI now? (Yes/No): " START_PROGRAM
if [[ $START_PROGRAM =~ ^[Yy]([Ee][Ss])?$ ]]; then
    print_status "green" "Starting op1REpackerGUI..."
    print_status "green" "You can start the program later by running: ./install.sh"
    python3 main.py
else
    print_status "yellow" "You can start the program later by running the install.sh script again or 'source .vrepacker/bin/activate' then 'python3 main.py'"
fi
