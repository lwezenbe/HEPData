from hepdataTools import addCommonQualifiersTo, addCommonKeywordsTo

def readHist(hist_loc, name):
    from hepdata_lib import RootFileReader

    # Create a reader for the input file
    reader = RootFileReader(hist_loc)
    
    # Read the histogram, "correlation" is the histogram name
    data = reader.read_hist_2d(name)
    return data

def createAxes(hist_loc, name):
    data = readHist(hist_loc, name) 
    
    from hepdata_lib import Variable
    x = Variable("First Bin", is_independent=True, is_binned=False)
    x.values = data['x']    
 
    y = Variable("Second Bin", is_independent=True, is_binned=False)
    y.values = data['y']
    
    return x, y
    

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

def createTable(hist_loc, name, x_labels):
    
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
    x_labels = {0.5 : 'La1',
                1.5 : 'La2',
                2.5 : 'La3',
                3.5 : 'La4',
                4.5 : 'La5',
                5.5 : 'La6',
                6.5 : 'La7',
                7.5 : 'La8'
    }
    table_lowmass_la = createTable('../data/Covar/lowMassSR-La.root', 'Covariance Matrix (Low Mass SR La)', x_labels)
    table_lowmass_la.description = "Covariance matrix for the postfit background prediction in signal region bins La."
    table_lowmass_la.location = ""
    submission.add_table(table_lowmass_la)
    
    x_labels = {0.5 : 'Lb1',
                1.5 : 'Lb2',
                2.5 : 'Lb3',
                3.5 : 'Lb4',
                4.5 : 'Lb5',
                5.5 : 'Lb6',
                6.5 : 'Lb7',
                7.5 : 'Lb8'
    }
    table_lowmass_lb = createTable('../data/Covar/lowMassSR-Lb.root', 'Covariance Matrix (Low Mass SR Lb)', x_labels)
    table_lowmass_lb.description = "Covariance matrix for the postfit background prediction in signal region bins Lb."
    table_lowmass_lb.location = ""
    submission.add_table(table_lowmass_lb)

def addHighMassTablesTo(submission):
    x_labels = {0.5 : 'Ha1',
                1.5 : 'Ha2',
                2.5 : 'Ha3',
                3.5 : 'Ha4',
                4.5 : 'Ha5',
                5.5 : 'Ha6',
                6.5 : 'Ha7',
                7.5 : 'Ha8',
                8.5 : 'Ha9'}
    table_highmass_ha = createTable('../data/Covar/highMassSR-Ha.root', 'Covariance Matrix (High Mass SR Ha)', x_labels)
    table_highmass_ha.description = "Covariance matrix for the postfit background prediction in signal region bins Ha."
    table_highmass_ha.location = ""
    submission.add_table(table_highmass_ha)
    
    x_labels = {0.5 : 'Hb1',
                1.5 : 'Hb2',
                2.5 : 'Hb3',
                3.5 : 'Hb4',
                4.5 : 'Hb5',
                5.5 : 'Hb6',
                6.5 : 'Hb7',
                7.5 : 'Hb8',
                8.5 : 'Hb9',
                9.5 : 'Hb10',
                10.5 : 'Hb11',
                11.5 : 'Hb12',
                12.5 : 'Hb13',
                13.5 : 'Hb14',
                14.5 : 'Hb15',
                15.5 : 'Hb16'}
    table_highmass_hb = createTable('../data/Covar/highMassSR-Hb.root', 'Covariance Matrix (High Mass SR Hb)', x_labels)
    table_highmass_hb.description = "Covariance matrix for the postfit background prediction in signal region bins Hb."
    table_highmass_hb.location = ""
    submission.add_table(table_highmass_hb)
    
def addAllCovarTo(submission):
    addLowMassTablesTo(submission)
    addHighMassTablesTo(submission)

if __name__ == '__main__':
    from hepdata_lib import Submission

    submission = Submission()
    addLowMassTablesTo(submission)
    addHighMassTablesTo(submission)
    submission.create_files('./submission')
 

         
    

    
