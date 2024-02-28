#import hepdata_lib
from hepdata_lib import Table, Uncertainty, Variable
from hepdataTools import addCommonQualifiersTo, addCommonKeywordsTo

#Qualifiers
COUPLINGE = [["Limits", "Primary exclusion limit on $|V_{eN}|^2$"], ["Limits", "Secondary exclusion limit on $|V_{eN}|^2$"], ["Limits", "Tertiary exclusion limit on $|V_{eN}|^2$"]]
COUPLINGMU = [["Limits", "Primary exclusion limit on $|V_{\mu N}|^2$"], ["Limits", "Secondary exclusion limit on $|V_{\mu N}|^2$"], ["Limits", "Tertiary exclusion limit on $|V_{\mu N}|^2$"]]
COUPLINGTAU = [["Limits", "Primary exclusion limit on $|V_{\tau N}|^2$"], ["Limits", "Secondary exclusion limit on $|V_{\\tau N}|^2$"], ["Limits", "Tertiary exclusion limit on $|V_{\\tau N}|^2$"]]

#COUPLING = {
#    'e' : COUPLINGE,
#    'mu' : COUPLINGMU,
#    'tau' : COUPLINGTAU
#}
COUPLING = {
    'e' : ["Limits", "Exclusion limit on $|V_{eN}|^2$"],
    'mu' : ["Limits", "Exclusion limit on $|V_{\mu N}|^2$"],
    'tau' : ["Limits", "Exclusion limit on $|V_{\\tau N}|^2$"]
}

#Units
GEV = "GeV"

def gatherLimits(in_files, flavor):
    import numpy as np
    import json
    in_limits = []
    for f in in_files:
        with open(f, 'r') as open_file:
            in_limits.append(json.load(open_file))

    merged_limits = {}
    for l in in_limits:
        for m in l.keys():
            if float(m) not in merged_limits.keys():
                merged_limits[float(m)] = [l[m]]
            else:
                merged_limits[float(m)].append(l[m])

    ##Now sort all the ones with length longer than one according to the observed limit
    #def sortkey(limit_dict):
    #    return float(limit_dict['-1.0'])


    #for m in merged_limits.keys():
    #    if len(merged_limits[m]) > 1:
    #        merged_limits[m] = [x for x in sorted(merged_limits[m], key = sortkey)]

    sorted_masses = sorted(merged_limits.keys())
    #Append extra if needed
    sorted_masses_for_var = []
    for m in sorted_masses:
        sorted_masses_for_var.extend([m]*len(merged_limits[m]))

    #Mass variable
    mass_points = Variable('HNL mass')
    mass_points.is_independent = True
    mass_points.is_binned = False
    mass_points.units = GEV
    mass_points.values = sorted_masses_for_var

    observed = []
    expected = []
    onesup = []
    onesdown = []
    twosup = []
    twosdown = []
    for m in sorted_masses:
        tmp_observed = []
        tmp_expected = []
        tmp_1sup = []
        tmp_1sdown = []
        tmp_2sup = []
        tmp_2sdown = []
        for i in range(len(merged_limits[m])):
            tmp_observed.append(merged_limits[m][i]['-1.0'])
            tmp_expected.append(merged_limits[m][i]['0.5'])
            tmp_1sup.append(merged_limits[m][i]['0.84'])
            tmp_1sdown.append(merged_limits[m][i]['0.16'])
            tmp_2sup.append(merged_limits[m][i]['0.975'])
            tmp_2sdown.append(merged_limits[m][i]['0.025'])

        observed.extend(tmp_observed)
        expected.extend(tmp_expected)
        onesup.extend(tmp_1sup)
        twosup.extend(tmp_2sup)
        onesdown.extend(tmp_1sdown)
        twosdown.extend(tmp_2sdown)
            
        
    observed_var = Variable('Observed',
                            is_independent=False,
                            is_binned=False,
                            units = "") 
    observed_var.add_qualifier(*COUPLING[flavor])
    observed_var.values = [x for x in observed]
    addCommonQualifiersTo(observed_var)

    expected_var = Variable('Expected',
                            is_independent=False,
                            is_binned=False,
                            units = "")
    expected_var.add_qualifier(*COUPLING[flavor])
    expected_var.values = [x for x in expected]
    addCommonQualifiersTo(expected_var)   
 
    onesup_var = Variable('68% exp. higher',
                            is_independent=False,
                            is_binned=False,
                            units = "")
    onesup_var.add_qualifier(*COUPLING[flavor])
    onesup_var.values = [x for x in onesup]
    addCommonQualifiersTo(onesup_var)   
 
    onesdown_var = Variable('68% exp. lower',
                            is_independent=False,
                            is_binned=False,
                            units = "")
    onesdown_var.add_qualifier(*COUPLING[flavor])
    onesdown_var.values = [x for x in onesdown]
    addCommonQualifiersTo(onesdown_var)

    twosup_var = Variable('95% exp. higher',
                            is_independent=False,
                            is_binned=False,
                            units = "") 
    twosup_var.add_qualifier(*COUPLING[flavor])
    twosup_var.values = [x for x in twosup]
    addCommonQualifiersTo(twosup_var)   
 
    twosdown_var = Variable('95% exp. lower',
                            is_independent=False,
                            is_binned=False,
                            units = "")
    twosdown_var.add_qualifier(*COUPLING[flavor])
    twosdown_var.values = [x for x in twosdown]
    addCommonQualifiersTo(twosdown_var)

    return [
        mass_points,
        observed_var,
        expected_var,
        onesdown_var,
        onesup_var,
        twosdown_var,
        twosup_var
    ]
        

