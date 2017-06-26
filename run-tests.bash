#!/bin/bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

set -e

python3.5 --version
pip3.5 install requests

python3.5 python/search.py industry database GB
python3.5 python/search.py search database GB 511210
python3.5 python/search.py match apple
python3.5 python/similar_companies.py US0000000060704780
python3.5 python/news.py relation US0000000060704780 competitors
