# Import necessary libraries
from run_test import Test

# Set up directory
Test().find_dir()

# Import Path
from file_path import Path

# Set variables
test_shuffle = 1
test_shoes = 96
run_time = 30
shoe_fh = Path('shoe_test_1.csv').path
hand_fh = Path('hand_test_1.csv').path
# Run test
for i in range(run_time):
    Test().run_test(test_shuffle, test_shoes, shoe_fh, hand_fh)
