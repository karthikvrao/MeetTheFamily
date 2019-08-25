from meetTheFamily.constants import MALE, FEMALE
from meetTheFamily.FamilyMember import FamilyMember
from meetTheFamily.FamilyNode import FamilyNode


class FamilyTree:
    ADD_CHILD = 'ADD_CHILD'
    GET_RELATIONSHIP = 'GET_RELATIONSHIP'

    supported_public_commands = [
        ADD_CHILD,
        GET_RELATIONSHIP
    ]

    ADD_MEMBER = 'ADD_MEMBER'

    PATERNAL_UNCLE = 'paternal-uncle'
    MATERNAL_UNCLE = 'maternal-uncle'
    PATERNAL_AUNT = 'paternal-aunt'
    MATERNAL_AUNT = 'maternal-aunt'
    SISTER_IN_LAW = 'sister-in-law'
    BROTHER_IN_LAW = 'brother-in-law'
    SON = 'son'
    DAUGHTER = 'daughter'
    SIBLINGS = 'siblings'

    supported_relationships = [
        PATERNAL_UNCLE,
        MATERNAL_UNCLE,
        PATERNAL_AUNT,
        MATERNAL_AUNT,
        SISTER_IN_LAW,
        BROTHER_IN_LAW,
        SON,
        DAUGHTER,
        SIBLINGS
    ]

    def __init__(self):
        self._tree_index = {}
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

        new_child_node = self._add_member_to_family_tree(new_member, selected_node, [])
        selected_node.add_child(new_child_node)
        if not suppress_output:
            print('CHILD_ADDITION_SUCCEEDED')

    def find_related_members(self, member_name, relationship):
        relationship_in_lowercase = relationship.lower()
        if relationship_in_lowercase not in FamilyTree.supported_relationships:
            print(f'UNSUPPORTED_RELATIONSHIP: {relationship}')
            return

        if member_name not in self._tree_index:
            print('PERSON_NOT_FOUND')
            return

        selected_node = self._tree_index[member_name]
        people = []

        if relationship_in_lowercase == FamilyTree.PATERNAL_UNCLE:
            people = selected_node.get_parent_siblings(member_name, MALE, MALE)

        elif relationship_in_lowercase == FamilyTree.MATERNAL_UNCLE:
            people = selected_node.get_parent_siblings(member_name, FEMALE, MALE)

        elif relationship_in_lowercase == FamilyTree.PATERNAL_AUNT:
            people = selected_node.get_parent_siblings(member_name, MALE, FEMALE)

        elif relationship_in_lowercase == FamilyTree.MATERNAL_AUNT:
            people = selected_node.get_parent_siblings(member_name, FEMALE, FEMALE)

        elif relationship_in_lowercase == FamilyTree.SISTER_IN_LAW:
            member_gender = selected_node.get_member(member_name).gender
            people = [
                *selected_node.get_spouse_siblings(member_gender, FEMALE),
                *selected_node.get_sibling_spouses(member_gender, FEMALE)
            ]

        elif relationship_in_lowercase == FamilyTree.BROTHER_IN_LAW:
            member_gender = selected_node.get_member(member_name).gender
            people = [
                *selected_node.get_spouse_siblings(member_gender, MALE),
                *selected_node.get_sibling_spouses(member_gender, MALE)
            ]

        elif relationship_in_lowercase == FamilyTree.SON:
            people = selected_node.get_children_by_gender(MALE)

        elif relationship_in_lowercase == FamilyTree.DAUGHTER:
            people = selected_node.get_children_by_gender(FEMALE)

        elif relationship_in_lowercase == FamilyTree.SIBLINGS:
            member_gender = selected_node.get_member(member_name).gender
            people = map(lambda node: node.primary_member, selected_node.get_sibling_nodes(member_gender))

        self.print_output(people)

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
            f'ADD_MEMBER Shan {MALE}',
            f'ADD_MEMBER Shan Anga {FEMALE}',
            f'ADD_CHILD Anga Chit {MALE}',
            f'ADD_MEMBER Chit Amba {FEMALE}',
            f'ADD_CHILD Anga Ish {MALE}',
            f'ADD_CHILD Anga Vich {MALE}',
            f'ADD_MEMBER Vich Lika {FEMALE}',
            f'ADD_CHILD Anga Aras {MALE}',
            f'ADD_MEMBER Aras Chitra {FEMALE}',
            f'ADD_CHILD Anga Satya {FEMALE}',
            f'ADD_MEMBER Satya Vyan {MALE}',
            f'ADD_CHILD Amba Dritha {FEMALE}',
            f'ADD_MEMBER Dritha Jaya {MALE}',
            f'ADD_CHILD Amba Tritha {FEMALE}',
            f'ADD_CHILD Amba Vritha {MALE}',
            f'ADD_CHILD Lika Vila {FEMALE}',
            f'ADD_CHILD Lika Chika {FEMALE}',
            f'ADD_CHILD Chitra Jnki {FEMALE}',
            f'ADD_MEMBER Jnki Arit {MALE}',
            f'ADD_CHILD Chitra Ahit {MALE}',
            f'ADD_CHILD Satya Asva {MALE}',
            f'ADD_MEMBER Asva Satvy {FEMALE}',
            f'ADD_CHILD Satya Vyas {MALE}',
            f'ADD_MEMBER Vyas Krpi {FEMALE}',
            f'ADD_CHILD Satya Atya {FEMALE}',
            f'ADD_CHILD Dritha Yodhan {MALE}',
            f'ADD_CHILD Jnki Laki {MALE}',
            f'ADD_CHILD Jnki Lavnya {FEMALE}',
            f'ADD_CHILD Satvy Vasa {MALE}',
            f'ADD_CHILD Krpi Kriya {MALE}',
            f'ADD_CHILD Krpi Krithi {FEMALE}'
        ]

        for operation in self.initial_operations:
            command, *params = operation.split(' ')
            command_in_uppercase = command.upper()

            if command_in_uppercase == FamilyTree.ADD_MEMBER:
                if len(params) == 2:
                    name, gender = params
                    new_member = FamilyMember(name, gender)
                    self._add_member_to_family_tree(new_member, None)

                elif len(params) == 3:
                    spouse_of, name, gender = params
                    new_member = FamilyMember(name, gender)
                    spouse_node = self._tree_index[spouse_of]
                    self._add_member_to_family_tree(new_member, None, spouse_node)

            elif command_in_uppercase == FamilyTree.ADD_CHILD:
                mother_name, name, gender = params
                new_member = FamilyMember(name, gender)
                self.add_child_member_to_family_tree(new_member, mother_name, True)
