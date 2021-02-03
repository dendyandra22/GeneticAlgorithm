import random
import math

def genotipeDecoder(genotipe, fenotipe, h):
    i,j= 0,0
    x1,x2 = 0,0
    while i < len(genotipe):
        while j < len(genotipe[i]):
            if (genotipe[i][j] == 0 and genotipe[i][j+1] == 0):
                if (j == 0):
                    x1 = 0
                elif (j == 2):
                    x2 = 0
            elif (genotipe[i][j] == 0 and genotipe[i][j+1] == 1):
                if (j == 0):
                    x1 = 1
                elif (j == 2):
                    x2 = 1
            elif (genotipe[i][j] == 1 and genotipe[i][j+1] == 0):
                if (j == 0):
                    x1 = 2
                elif (j == 2):
                    x2 = 2
            # dimisalkan biner 11 = -1
            elif (genotipe[i][j] == 1 and genotipe[i][j+1] == 1):
                if (j == 0):
                    x1 = -1
                elif (j == 2):
                    x2 = -1
            j+= 2
        fenotipe.append([x1,x2])
        h.append(fungsiMinimum(x1,x2))
        j = 0
        i += 1

def fungsiMinimum(x1,x2):
    if (x2 == 0):
        res = (math.cos(x1)) * (math.sin(x2)) - (x1 / 1)
    else:
        res = (math.cos(x1)) * (math.sin(x2)) - (x1 / (x2 ** 2) + 1)
    return res

def fungsiFitness(h):
    # misalkan a = 0.1
    return 1 / (h + 0.1)

def seleksiOrtu(fitness):
    ortu = []
    temp = []
    fitnessSort = fitness.copy()
    fitnessSort = sorted(fitnessSort)
    rb, ra = fitnessSort[0] - 1, fitnessSort[len(fitnessSort) -1]
    while len(fitnessSort) != 0:
        # random number buat seleksi ortu
        x = random.uniform(rb,ra)
        i = 0
        found = False
        while i < len(fitnessSort) and not found:
            if(x <= fitnessSort[i]):
                idx = [j for j, fitIdx in enumerate(fitness) if fitIdx == fitnessSort[i]]
                if len(idx) == 1:
                    temp.append(idx[0])
                else:
                    k = 0
                    stop = False
                    while not stop:
                        if idx[k] not in temp:
                            temp.append(idx[k])
                            stop = True
                        k += 1
                fitnessSort.pop(i)
                found = True
            i += 1
    # append temp ke ortu
    a = 0
    while a < len(temp):
        ortu.append([temp[a],temp[a+1]])
        a += 2
    return ortu

def crossOver(ortu,genotipe):
    newGen = []
    for a in range(len(ortu)):
        x1, x2 = ortu[a][0], ortu[a][1]
        newGen1,newGen2 = [],[]
        # random set point
        x = random.randrange(1,4)
        for i in range(x):
            newGen1.append(genotipe[x1][i])
            newGen2.append(genotipe[x2][i])
        for i in range(x,4):
            newGen1.append(genotipe[x2][i])
            newGen2.append(genotipe[x1][i])
        newGen.append(newGen1)
        newGen.append(newGen2)
    return newGen

def mutasi(genAnak):
    # probabilitas mutasi misal 0.1
    p = 0.1
    for i in range(len(genAnak)):
        for j in range(len(genAnak[i])):
            x = random.uniform(0,1)
            if (x <= p):
                if(genAnak[i][j] == 0):
                    genAnak[i][j] = 1
                else:
                    genAnak[i][j] = 0

def gantiGenerasi(genLama,genBaru,ortu):
    print("gen lama : ", genLama)
    for i in range(len(ortu)):
        k1,k2 = ortu[i][0],ortu[i][1]
        genLama[k1] = genBaru[k1]
        genLama[k2] = genBaru[k2]
    print()
    print("gen baru : ", genLama)


# main
genotipe = [[0,0,0,0],[0,0,0,1],[0,0,1,1],[0,1,0,0,],[0,1,0,1],[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,1],[1,1,0,0],[1,1,0,1],[1,1,1,1]]
h1 = []
f1 = []
ortu1 = []
generasi = 100

for i in range(generasi):
    fenotipe = []
    h = []
    fitness = []
    # genotipe dekoder
    print()
    print("genotipe dekoder")
    genotipeDecoder(genotipe,fenotipe,h)
    print("genotipe = ", genotipe)
    print("fenotipe = ", fenotipe)
    print("hasil fungsi minimum", h)
    h1.append(h)
    print()

    # menghitung fungsi fitness
    print()
    print("hasil fungsi fitness")
    for i in range(len(h)):
        print("ortu",i," h =",h[i], end=" ")
        fitness.append(fungsiFitness(h[i]))
        print("hasil fitness ",fitness[i])
    # append hasil fitness tiap gen
    f1.append(fitness)

    # seleksi ortu
    print()
    print("Seleksi ortu")
    ortu = seleksiOrtu(fitness)
    print("ortu terpilih ",ortu)
    ortu1.append(ortu)

    # rekombinasi 1-point crossover
    print()
    print("crossover ortu")
    genAnak = crossOver(ortu,genotipe)
    print("gen anak ",genAnak)

    # mutasi gen
    print()
    print("mutasi gen anak")
    mutasi(genAnak)
    print("hasil mutasi: ",genAnak)

    genotipe1 = genotipe.copy()
    fenotipe1 = fenotipe.copy()

    # pergantian generasi
    print()
    print("pergantian generasi")
    gantiGenerasi(genotipe,genAnak,ortu)




# cek hasil akhir
fit = 0
min = 0
idx = 0
for i in range(len(h)):
    temp = fitness[i]
    if(fit <= temp):
        fit = temp
        idx = i
        min = h[i]


print()
# print("idx",idx)
# print("h",h)
# print("f",fitness)
# print("g",genotipe1)
# print("f",fenotipe1)
print("hasil fungsi paling minimum adalah ",min," yang dihasilkan dari kromosom terbaik:",genotipe1[idx]," memiliki nilai fitness:",fitness[idx])
print(" dengan nilai x1:",fenotipe1[idx][0]," dan x2:",fenotipe1[idx][1])


