# -*- mode: ruby -*-
# Vagrantfile — provisions the 3-VM lab (manager, Windows victim, Linux
# victim) on a shared host-only network. Requires VirtualBox + Vagrant.
#
#   vagrant up manager
#   vagrant up linux_victim
#   vagrant up windows_victim   # requires a Vagrant box with a Windows eval image
#
# Windows boxes aren't freely redistributable, so windows_victim points at
# a placeholder box name — swap in your own Vagrant box built from
# Microsoft's free evaluation ISO (see docs/02-victim-vm-setup.md).

Vagrant.configure("2") do |config|

  config.vm.define "manager" do |m|
    m.vm.box = "ubuntu/jammy64"
    m.vm.hostname = "wazuh-manager"
    m.vm.network "private_network", ip: "192.168.56.10"
    m.vm.provider "virtualbox" do |vb|
      vb.memory = 4096
      vb.cpus = 2
    end
    m.vm.provision "shell", path: "install/install-wazuh-manager.sh"
  end

  config.vm.define "linux_victim" do |v|
    v.vm.box = "ubuntu/jammy64"
    v.vm.hostname = "linux-victim"
    v.vm.network "private_network", ip: "192.168.56.21"
    v.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus = 1
    end
    v.vm.provision "shell", path: "install/setup-linux-victim.sh", args: "192.168.56.10"
  end

  config.vm.define "windows_victim" do |w|
    w.vm.box = "REPLACE_WITH_YOUR_WINDOWS_EVAL_BOX"  # see docs/02-victim-vm-setup.md
    w.vm.hostname = "win-victim"
    w.vm.network "private_network", ip: "192.168.56.20"
    w.vm.provider "virtualbox" do |vb|
      vb.memory = 4096
      vb.cpus = 2
    end
    w.vm.provision "shell", path: "install/setup-windows-victim.ps1", args: "-ManagerIp 192.168.56.10"
  end

end
