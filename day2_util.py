import itertools


def get_day2_possibility():
    ranks = []

    GA = [1, 4, 5, 8]
    GB = [2, 3, 6, 7]

    sumrepA = 0
    for iterA in itertools.permutations(GA):
        repA = 1
        if iterA[0] + iterA[3] == 9:
            repA = 2
        sumrepA += repA
        for iterB in itertools.permutations(GB):
            repB = 1
            if iterB[0] + iterB[3] == 9:
                repB = 2
            rank = []
            if iterA[0] > iterB[0]:
                rank.append(iterA[0])
                rank.append(iterB[0])
            else:
                rank.append(iterB[0])
                rank.append(iterA[0])
            if iterA[1] > iterB[1]:
                rank.append(iterA[1])
                rank.append(iterB[1])
            else:
                rank.append(iterB[1])
                rank.append(iterA[1])
            top4 = [
                [iterA[3], iterA[2], iterB[3], iterB[2]],
                [iterA[3], iterA[2], iterB[2], iterB[3]],
                [iterA[2], iterA[3], iterB[3], iterB[2]],
                [iterA[2], iterA[3], iterB[2], iterB[3]],
                [iterB[3], iterB[2], iterA[3], iterA[2]],
                [iterB[3], iterB[2], iterA[2], iterA[3]],
                [iterB[2], iterB[3], iterA[3], iterA[2]],
                [iterB[2], iterB[3], iterA[2], iterA[3]],

                [iterB[2], iterA[2], iterB[3], iterA[3]],
                [iterB[2], iterA[2], iterA[3], iterB[3]],
                [iterA[2], iterB[2], iterB[3], iterA[3]],
                [iterA[2], iterB[2], iterA[3], iterB[3]],
                [iterB[3], iterA[3], iterB[2], iterA[2]],
                [iterB[3], iterA[3], iterA[2], iterB[2]],
                [iterA[3], iterB[3], iterB[2], iterA[2]],
                [iterA[3], iterB[3], iterA[2], iterB[2]]
            ]
            for _ in range(repA * repB):
                for iter4 in top4:
                    real_rank = list(rank)
                    if iter4[0] < iter4[1]:
                        continue
                    real_rank.extend(iter4)
                    real_rank.reverse()
                    ranks.append(tuple(real_rank))
    inverted_rank_list = []
    for p in ranks:
        inverted_rank_list.append([p.index(l + 1) + 1 for l in range(len(p))])
    return inverted_rank_list


if __name__ == '__main__':
    ranks = get_day2_possibility()
    print(len(ranks))
    for i in range(10):
        print(ranks[i])
