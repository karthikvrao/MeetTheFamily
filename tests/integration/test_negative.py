from io import StringIO
import unittest
from unittest.mock import patch
from meet_the_family.family_tree import FamilyTree


@patch('sys.stdout', new_callable=StringIO)
class TestNegative(unittest.TestCase):
    def setUp(self):
        self.family_tree = FamilyTree()

    def test_get_siblings_for_non_existent_member(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Ram Siblings')
        self.assertEqual(mock_stdout.getvalue(), 'PERSON_NOT_FOUND\n')

    def test_add_child_to_non_mother_member(self, mock_stdout):
        self.family_tree.perform_operation('ADD_CHILD Atya Tyor Female')
        self.assertEqual(mock_stdout.getvalue(), 'CHILD_ADDITION_FAILED\n')

    def test_get_non_existent_paternal_aunt(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Laki Paternal-Aunt')
        self.assertEqual(mock_stdout.getvalue(), 'NONE\n')

    def test_get_non_existent_maternal_aunt(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Vasa Maternal-Aunt')
        self.assertEqual(mock_stdout.getvalue(), 'NONE\n')


if __name__ == '__main__':
    unittest.main()
