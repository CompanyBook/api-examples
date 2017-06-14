#!/bin/bash

echo "API_KEY='$1'" > python/search/authority.py

python python/search/service.py industry database GB
python python/search/service.py search database GB 511210
python python/search/service.py match apple
python python/similar_companies/service.py US0000000060704780
