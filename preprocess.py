import torch
from torch.utils.data import Dataset, DataLoader

def levenshtein_distance(s1, s2):
    """
    https://en.wiki'ipedia.org/wiki/Levenshtein_distance
    """
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + (0 if s1[i-1]==s2[j-1] else 1)
            )
    return dp[m][n]

def clean_target_segmentation(src, tgt_line):
    tgt_segs = tgt_line.split()
    k = len(tgt_segs)
    n = len(src)
    dp = [[float('inf')] * (k+1) for _ in range(n+1)]
    bp = [[-1] * (k+1) for _ in range(n+1)]
    dp[0][0] = 0
    for i in range(n+1):
        for j in range(k):
            if dp[i][j] < float('inf'):
                for l in range(1, n - i + 1):
                    segment = src[i:i+l]
                    cost = levenshtein_distance(segment, tgt_segs[j])
                    if dp[i][j] + cost < dp[i+l][j+1]:
                        dp[i+l][j+1] = dp[i][j] + cost
                        bp[i+l][j+1] = l
    if dp[n][k] == float('inf'):
        return tgt_segs
    segments = []
    i, j = n, k
    while j > 0:
        l = bp[i][j]
        segments.append(src[i-l:i])
        i -= l
        j -= 1
    return list(reversed(segments))