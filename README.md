# The Shan Family Tree

## About
This is a Python3 program that enables the user to interact with King Shan's family tree. When run from the 
command-line it expects a text file as an argument.

### How to run
After `cd`ing into the root directory, the program can be run from command-line like so:
```
python3 -m meet_the_family test_input_file.txt
```

The text file may contain all the operations that the user desires to perform on the family tree line-by-line. 

### Supported operations
The program supports two operations:

* Adding a child

Syntax:
```
ADD_CHILD 'Mother's_name' 'Child's_name' 'Gender'
```
Example:
```
ADD_CHILD Satya Ketu Male
```

* Checking relationships

Syntax:
```
GET_RELATIONSHIP 'Member's_name' 'Relationship'
```
Example:
```
GET_RELATIONSHIP Vila Paternal-Uncle
```

### Supported relationships
Following relationships are supported
* Paternal-Uncle
* Maternal-Uncle
* Paternal-Aunt
* Maternal-Aunt
* Sister-In-Law
* Brother-In-Law
* Son
* Daughter
* Siblings

### Expected outputs per line
* When results are found: `Names seperated by spaces`
* When no results found: `NONE`
* When member name is not found: `PERSON_NOT_FOUND`
* When child addition is successful: `CHILD_ADDITION_SUCCEEDED`
* When child addition fails: `CHILD_ADDITION_FAILED`

### Assumptions
* The program only supports Single word names of family members
* Names are case-sensitive
