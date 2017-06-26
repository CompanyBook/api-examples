#!/bin/bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

set -e

python3.5 --version
pip3.5 install requests

python3.5 python/search/service.py industry database GB
python3.5 python/search/service.py search database GB 511210
python3.5 python/search/service.py match apple
python3.5 python/similar_companies/service.py US0000000060704780
