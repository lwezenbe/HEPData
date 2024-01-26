from hepdataTools import addCommonQualifiersTo, addCommonKeywordsTo

def readHist(hist_loc, name):
    from hepdata_lib import RootFileReader

    # Create a reader for the input file
    reader = RootFileReader(hist_loc)
    
    # Read the histogram, "correlation" is the histogram name
    data = reader.read_hist_2d(name)
    return data

def createVar(hist_loc, name):
   
    data = readHist(hist_loc, name) 

    from hepdata_lib import Variable
    covar = Variable("Covariance", is_independent=False, is_binned=False)
    covar.values = data["z"]

    addCommonQualifiersTo(covar) 
    return covar


channel_dict = {
    'EEE-Mu'    : '$e^{\pm}e^{\pm}\mu$',
    'MuMuMu-E'  : '$\mu^{\pm}\mu^{\pm}e$',
    'TauEMu'    : '$e\mu\\tau$',
    'TauEE'     : '$e^{\pm}e^{\pm}\\tau$',
    'TauMuMu'   : '$\mu^{\pm}\mu^{\pm}\\tau$'
}

def createTable(hist_loc, x_labels, name):
    
    from hepdata_lib import Table, Variable
    table = Table(name)


    from hnlTools import rootFileContent
    from ROOT import TFile
    in_file = TFile(hist_loc, 'read')
    rfc = rootFileContent(in_file)
    channels = [x[0].split('/')[-1] for x in rfc]
    in_file.Close()
    
    tmp_var = readHist(hist_loc, channels[0])

    x = Variable("First Bin", is_independent=True, is_binned=False)
    x.values = [x_labels[l] for l in tmp_var['x']]
    table.add_variable(x)

    y = Variable("Second Bin", is_independent=True, is_binned=False)
    y.values = [x_labels[l] for l in tmp_var['y']]
    table.add_variable(y)
    
    for c in channels:
        tmp_var = createVar(hist_loc, c)
        try:
            tmp_var.add_qualifier('Channel', channel_dict[c])
        except:
            tmp_var.add_qualifier('Channel', c)

        table.add_variable(tmp_var)

    addCommonKeywordsTo(table)
    return table

def addLowMassTablesTo(submission):
    x_labels = {
        0.5 : 'Ha1',
        1.5 : 'Ha2',
        2.5 : 'Ha3',
        3.5 : 'Ha4',
        4.5 : 'Ha5',
        5.5 : 'Ha6',
        6.5 : 'Ha7',
        7.5 : 'Ha8',
        8.5 : 'Hb1',
        9.5 : 'Hb2',
        10.5 : 'Hb3',
        11.5 : 'Hb4',
        12.5 : 'Hb5',
        13.5 : 'Hb6',
        14.5 : 'Hb7',
        15.5 : 'Hb8',
    }
    table_lowmass = createTable('../data/Covar/test.root', x_labels, 'Covariance Matrix (Low Mass SR)')
    submission.add_table(table_lowmass)

if __name__ == '__main__':
    from hepdata_lib import Submission

    submission = Submission()
    addLowMassTablesTo(submission)
    submission.create_files('./submission')
 

         
    

    
