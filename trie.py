from document import *
from dataclasses import dataclass, field

TERMINATOR: str = '^'


@dataclass
class TrieNode:
    """A node in a standard trie."""
    children: dict = field(default_factory=dict)


# ------------------------- Helpers -------------------------


def trie_preprocess(word: str) -> str:
    """Returns a processed version of word appropriate for adding to the trie.
    Implement as you wish. The default version returns word as is .
    Args:
    - word: the word to process.
    Returns:
    An appropriately processed version of word.
    """
    final = ""
    for i in word:
        if i.isalpha():
            final += i
        try:
            integer = int(i)
            final += i
        except:
            continue

    return final


def prefix_tokenize(prefix_string: str):
    """Returns a list of prefixes tokenized from prefix_string and appropriate
    for prefix matching in the trie.
    Implement as you wish. The default splits at whitespace.
    Args:
    - prefix_string: the string to tokenize.
    Returns:
    A list of prefix tokens appropriate for querying the index.
    """
    lst = prefix_string.split()
    for i in range(len(lst)):
        lst[i] = trie_preprocess(lst[i])

    return lst


def add_word(node: TrieNode, word: str, locs: [Location]) -> None:
    """Adds word as a path beginning at node and saves the document locations of
    words.
    Args:
    - node: the addition has to start at node
    - word: the word to add
    - locs: the locations where word appears in different documents
    Returns:
    None.
    """

    i = 0  # to keep track of the letters that are present in the trie already
    for char in word:
        if char not in node.children.keys():
            # create a new node if its not in the trie
            node.children[char] = TrieNode()
        node = node.children[char]
        i += 1

    if TERMINATOR not in node.children.keys():
        node.children[TERMINATOR] = locs


def dfs(root: TrieNode, word: str) -> [(str, [Location])]:

    final = []
    for a in root.children.keys():
        if a == TERMINATOR:
            # append the word and the location
            final.append((word, root.children[a]))
        else:
            # run the function again for updated node and word
            final.extend(dfs(root.children[a], word+a))
    return final


def match(node: TrieNode, prefix: str, trace: str) -> [(str, [Location])]:
    """Returns prefix-matching words starting at node and the document locations
    where the words occur.
    Prefix-matching is performed by tracing down the tree rooted at node. trace
    keeps track of the string remaining to be traced. When this function is
    called the first time, i.e. not recurcsively, prefix and trace MUST be the
    same.
    Args:
    - node: start prefix-matching at node.
    - prefix: the prefix to be matched.
    - trace: string to trace at node, MUST be == prefix at first call
    Returns:
    List of pairs where each pair contains a prefix-matched word and the
    locations where the word appears."""

    if len(prefix) == 0:  # when completely traversed
        return dfs(node, trace)  # return possible suggestions
    else:
        for a in node.children.keys():
            if a == prefix[0]:
                node = node.children[a]
                # run the function again for updated node and prefix
                return match((node), prefix[1:], trace)


@dataclass
class Trie:
    """A standard trie."""
    _root: TrieNode = field(default_factory=TrieNode)

    def add_doc(self, doc: Document) -> None:
        """Adds words from doc to the trie.
        Args:
        - self: this trie, the one to add to. mandatory object reference.
        - doc: the document whose words are to be added.
        Returns:
        None.
        """
        for w, locs in doc.words():
            add_word(self._root, trie_preprocess(w), locs)

    def complete(self, words: str) -> [(str, [Location])]:
        """Returns prefix-matches in the trie to each of the words and their locations
        in their documents.
        Args:
        - self: this trie, the one to match in . mandatory object reference.
        - words: contains words to match
        Returns:
        A list of pairs where each pair contains a prefix-matched word from the
        trie and a list of the locations where the word occurs in documents.
        """
        words = prefix_tokenize(words)
        matches = []
        for w in words:
            matches.extend(match(self._root, w, w))
        return matches
