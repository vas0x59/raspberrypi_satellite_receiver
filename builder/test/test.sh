#! /usr/bin/env bash

set -ex

python3 --version
pip3 --version

command -v rtl_sdr
command -v rtl_fm

command -v wxtoimg

echo "==OK=="