def gatherLimitsObnoxious(in_files, flavor):
    import numpy as np
    import json
    in_limits = []
    for f in in_files:
        with open(f+'/limits.json', 'r') as open_file:
            in_limits.append(json.load(open_file))

    merged_limits = {}
    for l in in_limits:
        for m in l.keys():
            if float(m) not in merged_limits.keys():
                merged_limits[float(m)] = [l[m]]
            else:
                merged_limits[float(m)].append(l[m])

    #Now sort all the ones with length longer than one according to the observed limit
    def sortkey(limit_dict):
        return float(limit_dict['-1.0'])
        
    
    for m in merged_limits.keys():
        if len(merged_limits[m]) > 1:
            merged_limits[m] = [x for x in sorted(merged_limits[m], key = sortkey)]

    sorted_masses = sorted(merged_limits.keys())

    #Mass variable
    mass_points = Variable('HNL mass')
    mass_points.is_independent = True
    mass_points.is_binned = False
    mass_points.units = GEV
    mass_points.values = sorted_masses

    max_overlap = max([len(merged_limits[m]) for m in merged_limits.keys()])
    
    def getLimit(limits, mass, quantile, iteration):
        if iteration < len(limits[mass]):
            return limits[mass][i][quantile]
        else:
            return -1.

    observed = []
    expected = []
    onesup = []
    onesdown = []
    twosup = []
    twosdown = []
    for i in range(max_overlap):
        tmp_observed = []
        tmp_expected = []
        tmp_1sup = []
        tmp_1sdown = []
        tmp_2sup = []
        tmp_2sdown = []
        for m in sorted_masses:
            tmp_observed.append(getLimit(merged_limits, m, '-1.0', i))
            tmp_expected.append(getLimit(merged_limits, m, '0.5', i))
            tmp_1sup.append(getLimit(merged_limits, m, '0.84', i))
            tmp_1sdown.append(getLimit(merged_limits, m, '0.16', i))
            tmp_2sup.append(getLimit(merged_limits, m, '0.975', i))
            tmp_2sdown.append(getLimit(merged_limits, m, '0.025', i))

        observed.append(Variable('Observed',
                                is_independent=False,
                                is_binned=False,
                                units = "")) 
        observed[i].add_qualifier(*COUPLING[flavor][i])
        observed[i].values = [x for x in tmp_observed]
        
        expected.append(Variable('Expected',
                                is_independent=False,
                                is_binned=False,
                                units = "")) 
        expected[i].add_qualifier(*COUPLING[flavor][i])
        expected[i].values = [x for x in tmp_expected]
        
        onesup.append(Variable('68% exp. higher',
                                is_independent=False,
                                is_binned=False,
                                units = "")) 
        onesup[i].add_qualifier(*COUPLING[flavor][i])
        onesup[i].values = [x for x in tmp_1sup]
        
        onesdown.append(Variable('68% exp. lower',
                                is_independent=False,
                                is_binned=False,
                                units = "")) 
        onesdown[i].add_qualifier(*COUPLING[flavor][i])
        onesdown[i].values = [x for x in tmp_1sdown]

        twosup.append(Variable('95% exp. higher',
                                is_independent=False,
                                is_binned=False,
                                units = "")) 
        twosup[i].add_qualifier(*COUPLING[flavor][i])
        twosup[i].values = [x for x in tmp_2sup]
        
        twosdown.append(Variable('95% exp. lower',
                                is_independent=False,
                                is_binned=False,
                                units = "")) 
        twosdown[i].add_qualifier(*COUPLING[flavor][i])
        twosdown[i].values = [x for x in tmp_2sdown]

    variables_reordered = [mass_points]
    for i in range(max_overlap):
        variables_reordered.append([observed[i], expected[i], onesdown[i], onesup[i], twosup[i], twosdown[i]])

    return variables_reordered


