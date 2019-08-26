import unittest
from meet_the_family.family_member import FamilyMember


class TestFamilyMember(unittest.TestCase):
    def setUp(self):
        self.family_member = FamilyMember('Ram', 'male')

    def test_primary_member(self):
        self.assertEqual(self.family_member.name, 'Ram')

    def test_member_gender(self):
        self.assertEqual(self.family_member.gender, 'male')


if __name__ == '__main__':
    unittest.main()
