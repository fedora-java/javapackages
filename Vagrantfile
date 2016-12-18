# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
dnf update -y
dnf install -y \
    rpm-build \
    make \
    asciidoc \
    dia \
    which \
    xmlto \
    python{,3} \
    python{,3}-lxml \
    python{,3}-six \
    python{,3}-nose \
    python{,3}-coverage
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "fedora-25"
  config.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/25/CloudImages/x86_64/images/Fedora-Cloud-Base-Vagrant-25-1.3.x86_64.vagrant-libvirt.box"
  config.vm.provision :shell, inline: $script
  # workaround for intentionally broken symlinks in test suite: https://github.com/mitchellh/vagrant/issues/5471
  config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__args: ["--verbose", "--archive", "--delete", "-z"]
end
