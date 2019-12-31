


class StringToTree:

    parenMarker = 0  # Helps indicates if a substring is surrounded by open and closed parentheses

    parenIndex = -1  # Marks positions of parenthesis in the function string

    cropIndex = [0, 0]  # Indicates the positions of two corresponding open and closed parentheses

    firstTreeList = []  # Inital representation of function tree

    subLists = []  # Stores sublist for recursion

    operands = {"prod": "*", "sum": "+", "diff": "-", "quot": "/", "mod": "%"}  # Acts as a operator bank 

    finalTreeList = []  # Final (Level Traversed) representation of function tree 

    kidslist = []  # Stores kids of each level traversed node

    '''String to tree:
        This class uses three functions to convert from a function to a usable
        tree for evolf based on the function paramenters.

        StringToTree1: This turns a function to a list that contains nodes 
        represented as "[node function, level, children]" where the level 
        is a marker of how deep a node is in the function

        StringToTree2: This turns the output from the above function into a 
        similar function with null nodes included

        StringToTree3: This turns the output from the above function above 
        into a level trvaversed list of function names.

        To make use of the class use the function StringToTree which combines
        all three of the functions above.
              '''
    @classmethod
    def stringToTree1(cls, string, level=0):

        cls.subLists = []
        string = string.replace(" ", "")
        if ')' and ',' not in string:

            cls.firstTreeList.append([string, level, ""])
            return string

        else:

            for i in string:

                cls.parenIndex += 1
                if i == '(':

                    cls.parenMarker += 1

                elif i == ')':

                    cls.parenMarker -= 1

                if i == '(' and cls.parenMarker == 1:

                    cls.cropIndex[0] = cls.parenIndex+1

                elif i == ')' and cls.parenMarker == 0:

                    cls.cropIndex[1] = cls.parenIndex
                    cls.subLists.append(string[cls.cropIndex[0]:cls.cropIndex[1]])

            for items in cls.subLists:

                string = string.replace(items, "")

            string = string.replace(")", "")
            string = string.replace("(", "")

            string = string.split(',')

            if type(string) == str:

                string = [string]

            cls.parenMarker = 0
            cls.parenIndex = -1
            cls.cropIndex = [0, 0]

            kids = []
            stuff = cls.subLists
            stuff2 = string

            if(len(stuff2) != len(stuff)):

                if(len(stuff2[0]) == 1):

                    stuff.insert(0, '')

                else:

                    stuff.append('')

            for item in range(0, len(stuff)):

                kids = cls.stringToTree1(stuff[item], level + 1)
                cls.firstTreeList.append([stuff2[item], level, kids])

            for j in range(0, len(cls.firstTreeList)):

                try:

                    cls.firstTreeList[j][2] = list(cls.firstTreeList[j][2])

                except:

                    pass

            for j in cls.firstTreeList:

                if(j[0] == ""):

                    cls.firstTreeList.remove(j)

            return string

    @classmethod
    def stringToTree2(cls):

        for item in cls.firstTreeList:

            if len(item[2]) == 1:

                item[2].append("")

            elif len(item[2]) == 0:

                item[2].append("")
                item[2].append("")

    @classmethod
    def stringToTree3(cls, level=0):
        if len(cls.firstTreeList) == 0:

            return

        elif level == 0:

            for items in cls.firstTreeList:

                if items[1] == level:

                    cls.firstTreeList.remove(items)

                    for i in items[2]:

                        cls.kidslist.append(i)

                    cls.finalTreeList.append(items[0])
            cls.stringToTree3(level+1)
        else:

            flaglist = []

            for i in cls.kidslist:

                for items in cls.firstTreeList:

                    if (items[0] == i and items[1] == level):

                        cls.firstTreeList.remove(items)
                        cls.finalTreeList.append(items[0])
                        for j in items[2]:

                            flaglist.append(j)
                if i == "":

                    cls.finalTreeList.append(None)

            cls.kidslist = flaglist
            cls.stringToTree3(level+1)

    @classmethod
    def stringToTree(cls, string):
        StringToTree.stringToTree1(string)
        StringToTree.stringToTree2()
        StringToTree.stringToTree3()
        for i in range(0, len(cls.finalTreeList)):

            if cls.finalTreeList[i] in cls.operands:

                cls.finalTreeList[i] = cls.operands[cls.finalTreeList[i]]

        return cls.finalTreeList


print(StringToTree.stringToTree("sum(sin(prod(x,cos(y))),exp(y))"))