def addFiguresTo(submission):
    
    #Majorana electron limits
    figure_maj_e = Table("Limits on Majorana HNL with electron coupling")
    figure_maj_e.description =     "The 95% CL limits on $|V_{eN}|^2$ as a function of the HNL mass for a Majorana HNL."
    figure_maj_e.location =     "Figure 12 (top left)"
    figure_maj_e.add_image('../data/limits/Majorana-electron/limits-e-maj.pdf')
    in_files = [
        '../data/limits/Majorana-electron/bdt4080.json',
        '../data/limits/Majorana-electron/bdt1040-displaced.json',
        '../data/limits/Majorana-electron/bdt1040-prompt.json',
        '../data/limits/Majorana-electron/bdt85100.json',
        '../data/limits/Majorana-electron/bdt150200.json',
        '../data/limits/Majorana-electron/bdt250400.json',
        '../data/limits/Majorana-electron/cutbased4001500.json',
    ]
    for variable in gatherLimits(in_files, 'e'):
        figure_maj_e.add_variable(variable)
    addCommonKeywordsTo(figure_maj_e)
    submission.add_table(figure_maj_e)
    
    #Majorana muon limits
    figure_maj_mu = Table("Limits on Majorana HNL with muon coupling")
    figure_maj_mu.description =     "The 95% CL limits on $|V_{\mu N}|^2$ as a function of the HNL mass for a Majorana HNL."
    figure_maj_mu.location =     "Figure 12 (middle left)"
    figure_maj_mu.add_image('../data/limits/Majorana-muon/limits-mu-maj.pdf')
    in_files = [
        '../data/limits/Majorana-muon/bdt4080.json',
        '../data/limits/Majorana-muon/bdt1040-displaced.json',
        '../data/limits/Majorana-muon/bdt1040-prompt.json',
        '../data/limits/Majorana-muon/bdt85100.json',
        '../data/limits/Majorana-muon/bdt150200.json',
        '../data/limits/Majorana-muon/bdt250400.json',
        '../data/limits/Majorana-muon/cutbased4001500.json',
    ]
    for variable in gatherLimits(in_files, 'mu'):
        figure_maj_mu.add_variable(variable)
    submission.add_table(figure_maj_mu)
    addCommonKeywordsTo(figure_maj_mu)

    #Majorana tau limits
    figure_maj_tau = Table("Limits on Majorana HNL with tau coupling")
    figure_maj_tau.description =     "The 95% CL limits on $|V_{\\tau N}|^2$ as a function of the HNL mass for a Majorana HNL."
    figure_maj_tau.location =     "Figure 12 (bottom left)"
    figure_maj_tau.add_image('../data/limits/Majorana-tau/limits-tau-maj.pdf')
    in_files = [
        '../data/limits/Majorana-tau/bdt4080.json',
        '../data/limits/Majorana-tau/bdt1040-displaced.json',
        '../data/limits/Majorana-tau/bdt1040-prompt.json',
        '../data/limits/Majorana-tau/cutbased851000.json',
    ]
    for variable in gatherLimits(in_files, 'tau'):
        figure_maj_tau.add_variable(variable)
    addCommonKeywordsTo(figure_maj_tau)
    submission.add_table(figure_maj_tau)

    #Dirac electron limits
    figure_dir_e = Table("Limits on Dirac HNL with electron coupling")
    figure_dir_e.description =     "The 95% CL limits on $|V_{eN}|^2$ as a function of the HNL mass for a Dirac HNL."
    figure_dir_e.location =     "Figure 12 (top right)"
    figure_dir_e.add_image('../data/limits/Dirac-electron/limits-e-dir.pdf')
    in_files = [
        '../data/limits/Dirac-electron/bdt4080.json',
        '../data/limits/Dirac-electron/bdt1040-displaced.json',
        '../data/limits/Dirac-electron/bdt1040-prompt.json',
        '../data/limits/Dirac-electron/bdt85100.json',
        '../data/limits/Dirac-electron/bdt150200.json',
        '../data/limits/Dirac-electron/bdt250400.json',
        '../data/limits/Dirac-electron/cutbased4001500.json',
    ]
    for variable in gatherLimits(in_files, 'e'):
        figure_dir_e.add_variable(variable)
    addCommonKeywordsTo(figure_dir_e)
    submission.add_table(figure_dir_e)

    #Dirac muon limits
    figure_dir_mu = Table("Limits on Dirac HNL with muon coupling")
    figure_dir_mu.description =     "The 95% CL limits on $|V_{\mu N}|^2$ as a function of the HNL mass for a Dirac HNL."
    figure_dir_mu.location =     "Figure 12 (middle right)"
    figure_dir_mu.add_image('../data/limits/Dirac-muon/limits-mu-dir.pdf')
    in_files = [
        '../data/limits/Dirac-muon/bdt4080.json',
        '../data/limits/Dirac-muon/bdt1040-displaced.json',
        '../data/limits/Dirac-muon/bdt1040-prompt.json',
        '../data/limits/Dirac-muon/bdt85100.json',
        '../data/limits/Dirac-muon/bdt150200.json',
        '../data/limits/Dirac-muon/bdt250400.json',
        '../data/limits/Dirac-muon/cutbased4001500.json',
    ]
    for variable in gatherLimits(in_files, 'mu'):
        figure_dir_mu.add_variable(variable)
    submission.add_table(figure_dir_mu)
    addCommonKeywordsTo(figure_dir_mu)

    #Dirac tau limits
    figure_dir_tau = Table("Limits on Dirac HNL with tau coupling")
    figure_dir_tau.description =     "The 95% CL limits on $|V_{\\tau N}|^2$ as a function of the HNL mass for a Dirac HNL."
    figure_dir_tau.location =     "Figure 12 (bottom right)"
    figure_dir_tau.add_image('../data/limits/Dirac-tau/limits-tau-dir.pdf')
    in_files = [
        '../data/limits/Dirac-tau/bdt4080.json',
        '../data/limits/Dirac-tau/bdt1040-displaced.json',
        '../data/limits/Dirac-tau/bdt1040-prompt.json',
        '../data/limits/Dirac-tau/cutbased851000.json',
    ]
    for variable in gatherLimits(in_files, 'tau'):
        figure_dir_tau.add_variable(variable)
    addCommonKeywordsTo(figure_dir_tau)
    submission.add_table(figure_dir_tau)
    

if __name__ == '__main__':
    from hepdata_lib import Submission

    submission = Submission()
    addFiguresTo(submission)
    submission.create_files('./submission')

    
