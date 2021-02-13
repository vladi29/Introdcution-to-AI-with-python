import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    corpuslen = len(corpus.keys())
    PagesInside = corpus.get(page)
    TM = corpus.copy()

    if len(PagesInside) != 0:
        p1 = (1 - damping_factor)/corpuslen
        p2 = damping_factor/len(PagesInside)
        for page in PagesInside:
            TM[page] = p1 + p2
        for page in (corpus.keys()-PagesInside):
            TM[page] = p1
        #print(f"Transition model if: {TM}")
    else:
        p = 1/corpuslen
        for page in corpus.keys():
            TM[page] = p
        #print(f"Transition model else: {TM}")
    return TM

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    FirstPage = random.choices(list(corpus.keys()), k=1)[0]
    SP = dict()

    #Update of corpus with 0
    for page in corpus.keys():
        SP[page] = 0

    for i in range(n):
        SP[FirstPage] = SP[FirstPage] + 1
        TM = transition_model(corpus, FirstPage, damping_factor)
        Pages, Probs = zip(*TM.items())
        FirstPage = random.choices(Pages, weights=Probs, k=1)[0]  #Why [0]?
        #print(f"Prove Page: {FirstPage}")
        #print(f"Iteration: {i}")
    for page in TM.keys():
        SP[page] = SP[page]/n
    
    return SP 

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    N = len(corpus.keys())
    Const1 = (1-damping_factor)/N
    Const2 = 0
    IPR = dict()
    IPR1 = dict()
    IPR2 = dict()
    Iteration = True

    for page in corpus.keys():
        IPR[page] = 1/N
        IPR2[page] = True

    IPR1 = IPR.copy()

    while Iteration:
        for page in corpus.keys():
            for link in Links_List(corpus, page):
                Const2 = Const2 + IPR[link]/len(corpus.get(link))
            IPR[page] = Const1 + damping_factor*Const2
            Const2 = 0 
        for page in IPR.keys():
            if (abs(IPR[page] - IPR1[page]) <= 0.001 and IPR2[page]==True) or IPR2[page]==False:
                IPR2[page] = False
            else:
                IPR2[page] = True
        IPR1 = IPR.copy()
        if set(IPR2.values()) == {False}:
            Iteration = False
        else:
            Iteration = True
    return IPR          
    
def Links_List(corpus, page):
    #select the pages with link to page
    LinkToPage = []
    for Page in corpus.keys():
        for links in corpus.get(Page):
            if links == page:
                LinkToPage.append(Page)
    
    return LinkToPage
    
if __name__ == "__main__":
    main()
