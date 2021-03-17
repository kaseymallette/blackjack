# Set up directory
from run_test import Test
Test().find_dir()

# Import Path
from file_path import Path

# Set variables
test_shuffle = [1, 4, 7, 11, 'part_1', 'part_2', 'casino']
test_shoes = 96
run_time = 7
shoe_fh = Path('shoe_test_2.csv').path
hand_fh = Path('hand_test_2.csv').path

# Run test
for shuffle in test_shuffle:
    for i in range(run_time):
        Test().run_test(shuffle, test_shoes, shoe_fh, hand_fh)
