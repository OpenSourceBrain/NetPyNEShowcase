from LEMS_TwoCell_netpyne import NetPyNESimulation

print('------ stage 1')
n = NetPyNESimulation()
print('------ stage 2')

# Run nrnivmodl first...
n.generate_json_only()
print('------ stage 3')

print("Validating: %s"%n.simConfig.validateNetParams)

cfg = n.simConfig
