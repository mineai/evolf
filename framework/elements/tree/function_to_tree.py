from framework.elements.node.node_constructor import NodeConstructor
from search_space.search_space import SearchSpace
from search_space.populate_search_space import PopulateSearchSpace


class StringToTree:

    paren_marker = 0  # Helps indicates if a substring is surrounded by open and closed parentheses

    paren_index = -1  # Marks positions of parenthesis in the function string

    crop_index = [0, 0]  # Indicates the positions of two corresponding open and closed parentheses

    first_tree_list = []  # Inital representation of function tree

    sub_lists = []  # Stores sublist for recursion

    operands = {"prod": "*", "sum": "+", "diff": "-", "quot": "/", "mod": "%"}  # Acts as a operator bank 

    final_tree_list = []  # Final (Level Traversed) representation of function tree 

    kids_list = []  # Stores kids of each level traversed node

    '''
    String to tree:
        This class uses three functions to convert from a function to a usable
    tree for evolf based on the function paramenters.To make use of the class 
    use the function string_to_tree which combines all three of the functions in 
    question.Description of questions seen below.
    '''
    @classmethod
    def function_to_level_list(cls, string, level=0):
        '''
        function_to_level_list: 
            This turns a function to a list that contains nodes 
        represented as "[node function, level, children]" where the level 
        is a marker of how deep a node is in the function
        '''

        cls.sub_lists = []
        string = string.replace(" ", "")
        if ')' and ',' not in string:

            cls.first_tree_list.append([string, level, ""])
            return string

        else:

            for i in string:

                cls.paren_index += 1
                if i == '(':

                    cls.paren_marker += 1

                elif i == ')':

                    cls.paren_marker -= 1

                if i == '(' and cls.paren_marker == 1:

                    cls.crop_index[0] = cls.paren_index+1

                elif i == ')' and cls.paren_marker == 0:

                    cls.crop_index[1] = cls.paren_index
                    cls.sub_lists.append(string[cls.crop_index[0]:cls.crop_index[1]])

            for items in cls.sub_lists:

                string = string.replace(items, "")

            string = string.replace(")", "")
            string = string.replace("(", "")

            string = string.split(',')

            if type(string) == str:

                string = [string]

            cls.paren_marker = 0
            cls.paren_index = -1
            cls.crop_index = [0, 0]

            kids = []
            stuff = cls.sub_lists
            stuff2 = string

            if(len(stuff2) != len(stuff)):

                if(len(stuff2[0]) == 1):

                    stuff.insert(0, '')

                else:

                    stuff.append('')

            for item in range(0, len(stuff)):

                kids = cls.function_to_level_list(stuff[item], level + 1)
                cls.first_tree_list.append([stuff2[item], level, kids])

            for j in range(0, len(cls.first_tree_list)):

                try:

                    cls.first_tree_list[j][2] = list(cls.first_tree_list[j][2])

                except:

                    pass

            for j in cls.first_tree_list:

                if(j[0] == ""):

                    cls.first_tree_list.remove(j)

            return string

    @classmethod
    def level_list_to_null_list(cls):
        '''
        level_list_to_null_list: 
            This turns the output from the above function into a similar function 
            with null nodes included
        '''

        for item in cls.first_tree_list:

            if len(item[2]) == 1:

                item[2].append("")

            elif len(item[2]) == 0:

                item[2].append("")
                item[2].append("")

    @classmethod
    def null_list_to_tree_list(cls, level=0):
        '''
        null_list_to_tree_list: 
        This turns the output from the above function above into a level 
        trvaversed list of function names.
        '''
        if len(cls.first_tree_list) == 0:

            return

        elif level == 0:

            for items in cls.first_tree_list:

                if items[1] == level:

                    cls.first_tree_list.remove(items)

                    for i in items[2]:

                        cls.kids_list.append(i)

                    cls.final_tree_list.append(items[0])
            cls.null_list_to_tree_list(level+1)
        else:

            flag_list = []

            for i in cls.kids_list:

                for items in cls.first_tree_list:

                    if (items[0] == i and items[1] == level):

                        cls.first_tree_list.remove(items)
                        cls.final_tree_list.append(items[0])
                        for j in items[2]:

                            flag_list.append(j)
                if i == "":

                    cls.final_tree_list.append(None)

            cls.kids_list = flag_list
            cls.null_list_to_tree_list(level+1)

    @classmethod
    def string_to_tree(cls, string, searchspace):
        cls.function_to_level_list(string)
        cls.level_list_to_null_list()
        cls.null_list_to_tree_list()
        for i in range(0, len(cls.final_tree_list)):

            if cls.final_tree_list[i] in cls.operands:

                cls.final_tree_list[i] = cls.operands[cls.final_tree_list[i]]

        search = SearchSpace()
        search_space = searchspace
        PopulateSearchSpace.populate_search_space(search, search_space)
        cls.final_tree_list[0] = NodeConstructor.create_root_node(cls.final_tree_list[0], search)
        for i in range(1, len(cls.final_tree_list)):
            if cls.final_tree_list[i]:
                try:
                    cls.final_tree_list[i] = NodeConstructor.create_binary_node(cls.final_tree_list[i], search)
                except:
                    pass

                try:
                    cls.final_tree_list[i] = NodeConstructor.create_unary_node(cls.final_tree_list[i], search)
                except:
                    pass

                try:
                    cls.final_tree_list[i] = NodeConstructor.create_literal_node(cls.final_tree_list[i], search)
                except:
                    pass
        return (cls.final_tree_list)

