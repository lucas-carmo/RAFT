# example script for running RAFT from a YAML input file

import numpy as np
import matplotlib.pyplot as plt
import yaml
import raft
import os.path as path

# open the design YAML file and parse it into a dictionary for passing to raft
flNm = 'OC3spar-SlenderBodyQTF'
with open('./examples/' + flNm + '.yaml') as file:
    design = yaml.load(file, Loader=yaml.FullLoader)

# Create the RAFT model (will set up all model objects based on the design dict)
model = raft.Model(design)  

# Evaluate the system properties and equilibrium position before loads are applied
model.analyzeUnloaded()

# Compute natural frequencie
model.solveEigen()

# Simule the different load cases
model.analyzeCases(display=1)

# Plot the power spectral densities from the load cases
model.plotResponses()

# Visualize the system in its most recently evaluated mean offset position
model.plot(hideGrid=True)

model.saveResponses(path.join(model.fowtList[0].outFolderQTF, flNm))

plt.show()

# 0.02
# 12.37