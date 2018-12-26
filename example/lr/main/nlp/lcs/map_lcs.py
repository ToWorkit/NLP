# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys

def cal_lcs_sim(first_str, second_str):
    # 构建容器
    len_vv = [[0] * 50] * 50

    first_str = unicode(first_str, "utf-8", errors = "ignore")
    second_str = unicode(second_str, "utf-8", errors = "ignore")

    len_1 = len(first_str)
    len_2 = len(second_str)

    for i in range(1, len_1 + 1):
        for j in range(1, len_2 + 1):
            if first_str[i - 1] == second_str[j - 1]:
                len_vv[i][j] = 1 + len_vv[i - 1][j - 1]
            else:
                len_vv[i][j] = max(len_vv[i - 1][j], len_vv[i][j - 1])

    return float(float(len_vv[len_1][len_2] * 2) / float(len_1 + len_2))

# 标准输入
for line in sys.stdin:
    ss = line.strip().split("\t")
    if len(ss) != 2:
        continue
    first_str = ss[0].strip()
    second_str = ss[1].strip()

    sim_score = cal_lcs_sim(first_str, second_str)
    print("\t".join([first_str, second_str, str(sim_score)]))
