import xml.etree.ElementTree as ET

def getSubTree(tree):
    trees = []
    for child in tree.getroot():
        trees.append(child)
    return trees

def costOfDeletion(treeOne, treeTwo):
    rootOne = treeOne.getroot()
    rootTwo = treeTwo.getroot()
    if(isSubTree(rootOne, rootTwo)):
        return 1
    else:
        return sum(1 for _ in rootOne.iter())

def costOfInsertion(treeOne, treeTwo):
    rootOne = treeOne.getroot()
    rootTwo = treeTwo.getroot()
    if(isSubTree(rootOne, rootTwo)):
        return 1
    else:
        return sum(1 for _ in rootTwo.iter())

def isSubTree(rootOne, rootTwo):
    disectionsOne = disect(rootOne)
    for disection in disectionsOne:
        if(isSameTree(rootTwo, disection)):
            return True
    
    return False

def isSameTree(rootOne, rootTwo):
    return [x.tag for x in disect(rootOne)] == [y.tag for y in disect(rootTwo)]

def disect(root):
    if root is None:
        return []
    
    result = [root]
    for x in root:
        result += disect(x)        
    return result

def TED(firstTree, secondTree):
    roots = []
    roots.append(firstTree.getroot())
    roots.append(secondTree.getroot())

    childrenCount = []

    for rootIndex in range(0, len(roots)):
        childrenCount.append(len(roots[rootIndex]))

    M = childrenCount[0]
    N = childrenCount[1]

    rowsCount = M + 1
    columnsCount = N + 1

    table = [[0 for x in range(columnsCount)] for y in range(rowsCount)]

    # table[row][column]
    if(roots[0].tag != roots[1].tag):
        table[0][0] = 1
    
    subTreeOne = getSubTree(firstTree)
    for i in range(1, rowsCount):
        tempTreeA = ET.ElementTree()
        tempTreeA._setroot(subTreeOne[i-1])
        table[i][0] = table[i-1][0] + costOfDeletion(tempTreeA, secondTree)

    subTreeTwo = getSubTree(secondTree)
    for j in range(1, columnsCount):
        tempTreeB = ET.ElementTree()
        tempTreeB._setroot(subTreeTwo[j-1])
        table[0][j] = table[0][j-1] + costOfInsertion(firstTree, tempTreeB)

    for i in range(1, rowsCount):
        treeA = ET.ElementTree()
        treeA._setroot(subTreeOne[i-1])
        for j in range(1, columnsCount):
            treeB = ET.ElementTree()
            treeB._setroot(subTreeTwo[j-1])
            table[i][j] = min(
                table[i-1][j-1] + TED(treeA, treeB),
                table[i-1][j] + costOfDeletion(treeA, secondTree),
                table[i][j-1] + costOfInsertion(firstTree, treeB)
            )
            
    return table[M][N]

tree1 = ET.parse('trees/tree1.xml')
tree2 = ET.parse('trees/tree2.xml')
lastCell = TED(tree1, tree2)
similarity = 1/(1+lastCell)

print(lastCell)
print(similarity)
