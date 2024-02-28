from hepdataTools import addCommonQualifiersTo, addCommonKeywordsTo
def createYieldVariable(nominal, up = None, down = None):
    from hepdata_lib import Variable, Uncertainty
    out_var = Variable("Event Yield",
                    is_independent = False,
                    is_binned=False,
                    units = "")

    out_var.values = nominal
    addCommonQualifiersTo(out_var)

    if up is None or len(up) == 0 or down is None or len(down) == 0: return out_var

    is_symmetric = up == down
    unc = Uncertainty("stat+syst", is_symmetric = is_symmetric)
    if is_symmetric:
        unc.values = up
    else:
        unc.values = [(d, u) for u,d in zip(up, down)]

    out_var.add_uncertainty(unc)
    return out_var


GEV = "GeV"

def addBackgroundAndData(table, numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = None):
    #Create Yield Variables
    yield_eem_data = createYieldVariable(numbers_eem["data"], None, None)
    yield_eem_data.add_qualifier('Channel', '$e^{\pm}e^{\pm}\mu$')
    yield_eem_data.add_qualifier('Process', 'Data')
    yield_eem_bkgr = createYieldVariable(numbers_eem["bkgr"]["Total Background"]["nominal"], numbers_eem["bkgr"]["Total Background"]["up"], numbers_eem["bkgr"]["Total Background"]["down"])
    yield_eem_bkgr.add_qualifier('Channel', '$e^{\pm}e^{\pm}\mu$')
    yield_eem_bkgr.add_qualifier('Process', 'Background')

    yield_emm_data = createYieldVariable(numbers_emm["data"], None, None)
    yield_emm_data.add_qualifier('Process', 'Data')
    yield_emm_data.add_qualifier('Channel', '$\mu^{\pm}\mu^{\pm}e$')
    yield_emm_bkgr = createYieldVariable(numbers_emm["bkgr"]["Total Background"]["nominal"], numbers_emm["bkgr"]["Total Background"]["up"], numbers_emm["bkgr"]["Total Background"]["down"])
    yield_emm_bkgr.add_qualifier('Channel', '$\mu^{\pm}\mu^{\pm}e$')
    yield_emm_bkgr.add_qualifier('Process', 'Background')

    yield_tee_data = createYieldVariable(numbers_tee["data"], None, None)
    yield_tee_data.add_qualifier('Channel', '$e^{\pm}e^{\pm}\\tau$')
    yield_tee_data.add_qualifier('Process', 'Data')
    yield_tee_bkgr = createYieldVariable(numbers_tee["bkgr"]["Total Background"]["nominal"], numbers_tee["bkgr"]["Total Background"]["up"], numbers_tee["bkgr"]["Total Background"]["down"])
    yield_tee_bkgr.add_qualifier('Process', 'Background')
    yield_tee_bkgr.add_qualifier('Channel', '$e^{\pm}e^{\pm}\\tau$')

    yield_tmm_data = createYieldVariable(numbers_tmm["data"], None, None)
    yield_tmm_data.add_qualifier('Process', 'Data')
    yield_tmm_data.add_qualifier('Channel', '$\mu^{\pm}\mu^{\pm}\\tau$')
    yield_tmm_bkgr = createYieldVariable(numbers_tmm["bkgr"]["Total Background"]["nominal"], numbers_tmm["bkgr"]["Total Background"]["up"], numbers_tmm["bkgr"]["Total Background"]["down"])
    yield_tmm_bkgr.add_qualifier('Process', 'Background')
    yield_tmm_bkgr.add_qualifier('Channel', '$\mu^{\pm}\mu^{\pm}\\tau$')

    if numbers_tem is not None:
        yield_tem_data = createYieldVariable(numbers_tem["data"], None, None)
        yield_tem_data.add_qualifier('Process', 'Data')
        yield_tem_data.add_qualifier('Channel', '$e\mu\\tau$')
        yield_tem_bkgr = createYieldVariable(numbers_tem["bkgr"]["Total Background"]["nominal"], numbers_tem["bkgr"]["Total Background"]["up"], numbers_tem["bkgr"]["Total Background"]["down"])
        yield_tem_bkgr.add_qualifier('Process', 'Background')
        yield_tem_bkgr.add_qualifier('Channel', '$e\mu\\tau$')

    table.add_variable(yield_eem_data)
    table.add_variable(yield_eem_bkgr)
    table.add_variable(yield_emm_data)
    table.add_variable(yield_emm_bkgr)
    table.add_variable(yield_tee_data)
    table.add_variable(yield_tee_bkgr)
    table.add_variable(yield_tmm_data)
    table.add_variable(yield_tmm_bkgr)
    if numbers_tem is not None:
        table.add_variable(yield_tem_data)
        table.add_variable(yield_tem_bkgr)


