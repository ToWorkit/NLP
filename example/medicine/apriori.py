import pandas as pd
# 自定义连接函数，用于实现L_{k-1}到C_k的连接
def connect_string(x, ms):
    # split 返回结果为list -> 'a' => ['a']
    x = list(map(lambda i: sorted(i.split(ms)), x))
    print(x, '____1')
    l = len(x[0])
    r = []
    print(x[1][:0], '____2')
    print(sorted([x[l-2][l-1], x[0][l-1]]), '___3')
    for i in range(len(x)):
        for j in range(i, len(x)):
            if x[i][:l-1] == x[j][:l-1] and x[i][l-1] != x[j][l-1]:
                r.append(x[i][:l-1] + sorted([x[j][l-1], x[i][l-1]]))
    return r

# 寻找关联规则的函数
def find_rule(d, support, confidence, ms = u'-->'):
    # 定义输出结果
    result = pd.DataFrame(index = ['support', 'confidence'])
    # 支持度序列 平均数(每一项的和(列) / 长度(列)) => 项集的频率
    support_series = 1.0 * d.sum() / len(d)
    # 初步根据支持度筛序, 取索引值('a', 'b, 'c'...)
    print(list(support_series[support_series > support]), '___4')
    column = list(support_series[support_series > support].index)
    print(column, '___5')
    
    k = 0
    while len(column) > 1:
        k += 1
        print('\n正在进行第{}次搜索...'.format(k))
        column = connect_string(column, ms)
        print(column, '___6')
        print('数目: %s' % len(column))

        # 新一批支持度的计算函数
        # 按列(竖着看)计算乘积
        sf = lambda i: d[i].prod(axis = 1, numeric_only = True)
        # 创建连接数据（转置与原数据维度保持一致），这一操作很耗时间，耗内存，当数据集较大时，可以考虑并行计算进行优化
        d_2 = pd.DataFrame(list(map(sf, column)), index = [ms.join(i) for i in column]).T
        print(d_2, '___7')
        print([ms.join(i) for i in column], '___8')
        # 计算连接后的支持度 -> 平均数(每一项的和(列) / 长度(列)) => 项集的频率
        support_series_2 = 1.0 * d_2[[ms.join(i) for i in column]].sum() / len(d)
        print(type(support_series_2), '___9')
        # 新一轮支持度筛序,去索引值
        column = list(support_series_2[support_series_2 > support].index)
        print(column, '__10')
        # 合并支持度序列, Series需要赋值操作
        support_series = support_series.append(support_series_2)
        print(support_series, '__11')
        column2 = []

        # 遍历可能的推理，如 {A, B, c}究竟是 A + B --> C 还是B + C --> A 还是 C + A --> B
        for i in column:
            i = i.split(ms)
            for j in range(len(i)):
                column2.append(i[:j] + i[j + 1:] + i[j : j + 1])
        print(column2, '__12')

        # 定义置信度序列
        cofidence_series = pd.Series(index = [ms.join(i) for i in column2])
        # 计算置信度序列
        for i in column2:
            cofidence_series[ms.join(i)] = support_series[ms.join(sorted(i))] / support_series[ms.join(i[:len(i) - 1])]
        print(cofidence_series, '__13')

        # 置信度筛选,去索引值
        for i in cofidence_series[cofidence_series > confidence].index:
            result[i] = 0.0
            result[i]['confidence'] = cofidence_series[i]
            result[i]['support'] = support_series[ms.join(sorted(i.split(ms)))]
    print(result, '__14')
    # 结果整理，输出
    result = result.T.sort_values(['confidence', 'support'], ascending = False)
    print('\n结果为')
    print(result)
    return result
