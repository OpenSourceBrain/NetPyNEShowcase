from LEMS_TwoCell_netpyne import NetPyNESimulation

n = NetPyNESimulation()
n.generate_json_only()

print("Validating: %s"%n.simConfig.validateNetParams)

cfg = n.simConfig
