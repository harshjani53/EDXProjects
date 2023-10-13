import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = pagesParse(sys.argv[1])
    ranks = samplesPagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = pageRank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def pagesParse(directory):
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


def transitionModel(corpus, page, dampingFactor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probs = {}

    dictionaryLength = len(corpus.keys())
    pagesLength = len(corpus[page])

    if len(corpus[page]) < 1:
        for key in corpus.keys():
            probs[key] = 1 / dictionaryLength

    else:
        randoms = (1 - dampingFactor) / dictionaryLength
        evens = dampingFactor / pagesLength

        for key in corpus.keys():
            if key not in corpus[page]:
                probs[key] = randoms
            else:
                probs[key] = evens + randoms

    return probs


def samplesPagerank(corpus, dampingFactor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # prepare dictionary with number of samples == 0
    samples = corpus.copy()
    for i in samples:
        samples[i] = 0
    sample = None


    for _ in range(n):
        if sample:
            distribution = transitionModel(corpus, sample, dampingFactor)
            distributionList = list(distribution.keys())
            distributionWeights = [distribution[i] for i in distribution]
            sample = random.choices(distributionList, distributionWeights, k=1)[0]
        else:

            sample = random.choice(list(corpus.keys()))


        samples[sample] += 1


    for item in samples:
        samples[item] /= n

    return samples


def pageRank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_number = len(corpus)
    old_dict = {}
    new_dict = {}

    for page in corpus:
        old_dict[page] = 1 / pages_number

    while True:
        for page in corpus:
            temp = 0
            for linking_page in corpus:

                if page in corpus[linking_page]:
                    temp += (old_dict[linking_page] / len(corpus[linking_page]))

                if len(corpus[linking_page]) == 0:
                    temp += (old_dict[linking_page]) / len(corpus)
            temp *= damping_factor
            temp += (1 - damping_factor) / pages_number

            new_dict[page] = temp

        difference = max([abs(new_dict[x] - old_dict[x]) for x in old_dict])
        if difference < 0.001:
            break
        else:
            old_dict = new_dict.copy()

    return old_dict

if __name__ == "__main__":
    main()
