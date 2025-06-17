#bm25S_func()
"""
adapted from BM25S by Poppy Riddle
June 2025

References:
BM25 Sparse: https://bm25s.github.io/
documentation: https://github.com/xhluca/bm25s

Inputs: 
    file location is coded into where the indexed files are stored. This should be local. 
    your working folder should have a 'lns_bm25' folder with the indexed corpus. 
    It should include:
    -corpus.jsonl
    -corpus.mmindex.json
    -data.csc.index.npy
    -indices.csc.index.npy
    -indptr.csc.index.npy
    -params.index.json
    -vocab.index.json

Outputs: 
    for a query, returns top-k highest scoring documents. Currently set to 3

Requirements:
bm25s
os
pickle

"""


import bm25s
import os
import pickle

# ...and load them when you need them
retriever = bm25s.BM25.load("lns_bm25", load_corpus=True)
# set load_corpus=False if you don't need the corpus

#load the url_list
with open('url.pkl', 'rb') as file:
    url_list = pickle.load(file)
print(len(url_list))

def run_query():
    """
    Runs a query against the BM25 retriever and prints the top-k results.

    Returns:
        None
    """
    #You can now search the corpus with a query
    query = input("what is your query")
    
    #you can also add a stemmer here as an arg: stemmer=stemmer
    query_tokens = bm25s.tokenize(query)
    results, scores = retriever.retrieve(query_tokens, k=3)

    #note: if you pass a new corpus here, it must have the same length as your indexed corpus
    #in this case, I am passing the new list 'url_list'
    results = retriever.retrieve(query_tokens, corpus=url_list, k=3, return_as="documents")
    #loop through results
    if all(score ==0.00 for score in scores[0]):
        print("Nothing found, please try another query.")
    else:
        for i in range(results.shape[1]):
            doc, score = results[0, i], scores[0, i]
            print(f"Rank {i+1} (score: {score:.2f}): {doc}")


def main():
    print(run_query())
    
if __name__ == "__main__":
    main()