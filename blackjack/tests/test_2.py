# Import necessary libraries
from run_test import Test

# Set up directory
Test().find_dir()

# Set variables
test_shuffle = [1, 3, 5, 9, 15, 'part_1', 'part_2', 'casino']
test_shoes = 96
run_time = 3

# Run test
for shuffle in test_shuffle:
    for i in range(run_time):
        Test().run_test(shuffle, test_shoes)