flavor_tex_dict = {'e' : 'e', 'mu' : '\mu', 'tau' : '\\tau'}
def returnSignalVar(numbers, channel, flavor):
    from hnlTools import getSignalMass, getSignalFlavor, getSignalCouplingSquared
    masses = set()
    for sk in numbers['signal'].keys():
        if 'HNL' in sk:
            masses.add(getSignalMass(sk))
    masses = sorted([sk for sk in masses])
    out_yields = []
    for mass in masses:
        for sk in numbers['signal']:
            if getSignalMass(sk) != mass or getSignalFlavor(sk) != flavor:
                continue
            else:
                out_yields.append(createYieldVariable(numbers['signal'][sk]['nominal'], numbers['signal'][sk]['up'], numbers['signal'][sk]['down']))
                out_yields[-1].add_qualifier('HNL mass', '{0} GeV'.format(mass))
                out_yields[-1].add_qualifier('$|V_{'+flavor_tex_dict[getSignalFlavor(sk)]+' N}|^2$', str(getSignalCouplingSquared(sk)))
                out_yields[-1].add_qualifier('Channel', channel)

    return out_yields

#def addLowMassTables(submission):
#    from hepdata_lib import Table, Variable
#
#    #First get the independent variables
#    bins_binnb = Variable("bin number",
#                    is_independent = True,
#                    is_binned = False,
#                    units = ""
#                    )
#    bins_binnb.values = ['La{0}'.format(x) for x in range(1, 9)] + ['Lb{0}'.format(x) for x in range(1, 9)]
#
#    bins_ptl1 = Variable("$p_{T}(l_{1})$",
#                    is_independent = True,
#                    is_binned = False,
#                    units = GEV    
#                    )
#    bins_ptl1.values = ["<30", "<30", "<30", "<30", "30 to 55", "30 to 55", "30 to 55", "30 to 55", "<30", "<30", "<30", "<30", "30 to 55", "30 to 55", "30 to 55", "30 to 55"]
# 
#    bins_minMos = Variable("min $m(2l|$OS)",
#                    is_independent = True,
#                    is_binned = False,
#                    units = GEV    
#                    )
#    bins_minMos.values = ["<10", "10 to 20", "20 to 30", ">30", "<10", "10 to 20", "20 to 30", ">30", "<10", "10 to 20", "20 to 30", ">30", "<10", "10 to 20", "20 to 30", ">30"]
#    
#    bins_ossf = Variable("OSSF pair",
#                    is_independent = True,
#                    is_binned = False,
#                    units = ""    
#                    )
#    bins_ossf.values = ["No"] * 8 + ["Yes"] * 8 
#
#    #Create Table for background and data yields
#    #Start by loading in the json
#    def loadJsons():
#        import json
#        eem_path = '/user/lwezenbe/private/PhD/Analysis_CMSSW_10_2_22/CMSSW_10_2_22/src/HNL/Stat/data/output/HEPDATA/LowMass/SR/EEE-Mu.json'
#        with open(eem_path, 'r') as infile:
#            numbers_eem = json.load(infile)
#        emm_path = '/user/lwezenbe/private/PhD/Analysis_CMSSW_10_2_22/CMSSW_10_2_22/src/HNL/Stat/data/output/HEPDATA/LowMass/SR/MuMuMu-E.json'
#        with open(emm_path, 'r') as infile:
#            numbers_emm = json.load(infile)
#        tee_path = '/user/lwezenbe/private/PhD/Analysis_CMSSW_10_2_22/CMSSW_10_2_22/src/HNL/Stat/data/output/HEPDATA/LowMass/SR/TauEE.json'
#        with open(tee_path, 'r') as infile:
#            numbers_tee = json.load(infile)
#        tmm_path = '/user/lwezenbe/private/PhD/Analysis_CMSSW_10_2_22/CMSSW_10_2_22/src/HNL/Stat/data/output/HEPDATA/LowMass/SR/TauMuMu.json'
#        with open(tmm_path, 'r') as infile:
#            numbers_tmm = json.load(infile)
#        tem_path = '/user/lwezenbe/private/PhD/Analysis_CMSSW_10_2_22/CMSSW_10_2_22/src/HNL/Stat/data/output/HEPDATA/LowMass/SR/TauEMu.json'
#        with open(tem_path, 'r') as infile:
#            numbers_tem = json.load(infile)
#        return (numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)
#
#    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
#
#    table_bkgr = Table("Data and background yields (Low Mass Region)")
#    table_bkgr.add_variable(bins_binnb)
#    table_bkgr.add_variable(bins_ossf)
#    table_bkgr.add_variable(bins_ptl1)
#    table_bkgr.add_variable(bins_minMos)
#    addBackgroundAndData(table_bkgr, numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)
#    addCommonKeywordsTo(table_bkgr)
#    submission.add_table(table_bkgr)
#
#    #Signal Tables
#    yields_eem = []
#    yields_emm = []
#
#
#    #E-coupling
#    yields = {}
#    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'e')
#    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'e')
#
#    table_ecoupl = Table("Predicted signal yields (Low Mass Region, $e$-coupling)")
#    table_ecoupl.add_variable(bins_binnb)
#    table_ecoupl.add_variable(bins_ossf)
#    table_ecoupl.add_variable(bins_ptl1)
#    table_ecoupl.add_variable(bins_minMos)
#    for k in yields.keys():
#        for s in yields[k]:
#            table_ecoupl.add_variable(s)
#    addCommonKeywordsTo(table_ecoupl)
#    submission.add_table(table_ecoupl)
#
#    #Mu-coupling
#    yields = {}
#    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'mu')
#    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'mu')
#
#    table_mcoupl = Table("Predicted signal yields (Low Mass Region, $\mu$-coupling)")
#    table_mcoupl.add_variable(bins_binnb)
#    table_mcoupl.add_variable(bins_ossf)
#    table_mcoupl.add_variable(bins_ptl1)
#    table_mcoupl.add_variable(bins_minMos)
#    for k in yields.keys():
#        for s in yields[k]:
#            table_mcoupl.add_variable(s)
#    addCommonKeywordsTo(table_mcoupl)
#    submission.add_table(table_mcoupl)
#
#    #tau-coupling
#    yields = {}
#    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'tau')
#    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'tau')
#    yields['tee'] = returnSignalVar(numbers_tee, '$e^{\pm}e^{\pm}\\tau$', 'tau')
#    yields['tmm'] = returnSignalVar(numbers_tmm, '$\mu^{\pm}\mu^{\pm}\\tau$', 'tau')
#    yields['tem'] = returnSignalVar(numbers_tem, '$e\mu\\tau$', 'tau')
#
#    table_tcoupl = Table("Predicted signal yields (Low Mass Region, $\\tau$-coupling)")
#    table_tcoupl.add_variable(bins_binnb)
#    table_tcoupl.add_variable(bins_ossf)
#    table_tcoupl.add_variable(bins_ptl1)
#    table_tcoupl.add_variable(bins_minMos)
#    for k in yields.keys():
#        for s in yields[k]:
#            table_tcoupl.add_variable(s)
#    addCommonKeywordsTo(table_tcoupl)
#    submission.add_table(table_tcoupl)
    
