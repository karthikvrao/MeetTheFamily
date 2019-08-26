from io import StringIO
import unittest
from unittest.mock import patch
from meet_the_family.family_tree import FamilyTree


@patch('sys.stdout', new_callable=StringIO)
class TestPositive(unittest.TestCase):
    def setUp(self):
        self.family_tree = FamilyTree()

    def test_get_son(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Anga Son')
        self.assertEqual(mock_stdout.getvalue(), 'Chit Ish Vich Aras\n')

    def test_get_siblings(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Aras Siblings')
        self.assertEqual(mock_stdout.getvalue(), 'Chit Ish Vich Satya\n')

    def test_add_child(self, mock_stdout):
        self.family_tree.perform_operation('ADD_CHILD Satya Ketu Male')
        self.assertEqual(mock_stdout.getvalue(), 'CHILD_ADDITION_SUCCEEDED\n')

    def test_get_paternal_uncle(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Vila Paternal-Uncle')
        self.assertEqual(mock_stdout.getvalue(), 'Chit Ish Aras\n')

    def test_get_maternal_uncle(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Vyas Maternal-Uncle')
        self.assertEqual(mock_stdout.getvalue(), 'Chit Ish Vich Aras\n')

    def test_get_paternal_aunt(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Vasa Paternal-Aunt')
        self.assertEqual(mock_stdout.getvalue(), 'Atya\n')

    def test_get_maternal_aunt(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Yodhan Maternal-Aunt')
        self.assertEqual(mock_stdout.getvalue(), 'Tritha\n')

    def test_get_sister_in_law(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Jaya Sister-In-Law')
        self.assertEqual(mock_stdout.getvalue(), 'Tritha\n')

    def test_get_daughter(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Lika Daughter')
        self.assertEqual(mock_stdout.getvalue(), 'Vila Chika\n')

    def test_get_brother_in_law(self, mock_stdout):
        self.family_tree.perform_operation('GET_RELATIONSHIP Krpi Brother-In-Law')
        self.assertEqual(mock_stdout.getvalue(), 'Asva\n')


if __name__ == '__main__':
    unittest.main()
