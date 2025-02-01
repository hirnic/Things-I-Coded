import numpy as np
import tensorflow as tf
from tensorflow import keras
import DQClass
import RandomizerRedacted
import time

loaded_model = tf.keras.models.load_model(r"C:\Users\cch30\PycharmProjects\QuaternionKinematics")

# init is a dual quaternion pose, and lengths is an array of 6 floats. Output is a dual quaternion pose.
def PoseFinder(init, lengths, TableID, Base):
    X, Y = init, DQClass.ZeroDQ()
    while (X-Y).size() > 10**(-4):
        Y = X
        f, Lf = [], []
        for n in range(6):                                                 # This loop finds the function and derivative
            s = (X.A.conjugate() * Base[n] + X.B.conjugate() * 2) * X.A           # Formula (8), page 4
            f.append((TableID[n] - s).norm() - lengths[0][n])                     # Formula (80), page 16
            u = np.array((TableID[n] - s).normalization().ToPureVec())            # Formula (66), page 13,
            Cross = np.cross(np.array(TableID[n].ToPureVec()), u)                 # Formula (67), page 13
            Lf.append(np.concatenate([Cross, u]) * 2)                             # Formula (68), page 14
        LInv = np.linalg.inv(np.array(Lf)) * (-1)
        Theta = DQClass.ToVectorDualQuaternion(LInv.dot(np.array(f)))             # Equation (80), page 16
        Hat = (DQClass.IdentityDQ() + Theta).normalization()                      # Formula (79), page 16
        X = X * Hat                                                               # Formula (79), page 16
    return X

RandomPoses = [RandomizerRedacted.MakeRandomPose() for _ in range(100)]
LegLengths = [RandomizerRedacted.LegLengthsRedacted(RandomPose) for RandomPose in RandomPoses]
LegLengths = np.array(LegLengths)                                               # Ensure it's a 2D array
Now = time.time()
for i in range(100):
    prediction = loaded_model.predict(LegLengths, verbose=0)                    # Use model to get initial guess
    Init = DQClass.ToDualQuaternion(prediction[0]).normalization()              # Make sure it is a unit dual quaternion
    PoseFinder(Init, LegLengths, RandomizerRedacted.TableID, RandomizerRedacted.Base)
print((time.time()-Now)/100)
