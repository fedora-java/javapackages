#!/usr/bin/env bash

dnf update -y
dnf install -y rpm-build python{,3} python{,3}-lxml python{,3}-six python{,3}-nose
