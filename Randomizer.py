# This file generates a random pose and converts it to a set of leg lengths.
import random
import math
import DQClass

# Here are the base coordinates
Base = [[952.5055, 91.0723, -1410.0000], [-398.5396, 869.5826, -1409.8621], [-555.4801, 779.1038, -1410.0000], [-555.0219, -779.3507, -1409.6010], [-398.5396, -869.9006, -1410.0000], [952.7381, -89.7865, -1409.8718]]

# Here is are the table coordinates in the identity pose
TableID = [[314.4868, 327.8608, -111.0000], [126.7447, 436.2739, -111.1102], [-441.2953, 107.9497, -111.0000], [-441.2826, -108.6562, -111.3975], [126.7447, -436.2688, -111.0000], [314.5916, -328.3827, -110.9675]]

# Here are the limitations on the P3350
# MaxTranslation = 635 mm (X,Y)
# MaxHeave = 694 mm (Z)
# Pitch = 30 degrees
# Yaw = 45 degrees

# Here we generate a random rotation
theta = random.uniform(-0.5, 0.5)  # Rotation Angle between -30 and 30 degrees
i = random.uniform(-1, 1)
j = random.uniform(-1, 1)
k = random.uniform(-1, 1)
Q = DQClass.Quaternion(0, i, j, k).normalization() * DQClass.Quaternion(math.sin(1 / 2 * theta), 0, 0, 0) + DQClass.Quaternion(math.cos(1 / 2 * theta), 0, 0, 0)

# Here we generate a random translation
t1 = random.randrange(1, 100)
t2 = random.randrange(1, 100)
t3 = random.randrange(1, 100)
t = DQClass.Quaternion(0, t1, t2, t3)

# Here we extract the coordinates under the pose (Q, t)
TablePosition = []
n = 0
while n < 6:
    r = DQClass.Quaternion(0, TableID[n][0], TableID[n][1], TableID[n][2])
    s = Q * r * Q.conjugate() + t * Q * Q.conjugate()
    TablePosition.append([s.x, s.y, s.z])
    n += 1

# Here we compute the lengths of the legs
def LegLengths():
    Lengths = []
    n = 0
    while n < 6:
        L = math.sqrt((TablePosition[n][0] - Base[n][0])**2 + (TablePosition[n][1] - Base[n][1])**2 + (TablePosition[n][2] - Base[n][2])**2)
        Lengths.append(L)
        n += 1
    return Lengths

print("Randomly Generated Pose:", DQClass.DQuaternion(Q,t))
print("Randomly Generated Lengths:", LegLengths())
