# This program takes randomly generated leg lengths and tries to recover the pose of the table
# The idea is to use Newton-Raphson with Randomizer.Lengths() as our function to invert

import DQClass
import Randomizer
import math
import numpy as np

Base = Randomizer.Base
TablePositions = Randomizer.TableID
LegLengths = Randomizer.LegLengths()
RandomPose = Randomizer.RandomPose


# This function finds the new position of the table (list of lists) under the given pose (dual quaternion)
def Position(points, pose):
    rot = pose.A
    trans = pose.B
    Q0 = rot.w
    Q1 = rot.x
    Q2 = rot.y
    Q3 = rot.z
    t1 = trans.x
    t2 = trans.y
    t3 = trans.z

    positions = []
    n = 0
    while n < 6:
        r1 = points[n][0]
        r2 = points[n][1]
        r3 = points[n][2]
        A = 2 * (r3 * (Q0 * Q2 + Q1 * Q3) + r2 * (Q1 * Q2 - Q0 * Q3)) + r1 * (Q0**2 + Q1**2 - Q2**2 - Q3**2)
        B = 2 * (r1 * (Q1 * Q2 + Q0 * Q3) + r3 * (Q2 * Q3 - Q0 * Q1)) + r2 * (Q0**2 - Q1**2 + Q2**2 - Q3**2)
        C = 2 * (r1 * (Q1 * Q3 - Q0 * Q2) + r2 * (Q0 * Q1 + Q2 * Q3)) + r3 * (Q0**2 - Q1**2 - Q2**2 + Q3**2)
        pos = [A + t1, B + t2, C + t3]
        positions.append(pos)
        n += 1

    return positions


# This function takes the 6 table positions (list of lists) and measures the lengths of the legs
def MeasuringTape(positions):
    n = 0
    Lengths = []
    while n < 6:
        langkth = math.sqrt(
            (positions[n][0] - Base[n][0])**2 + (positions[n][1] - Base[n][1])**2 + (positions[n][2] - Base[n][2])**2)
        Lengths.append(langkth)
        n += 1
    return Lengths


