"""
From Phil's network file
re-written in Python
April 2025
Poppy Riddle

input files come from 'file_to_works.csv.py' and 'citations.csv.py'
there are two files that should be in a data subfolder:
citations.csv
works.csv

This works with metadata pulled from OpenAlex
"""

import pandas as pd
import numpy as np

# Read CSV files
works = pd.read_csv('data/works.csv')
citations = pd.read_csv('data/citations.csv')

# Fix data types to make sure all are string - could expand to check before doing this
works['id'] = works['id'].astype(str)
citations['citing_id'] = citations['citing_id'].astype(str)
citations['cited_id'] = citations['cited_id'].astype(str)

# EDGES ----
# Bibliographic coupling ----

net_bc = works[['id']].merge(citations, left_on='id', right_on='citing_id', how='inner')
net_bc = net_bc.merge(citations, left_on='id', right_on='citing_id', how='inner')
net_bc = net_bc[net_bc['citing_id'].isin(works['id'])]
net_bc = net_bc[['id', 'cited_id']].rename(columns={'id': 'source', 'cited_id': 'target'})
net_bc['weight'] = 1
net_bc['type'] = 'undirected'

net_bc = net_bc.groupby(['source', 'target']).sum().reset_index()
net_bc['source'] = net_bc['source'].astype(float)
net_bc['target'] = net_bc['target'].astype(float)

# Direct citations ----
net_dc = citations[citations['citing_id'].isin(works['id'])]
net_dc = net_dc[['citing_id', 'cited_id']].rename(columns={'citing_id': 'source', 'cited_id': 'target'})
net_dc['weight'] = 1
net_dc['type'] = 'directed'

net_dc = net_dc.groupby(['source', 'target']).sum().reset_index()
net_dc['source'] = net_dc['source'].astype(float)
net_dc['target'] = net_dc['target'].astype(float)

# Co-citation ----
net_cc = works[['id']].merge(citations, left_on='id', right_on='cited_id', how='inner')
net_cc = net_cc.merge(citations, left_on='id', right_on='cited_id', how='inner')
net_cc = net_cc[net_cc['cited_id'].isin(works['id'])]
net_cc = net_cc[['id', 'citing_id']].rename(columns={'id': 'source', 'citing_id': 'target'})
net_cc['weight'] = 1
net_cc['type'] = 'undirected'

net_cc = net_cc.groupby(['source', 'target']).sum().reset_index()
net_cc['source'] = net_cc['source'].astype(float)
net_cc['target'] = net_cc['target'].astype(float)

# Combined ----
net_bc_cc_dc = pd.concat([net_cc, net_bc, net_dc], ignore_index=True)
net_bc_cc_dc = net_bc_cc_dc.groupby(['source', 'target']).sum().reset_index()

# Export Network Files
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

net_cc.to_sql('net_cc', engine, if_exists='replace')
net_dc.to_sql('net_dc', engine, if_exists='replace')
net_bc.to_sql('net_bc', engine, if_exists='replace')
net_bc_cc_dc.to_sql('net_bc_cc_dc', engine, if_exists='replace')

net_cc.to_excel('data/networks/net_cc.xlsx')
net_dc.to_excel('data/networks/net_dc.xlsx')
net_bc.to_excel('data/networks/net_bc.xlsx')
net_bc_cc_dc.to_excel('data/networks/net_bc_cc_dc.xlsx')