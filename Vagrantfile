# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.vm.box = "fedora-22"
  config.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/22/Cloud/x86_64/Images/Fedora-Cloud-Base-Vagrant-22-20150521.x86_64.vagrant-libvirt.box"
  config.vm.provision :shell, path: "vagrant_bootstrap.sh"
  # workaround for intentionally broken symlinks in test suite: https://github.com/mitchellh/vagrant/issues/5471
  config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__args: ["--verbose", "--archive", "--delete", "-z"]
end
