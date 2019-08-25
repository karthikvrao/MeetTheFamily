class FamilyNode:
    def __init__(self, primary_member, parent_node=None):
        self.primary_member = primary_member
        self.secondary_member = None
        self._parent_node = parent_node
        self.child_nodes = []

    def set_secondary_member(self, family_member):
        self.secondary_member = family_member

    def add_child(self, family_node):
        self.child_nodes.append(family_node)

    def get_member(self, member_name):
        if self.primary_member.name == member_name:
            return self.primary_member

        elif self.secondary_member and self.secondary_member.name == member_name:
            return self.secondary_member

    def has_couple(self):
        return self.primary_member and self.secondary_member

    def get_sibling_nodes(self, member_gender, sibling_gender=None):
        sibling_nodes = []

        if self.is_primary_member(member_gender):
            if sibling_gender:
                sibling_nodes = filter(
                    lambda node: node != self and node.primary_member.gender == sibling_gender,
                    self._parent_node.child_nodes
                )

            else:
                sibling_nodes = filter(lambda node: node != self, self._parent_node.child_nodes)

        return sibling_nodes

    def get_parent_siblings(self, member_name, parent_gender, parent_sibling_gender=None):
        parent_sibling_nodes = []

        member_gender = self.get_member(member_name).gender
        if self.is_primary_member(member_gender):
            parent_node = self._parent_node

            # Check if parent is primary member
            if parent_node.is_primary_member(parent_gender):
                if parent_sibling_gender:
                    parent_sibling_nodes = filter(
                        lambda node: node != self and node.primary_member.gender == parent_sibling_gender,
                        parent_node.get_sibling_nodes(parent_gender, parent_sibling_gender)
                    )

                else:
                    parent_sibling_nodes = filter(
                        lambda node: node != self, parent_node.get_sibling_nodes(parent_gender)
                    )

        return map(lambda node: node.primary_member, parent_sibling_nodes)

    def get_spouse_siblings(self, member_gender, spouse_sibling_gender=None):
        spouse_sibling_nodes = []

        # Check if given member is not primary member
        if not self.is_primary_member(member_gender):
            spouse_gender = self.primary_member.gender
            if spouse_sibling_gender:
                spouse_sibling_nodes = filter(
                    lambda node: node != self and node.primary_member.gender == spouse_sibling_gender,
                    self.get_sibling_nodes(spouse_gender, spouse_sibling_gender)
                )

            else:
                spouse_sibling_nodes = filter(lambda node: node != self, self.get_sibling_nodes(spouse_gender))

        return map(lambda node: node.primary_member, spouse_sibling_nodes)

    def get_sibling_spouses(self, member_gender, sibling_spouse_gender):
        sibling_spouse_nodes = []

        # Check if given member is primary member
        if self.is_primary_member(member_gender):
            sibling_spouse_nodes = filter(
                lambda node: node.secondary_member and node.secondary_member.gender == sibling_spouse_gender,
                self.get_sibling_nodes(self.primary_member.gender)
            )

        return map(lambda node: node.secondary_member, sibling_spouse_nodes)

    def is_primary_member(self, member_gender):
        return member_gender == self.primary_member.gender

    def get_children_by_gender(self, children_gender):
        filtered_child_nodes = filter(lambda node: node.primary_member.gender == children_gender, self.child_nodes)

        return map(lambda node: node.primary_member, filtered_child_nodes)
