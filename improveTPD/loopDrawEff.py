import subprocess

for iseed in ['8', '9', '10', '11', 'All']:
  seed_str = '_seed'+str(iseed)
  if iseed == 'All':
    seed_str = ''
  subprocess.run(["python", "drawEfficiencyL1.py", 
                  "-i", "output_dispSUSY_50mm_original_beforePR{}_pt3.root,\
                         output_dispSUSY_50mm_cut_inner_VMROuterPR_noDRcut_yesFirstBin{}_pt3.root,\
                         output_dispSUSY_50mm_cut_inner_VMROuterPR_yesDRcut_noFirstBin{}_pt3.root".format(seed_str, seed_str, seed_str), 
                  "-l", "original,cut (first bin only),cut (deltaR only)", 
                  "-s", str(iseed), 
                  "-o", "understandCut{}".format(seed_str)
                  ]) 


# output_dispSUSY_50mm_cut_inner_VMROuterPR_noDRcut_yesFirstBin_seed11_pt3.root
# output_dispSUSY_50mm_cut_inner_VMROuterPR_yesDRcut_noFirstBin_pt3.root
# output_dispSUSY_50mm_original_beforePR_seed11_pt3.root

# python drawEfficiencyL1.py -i output_dispSUSY_50mm_original_beforePR_seed8_pt3.root,output_dispSUSY_50mm_original_cut_rvalue_seed8_pt3.root -l 'original,rzbin cut inner' -o seed8

#  python drawEfficiencyL1.py -i output_dispSUSY_50mm_cut_inner_VMROuterPR_noDRcut_yesFirstBin_pt3.root,output_dispSUSY_50mm_cut_inner_VMROuterPR_noDRcut_yesFirstBin_seed8_pt3.root,output_dispSUSY_50mm_cut_inner_VMROuterPR_noDRcut_yesFirstBin_seed9_pt3.root,output_dispSUSY_50mm_cut_inner_VMROuterPR_noDRcut_yesFirstBin_seed10_pt3.root,output_dispSUSY_50mm_cut_inner_VMROuterPR_noDRcut_yesFirstBin_seed11_pt3.root -l 'all,8,9,10,11' -o test_overlay