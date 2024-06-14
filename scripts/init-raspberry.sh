#!/bin/env bash

# This script is used to initialize a raspberry pi with k3s (not tested yet, all manually executed)

read -rp "Enter the hostname of the raspberry: " hostname

echo "cgroup_memory=1 cgroup_enable=memory" | sudo tee -a /boot/firmware/cmdline.txt
sudo reboot

# Install k3s
sudo curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--tls-san ${hostname}" sh -
