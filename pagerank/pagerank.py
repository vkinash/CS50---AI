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
    # raise NotImplementedError
    t_model = dict()
    links_from_page = corpus[page]
    if not links_from_page:
        links_from_page = set(corpus.keys())
        probabilities_of_links_from_page = 1 / len(links_from_page)
        return {p: probabilities_of_links_from_page for p in links_from_page}

    probability_of_links_from_page = damping_factor / len(links_from_page)
    probability_of_all_links = (1-damping_factor) / len(corpus)

    for pg in corpus:
        if pg in links_from_page:
            t_model[pg] = probability_of_links_from_page + probability_of_all_links
        else:
            t_model[pg] = probability_of_all_links

    return t_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    pages_counter = {p: 0 for p in corpus}
    page = random.choice(list(pages_counter.keys()))
    samples = n
    while samples >= 0:
        pages_counter[page] += 1

        t_model = transition_model(corpus, page, damping_factor)

        page = random.choices(list(t_model.keys()), list(t_model.values()))[0]
        samples -= 1
    return {pg: prb/n for pg, prb in pages_counter.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    len_corpus = len(corpus)
    rank = 1/len_corpus
    p_ranks = {p: rank for p in corpus}

    for p in corpus:
        if not corpus[p]:
            corpus[p] = set(corpus.keys())

    while True:
        new_pr = dict()
        for page in corpus:
            pr_page = (((1-damping_factor) / len_corpus) +
                       (damping_factor *
                        sum([p_ranks[i] / len(corpus[i]) for i in corpus if page in corpus[i]])))

            new_pr[page] = pr_page

        if all([abs((p_ranks[p] - new_pr[p])) < 0.001 for p in corpus]):
            break

        p_ranks = new_pr
    return p_ranks


if __name__ == "__main__":
    main()
