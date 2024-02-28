#
# Code to make final hepdata record
#

out_path = '/user/lwezenbe/public_html/HEPData/EXO-22-011'
import os
os.system('rm -rf /user/lwezenbe/public_html/HEPData/EXO-22-011')

def makeDirIfNeeded(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

makeDirIfNeeded(out_path+'/submission')

from hepdata_lib import Submission
submission = Submission()

from createLimits import addFiguresTo
addFiguresTo(submission)

from createPostfitYields import addAllYieldTables
addAllYieldTables(submission)

from createCovariances import addAllCovarTo
addAllCovarTo(submission)

from createCutFlows import addCutflowTo
addCutflowTo(submission)

submission.create_files(out_path+'/submission')
os.system('mv submission.tar.gz {0}/.'.format(out_path))
