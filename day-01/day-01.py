nums = [int(n) for n in open("input.txt").readlines()]
print(sum([curr > prev for curr, prev in zip(nums[1:], nums[:-1])]))
print(sum([sum(nums[i+1:i+4]) > sum(nums[i:i+3]) for i in range(len(nums) - 3)]))
