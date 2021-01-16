# Import necessary libraries
from run_test import Test

# Set up directory
Test().find_dir()

# Set variables
test_shuffle = 'part_2'
test_shoes = 96
run_time = 3

# Run test
for i in range(run_time):
    Test().run_test(test_shuffle, test_shoes)
