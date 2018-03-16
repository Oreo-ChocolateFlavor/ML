import matplotlib.pyplot as plt
import random
import matplotlib.cm as cm
import time
import numpy as np

class Position():
    def __init__(self,x,y):
        self.x = x;
        self.y = y;

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __truediv__(self, other):
        return Position(self.x/other.x,self.y/other.y)

    def __pow__(self, power, modulo=None):
        return self.x ** power + self.y ** power

    def __repr__(self):
        return "[" + str(self.x) + ',' + str(self.y) + "]"

cluster = [Position(random.randrange(0,10000),random.randrange(0,10000)) for i in range(32)]

x_list = [random.randrange(1,10000) for i in range(0,10000)]
y_list = [random.randrange(1,10000) for i in range(0,10000)]

def calc_error(pos,repre):
    return (repre - pos)**2

def clustering(x_posl,y_posl,cluster_pos):
    """
    :param x_posl: x의 좌표
    :param y_posl: y의 좌표
    :param cluster_pos: 대표값들
    :return: 분류된 리스트
    """
    pos = tuple( Position(x_posl[i],y_posl[i]) for i in range(0,len(x_posl)) )

    J = [-1 for i in range(0,len(pos))]
    Clust = []

    for i in range(0,len(pos)):
        for j in range(0,len(cluster_pos)):
            error = calc_error(pos[i],cluster_pos[j])

            if J[i] == -1:
                J[i] = error
                Clust.append(j)
            elif J[i] > error:
                J[i] = error
                Clust[i] = j

    ret = [[] for i in range(0,len(cluster_pos))]

    for i in range(0,len(Clust)):
        ret[Clust[i]].append(pos[i])

    ret_sum = 0
    for i in J:
        ret_sum += i

    return ret_sum,ret


def show(clustered,cluster):
    plt.figure()
    color = cm.rainbow(np.linspace(0, 1, len(cluster)))


    for i in range(0,len(clustered)):
        x_l = [];
        y_l = [];
        for j in clustered[i]:
            x_l.append(j.x)
            y_l.append(j.y)
        plt.scatter(x_l,y_l,color=color[i])

    for i in cluster:
        plt.scatter(i.x,i.y,c=123)

    plt.show()

def update(clustered):

    ret = []

    for i in clustered:
        sum = Position(0,0)
        for j in i:
            sum = sum + j
        ret.append(sum/Position(len(i),len(i)));

    return ret;

prev_J_sum = 1;

while True:
    J_sum , clustered = clustering(x_list,y_list,cluster)
    print(J_sum)

    cluster = update(clustered)
    diff = float(abs(prev_J_sum-J_sum))/float(abs(prev_J_sum))*100
    print(prev_J_sum,J_sum)
    print('변화율 : ' +  str(diff))
    print('좌표' ,end='')
    print(cluster)
    if diff < 1:
        show(clustered, cluster)
        break;
    else:
        prev_J_sum = J_sum

for i in clustered:
    print(len(i))

