# Release: take CMSSW_10_6_X as default (works for both UL and older reprocessings), fall back to CMSSW_10_2_X on T2_BE_IIHE
RELEASE=CMSSW_12_2_3

BRANCH=master

#If the release is already available using cmsenv, use it, otherwise set up a new one
if [[ $CMSSW_BASE == *$RELEASE ]] && [[ -d $CMSSW_BASE ]]; then
  echo "Setting up Hepdata framework in current release: $CMSSW_BASE"
  cd $CMSSW_BASE/src
else
  scram project CMSSW $RELEASE
  cd $RELEASE/src
  eval `scram runtime -sh`
  echo "Creating release for Hep framework: $CMSSW_BASE"
fi

git clone https://github.com/lwezenbe/HEPData
cd HEPData
scram b -j 10

echo "Setup finished"

