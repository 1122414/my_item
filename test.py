from scipy.stats import binomtest

# 执行单边检验（备择假设 p < 0.9）
result = binomtest(k=17, n=21, p=0.9, alternative='less')
print(f"单边 p 值: {result.pvalue:.3f}") 

# 执行双边检验（备择假设 p ≠ 0.9）
result = binomtest(k=17, n=21, p=0.9, alternative='two-sided')
print(f"双边 p 值: {result.pvalue:.3f}")  # 输出: 0.194