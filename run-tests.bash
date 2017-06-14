#!/bin/bash

python3.5 --version
pip3.5 install requests

echo "API_KEY='$1'" > python/search/authority.py
echo "API_KEY='$1'" > python/similar_companies/authority.py

python3.5 python/search/service.py industry database GB
python3.5 python/search/service.py search database GB 511210
python3.5 python/search/service.py match apple
python3.5 python/similar_companies/service.py US0000000060704780
