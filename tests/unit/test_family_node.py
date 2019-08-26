import unittest
from meet_the_family.family_member import FamilyMember
from meet_the_family.family_node import FamilyNode
from meet_the_family.constants import MALE, FEMALE


class TestFamilyNode(unittest.TestCase):
    def setUp(self):
        self.family_root_node_father = FamilyMember('Shan', MALE)
        self.family_root_node_mother = FamilyMember('Anga', FEMALE)
        self.root_node = FamilyNode(self.family_root_node_father)
        self.root_node.secondary_member = self.family_root_node_mother

        self.family_node1_member1 = FamilyMember('Chit', MALE)
        self.family_node1_member2 = FamilyMember('Amba', FEMALE)
        self.family_node1 = FamilyNode(self.family_node1_member1, self.root_node)
        self.family_node1.secondary_member = self.family_node1_member2
        self.root_node.child_nodes.append(self.family_node1)

        self.family_node2_member1 = FamilyMember('Ish', MALE)
        self.family_node2 = FamilyNode(self.family_node2_member1, self.root_node)
        self.root_node.child_nodes.append(self.family_node2)

        self.family_node3_member1 = FamilyMember('Vich', MALE)
        self.family_node3_member2 = FamilyMember('Lika', FEMALE)
        self.family_node3 = FamilyNode(self.family_node3_member1, self.root_node)
        self.family_node3.secondary_member = self.family_node3_member2
        self.root_node.child_nodes.append(self.family_node3)

        self.family_node4_member1 = FamilyMember('Aras', MALE)
        self.family_node4_member2 = FamilyMember('Chitra', FEMALE)
        self.family_node4 = FamilyNode(self.family_node4_member1, self.root_node)
        self.family_node4.secondary_member = self.family_node4_member2
        self.root_node.child_nodes.append(self.family_node4)

        self.family_node5_member1 = FamilyMember('Satya', FEMALE)
        self.family_node5_member2 = FamilyMember('Vyan', MALE)
        self.family_node5 = FamilyNode(self.family_node5_member1, self.root_node)
        self.family_node5.secondary_member = self.family_node5_member2
        self.root_node.child_nodes.append(self.family_node5)

    def test_primary_member(self):
        self.assertEqual(self.root_node.primary_member, self.family_root_node_father)

    def test_parent_node(self):
        self.assertEqual(self.root_node._parent_node, None)
        self.assertEqual(self.family_node1._parent_node, self.root_node)

    def test_secondary_member(self):
        self.assertEqual(self.root_node.secondary_member, self.family_root_node_mother)

    def test_set_secondary_member(self):
        new_family_node_member = FamilyMember('Bika', FEMALE)
        self.family_node2.set_secondary_member(new_family_node_member)
        self.assertEqual(self.family_node2.secondary_member, new_family_node_member)

    def test_add_child(self):
        new_family_node_member = FamilyMember('Dritha', FEMALE)
        new_family_node = FamilyNode(new_family_node_member, self.family_node1)
        self.family_node1.add_child(new_family_node)
        self.assertEqual(self.family_node1.child_nodes, [new_family_node])
        
    def test_get_member(self):
        self.assertEqual(self.root_node.get_member(self.root_node.primary_member.name), self.root_node.primary_member)
        self.assertEqual(self.root_node.get_member(self.root_node.secondary_member.name), self.root_node.secondary_member)

    def test_has_couple(self):
        self.assertTrue(self.family_node1.has_couple())
        self.assertFalse(self.family_node2.has_couple())

    def test_get_sibling_nodes(self):
        self.assertEqual(
            list(self.family_node1.get_sibling_nodes(self.family_node1.primary_member.gender)),
            [self.family_node2, self.family_node3, self.family_node4, self.family_node5]
        )
        self.assertEqual(
            list(self.family_node1.get_sibling_nodes(self.family_node1.primary_member.gender, MALE)),
            [self.family_node2, self.family_node3, self.family_node4]
        )
        self.assertEqual(
            list(self.family_node1.get_sibling_nodes(self.family_node1.primary_member.gender, FEMALE)),
            [self.family_node5]
        )

    def test_get_parent_siblings(self):
        new_family_node_member = FamilyMember('Dritha', FEMALE)
        new_family_node = FamilyNode(new_family_node_member, self.family_node1)
        self.family_node1.add_child(new_family_node)

        self.assertEqual(
            list(new_family_node.get_parent_siblings(new_family_node_member.name, MALE)),
            [
                self.family_node2.primary_member, self.family_node3.primary_member,
                self.family_node4.primary_member, self.family_node5.primary_member
            ]
        )
        self.assertEqual(
            list(new_family_node.get_parent_siblings(new_family_node_member.name, FEMALE)),
            []
        )
        self.assertEqual(
            list(new_family_node.get_parent_siblings(new_family_node_member.name, MALE, MALE)),
            [self.family_node2.primary_member, self.family_node3.primary_member, self.family_node4.primary_member]
        )
        self.assertEqual(
            list(new_family_node.get_parent_siblings(new_family_node_member.name, FEMALE, MALE)),
            []
        )
        self.assertEqual(
            list(new_family_node.get_parent_siblings(new_family_node_member.name, MALE, FEMALE)),
            [self.family_node5.primary_member]
        )
        self.assertEqual(
            list(new_family_node.get_parent_siblings(new_family_node_member.name, FEMALE, FEMALE)),
            []
        )

    def test_get_spouse_siblings(self):
        self.assertEqual(
            list(self.family_node1.get_spouse_siblings(self.family_node1_member2.gender)),
            [
                self.family_node2.primary_member, self.family_node3.primary_member,
                self.family_node4.primary_member, self.family_node5.primary_member
            ]
        )
        self.assertEqual(
            list(self.family_node1.get_spouse_siblings(self.family_node1_member2.gender, MALE)),
            [
                self.family_node2.primary_member, self.family_node3.primary_member,
                self.family_node4.primary_member
            ]
        )
        self.assertEqual(
            list(self.family_node1.get_spouse_siblings(self.family_node1_member2.gender, FEMALE)),
            [self.family_node5.primary_member]
        )

    def test_get_sibling_spouses(self):
        self.assertEqual(
            list(self.family_node1.get_sibling_spouses(self.family_node1_member1.gender)),
            [
                self.family_node3.secondary_member, self.family_node4.secondary_member,
                self.family_node5.secondary_member
            ]
        )
        self.assertEqual(
            list(self.family_node1.get_sibling_spouses(self.family_node1_member1.gender, MALE)),
            [self.family_node5.secondary_member]
        )
        self.assertEqual(
            list(self.family_node1.get_sibling_spouses(self.family_node1_member1.gender, FEMALE)),
            [self.family_node3.secondary_member, self.family_node4.secondary_member]
        )

    def test_is_primary_member(self):
        self.assertTrue(self.family_node1.is_primary_member(self.family_node1_member1.gender))
        self.assertFalse(self.family_node2.is_primary_member(self.family_node1_member2.gender))

    def test_get_children_by_gender(self):
        self.assertEqual(
            list(self.root_node.get_children_by_gender(MALE)),
            [
                self.family_node1.primary_member, self.family_node2.primary_member,
                self.family_node3.primary_member, self.family_node4.primary_member
            ]
        )
        self.assertEqual(
            list(self.root_node.get_children_by_gender(FEMALE)),
            [self.family_node5.primary_member]
        )


if __name__ == '__main__':
    unittest.main()
