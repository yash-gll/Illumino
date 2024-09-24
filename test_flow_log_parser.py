import unittest
import os
from flow_log_parser import load_lookup_table, parse_flow_logs, write_output

class TestFlowLogParserWithFiles(unittest.TestCase):
    
    def setUp(self):
        # Setting up file paths for the tests
        self.test_dir = os.path.join(os.path.dirname(__file__), 'tests')

        # File paths for test case 1
        self.flow_log_file_1 = os.path.join(self.test_dir, 'flow_logs_test_1.txt')
        self.lookup_table_file_1 = os.path.join(self.test_dir, 'lookup_table_test_1.csv')
        self.expected_output_file_1 = os.path.join(self.test_dir, 'expected_output_test_1.txt')
        self.output_file_1 = os.path.join(self.test_dir, 'output_test_1.txt')

        # File paths for test case 2
        self.flow_log_file_2 = os.path.join(self.test_dir, 'flow_logs_test_2.txt')
        self.lookup_table_file_2 = os.path.join(self.test_dir, 'lookup_table_test_2.csv')
        self.expected_output_file_2 = os.path.join(self.test_dir, 'expected_output_test_2.txt')
        self.output_file_2 = os.path.join(self.test_dir, 'output_test_2.txt')
    
    def compare_files(self, file1, file2):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            content1 = f1.read().strip()
            content2 = f2.read().strip()

            content1 = sorted([line.strip() for line in content1])
            content2 = sorted([line.strip() for line in content2])

            self.assertEqual(content1, content2, f"Files {file1} and {file2} are not equal.")
    
    def test_flow_log_parser_with_file_1(self):
        # Test case 1: Using flow_logs_test_1.txt and lookup_table_test_1.csv
        
        # Load the lookup table
        lookup_table = load_lookup_table(self.lookup_table_file_1)
        # Parse flow logs and get the counts
        tag_count, port_protocol_count, untagged_count = parse_flow_logs(self.flow_log_file_1, lookup_table)
        # Write output to a file
        write_output(tag_count, port_protocol_count, untagged_count, self.output_file_1)
        # Compare output file with expected output
        self.compare_files(self.output_file_1, self.expected_output_file_1)
    
    def test_flow_log_parser_with_file_2(self):
        # Test case 2: Using flow_logs_test_2.txt and lookup_table_test_2.csv
        
        # Load the lookup table
        lookup_table = load_lookup_table(self.lookup_table_file_2)
        # Parse flow logs and get the counts
        tag_count, port_protocol_count, untagged_count = parse_flow_logs(self.flow_log_file_2, lookup_table)
        # Write output to a file
        write_output(tag_count, port_protocol_count, untagged_count, self.output_file_2)
        # Compare output file with expected output
        self.compare_files(self.output_file_2, self.expected_output_file_2)
    
    def tearDown(self):
        # Clean up the output files after the tests are run
        if os.path.exists(self.output_file_1):
            os.remove(self.output_file_1)
        if os.path.exists(self.output_file_2):
            os.remove(self.output_file_2)

if __name__ == '__main__':
    unittest.main()
