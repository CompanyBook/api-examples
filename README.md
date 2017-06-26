# api-examples
A collection of examples of Companybook API use

## Python
### Prerequisites
Python 3 (not tested with Python 2)

requests (conda install requests or pip install requests)

You need to create a file called authority.py in the python directory: *python/authority.py*.

This file needs to define your **API_KEY** like this:

```
API_KEY='your api key here'
```

## Search
Contains a command line tool to query Companybook. 

To find the most prominent industry codes for a query:
```
python python/search.py industry database GB
```

To find the top result for a query within an industry:
```
python python/search.py search database GB 511210
```

To find the most likely Companybook IDs for a given company name:
```
python python/search.py match apple
```

## Similar Companies
Contains a command line tool to query Companybook for companies similar to a given company.
The example company must be given as a companybook id.
Similar companies in this respect are companies that are similar in texutal web site description,
revenue, industry and geographic location.

Running this is simple given the authority.py file is present:
```
python python/similar_companies.py US0000000060704780
```

## News Relations
Contains a command line tool to query Companybook for companies with specific relations to
a company. I.e the competitors of a company. Other relations are documented in the developer
portal.

```
python python/news.py relation US0000000060704780 competitors
```