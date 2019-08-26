from io import StringIO
import unittest
from unittest.mock import patch
from meet_the_family.family_member import FamilyMember
from meet_the_family.family_tree import FamilyTree
from meet_the_family.constants import MALE, FEMALE


class TestFamilyTree(unittest.TestCase):
    def setUp(self):
        self.family_tree = FamilyTree()

    def test__add_member_to_family_tree(self):
        new_family_node_member1 = FamilyMember('Pita', MALE)
        new_family_node_member2 = FamilyMember('Wita', FEMALE)

        # Test add to existing family node as secondary member
        existing_family_node = self.family_tree._tree_index['Tritha']
        self.family_tree._add_member_to_family_tree(new_family_node_member1, None, existing_family_node)
        self.assertEqual(existing_family_node.secondary_member, new_family_node_member1)
        self.assertEqual(self.family_tree._tree_index[new_family_node_member1.name], existing_family_node)

        # Test create independent family node as primary member
        new_family_node = self.family_tree._add_member_to_family_tree(new_family_node_member2, None)
        self.assertEqual(new_family_node.primary_member, new_family_node_member2)
        self.assertEqual(self.family_tree._tree_index[new_family_node_member2.name], new_family_node)

    def test_add_child_member_to_family_tree(self):
        # Valid mother
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            new_family_node_member = FamilyMember('Ketu', MALE)
            self.family_tree.add_child_member_to_family_tree(
                new_family_node_member,
                'Satya'
            )
            self.assertEqual(mock_stdout.getvalue(), 'CHILD_ADDITION_SUCCEEDED\n')

        # Invalid mother
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            new_family_node_member = FamilyMember('Petu', MALE)
            self.family_tree.add_child_member_to_family_tree(
                new_family_node_member,
                'Vila'
            )
            self.assertEqual(mock_stdout.getvalue(), 'CHILD_ADDITION_FAILED\n')

        # Non-existent mother
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            new_family_node_member = FamilyMember('Letu', MALE)
            self.family_tree.add_child_member_to_family_tree(
                new_family_node_member,
                'Hila'
            )
            self.assertEqual(mock_stdout.getvalue(), 'PERSON_NOT_FOUND\n')

    def test_find_related_members(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Vila', 'Paternal-Uncle')
            self.assertEqual(mock_stdout.getvalue(), 'Chit Ish Aras\n')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Vyas', 'Maternal-Uncle')
            self.assertEqual(mock_stdout.getvalue(), 'Chit Ish Vich Aras\n')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Vasa', 'Paternal-Aunt')
            self.assertEqual(mock_stdout.getvalue(), 'Atya\n')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Yodhan', 'Maternal-Aunt')
            self.assertEqual(mock_stdout.getvalue(), 'Tritha\n')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Jaya', 'Sister-In-Law')
            self.assertEqual(mock_stdout.getvalue(), 'Tritha\n')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Vyan', 'Son')
            self.assertEqual(mock_stdout.getvalue(), 'Asva Vyas\n')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Lika', 'Daughter')
            self.assertEqual(mock_stdout.getvalue(), 'Vila Chika\n')

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Krpi', 'Brother-In-Law')
            self.assertEqual(mock_stdout.getvalue(), 'Asva\n')

        # Non-existent member
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Hila', 'Brother-In-Law')
            self.assertEqual(mock_stdout.getvalue(), 'PERSON_NOT_FOUND\n')

        # Unsupported relationship
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.family_tree.find_related_members('Vasa', 'Grand-Father')
            self.assertEqual(mock_stdout.getvalue(), 'UNSUPPORTED_RELATIONSHIP: Grand-Father\n')
