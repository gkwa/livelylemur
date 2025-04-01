#!/bin/bash

# System Installation and Setup Script

# Create linuxbrew user without password
useradd -m -s /bin/bash linuxbrew
echo 'linuxbrew ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/linuxbrew
chmod 440 /etc/sudoers.d/linuxbrew

# Update package lists with force architecture
dpkg --add-architecture amd64
apt-get update

# Install essential packages
apt-get -y install curl git file imagemagick gcc

# Install graphics libraries with alternative package names
apt-get install -y libgl1 libglib2.0-0t64 libglx0

# Switch to linuxbrew home directory
cd /home/linuxbrew

# Install Homebrew for the linuxbrew user with automatic yes
sudo -u linuxbrew HOMEBREW_NO_INTERACTIVE_PROMPT=1 NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Set up Homebrew environment for the linuxbrew user
echo '' >> /home/linuxbrew/.bashrc
echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"' >> /home/linuxbrew/.bashrc
echo 'export MANPATH="/home/linuxbrew/.linuxbrew/share/man:$MANPATH"' >> /home/linuxbrew/.bashrc
echo 'export INFOPATH="/home/linuxbrew/.linuxbrew/share/info:$INFOPATH"' >> /home/linuxbrew/.bashrc
echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"' >> ~/.profile

source ~/.profile

# Explicitly set the PATH for subsequent commands
export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"

# Run Homebrew commands
sudo -Hi -u linuxbrew /home/linuxbrew/.linuxbrew/bin/brew install uv gcc tesseract

echo "Installation script completed successfully!"
