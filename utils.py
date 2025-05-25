from collections import defaultdict
from pybktree import BKTree
_bk_tree = None
_word_groups = None

def load_words(file_path: str) -> list[str]:
    """Load and clean word list from a text file."""
    with open(file_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def get_word_groups():
    """Group words by their lengths for faster candidate filtering."""
    global _word_groups
    if _word_groups is None:
        word_list = load_words("amharic.txt")
        _word_groups = defaultdict(list)
        for word in word_list:
            _word_groups[len(word)].append(word)
    return _word_groups

def levenshtein(a: str, b: str) -> int:
    """Calculate Levenshtein distance between two strings."""
    dp = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
    return dp[-1][-1]


def get_candidate_words(word: str) -> list[str]:
    """Get only words that are within ±1 character in length."""
    groups = get_word_groups()
    target_len = len(word)
    candidates = []
    for delta in [-1, 0, 1]:
        key = target_len + delta
        candidates.extend(groups.get(key, []))
    return candidates


def get_suggestions(word: str, max_distance: int = 2, max_results: int = 5) -> list[str]:
    """Return top spelling suggestions using filtered candidates and Levenshtein distance."""
    candidates = get_candidate_words(word)

    results = []
    for candidate in candidates:
        dist = levenshtein(word, candidate)
        if dist <= max_distance:
            results.append((dist, candidate))

    results.sort(key=lambda x: x[0])
    return [w for _, w in results[:max_results]]