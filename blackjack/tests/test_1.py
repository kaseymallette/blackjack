# Set up directory
from run_test import Test
Test().find_dir()

# Import Path
from file_path import Path

# Set variables
test_shuffle = ['computer', 'riffle_perfect', 'riffle_clumpy']
test_shoes = 96
run_time = 7
shoe_fh = Path('shoe_test.csv').path
hand_fh = Path('hand_test.csv').path

# Run test
for shuffle in test_shuffle:
    for i in range(run_time):
        Test().run_test(shuffle, test_shoes, shoe_fh, hand_fh)