def addLowMassTablesLa(submission):
    from hepdata_lib import Table, Variable

    #First get the independent variables
    bins_binnb = Variable("bin number",
                    is_independent = True,
                    is_binned = False,
                    units = ""
                    )
    bins_binnb.values = ['La{0}'.format(x) for x in range(1, 9)]

    bins_ptl1 = Variable("$p_{T}(l_{1})$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_ptl1.values = ["<30", "<30", "<30", "<30", "30 to 55", "30 to 55", "30 to 55", "30 to 55"]
 
    bins_minMos = Variable("min $m(2l|$OS)",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_minMos.values = ["<10", "10 to 20", "20 to 30", ">30", "<10", "10 to 20", "20 to 30", ">30"]
    
    bins_ossf = Variable("OSSF pair",
                    is_independent = True,
                    is_binned = False,
                    units = ""    
                    )
    bins_ossf.values = ["No"] * 8 

    #Create Table for background and data yields
    #Start by loading in the json
    def loadJsons():
        import json
        eem_path = '../data/yields/LowMass/SR-La/EEE-Mu.json'
        with open(eem_path, 'r') as infile:
            numbers_eem = json.load(infile)
        emm_path = '../data/yields/LowMass/SR-La/MuMuMu-E.json'
        with open(emm_path, 'r') as infile:
            numbers_emm = json.load(infile)
        tee_path = '../data/yields/LowMass/SR-La/TauEE.json'
        with open(tee_path, 'r') as infile:
            numbers_tee = json.load(infile)
        tmm_path = '../data/yields/LowMass/SR-La/TauMuMu.json'
        with open(tmm_path, 'r') as infile:
            numbers_tmm = json.load(infile)
        tem_path = '../data/yields/LowMass/SR-La/TauEMu.json'
        with open(tem_path, 'r') as infile:
            numbers_tem = json.load(infile)
        return (numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)

    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()

    table_bkgr = Table("Data and background yields (Low Mass Region La)")
    table_bkgr.description = "Comparison of the number of predicted background events and the observed events in search regions La. The predicted background yields are shown with the values of the normalizations and nuisance parameters obtained in the background-only fit applied."
    table_bkgr.location = "Figure 8"
    table_bkgr.add_variable(bins_binnb)
    table_bkgr.add_variable(bins_ossf)
    table_bkgr.add_variable(bins_ptl1)
    table_bkgr.add_variable(bins_minMos)
    addBackgroundAndData(table_bkgr, numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)
    addCommonKeywordsTo(table_bkgr)
    submission.add_table(table_bkgr)

    #Signal Tables
    yields_eem = []
    yields_emm = []


    #E-coupling
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'e')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'e')

    table_ecoupl = Table("Predicted signal yields (Low Mass Region La, $e$-coupling)")
    table_ecoupl.description = "Signal yields predicted in search regions La as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and an electron neutrino."
    table_ecoupl.location = "Figure 8"
    table_ecoupl.add_variable(bins_binnb)
    table_ecoupl.add_variable(bins_ossf)
    table_ecoupl.add_variable(bins_ptl1)
    table_ecoupl.add_variable(bins_minMos)
    for k in yields.keys():
        for s in yields[k]:
            table_ecoupl.add_variable(s)
    addCommonKeywordsTo(table_ecoupl)
    submission.add_table(table_ecoupl)

    #Mu-coupling
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'mu')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'mu')

    table_mcoupl = Table("Predicted signal yields (Low Mass Region La, $\mu$-coupling)")
    table_mcoupl.description = "Signal yields predicted in search regions La as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a muon neutrino."
    table_mcoupl.location = "Figure 8"
    table_mcoupl.add_variable(bins_binnb)
    table_mcoupl.add_variable(bins_ossf)
    table_mcoupl.add_variable(bins_ptl1)
    table_mcoupl.add_variable(bins_minMos)
    for k in yields.keys():
        for s in yields[k]:
            table_mcoupl.add_variable(s)
    addCommonKeywordsTo(table_mcoupl)
    submission.add_table(table_mcoupl)

    #tau-coupling
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'tau')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'tau')
    yields['tee'] = returnSignalVar(numbers_tee, '$e^{\pm}e^{\pm}\\tau$', 'tau')
    yields['tmm'] = returnSignalVar(numbers_tmm, '$\mu^{\pm}\mu^{\pm}\\tau$', 'tau')
    yields['tem'] = returnSignalVar(numbers_tem, '$e\mu\\tau$', 'tau')

    table_tcoupl = Table("Predicted signal yields (Low Mass Region La, $\\tau$-coupling)")
    table_tcoupl.description = "Signal yields predicted in search regions La as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a tau neutrino."
    table_tcoupl.location = "Figure 8"
    table_tcoupl.add_variable(bins_binnb)
    table_tcoupl.add_variable(bins_ossf)
    table_tcoupl.add_variable(bins_ptl1)
    table_tcoupl.add_variable(bins_minMos)
    for k in yields.keys():
        for s in yields[k]:
            table_tcoupl.add_variable(s)
    addCommonKeywordsTo(table_tcoupl)
    submission.add_table(table_tcoupl)
 
