import numpy as np
feature_2 = []
with open('../txt/feature2.txt', 'r') as fp:
    for line in fp:
        row = []
        num = line.strip().split('\t')[0]
        fvs = line.strip().split('\t')[1].split(',')
        row.append(num)
        for x in range(len(fvs)):
            row.append(fvs[x])
        feature_2.append(row)

    print(feature_2)
    feature_2 = np.array(feature_2)

    feature_2 = feature_2[:,1:]
    feature_2.tolist()
    print(feature_2)
    pass

