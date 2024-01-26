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

#
# Read the content of a root file
#
def rootFileContent(d, basepath="/", getNested=False, starting_dir=None):
    import ROOT

    #"Generator function to recurse into a ROOT file/dir and yield (path, obj) pairs"
    if starting_dir is not None: d = d.Get(starting_dir)
    for key in d.GetListOfKeys():
        kname = key.GetName()
        # print d.Get(kname)
        # if key.IsFolder() and getNested:
        if type(d.Get(kname)) == ROOT.TFile or type(d.Get(kname)) == ROOT.TDirectoryFile and getNested:
    #    if key.IsFolder():
            # TODO: -> "yield from" in Py3
            for i in rootFileContent(d.Get(kname), basepath+kname+"/", getNested):
                yield i
        else:
            if starting_dir is not None:
                yield basepath+starting_dir+'/'+kname, d.Get(kname)
            else:
                yield basepath+kname, d.Get(kname)