def addLowMassTablesLb(submission):
    from hepdata_lib import Table, Variable

    #First get the independent variables
    bins_binnb = Variable("bin number",
                    is_independent = True,
                    is_binned = False,
                    units = ""
                    )
    bins_binnb.values = ['Lb{0}'.format(x) for x in range(1, 9)]

    bins_ptl1 = Variable("$p_{T}(l_{1})$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_ptl1.values = ["<30", "<30", "<30", "<30", "30 to 55", "30 to 55", "30 to 55", "30 to 55"]
 
    bins_minMos = Variable("min $m(2l|$OS)",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_minMos.values = ["<10", "10 to 20", "20 to 30", ">30", "<10", "10 to 20", "20 to 30", ">30"]
    
    bins_ossf = Variable("OSSF pair",
                    is_independent = True,
                    is_binned = False,
                    units = ""    
                    )
    bins_ossf.values = ["Yes"] * 8 

    #Create Table for background and data yields
    #Start by loading in the json
    def loadJsons():
        import json
        eem_path = '../data/yields/LowMass/SR-Lb/EEE-Mu.json'
        with open(eem_path, 'r') as infile:
            numbers_eem = json.load(infile)
        emm_path = '../data/yields/LowMass/SR-Lb/MuMuMu-E.json'
        with open(emm_path, 'r') as infile:
            numbers_emm = json.load(infile)
        tee_path = '../data/yields/LowMass/SR-Lb/TauEE.json'
        with open(tee_path, 'r') as infile:
            numbers_tee = json.load(infile)
        tmm_path = '../data/yields/LowMass/SR-Lb/TauMuMu.json'
        with open(tmm_path, 'r') as infile:
            numbers_tmm = json.load(infile)
        tem_path = '../data/yields/LowMass/SR-Lb/TauEMu.json'
        with open(tem_path, 'r') as infile:
            numbers_tem = json.load(infile)
        return (numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)

    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()

    table_bkgr = Table("Data and background yields (Low Mass Region Lb)")
    table_bkgr.description = "Comparison of the number of predicted background events and the observed events in search regions Lb. The predicted background yields are shown with the values of the normalizations and nuisance parameters obtained in the background-only fit applied."
    table_bkgr.location = "Figure 8"
    table_bkgr.add_variable(bins_binnb)
    table_bkgr.add_variable(bins_ossf)
    table_bkgr.add_variable(bins_ptl1)
    table_bkgr.add_variable(bins_minMos)
    addBackgroundAndData(table_bkgr, numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = None)
    addCommonKeywordsTo(table_bkgr)
    submission.add_table(table_bkgr)

    #Signal Tables
    yields_eem = []
    yields_emm = []


    #E-coupling
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'e')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'e')

    table_ecoupl = Table("Predicted signal yields (Low Mass Region Lb, $e$-coupling)")
    table_ecoupl.description = "Signal yields predicted in search regions Lb as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and an electron neutrino."
    table_ecoupl.location = "Figure 8"
    table_ecoupl.add_variable(bins_binnb)
    table_ecoupl.add_variable(bins_ossf)
    table_ecoupl.add_variable(bins_ptl1)
    table_ecoupl.add_variable(bins_minMos)
    for k in yields.keys():
        for s in yields[k]:
            table_ecoupl.add_variable(s)
    addCommonKeywordsTo(table_ecoupl)
    submission.add_table(table_ecoupl)

    #Mu-coupling
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'mu')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'mu')

    table_mcoupl = Table("Predicted signal yields (Low Mass Region Lb, $\mu$-coupling)")
    table_mcoupl.description = "Signal yields predicted in search regions Lb as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a muon neutrino."
    table_mcoupl.location = "Figure 8"
    table_mcoupl.add_variable(bins_binnb)
    table_mcoupl.add_variable(bins_ossf)
    table_mcoupl.add_variable(bins_ptl1)
    table_mcoupl.add_variable(bins_minMos)
    for k in yields.keys():
        for s in yields[k]:
            table_mcoupl.add_variable(s)
    addCommonKeywordsTo(table_mcoupl)
    submission.add_table(table_mcoupl)

    #tau-coupling
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'tau')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'tau')
    yields['tee'] = returnSignalVar(numbers_tee, '$e^{\pm}e^{\pm}\\tau$', 'tau')
    yields['tmm'] = returnSignalVar(numbers_tmm, '$\mu^{\pm}\mu^{\pm}\\tau$', 'tau')
    #yields['tem'] = returnSignalVar(numbers_tem, '$e\mu\\tau$', 'tau')

    table_tcoupl = Table("Predicted signal yields (Low Mass Region Lb, $\\tau$-coupling)")
    table_tcoupl.description = "Signal yields predicted in search regions Lb as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a tau neutrino."
    table_tcoupl.location = "Figure 8"
    table_tcoupl.add_variable(bins_binnb)
    table_tcoupl.add_variable(bins_ossf)
    table_tcoupl.add_variable(bins_ptl1)
    table_tcoupl.add_variable(bins_minMos)
    for k in yields.keys():
        for s in yields[k]:
            table_tcoupl.add_variable(s)
    addCommonKeywordsTo(table_tcoupl)
    submission.add_table(table_tcoupl)

