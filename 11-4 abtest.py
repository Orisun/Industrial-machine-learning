from __future__ import division
from collections import defaultdict
import random
import math

# 质数表
PRIME_TABLE = [998537, 998539, 998551, 998561, 998617, 998623, 998629, 998633, 998651, 998653]

def choose_strategy(uid, rnd=0):
    """根据uid生成[0,100)上的一个随机整数
    """
    prime = PRIME_TABLE[rnd % len(PRIME_TABLE)]
    random.seed(uid ^ prime)  # 质数的加入是为了保证各A/B试验之间的正交性
    return random.randint(0, 99)

total_user = 1000000  # 每组试验内用户的总数

def sequential_uid_generator():
    """顺序uid生成器
    """
    for i in xrange(total_user):
        yield i

def random_uid_generator():
    """随机uid生成器
    """
    for i in xrange(total_user):
        yield random.randint(1e12, 1e20)

def gen_test_group(test_count, rnd, uid_generator):
    """生成一个大组，有test_count个小组，每个小组是uid构成的set
    """
    set_list = []
    for i in xrange(test_count):
        set_list.append(set())

    for uid in uid_generator():
        stg = choose_strategy(uid, rnd)
        modulus = stg % test_count
        set_list[modulus].add(uid)
    return set_list

def test_random(uid_generator):
    """测试随机性
    """
    set_list = gen_test_group(100, 1, uid_generator)  # 分为100个小组
    for i, set in enumerate(set_list):
        ratio = len(set) / total_user
        # 每个小组的占比都应该是0.01，误差容忍度是0.001
        if math.fabs(ratio - 0.01) > 1e-3:
            print i, ratio

def test_orthogonality(set_list1, set_list2):
    """
    验证对于大组1中的每个小组而言，它在大组2的各个小组上的分布是均匀的
    :param set_list1: 大组1
    :param set_list2: 大组2
    """
    for set1 in set_list1:
        total = len(set1)
        count_dict = defaultdict(int)
        for ele in set1:
            for i, set2 in enumerate(set_list2):
                if ele in set2:
                    count_dict[i] += 1
                    break
        # set1的元素应该均匀地分布在各个set2中
        for ele, count in count_dict.iteritems():
            ratio = count / total
            # 每一份的占比都应该是1/len(set_list2)，误差容忍度是0.1/len(set_list2)
            if math.fabs(ratio - 1 / len(set_list2)) > 0.1 / len(set_list2):
                print ele, ratio

def test_cross(uid_generator):
    """验证两个大组之间的正交性
    """
    group_count = 10  # 10个大组
    set_list_list = []
    for i in xrange(group_count):
        set_list = gen_test_group(4, i + 1, uid_generator)  # 每个大组内4个小组
        set_list_list.append(set_list)
    for i in xrange(group_count):
        for j in xrange(i + 1, group_count):
            set_list1 = set_list_list[i]
            set_list2 = set_list_list[j]
            test_orthogonality(set_list1, set_list2)
            test_orthogonality(set_list2, set_list1)

# 顺序生成uid
print "sequential_uid_generator:"
print "test_random:"
test_random(sequential_uid_generator)  # 测试同一大组内，uid在各个试验上分布得是否均匀
print "test_cross:"
test_cross(sequential_uid_generator)  # 测试不同大组之间，uid的分布是否正交
# 随机生成uid
print "random_uid_generator:"
print "test_random:"
test_random(random_uid_generator)
print "test_cross:"
test_cross(random_uid_generator)