# Now we will find the table position
def InverseKinematics(lengths, MaxM):
    # This is the initial guess of the table position.
    currentPose = DQClass.DQuaternion(
        DQClass.Quaternion(1.0, 0, 0, 0), DQClass.Quaternion(0, 0, 0, 0))
    currentPoints = TablePositions

    m = 0
    while m < MaxM:
        currentLengths = MeasuringTape(currentPoints)
        rot = currentPose.A
        trans = currentPose.B
        Q0 = rot.w
        Q1 = rot.x
        Q2 = rot.y
        Q3 = rot.z
        t1 = trans.x
        t2 = trans.y
        t3 = trans.z

        # Here we extract the Jacobian Matrix
        Jacobian = []
        n = 0
        while n < 6:
            r1 = TablePositions[n][0]
            r2 = TablePositions[n][1]
            r3 = TablePositions[n][2]
            point = DQClass.Quaternion(0, r1, r2, r3)
            s = rot * point * rot.conjugate()

            # s.x = A = 2 * (r2 * (Q1 * Q2 - Q0 * Q3) + r3 * (Q0 * Q2 + Q1 * Q3)) + r1 * (1 - 2 * Q2 ** 2 - 2 * Q3 ** 2)
            # s.y = B = 2 * (r1 * (Q1 * Q2 + Q0 * Q3) + r3 * (Q2 * Q3 - Q0 * Q1)) + r2 * (1 - 2 * Q1 ** 2 - 2 * Q3 ** 2)
            # s.z = C = 2 * (r1 * (Q1 * Q3 - Q0 * Q2) + r2 * (Q0 * Q1 + Q2 * Q3)) + r3 * (1 - 2 * Q1 ** 2 - 2 * Q2 ** 2)
            # RotVec = np.array([A, B, C])

            # Here are partial derivatives involved in the length function derived from formulas
            DADQ1 = 2 * (r2 * (Q2 + Q1 * Q3 / Q0) + r3 * (Q3 - Q1 * Q2 / Q0))
            DADQ2 = 2 * (r2 * (Q1 + Q2 * Q3 / Q0) + r3 * (Q0 - Q2 ** 2 / Q0)) - 4 * r1 * Q2
            DADQ3 = 2 * (r2 * (Q3 ** 2 / Q0 - Q0) + r3 * (Q1 - Q2 * Q3 / Q0)) - 4 * r1 * Q3
            DBDQ1 = 2 * (r1 * (Q2 - Q1 * Q3 / Q0) + r3 * (Q1 ** 2 / Q0 - Q0)) - 4 * r2 * Q1
            DBDQ2 = 2 * (r1 * (Q1 - Q2 * Q3 / Q0) + r3 * (Q3 + Q2 * Q1 / Q0))
            DBDQ3 = 2 * (r1 * (Q0 - Q3 ** 2 / Q0) + r3 * (Q2 + Q1 * Q3 / Q0)) - 4 * r2 * Q3
            DCDQ1 = 2 * (r1 * (Q3 + Q1 * Q2 / Q0) + r2 * (Q0 - Q1 ** 2 / Q0)) - 4 * r3 * Q1
            DCDQ2 = 2 * (r1 * (Q2 ** 2 / Q0 - Q0) + r2 * (Q3 - Q1 * Q2 / Q0)) - 4 * r3 * Q2
            DCDQ3 = 2 * (r1 * (Q1 + Q2 * Q3 / Q0) + r2 * (Q2 - Q1 * Q3 / Q0))
            DSDQ1 = DQClass.Quaternion(0, DADQ1, DBDQ1, DCDQ1)
            DSDQ2 = DQClass.Quaternion(0, DADQ2, DBDQ2, DCDQ2)
            DSDQ3 = DQClass.Quaternion(0, DADQ3, DBDQ3, DCDQ3)

            b1 = Base[n][0]
            b2 = Base[n][1]
            b3 = Base[n][2]
            DFDQ1 = ((s.x + t1 - b1) * DSDQ1.x
                     + (s.y + t2 - b2) * DSDQ1.y + (s.z + t3 - b3) * DSDQ1.z) / currentLengths[n]
            DFDQ2 = ((s.x + t1 - b1) * DSDQ2.x
                     + (s.y + t2 - b2) * DSDQ2.y + (s.z + t3 - b3) * DSDQ2.z) / currentLengths[n]
            DFDQ3 = ((s.x + t1 - b1) * DSDQ3.x
                     + (s.y + t2 - b2) * DSDQ3.y + (s.z + t3 - b3) * DSDQ3.z) / currentLengths[n]
            DFDT1 = (s.x + t1 - b1) / currentLengths[n]
            DFDT2 = (s.y + t2 - b2) / currentLengths[n]
            DFDT3 = (s.z + t3 - b3) / currentLengths[n]

            Jacobian.append([DFDQ1, DFDQ2, DFDQ3, DFDT1, DFDT2, DFDT3])
            n += 1

        matrix = np.array(Jacobian)
        IJ = np.linalg.inv(matrix)  # Inverse Jacobian

        # Here we will iterate and find the next closest pose
        diffVec = []
        n = 0
        while n < 6:
            f = currentLengths[n] - lengths[n]
            diffVec.append(f)
            n += 1

        addend = []
        n = 0
        while n < 6:
            x = (IJ[n][0] * diffVec[0] + IJ[n][1] * diffVec[1] + IJ[n][2] * diffVec[2] + IJ[n][3] * diffVec[3]
                 + IJ[n][4] * diffVec[4] + IJ[n][5] * diffVec[5])
            addend.append(x)
            n += 1

        Rotation = [0, Q1 - addend[0], Q2 - addend[1], Q3 - addend[2]]
        Rotation[0] = math.sqrt(1 - Rotation[1]**2 - Rotation[2]**2 - Rotation[3]**2)
        addedTranslation = DQClass.Quaternion(0, addend[3], addend[4], addend[5])
        currentRotation = DQClass.Quaternion(Rotation[0], Rotation[1], Rotation[2], Rotation[3])
        currentTranslation = trans - addedTranslation

        currentPose = DQClass.DQuaternion(currentRotation, currentTranslation)
        currentPoints = Position(TablePositions, currentPose)

        m += 1

    return currentPose


# InverseKinematics(LegLengths, 10)

# This is just a tool to show how the accuracy improves with each iteration. I think I saw an unstable random position.
c = 0
while c < 12:
    T = RandomPose
    F = InverseKinematics(LegLengths, c)
    absDist = math.sqrt((T.A.w - F.A.w)**2 + (T.A.x - F.A.x)**2 + (T.A.y - F.A.y)**2 + (T.A.z - F.A.z)**2
                        + (T.B.x - F.B.x)**2 + (T.B.y - F.B.y)**2 + (T.B.z - F.B.z)**2)
    relDist = absDist / math.sqrt(T.A.w**2 + T.A.x**2 + T.A.y**2 + T.A.z**2 + T.B.x**2 + T.B.y**2 + T.B.z**2)
    print("Absolute Error:", absDist)
    # print("Relative Error:", relDist)
    # print("Approximate Pose:", F)
    c += 1


# # We wish to find a reasonable initial guess
# # First, let's solve the easier 2-leg-1-point problem
# # Notice that the bases of the third and fourth legs have the same x coordinate and opposite y coordinates
# # Assuming the legs meet the same point on the table (they don't!), we find the coordinates of this point on the table
#
# L1 = Lengths[2]  # The third leg length
# L2 = Lengths[3]  # The fourth leg length
# X1 = Base[2][0]  # X coord of third leg base
# Y1 = Base[2][1]  # Y coord of third leg base
# Z1 = Base[2][2]  # Z coord of third leg base
# Y = (L2**2 - L1**2) / (4 * Y1)  # Y coord of point on table where legs meet
#
# # Then the third and fourth legs (don't) meet at some point on the circle given by
# # L1^2 = (x - x1)^2 + (y-y_1)^2 + (z - z1)^2

# # I got really frustrated and gave up. It ended up not mattering anyway because I cannot get very fast convergence.
