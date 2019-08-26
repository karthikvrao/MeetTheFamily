from meet_the_family.constants import MALE, FEMALE
from meet_the_family.family_member import FamilyMember
from meet_the_family.family_node import FamilyNode


class FamilyTree:
    ADD_CHILD = 'ADD_CHILD'
    GET_RELATIONSHIP = 'GET_RELATIONSHIP'
    ADD_MEMBER = 'ADD_MEMBER'

    supported_public_commands = [
        ADD_CHILD,
        GET_RELATIONSHIP,
    ]

    def __init__(self):
        self._tree_index = {}
        self.relationships_switch = {}
        self._initialize_tree()

    def _add_member_to_family_tree(self, new_member, parent_node, existing_family_node=None):
        if existing_family_node:
            existing_family_node.set_secondary_member(new_member)
            self._tree_index[new_member.name] = existing_family_node
        else:
            new_family_node = FamilyNode(new_member, parent_node)
            self._tree_index[new_member.name] = new_family_node
            return new_family_node

    def add_child_member_to_family_tree(self, new_member, potential_mother_name, suppress_output=False):
        if potential_mother_name not in self._tree_index:
            print('PERSON_NOT_FOUND')
            return

        selected_node = self._tree_index[potential_mother_name]
        if not selected_node.has_couple() or selected_node.get_member(potential_mother_name).gender != FEMALE:
            if not suppress_output:
                print('CHILD_ADDITION_FAILED')
            return

        new_child_node = self._add_member_to_family_tree(new_member, selected_node)
        selected_node.add_child(new_child_node)

        if not suppress_output:
            print('CHILD_ADDITION_SUCCEEDED')

    def find_related_members(self, member_name, relationship):
        if not self.relationships_switch:
            self.relationships_switch['paternal-uncle'] = lambda **kwargs: (
                kwargs['selected_node'].get_parent_siblings(kwargs['member_name'], MALE, MALE)
            )
            self.relationships_switch['maternal-uncle'] = lambda **kwargs: (
                kwargs['selected_node'].get_parent_siblings(kwargs['member_name'], FEMALE, MALE)
            )
            self.relationships_switch['paternal-aunt'] = lambda **kwargs: (
                kwargs['selected_node'].get_parent_siblings(kwargs['member_name'], MALE, FEMALE)
            )
            self.relationships_switch['maternal-aunt'] = lambda **kwargs: (
                kwargs['selected_node'].get_parent_siblings(kwargs['member_name'], FEMALE, FEMALE)
            )
            self.relationships_switch['sister-in-law'] = lambda **kwargs: [
                *kwargs['selected_node'].get_spouse_siblings(kwargs['member_gender'], FEMALE),
                *kwargs['selected_node'].get_sibling_spouses(kwargs['member_gender'], FEMALE)
            ]
            self.relationships_switch['brother-in-law'] = lambda **kwargs: [
                *kwargs['selected_node'].get_spouse_siblings(kwargs['member_gender'], MALE),
                *kwargs['selected_node'].get_sibling_spouses(kwargs['member_gender'], MALE)
            ]
            self.relationships_switch['son'] = lambda **kwargs: (
                kwargs['selected_node'].get_children_by_gender(MALE)
            )
            self.relationships_switch['daughter'] = lambda **kwargs: (
                kwargs['selected_node'].get_children_by_gender(FEMALE)
            )
            self.relationships_switch['siblings'] = lambda **kwargs: (
                map(lambda node: node.primary_member, kwargs['selected_node']
                    .get_sibling_nodes(kwargs['member_gender']))
            )

        if member_name not in self._tree_index:
            print('PERSON_NOT_FOUND')
            return

        selected_node = self._tree_index[member_name]
        member_gender = selected_node.get_member(member_name).gender
        get_members = self.relationships_switch.get(relationship.lower(), None)

        if get_members:
            people = []
            people = get_members(
                selected_node=selected_node,
                member_name=member_name,
                member_gender=member_gender
            )
            self.print_output(people)
        else:
            print(f'UNSUPPORTED_RELATIONSHIP: {relationship}')
            return

    def print_output(self, people):
        people_list = list(people)

        if people_list:
            print(' '.join(f'{person.name}' for person in people_list))
        else:
            print('NONE')

    def process_file(self, file):
        with file as f:
            for line in f:
                self.perform_operation(line.splitlines()[0])

    def perform_operation(self, operation):
        command, *params = operation.split(' ')
        command_in_uppercase = command.upper()

        if command_in_uppercase not in FamilyTree.supported_public_commands:
            print('COMMAND_NOT_FOUND')
            return

        if command_in_uppercase == FamilyTree.GET_RELATIONSHIP:
            member_name, relationship = params
            self.find_related_members(member_name, relationship)

        elif command_in_uppercase == FamilyTree.ADD_CHILD:
            mother_name, name, gender = params
            new_member = FamilyMember(name, gender.lower())
            self.add_child_member_to_family_tree(new_member, mother_name)

    def _initialize_tree(self):
        self.initial_operations = [
            f'{FamilyTree.ADD_MEMBER} Shan {MALE}',
            f'{FamilyTree.ADD_MEMBER} Shan Anga {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Anga Chit {MALE}',
            f'{FamilyTree.ADD_MEMBER} Chit Amba {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Anga Ish {MALE}',
            f'{FamilyTree.ADD_CHILD} Anga Vich {MALE}',
            f'{FamilyTree.ADD_MEMBER} Vich Lika {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Anga Aras {MALE}',
            f'{FamilyTree.ADD_MEMBER} Aras Chitra {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Anga Satya {FEMALE}',
            f'{FamilyTree.ADD_MEMBER} Satya Vyan {MALE}',
            f'{FamilyTree.ADD_CHILD} Amba Dritha {FEMALE}',
            f'{FamilyTree.ADD_MEMBER} Dritha Jaya {MALE}',
            f'{FamilyTree.ADD_CHILD} Amba Tritha {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Amba Vritha {MALE}',
            f'{FamilyTree.ADD_CHILD} Lika Vila {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Lika Chika {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Chitra Jnki {FEMALE}',
            f'{FamilyTree.ADD_MEMBER} Jnki Arit {MALE}',
            f'{FamilyTree.ADD_CHILD} Chitra Ahit {MALE}',
            f'{FamilyTree.ADD_CHILD} Satya Asva {MALE}',
            f'{FamilyTree.ADD_MEMBER} Asva Satvy {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Satya Vyas {MALE}',
            f'{FamilyTree.ADD_MEMBER} Vyas Krpi {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Satya Atya {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Dritha Yodhan {MALE}',
            f'{FamilyTree.ADD_CHILD} Jnki Laki {MALE}',
            f'{FamilyTree.ADD_CHILD} Jnki Lavnya {FEMALE}',
            f'{FamilyTree.ADD_CHILD} Satvy Vasa {MALE}',
            f'{FamilyTree.ADD_CHILD} Krpi Kriya {MALE}',
            f'{FamilyTree.ADD_CHILD} Krpi Krithi {FEMALE}',
        ]

        for operation in self.initial_operations:
            command, *params = operation.split(' ')
            command_in_uppercase = command.upper()

            if command_in_uppercase == FamilyTree.ADD_MEMBER and len(params) == 2:
                name, gender = params
                new_member = FamilyMember(name, gender)
                self._add_member_to_family_tree(new_member, None)

            elif command_in_uppercase == FamilyTree.ADD_MEMBER and len(params) == 3:
                spouse_of, name, gender = params
                new_member = FamilyMember(name, gender)
                spouse_node = self._tree_index[spouse_of]
                self._add_member_to_family_tree(new_member, None, spouse_node)

            elif command_in_uppercase == FamilyTree.ADD_CHILD:
                mother_name, name, gender = params
                new_member = FamilyMember(name, gender)
                self.add_child_member_to_family_tree(new_member, mother_name, True)
