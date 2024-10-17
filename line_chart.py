import pandas as pd
import matplotlib.pyplot as plt

# 设置绘图样式
plt.style.use('seaborn-whitegrid')
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'times new roman'
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 5  # 修正为 markersize

# 读取 CSV 文件
data = pd.read_csv('/Users/zhongzhiyi/Desktop/tarjan algorithm/1000_0.0001_erdos_renyi_network_results.csv')

# 计算比例
total_samples = 1000
data['strong_ratio'] = data['strong'] / total_samples
data['unilateral_ratio'] = data['unilateral'] / total_samples
data['weak_ratio'] = data['weak'] / total_samples
data['disconnected_ratio'] = data['disconnected'] / total_samples

# 创建图形
plt.figure(figsize=(14, 6))

# 绘制 scc_mean 和 p_value 的点状图
plt.subplot(1, 2, 1)
plt.plot(data['p_value'], data['scc_mean'], label='SCC Mean', color='orange', marker='o')
plt.title('The Number of SCCs vs. p_value')
plt.xlabel('p_value')
plt.ylabel('The Number of SCC')
plt.xticks(ticks=data['p_value'][::len(data['p_value']) // 10])
plt.grid(True)
plt.legend(loc='upper right')

# 绘制强连通、单向连通、弱连通、断开的比例图
plt.subplot(1, 2, 2)
plt.plot(data['p_value'], data['strong_ratio'], label='Strong', marker='o', color='blue')
plt.plot(data['p_value'], data['unilateral_ratio'], label='Unilateral', marker='o', color='green')
plt.plot(data['p_value'], data['weak_ratio'], label='Weak', marker='o', color='orange')
plt.plot(data['p_value'], data['disconnected_ratio'], label='Disconnected', marker='o', color='red')
plt.title('Proportions of Network Types vs. p_value')
plt.xlabel('p_value')
plt.ylabel('Proportion')
plt.xticks(ticks=data['p_value'][::len(data['p_value']) // 10])
plt.ylim(0, 1.1)

plt.legend(loc='upper right')


# 调整布局
plt.tight_layout()

# 导出图片
plt.savefig('1000_network_analysis_results.png', dpi=300, bbox_inches='tight')  # 确保图像边界紧凑

