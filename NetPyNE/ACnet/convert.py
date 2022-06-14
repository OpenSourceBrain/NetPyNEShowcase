import sys

sys.path.append("../UI")

from helpers import convertAndImportLEMSSimulation


convertAndImportLEMSSimulation("LEMS_MediumNet.xml", simulate=False)
