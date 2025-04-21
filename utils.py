from pybktree import BKTree

def levenshtein(a: str, b: str) -> int:
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

def load_words(file_path: str) -> list[str]:
    with open(file_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

word_list = load_words("amharic.txt")
bk_tree = BKTree(levenshtein, word_list)

def get_suggestions(word: str, max_distance: int = 2, max_results: int = 5) -> list[str]:
    results = bk_tree.find(word, max_distance)
    results.sort(key=lambda x: x[0])
    return [w for _, w in results[:max_results]]