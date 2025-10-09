qa1_config = [
    8,
    2,
    28,
    69,
]
qa2_config = [
    # 一，
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    # 二，
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    # 三，四，
    [17, 4],
    # 五，六，
    [15, 4],
    # 七，
    [1, 2],
    [1, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    # 八，
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [4, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
    [1, 2],
    [2, 4],
]

import random


def random_sum_list(qa_num, n):
    nums = [0] * n
    for i in range(qa_num):
        idx = random.randint(0, n - 1)
        nums[idx] += 1
    random.shuffle(nums)
    return nums


def generate_qa_case(qa_sum, qa_config):
    qa_cases = []
    for config in qa_config:
        if type(config) is int:
            for _ in range(config):
                qa_line = random_sum_list(qa_sum, 3)
                qa_cases.append(qa_line)
        elif type(config) is list:
            cases_len, cases_num = config
            for _ in range(cases_len):
                qa_line = random_sum_list(qa_sum, cases_num)
                qa_cases.append(qa_line)
    return qa_cases


def modify_qa1_case(qa_case, index, new_values):
    if 0 <= index < len(qa_case):
        qa_case[index] = new_values
    else:
        raise ValueError("Invalid index or new_values length")


def modify_qa1_case89qa(qa_case, length8, length9):
    qa1_8 = qa_case[7]
    qa1_9 = qa_case[8]
    qa1_8_sum = sum(qa1_8)
    qa1_9_sum = sum(qa1_9)
    modify_qa1_case(qa_case, 7, random_sum_list(qa1_8_sum, length8))
    modify_qa1_case(qa_case, 8, random_sum_list(qa1_9_sum, length9))


def reset_case_sum(qa_case, reset_config):
    for index, reset_sum in reset_config:
        length = len(qa_case[index])
        modify_qa1_case(qa_case, index, random_sum_list(reset_sum, length))


def generate_qa_modify(qa_sum, qa_config, qa8_len, qa9_len, reset_config):
    qa_case = generate_qa_case(qa_sum, qa_config)
    modify_qa1_case89qa(qa_case, qa8_len, qa9_len)
    reset_case_sum(qa_case, reset_config)
    return qa_case


# 问卷1

qa1_sum = 5
qa1_8_len, qa1_9_len = 6, 6
reset_config = [
    # [3, qa1_sum - 1],
    # [5, qa1_sum - 2],
]

qa1_case1 = generate_qa_modify(qa1_sum, qa1_config, qa1_8_len, qa1_9_len, reset_config)
# print(qa1_case1)

qa1_8_len, qa1_9_len = 8, 8
reset_config = [
    # [3, qa1_sum - 1],
    # [5, qa1_sum - 2],
]

qa1_case2 = generate_qa_modify(qa1_sum, qa1_config, qa1_8_len, qa1_9_len, reset_config)
# print(qa1_case2)

qa1_8_len, qa1_9_len = 6, 6
reset_config = [
    [3, qa1_sum - 1],
    [5, qa1_sum - 2],
    [6, qa1_sum + 2],
]

qa1_case3 = generate_qa_modify(qa1_sum, qa1_config, qa1_8_len, qa1_9_len, reset_config)
# print(qa1_case3)

qa1_sum = 3
qa1_8_len, qa1_9_len = 6, 6
reset_config = [
    [3, qa1_sum - 1],
    [5, qa1_sum - 2],
    [8, qa1_sum + 2],
]

qa1_case4 = generate_qa_modify(qa1_sum, qa1_config, qa1_8_len, qa1_9_len, reset_config)
# print(qa1_case4)

# 问卷2

qa2_sum = 5
qa2_8_len, qa2_9_len = qa2_sum, qa2_sum
reset_config = [
    # [3, qa2_sum - 1],
    # [5, qa2_sum - 2],
]

qa2_case1 = generate_qa_modify(qa2_sum, qa2_config, qa2_8_len, qa2_9_len, reset_config)
# print(qa2_case1)

qa2_8_len, qa2_9_len = qa2_sum, qa2_sum
reset_config = [
    # [3, qa2_sum - 1],
    # [5, qa2_sum - 2],
]

qa2_case2 = generate_qa_modify(qa2_sum, qa2_config, qa2_8_len, qa2_9_len, reset_config)
# print(qa2_case2)

qa2_8_len, qa2_9_len = qa2_sum, qa2_sum
reset_config = [
    [3, qa2_sum - 1],
    [5, qa2_sum - 2],
    [6, qa2_sum + 2],
]

qa2_case3 = generate_qa_modify(qa2_sum, qa2_config, qa2_8_len, qa2_9_len, reset_config)
# print(qa2_case3)

qa2_sum = 20
qa2_8_len, qa2_9_len = qa2_sum, qa2_sum
reset_config = [
    [3, qa2_sum - 1],
    [5, qa2_sum - 2],
    [8, qa2_sum + 2],
]

qa2_case4 = generate_qa_modify(qa2_sum, qa2_config, qa2_8_len, qa2_9_len, reset_config)
# print(qa2_case4)

if __name__ == "__main__":
    # print("问卷1，案例1：\n", qa1_case1)
    print("问卷1，案例2：\n", qa1_case2)
    # print("问卷1，案例3：\n", qa1_case3)
    # print("问卷1，案例4：\n", qa1_case4)
    # print("问卷2，案例1：\n", qa2_case1)
    print("问卷2，案例2：\n", qa2_case2)
    # print("问卷2，案例3：\n", qa2_case3)
    # print("问卷2，案例4：\n", qa2_case4)
    print("Done")
