from meetTheFamily.FamilyTree import FamilyTree


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Family tree')
    parser.add_argument('input_file', type=argparse.FileType(), help='Input file path')
    args = parser.parse_args()

    family_tree = FamilyTree()
    family_tree.process_file(args.input_file)
