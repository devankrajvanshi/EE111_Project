"""
This file reads the circuit from a file - 'number.txt--->1.txt,2.txt etc.'
Calculates the node voltage and current through the voltage sources
using modified node voltage analysis algorithm
and writes the output in the 'RCCircuit 1/2/3 output.txt' 
"""

import numpy as np

class Component:
    def __init__(self, Type, Node1, Node2, Value):
        self.Type = Type
        self.Node1 = Node1
        self.Node2 = Node2
        self.Value = Value


def init_mat_g(matrixG, ComponentList):
    """Resistances are used to make Matrix G
    
    Arguments:
        matrixG -- top left submatrix of the modified matrix
        ComponentList {class defined externally} -- components total list
    """
    for component in ComponentList:
        if component.Type == "R":
            node1 = int(component.Node1[1]) - 1
            node2 = int(component.Node2[1]) - 1
            if node1 < 0 or node2 < 0:                     # for Ground Logic
                NodeMax = max(node1, node2)
                node1 = node2 = NodeMax
                matrixG[node1][node1] += 1 / float(component.Value)
            else:
                matrixG[node1][node1] += 1 / float(component.Value)
                matrixG[node2][node2] += 1 / float(component.Value)
                matrixG[node1][node2] = -1 / float(component.Value)         
                matrixG[node2][node1] = -1 / float(component.Value)


def init_mat_b(matrixb, ComponentList):
    """Voltage sources are used to matrix B
    
    Arguments:
        matrixb -- top right submatrix of the modified matrix
    """
    VolCount = 0
    for component in ComponentList:
        if component.Type == "Vsrc":
            # for index, node in enumerate(matrixb):
            pos = int(component.Node1[1]) - 1
            neg = int(component.Node2[1]) - 1
            if pos >= 0:
                matrixb[pos][VolCount] = 1
            if neg >= 0:
                matrixb[neg][VolCount] = -1
            VolCount = VolCount + 1


def ParsingFile():
    """reading from a file, file name given in the main function
    """
    f = open("input.txt", "r")
    if f.mode == "r":                                 # check if file is open
        FileContent = f.readlines()                  # read file line by line
    for i in range(np.shape(FileContent)[0] - 1):    # loop for the lines before last
        FileContent[i] = FileContent[i][0:len(FileContent[i]) - 1]

    FileContent = FileContent[0:]
    nCompList = []
    for i in range(np.shape(FileContent)[0]):
        Line = FileContent[i].split()
        if Line[0] != 1 or Line[0] != -1:
            nCompList.append(Component(Line[0], Line[1], Line[2], Line[3]))
    return nCompList

def init_mat_C(B):
    """
    Transposing matrix B for matrix C
    """
    return B.transpose()


def IniMatA(G, B, C, D):
    """
    Constructing complete modified matrix
    """
    UpperA = np.hstack((G, B))
    DownA = np.hstack((C, D))
    return np.vstack((UpperA, DownA))

def initmate(matrixe, ComponentList):
    """
    Constructing voltage vector
    """
    Index = 0
    for component in ComponentList:
        if component.Type == "Vsrc":
            volt = int(component.Value)

            # for index, node in enumerate(matrixe):
            matrixe[Index][0] = volt
            Index = Index + 1


def initmati(matrixi, ComponentList):
    """
    Creating the current vector
    """
    for component in ComponentList:
        if component.Type == "Isrc":
            node1 = int(component.Node1[1]) - 1
            node2 = int(component.Node2[1]) - 1
            if node1 >= 0:
                matrixi[node1][0] = float(component.Value)
            if node2 >= 0:
                matrixi[node2][0] = float(component.Value)


def Write_To_File(File_Name, Values, n, m):
    """
    Writing the final output to the file
    """
    f = open("Circuit " + File_Name + ".txt", "w+")
    for i in range(n):
        mString = "V" + str(i + 1) + "\n"
        mString += str(Values[i][0]) + "\n"
        f.write(mString)
    for i in range(m):
        mString = "I_Vsrc" + str(i + 1) + "\n"
        mString += str(Values[i + n][0]) + "\n"
        f.write(mString)
    f.close()


### main function ###

ComponentList = []
ComponentList = ParsingFile()
n = 0  # representing Number of Nodes
m = 0  # representing Number of ID voltage Source

for mComponent in ComponentList:
    n = max(n, int(mComponent.Node1[1]), int(mComponent.Node2[1]))  
    # Getting how many no. of Nodes
    if mComponent.Type == "Vsrc":                                   
        # To count The no. of Voltage src
        m = m + 1


# Matrix A
# INITIALIZING the Matrices
##print(n)
G = np.zeros((n, n))  # for A resistance
B = np.zeros((n, m))  # connection of the voltage sources
C = np.zeros((m, n))  # Transpose of B
D = np.zeros((m, m))  # is a zero matrix

# Calculting The Matrices Values:

init_mat_g(G, ComponentList)
init_mat_b(B, ComponentList)
C = init_mat_C(B)
D = np.zeros((m, m))
##print("MatG:\n", G)
##print("MatB:\n", B)
##print("MatC:\n", C)
##print("MatD:\n", D)
A = IniMatA(G, B, C, D)

#   Mat X(Unknown)
V = np.zeros((n, 1))  # hold the unknown voltages at each node
J = np.zeros((m, 1))  # holds the unknown currents through the voltage sources.
X = np.vstack((V, J))

#   Mat Z
I = np.zeros((n, 1))
E = np.zeros((m, 1))
initmate(E, ComponentList)
initmati(I, ComponentList)
Z = np.vstack((I, E))

##print("Z:", Z)
# Solving The AX=Z
##print("MatA:", A, "\nMatZ", Z)
X = np.linalg.solve(A, Z)
Write_To_File("output",X, n, m)
