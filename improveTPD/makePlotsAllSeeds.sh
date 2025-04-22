#!/bin/tcsh
source  /cvmfs/cms.cern.ch/cmsset_default.csh
eval `scram runtime -csh`

foreach i ( 8 9 10 11 0)
    echo "running on seed ${i}"
    root -q -b 'L1TrackNtuplePlot.C("dispSUSY_50mm_cut_inner_VMROuterPR_yesDRcut_noFirstBin","/eos/cms/store/user/fiorendi/l1tt/improveTPD/ntuples/", "", 0,0,0,false,false,3.,100., 2., 10., 10., true, '$i')'

end