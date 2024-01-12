def getSignalMass(name):
    if 'HNL' in name:
        return float(name.split('-m')[-1].split('-Vsq')[0])
    else:
        return None

def getSignalCouplingSquared(name):
    if 'HNL' in name:
        coupling_squared = name.split('-Vsq')[1].split('-')[0]
        if 'em' in coupling_squared: coupling_squared = coupling_squared.replace('m', '-')
        return float(coupling_squared)
    else:
        return None

def getSignalFlavor(name):
    if 'HNL' in name:
        return name.split('-')[1].split('-m')[0]
    else:
        return None
