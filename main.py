import re
import json

print("Overwatch custom model maker created by Ernest326\n")
print("Please note that there might be a few bugs!")
print("Please note that this only works with small models because of the code limit!\n")

filename = input("Please input obj file name(include .obj): ")

reComp = re.compile("(?<=^)(v |vn |vt |f )(.*)(?=$)", re.MULTILINE)
with open(filename) as f:
    data = [txt.group() for txt in reComp.finditer(f.read())]

v_arr, vn_arr, vt_arr, f_arr = [], [], [], []
for line in data:
    tokens = line.split(' ')
    if tokens[0] == 'v':
        v_arr.append([float(c) for c in tokens[1:]])
    elif tokens[0] == 'vn':
        vn_arr.append([float(c) for c in tokens[1:]])
    elif tokens[0] == 'vt':
        vn_arr.append([float(c) for c in tokens[1:]])
    elif tokens[0] == 'f':
        f_arr.append([[int(i) if len(i) else 0 for i in c.split('/')] for c in tokens[1:]])

vertices, normals = [], []
for face in f_arr:
    for tp in face:
        vertices += v_arr[tp[0]-1]
        normals  += vn_arr[tp[2]-1]


vertices = []

arr = [[] for _ in range(len(f_arr))]
for i in range(len(f_arr)):

    for j in range(len(f_arr[i])):

        arr[i].append(f_arr[i][j][0])
        
vertices.append(arr)

#Variables
ModelName = "Model"
ArrayObject = False
Beam = input("Please input beam type (Good Beam, Bad Beam, Grapple Beam): ") #Good Beam, Bad Beam, Grapple Beam
Colour = input("Please input colour (Yellow, Green, Purple, Red, Blue, Team 1, Team 2, Aqua, Orange, Sky Blue, Turquoise, Lime Green): ") #Yellow, Green, Purple, Red, Blue, Team 1, Team 2, Aqua, Orange, Sky Blue, Turquoise, Lime Green

with open('output.txt', 'w') as f:

    #Set Variables
    f.write('variables\n{\n	global:\n')
    f.write('		' + '0: ModelPosition\n')
    f.write('		' + '1: ModelSize\n')
    f.write('		' + '2: ModelXRot\n')
    f.write('		' + '3: ModelYRot\n')
    f.write('		' + '4: ModelZRot\n')
    if(ArrayObject):
        f.write('		' + '5: ModelCount\n')
    f.write('}\n\n')

    #Set Subroutine
    f.write('subroutines\n{\n	0: BuildModel\n}\n\n')

    #Set Variable Defaults
    f.write('rule("Variable Defaults")\n{\n	event\n')
    f.write('	{\n		Ongoing - Global;\n	}\n\n')
    f.write('	actions\n	{\n		Global.ModelPosition = Vector(0,0,0);\n		Global.ModelSize = 1;\n		Global.ModelXRot = 0;\n		Global.ModelYRot = 0;\n		Global.ModelZRot = 0;\n')
    f.write('	}\n}\n')

    #Set Build Model Event
    f.write('rule("Build Model Event")\n{\n	event\n')
    f.write('	{\n		Subroutine;\n		BuildModel;\n	}\n\n')
    f.write('	actions\n	{\n')

    for i in range(len(vertices)):
        for j in range(len(vertices[i])):
            for k in range(len(vertices[i][j])):
                if (k < len(vertices[i][j]) - 1):
                    if(ArrayObject != True):

                        x1 = v_arr[vertices[i][j][k] - 1][0]
                        y1 = v_arr[vertices[i][j][k] - 1][1]
                        z1 = v_arr[vertices[i][j][k] - 1][2]

                        x2 = v_arr[vertices[i][j][k + 1] - 1][0]
                        y2 = v_arr[vertices[i][j][k + 1] - 1][1]
                        z2 = v_arr[vertices[i][j][k + 1] - 1][2]

                        f.write('		Create Beam Effect(All Players(All Teams), ' + Beam +
                            ', Vector(' + str(x1) + ' *  Cosine From Degrees(Global.ModelYRot) + ' + str(z1) + ' * Sine From Degrees(Global.ModelYRot)' + ', ' + str(y1) + ', ' + str(z1) + ' *  Cosine From Degrees(Global.ModelYRot) - ' + str(x1) + ' * Sine From Degrees(Global.ModelYRot)' + ') * Global.ModelSize + Global.ModelPosition, Vector(' +
                            str(x2) + ' *  Cosine From Degrees(Global.ModelYRot) + ' + str(z2) + ' * Sine From Degrees(Global.ModelYRot)' + ', ' + str(y2) + ', ' + str(z2) + ' *  Cosine From Degrees(Global.ModelYRot) - ' + str(x2) + ' * Sine From Degrees(Global.ModelYRot)' + ') * Global.ModelSize + Global.ModelPosition, ' +
                            'Color(' + Colour + ')' + ',Visible To Position and Radius);\n')
                    else:
                        f.write('		Create Beam Effect(All Players(All Teams), ' + Beam + ', Vector(' + str(
                            v_arr[vertices[i][j][k] - 1][0]) + ', ' + str(v_arr[vertices[i][j][k] - 1][1]) + ', ' + str(
                            v_arr[vertices[i][j][k] - 1][
                                2]) + ') * Global.ModelSize[Global.ModelCount] + Global.ModelPosition[Global.ModelCount], Vector(' + str(
                            v_arr[vertices[i][j][k + 1] - 1][0]) + ', ' + str(
                            v_arr[vertices[i][j][k + 1] - 1][1]) + ', ' + str(v_arr[vertices[i][j][k + 1] - 1][
                                                                                  2]) + ') * Global.ModelSize[Global.ModelCount] + Global.ModelPosition[Global.ModelCount], ' + "Color(" + Colour + ")" + ',Visible To Position and Radius);\n')


        f.write('	}\n}\n\n')

print("Model successfully generated! Copy all contents in output.txt and paste it in your code editor in Overwatch")
                
                

    

    

        