def addHighMassTables(submission):
    from hepdata_lib import Table, Variable

    #First get the independent variables
    bins_binnb = Variable("bin number",
                    is_independent = True,
                    is_binned = False,
                    units = ""    
                    )
    bins_binnb.values = ['Ha{0}'.format(x) for x in range(1, 10)] + ['Hb{0}'.format(x) for x in range(1, 17)]
    
    bins_m3l = Variable("$m(3l)$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_m3l.values = ["<100", "<100", ">100", ">100", ">100", ">100", ">100", ">100", ">100", "<75", "<75", "<75", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105"]
    
    bins_minMos = Variable("min $m(2l|$OS)",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_minMos.values = ["any", "any", "<100", "<100", "<100", "<100", "100 to 200", "100 to 200", ">200", "any", "any", "any", "<100", "<100", "<100", "<100", "<100", "100 to 200", "100 to 200", "100 to 200", "100 to 200", ">200", ">200", ">200", ">200"]
    
    bins_mt = Variable("$m_T$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_mt.values = ["<100", ">100", "<100", "100 to 150", "150 to 250", ">250", "<100", ">100", "any", "<100", "100 to 200", ">200", "<100", "100 to 200", "200 to 300", "300 to 400",">400", "<100", "100 to 200", "200 to 300", ">300", "<100", "100 to 200", "200 to 300", ">300"]
    
    bins_ossf = Variable("OSSF pair",
                    is_independent = True,
                    is_binned = False,
                    units = ""
                    )
    bins_ossf.values = ["No"] * 9 + ["Yes"] * 16

    #Create Table for background and data yields
    #Start by loading in the json
    def loadJsons():
        import json
        eem_path = '../data/yields/HighMass/SR/EEE-Mu.json'
        with open(eem_path, 'r') as infile:
            numbers_eem = json.load(infile)
        emm_path = '../data/yields/HighMass/SR/MuMuMu-E.json'
        with open(emm_path, 'r') as infile:
            numbers_emm = json.load(infile)
        tee_path = '../data/yields/HighMass/SR/TauEE.json'
        with open(tee_path, 'r') as infile:
            numbers_tee = json.load(infile)
        tmm_path = '../data/yields/HighMass/SR/TauMuMu.json'
        with open(tmm_path, 'r') as infile:
            numbers_tmm = json.load(infile)
        tem_path = '../data/yields/HighMass/SR/TauEMu.json'
        with open(tem_path, 'r') as infile:
            numbers_tem = json.load(infile)
        return (numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)

    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()

    table_bkgr = Table("Data and background yields (High Mass Region)")
    table_bkgr.add_variable(bins_binnb)
    table_bkgr.add_variable(bins_m3l)
    table_bkgr.add_variable(bins_minMos)
    table_bkgr.add_variable(bins_mt)
    table_bkgr.add_variable(bins_ossf)
    addBackgroundAndData(table_bkgr, numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)
    addCommonKeywordsTo(table_bkgr)
    submission.add_table(table_bkgr)

    #Signal Tables
    yields_eem = []
    yields_emm = []

    flavor_tex_dict = {'e' : 'e', 'mu' : '\mu', 'tau' : '\\tau'}

    #E-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'e')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'e')

    table_ecoupl = Table("Predicted signal yields (High Mass Region, $e$-coupling)")
    table_ecoupl.add_variable(bins_binnb)
    table_ecoupl.add_variable(bins_m3l)
    table_ecoupl.add_variable(bins_minMos)
    table_ecoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_ecoupl.add_variable(s)
    addCommonKeywordsTo(table_ecoupl)
    submission.add_table(table_ecoupl)

    #Mu-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'mu')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'mu')

    table_mcoupl = Table("Predicted signal yields (High Mass Region, $\mu$-coupling)")
    table_mcoupl.add_variable(bins_binnb)
    table_mcoupl.add_variable(bins_m3l)
    table_mcoupl.add_variable(bins_minMos)
    table_mcoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_mcoupl.add_variable(s)
    addCommonKeywordsTo(table_mcoupl)
    submission.add_table(table_mcoupl)

    #tau-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'tau')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'tau')
    yields['tee'] = returnSignalVar(numbers_tee, '$e^{\pm}e^{\pm}\\tau$', 'tau')
    yields['tmm'] = returnSignalVar(numbers_tmm, '$\mu^{\pm}\mu^{\pm}\\tau$', 'tau')
    yields['tem'] = returnSignalVar(numbers_tem, '$e\mu\\tau$', 'tau')

    table_tcoupl = Table("Predicted signal yields (High Mass Region, $\\tau$-coupling)")
    table_tcoupl.add_variable(bins_binnb)
    table_tcoupl.add_variable(bins_m3l)
    table_tcoupl.add_variable(bins_minMos)
    table_tcoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_tcoupl.add_variable(s)
    addCommonKeywordsTo(table_tcoupl)
    submission.add_table(table_tcoupl)

def addHighMassTablesHa(submission):
    from hepdata_lib import Table, Variable

    #First get the independent variables
    bins_binnb = Variable("bin number",
                    is_independent = True,
                    is_binned = False,
                    units = ""    
                    )
    bins_binnb.values = ['Ha{0}'.format(x) for x in range(1, 10)]
    
    bins_m3l = Variable("$m(3l)$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_m3l.values = ["<100", "<100", ">100", ">100", ">100", ">100", ">100", ">100", ">100"]
    
    bins_minMos = Variable("min $m(2l|$OS)",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_minMos.values = ["any", "any", "<100", "<100", "<100", "<100", "100 to 200", "100 to 200", ">200"]
    
    bins_mt = Variable("$m_T$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_mt.values = ["<100", ">100", "<100", "100 to 150", "150 to 250", ">250", "<100", ">100", "any"]
    
    bins_ossf = Variable("OSSF pair",
                    is_independent = True,
                    is_binned = False,
                    units = ""
                    )
    bins_ossf.values = ["No"] * 9 

    #Create Table for background and data yields
    #Start by loading in the json
    def loadJsons():
        import json
        eem_path = '../data/yields/HighMass/SR-Ha/EEE-Mu.json'
        with open(eem_path, 'r') as infile:
            numbers_eem = json.load(infile)
        emm_path = '../data/yields/HighMass/SR-Ha/MuMuMu-E.json'
        with open(emm_path, 'r') as infile:
            numbers_emm = json.load(infile)
        tee_path = '../data/yields/HighMass/SR-Ha/TauEE.json'
        with open(tee_path, 'r') as infile:
            numbers_tee = json.load(infile)
        tmm_path = '../data/yields/HighMass/SR-Ha/TauMuMu.json'
        with open(tmm_path, 'r') as infile:
            numbers_tmm = json.load(infile)
        tem_path = '../data/yields/HighMass/SR-Ha/TauEMu.json'
        with open(tem_path, 'r') as infile:
            numbers_tem = json.load(infile)
        return (numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)

    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    table_bkgr = Table("Data and background yields (High Mass Region Ha)")
    table_bkgr.description = "Comparison of the number of predicted background events and the observed events in search regions Ha. The predicted background yields are shown with the values of the normalizations and nuisance parameters obtained in the background-only fit applied." 
    table_bkgr.location = "Figure 8"
    table_bkgr.add_variable(bins_binnb)
    table_bkgr.add_variable(bins_m3l)
    table_bkgr.add_variable(bins_minMos)
    table_bkgr.add_variable(bins_mt)
    table_bkgr.add_variable(bins_ossf)
    addBackgroundAndData(table_bkgr, numbers_eem, numbers_emm, numbers_tee, numbers_tmm)
    addCommonKeywordsTo(table_bkgr)
    submission.add_table(table_bkgr)

    #Signal Tables
    yields_eem = []
    yields_emm = []

    flavor_tex_dict = {'e' : 'e', 'mu' : '\mu', 'tau' : '\\tau'}

    #E-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'e')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'e')

    table_ecoupl = Table("Predicted signal yields (High Mass Region Ha, $e$-coupling)")
    table_ecoupl.description = "Signal yields predicted in search regions Ha as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and an electron neutrino."
    table_ecoupl.location = "Figure 8"
    table_ecoupl.add_variable(bins_binnb)
    table_ecoupl.add_variable(bins_m3l)
    table_ecoupl.add_variable(bins_minMos)
    table_ecoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_ecoupl.add_variable(s)
    addCommonKeywordsTo(table_ecoupl)
    submission.add_table(table_ecoupl)

    #Mu-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'mu')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'mu')

    table_mcoupl = Table("Predicted signal yields (High Mass Region Ha, $\mu$-coupling)")
    table_mcoupl.description = "Signal yields predicted in search regions Ha as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a muon neutrino."
    table_mcoupl.location = "Figure 8"
    table_mcoupl.add_variable(bins_binnb)
    table_mcoupl.add_variable(bins_m3l)
    table_mcoupl.add_variable(bins_minMos)
    table_mcoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_mcoupl.add_variable(s)
    addCommonKeywordsTo(table_mcoupl)
    submission.add_table(table_mcoupl)

    #tau-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'tau')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'tau')
    yields['tee'] = returnSignalVar(numbers_tee, '$e^{\pm}e^{\pm}\\tau$', 'tau')
    yields['tmm'] = returnSignalVar(numbers_tmm, '$\mu^{\pm}\mu^{\pm}\\tau$', 'tau')
    yields['tem'] = returnSignalVar(numbers_tem, '$e\mu\\tau$', 'tau')

    table_tcoupl = Table("Predicted signal yields (High Mass Region Ha, $\\tau$-coupling)")
    table_tcoupl.description = "Signal yields predicted in search regions Ha as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a tau neutrino."
    table_tcoupl.location = "Figure 8"
    table_tcoupl.add_variable(bins_binnb)
    table_tcoupl.add_variable(bins_m3l)
    table_tcoupl.add_variable(bins_minMos)
    table_tcoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_tcoupl.add_variable(s)
    addCommonKeywordsTo(table_tcoupl)
    submission.add_table(table_tcoupl)

def addHighMassTablesHb(submission):
    from hepdata_lib import Table, Variable

    #First get the independent variables
    bins_binnb = Variable("bin number",
                    is_independent = True,
                    is_binned = False,
                    units = ""    
                    )
    bins_binnb.values = ['Hb{0}'.format(x) for x in range(1, 17)]
    
    bins_m3l = Variable("$m(3l)$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_m3l.values = ["<75", "<75", "<75", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105", ">105"]
    
    bins_minMos = Variable("min $m(2l|$OS)",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_minMos.values = ["any", "any", "any", "<100", "<100", "<100", "<100", "<100", "100 to 200", "100 to 200", "100 to 200", "100 to 200", ">200", ">200", ">200", ">200"]
    
    bins_mt = Variable("$m_T$",
                    is_independent = True,
                    is_binned = False,
                    units = GEV    
                    )
    bins_mt.values = ["<100", "100 to 200", ">200", "<100", "100 to 200", "200 to 300", "300 to 400",">400", "<100", "100 to 200", "200 to 300", ">300", "<100", "100 to 200", "200 to 300", ">300"]
    
    bins_ossf = Variable("OSSF pair",
                    is_independent = True,
                    is_binned = False,
                    units = ""
                    )
    bins_ossf.values = ["Yes"] * 16

    #Create Table for background and data yields
    #Start by loading in the json
    def loadJsons():
        import json
        eem_path = '../data/yields/HighMass/SR-Hb/EEE-Mu.json'
        with open(eem_path, 'r') as infile:
            numbers_eem = json.load(infile)
        emm_path = '../data/yields/HighMass/SR-Hb/MuMuMu-E.json'
        with open(emm_path, 'r') as infile:
            numbers_emm = json.load(infile)
        tee_path = '../data/yields/HighMass/SR-Hb/TauEE.json'
        with open(tee_path, 'r') as infile:
            numbers_tee = json.load(infile)
        tmm_path = '../data/yields/HighMass/SR-Hb/TauMuMu.json'
        with open(tmm_path, 'r') as infile:
            numbers_tmm = json.load(infile)
        tem_path = '../data/yields/HighMass/SR-Hb/TauEMu.json'
        with open(tem_path, 'r') as infile:
            numbers_tem = json.load(infile)
        return (numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem)

    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()

    table_bkgr = Table("Data and background yields (High Mass Region Hb)")
    table_bkgr.description = "Comparison of the number of predicted background events and the observed events in search regions Hb. The predicted background yields are shown with the values of the normalizations and nuisance parameters obtained in the background-only fit applied. Search regions Hb2 and Hb3 are merged for final states including a hadronically decayed tau lepton. This is represented by the value of -1 in the Hb2 entry."
    table_bkgr.location = "Figure 8"
    table_bkgr.add_variable(bins_binnb)
    table_bkgr.add_variable(bins_m3l)
    table_bkgr.add_variable(bins_minMos)
    table_bkgr.add_variable(bins_mt)
    table_bkgr.add_variable(bins_ossf)
    addBackgroundAndData(table_bkgr, numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem =  None)
    addCommonKeywordsTo(table_bkgr)
    submission.add_table(table_bkgr)

    #Signal Tables
    yields_eem = []
    yields_emm = []

    flavor_tex_dict = {'e' : 'e', 'mu' : '\mu', 'tau' : '\\tau'}

    #E-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'e')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'e')

    table_ecoupl = Table("Predicted signal yields (High Mass Region Hb, $e$-coupling)")
    table_ecoupl.description = "Signal yields predicted in search regions Hb as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and an electron neutrino. Search regions Hb2 and Hb3 are merged for final states including a hadronically decayed tau lepton. This is represented by the value of -1 in the Hb2 entry."
    table_ecoupl.location = "Figure 8"
    table_ecoupl.add_variable(bins_binnb)
    table_ecoupl.add_variable(bins_m3l)
    table_ecoupl.add_variable(bins_minMos)
    table_ecoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_ecoupl.add_variable(s)
    addCommonKeywordsTo(table_ecoupl)
    submission.add_table(table_ecoupl)

    #Mu-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'mu')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'mu')

    table_mcoupl = Table("Predicted signal yields (High Mass Region Hb, $\mu$-coupling)")
    table_mcoupl.description = "Signal yields predicted in search regions Hb as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a muon neutrino. Search regions Hb2 and Hb3 are merged for final states including a hadronically decayed tau lepton. This is represented by the value of -1 in the Hb2 entry."
    table_mcoupl.location = "Figure 8"
    table_mcoupl.add_variable(bins_binnb)
    table_mcoupl.add_variable(bins_m3l)
    table_mcoupl.add_variable(bins_minMos)
    table_mcoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_mcoupl.add_variable(s)
    addCommonKeywordsTo(table_mcoupl)
    submission.add_table(table_mcoupl)

    #tau-coupling
    numbers_eem, numbers_emm, numbers_tee, numbers_tmm, numbers_tem = loadJsons()
    yields = {}
    yields['eem'] = returnSignalVar(numbers_eem, '$e^{\pm}e^{\pm}\mu$', 'tau')
    yields['emm'] = returnSignalVar(numbers_emm, '$\mu^{\pm}\mu^{\pm}e$', 'tau')
    yields['tee'] = returnSignalVar(numbers_tee, '$e^{\pm}e^{\pm}\\tau$', 'tau')
    yields['tmm'] = returnSignalVar(numbers_tmm, '$\mu^{\pm}\mu^{\pm}\\tau$', 'tau')
    #yields['tem'] = returnSignalVar(numbers_tem, '$e\mu\\tau$', 'tau')

    table_tcoupl = Table("Predicted signal yields (High Mass Region Hb, $\\tau$-coupling)")
    table_tcoupl.description = "Signal yields predicted in search regions Hb as function of HNL mass and coupling strength for a scenario with exclusive coupling between a Majorana HNL and a tau neutrino. Search regions Hb2 and Hb3 are merged for final states including a hadronically decayed tau lepton. This is represented by the value of -1 in the Hb2 entry."
    table_tcoupl.location = "Figure 8"
    table_tcoupl.add_variable(bins_binnb)
    table_tcoupl.add_variable(bins_m3l)
    table_tcoupl.add_variable(bins_minMos)
    table_tcoupl.add_variable(bins_mt)
    for k in yields.keys():
        for s in yields[k]:
            table_tcoupl.add_variable(s)
    addCommonKeywordsTo(table_tcoupl)
    submission.add_table(table_tcoupl)

def addAllYieldTables(submission):
    #addLowMassTables(submission)
    #addHighMassTables(submission)
    
    addLowMassTablesLa(submission)
    addLowMassTablesLb(submission)
    addHighMassTablesHa(submission)
    addHighMassTablesHb(submission)

if __name__ == '__main__':
    from hepdata_lib import Submission

    submission = Submission()
    addAllYieldTables(submission)
    submission.create_files('./submission')
 
