# This file generates a random pose and converts it to a set of leg lengths.
import random
import math
import DQClass

# Here are the base coordinates
Base = [[952.5055, 91.0723, -1410.0000], [-398.5396, 869.5826, -1409.8621],
        [-555.4801, 779.1038, -1410.0000], [-555.0219, -779.3507, -1409.6010],
        [-398.5396, -869.9006, -1410.0000], [952.7381, -89.7865, -1409.8718]]

BaseM = [[.9525055, .0910723, -1.4100000], [-.3985396, .8695826, -1.4098621],
         [-.5554801, .7791038, -1.4100000], [-.5550219, -.7793507, -1.4096010],
         [-.3985396, -.8699006, -1.4100000], [.9527381, -.0897865, -1.4098718]]

# Here are the table coordinates in the identity pose
TableID = [[314.4868, 327.8608, -111.0000], [126.7447, 436.2739, -111.1102],
           [-441.2953, 107.9497, -111.0000], [-441.2826, -108.6562, -111.3975],
           [126.7447, -436.2688, -111.0000], [314.5916, -328.3827, -110.9675]]

TableIDM = [[.3144868, .3278608, -.1110000], [.1267447, .4362739, -.1111102],
            [-.4412953, .1079497, -.1110000], [-.4412826, -.1086562, -.1113975],
            [.1267447, -.4362688, -.1110000], [.3145916, -.3283827, -.1109675]]

# Here are the limitations on the P3350
# MaxTranslation = 635 mm (X,Y)
# MaxHeave = 694 mm (Z)
# Pitch = 30 degrees
# Yaw = 45 degrees


def MakeRandomPose():
    # Here we generate a random rotation
    theta = random.uniform(-0.5, 0.5)  # Rotation Angle between -30 and 30 degrees
    i = random.uniform(-1, 1)
    j = random.uniform(-1, 1)
    k = random.uniform(-1, 1)
    Q = (DQClass.Quaternion(0, i, j, k).normalization() * math.sin(1 / 2 * theta)
         + DQClass.Quaternion(math.cos(1 / 2 * theta), 0, 0, 0))
    #
    # Here we generate a random translation
    t1 = random.randrange(1, 500)
    t2 = random.randrange(1, 500)
    t3 = random.randrange(1, 500)
    t = DQClass.Quaternion(0, t1, t2, t3)
    #
    RandomPose = DQClass.DQuaternion(Q, t * Q * (1/2))
    return RandomPose


# Here we extract the coordinates under the pose (Q, t)
def TableCoords(pose):
    TablePosition = []
    Q = pose.A
    t = pose.B * pose.A.conjugate() * 2
    for n in range(6):
        r = DQClass.ToVectorQuaternion(TableID[n])
        s = Q * r * Q.conjugate() + t
        TablePosition.append([s.x, s.y, s.z])


# Here we compute the lengths of the legs
def LegLengths(pose):
    Q = pose.A
    t = pose.B * pose.A.conjugate() * 2
    Lengths = []
    for n in range(6):
        r = DQClass.ToVectorQuaternion(TableID[n])
        s = Q * r * Q.conjugate() + t
        b = DQClass.ToVectorQuaternion(Base[n])
        L = (s-b).norm()
        Lengths.append(L)
    return Lengths


def LegLengthsM(pose):
    Q = pose.A
    t = pose.B * pose.A.conjugate() * 2
    Lengths = []
    for n in range(6):
        r = DQClass.ToVectorQuaternion(TableID[n])
        s = Q * r * Q.conjugate() + t
        b = DQClass.ToVectorQuaternion(Base[n])
        L = (s - b).norm()
        Lengths.append(L/1000)
    return Lengths
