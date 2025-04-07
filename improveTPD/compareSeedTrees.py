import os, sys
import matplotlib.pyplot as plt
import pandas, uproot
import pdb
import numpy as np

# input_file = 'testSeeds_50ev.root'
# out_tag = '_50ev'
# input_file = 'testSeeds_cutOnInner_50ev.root'
# out_tag = '_cutOnInner_50ev'
import cmasher as cmr
mycmap = cmr.get_sub_cmap('GnBu', 0.2, 1)

# input_file = 'testSeeds_20DisplSUSY_no_cut_mirror_updateVMRouter_v5.root'
input_file = 'testSeeds_20DisplSUSY_no_cut_mirror_updateVMRouter_v5_deltaRhalfOK.root'

# input_file_cut = 'testSeeds_20DisplSUSY_inner_cut_mirror_updateVMRouter_v5.root' ## this is the new one ok
# input_file_cut = 'testSeeds_20DisplSUSY_inner_cut_mirror_updateVMRouter_v5_deltaRhalfOK.root'
input_file_cut = 'testSeeds_20DisplSUSY_inner_cut_mirror_updateVMRouter_v5_deltaRhalfOK_myLUTonPSv2.root'
out_tag = '_compareWithCut_mirror_updateVMRouter_v5_deltaRhalf_myLUTOnPSv2'

## load input file and create pandas df
all_seeds_input = [
          input_file + ':L1SeedsNtuple/tripletsTree',  
]
input_uproot = uproot.concatenate(all_seeds_input, library="np")
dataframe = pandas.DataFrame(input_uproot)


all_seeds_cut = [
          input_file_cut + ':L1SeedsNtuple/tripletsTree',  
]
cut_input_uproot = uproot.concatenate(all_seeds_cut, library="np")
dataframe_cut = pandas.DataFrame(cut_input_uproot)


all_good_seeds = [
          input_file + ':L1AcceptedSeedsNtuple/tripletsTree',  
]
in_good_uproot = uproot.concatenate(all_good_seeds, library="np")
dataframe_good = pandas.DataFrame(in_good_uproot)

good_seeds_after_cut = [
          input_file_cut + ':L1AcceptedSeedsNtuple/tripletsTree',  
]
cut_good_uproot = uproot.concatenate(good_seeds_after_cut, library="np")
dataframe_good_cut = pandas.DataFrame(cut_good_uproot)


plt.figure(figsize=(10, 6))
## now compare all seeds to selected ones
sel_cols = ['eventNumber', 'inner_r', 'middle_r', 'outer_r', 
                           'inner_z', 'middle_z', 'outer_z', 
                           'inner_bend', 'middle_bend', 'outer_bend', 
#                            'inner_rzbin','middle_rzbin', 'outer_rzbin', ## old files have wrong middle_rzbin 
                           'inner_index', 'middle_index', 'outer_index', 
                           'inner_layerdisk', 'middle_layerdisk', 'outer_layerdisk',
                           'sector', 'region', 
]

## find not produced seeds (need to merge on sel cols because trp unit could be different)
df_red = dataframe[sel_cols] 
df_cut_red = dataframe_cut[sel_cols]
df_fail = pandas.concat([df_cut_red, df_red]).drop_duplicates(keep=False)

## find common seeds
df_dupl = pandas.concat([df_cut_red, df_red])
df_dupl = df_dupl[df_dupl.duplicated()]

## find seeds that were good but got removed
## first go back to original df and select failing seeds with full info
full_fail = dataframe.merge(df_fail, on=sel_cols, how='inner')
losses = dataframe_good.merge(full_fail, on=sel_cols, how='inner', suffixes=('_good', '_fail'))

## keep values from full_fail for columns which are only filled in that df
for col in full_fail.columns:
    if col not in sel_cols:  # Avoid overwriting the key columns
        losses[col] = losses[f'{col}_fail']
losses = losses[[col for col in losses.columns if not col.endswith('_good') and not col.endswith('_fail')]]
losses['delta_bin'] = losses.rzeff_in - losses.firstbin_in
losses['out_of_window'] = losses.rzeff_in < losses.firstbin_in

losses_d1tol2 = losses[(losses.middle_layerdisk == 6) & (losses.inner_layerdisk == 1) ]
losses_l2tod1 = losses[(losses.middle_layerdisk == 1) & ((losses.inner_layerdisk == 6))]
losses_else   = losses[(losses.middle_layerdisk == 2) | (losses.middle_layerdisk == 4)]

## find good seeds that are created originally and with the cut
df_ok = dataframe_good[sel_cols] 
df_ok_cut = dataframe_good_cut[sel_cols]
df_good_both = pandas.concat([df_ok_cut, df_ok]).drop_duplicates(keep=False)
df_good_both_l2tod1 = df_good_both[(df_good_both.middle_layerdisk == 1) & ((df_good_both.inner_layerdisk == 6))]


## plot distributions for failing seeds
plt.clf()
fig, ax = plt.subplots()
xrange = [-120, 120]
yrange = [-120, 120]

def add_labels(x,y, xrange, yrange, text):
    plt.xlim(xrange[0], xrange[1])
    plt.ylim(yrange[0], yrange[1])
    plt.xlabel(x.replace('_', ' '))
    plt.ylabel(y.replace('_', ' '))
    plt.text(0.5, 1.05, text, fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )


def make_scatter_plot(df, x, y, xrange, yrange, text, colormap = 'viridis', alphaVal=0.3, sizeVal = 20):
    plt.clf()
    counts = df.groupby([x, y]).size().reset_index(name='counts')
    plt.scatter(counts[x], counts[y], c=counts['counts'], cmap=colormap, s=sizeVal, label='failing', alpha=alphaVal, edgecolors='none')
    plt.colorbar(label='Counts')  # Add color bar for reference
    add_labels(x,y, xrange, yrange, text)

def make_hist2d(df, x,y, xrange, yrange, Nx, Ny, min_counts, text):
    plt.clf()
    xbins = np.linspace(xrange[0], xrange[1], Nx+1)
    ybins = np.linspace(yrange[0], yrange[1], Ny+1)
    hist, x_bins, y_bins, im = plt.hist2d(df[x], df[y], bins=[xbins,ybins], cmap=mycmap, cmin = 1)
    cb = plt.colorbar()
    cb.set_label('counts per bin')
    add_labels(x,y, xrange, yrange, text)


pair_list = [
#   ['inner_r', 'middle_r'],
#   ['inner_z', 'middle_z'],
#   ['inner_layerdisk', 'middle_layerdisk'],
# # #   ['inner_rzbin', 'middle_rzbin'],
#   ['inner_z', 'inner_r'],
#   ['middle_z', 'middle_r'],
]

for pair in pair_list:
  x = pair[0]
  y = pair[1]
  print (y, 'vs', x)
  if '_r' in x[-2:]:
    xrange = [20,120]
  elif '_z' in x[-2:]:
    xrange = [-150, 150]
  if '_r' in y[-2:]:
    yrange = [20,120]
  elif '_z' in y[-2:]:
    yrange = [-150, 150]
  if 'layerdisk' in y:
    xrange = [0,8]
    yrange = [0,8]

  N = 100
  if 'layerdisk' in x:
    N = 8
    

  plt.clf()

  make_hist2d(df_fail, x, y, xrange, yrange , N, N, 2, "removed seeds")
  plt.savefig('plots/{}_vs_{}_removed{}_binned.pdf'.format(y,x,out_tag))
  make_hist2d(df_dupl, x, y, xrange, yrange , N, N, 2, "common seeds")
  plt.savefig('plots/{}_vs_{}_common{}_binned.pdf'.format(y,x,out_tag))
  make_hist2d(losses, x, y, xrange, yrange , N, N, 2, "good seeds that are lost")
  plt.savefig('plots/{}_vs_{}_lost{}_binned.pdf'.format(y,x,out_tag))
  ## only for D1->L2
  make_hist2d(losses_d1tol2, x, y, xrange, yrange , N, N, 2, "good seeds that are lost for D1L2")
  plt.savefig('plots/seed11/{}_vs_{}_lostD1L2{}_binned.pdf'.format(y,x,out_tag))
  ## only for L2->D1
  make_hist2d(losses_l2tod1, x, y, xrange, yrange , N, N, 2, "good seeds that are lost for L2D1")
  plt.savefig('plots/seed10/{}_vs_{}_lostL2D1{}_binned.pdf'.format(y,x,out_tag))
  ## losses others
  make_hist2d(losses_else, x, y, xrange, yrange , N, N, 2, "good seeds that are lost (seed 8 and 9)")
  plt.savefig('plots/seed8_9/{}_vs_{}_lostOthers{}_binned.pdf'.format(y,x,out_tag))


  ##now make scatter plots
  if 'layerdisk' in x:  continue
  make_scatter_plot(df_fail, x, y, xrange, yrange, "removed seeds")
  plt.savefig('plots/{}_vs_{}_removed{}.pdf'.format(y,x,out_tag))
  make_scatter_plot(df_dupl, x, y, xrange, yrange, "common seeds")
  plt.savefig('plots/{}_vs_{}_common{}.pdf'.format(y,x,out_tag))
  make_scatter_plot(losses, x, y, xrange, yrange, "good seeds that are lost")
  plt.savefig('plots/{}_vs_{}_lost{}.pdf'.format(y,x,out_tag))

  ## only for D1->L2
  make_scatter_plot(losses_d1tol2, x, y, xrange, yrange, "good seeds that are lost for D1L2")
  plt.savefig('plots/seed11/{}_vs_{}_lostD1L2{}.pdf'.format(y,x,out_tag))
  ## only for L2->D1
  make_scatter_plot(losses_l2tod1, x, y, xrange, yrange, "good seeds that are lost for L2D1")
  plt.savefig('plots/seed10/{}_vs_{}_lostL2D1{}.pdf'.format(y,x,out_tag))
  make_scatter_plot(df_good_both_l2tod1, x, y, xrange, yrange, "good seeds that are kept for L2D1")
  plt.savefig('plots/seed10/{}_vs_{}_bothPassL2D1{}.pdf'.format(y,x,out_tag))
  ## losses others
  make_scatter_plot(losses_else, x, y, xrange, yrange, "good seeds that are lost (seed 8 and 9)")
  plt.savefig('plots/seed8_9/{}_vs_{}_lostOthers{}.pdf'.format(y,x,out_tag))



## 1D plots   
plt.clf()
plt.text(0.5, 1.05, "good seeds that are lost for D1L2", fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )
plt.hist(losses_d1tol2.diffmax_in, bins=100)
plt.hist(losses_d1tol2[losses_d1tol2.middle_z < 0].diffmax_in, bins=100, label='middle_z < 0')
plt.legend()
plt.xlim(0, 7)
plt.xlabel('diffmax_in')
plt.savefig('plots/seed11/{}_lostD1L2{}.pdf'.format('diffmax_in',out_tag))

plt.clf()
plt.text(0.5, 1.05, "good seeds that are lost for L2D1", fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )
plt.hist(losses_l2tod1.diffmax_in, bins=100)
plt.hist(losses_l2tod1[losses_l2tod1.middle_z < 0].diffmax_in, bins=100, label='middle_z < 0')
plt.legend()
plt.xlim(0, 7)
plt.xlabel('diffmax_in')
plt.savefig('plots/{}_lostL2D1{}.pdf'.format('diffmax_in',out_tag))

## now go back to original df and select passing seeds with full info
full_seeds = dataframe.merge(dataframe_good, on=sel_cols, how='inner', suffixes=('_all', '_good'))
for col in dataframe.columns:
    if col not in sel_cols:  # Avoid overwriting the key columns
        full_seeds[col] = full_seeds[f'{col}_all']

plt.clf()
plt.text(0.5, 1.05, "good seeds original", fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )
plt.hist(full_seeds.diffmax_in, bins=100)
plt.xlabel('diffmax_in')
plt.xlim(0, 7)
plt.savefig('plots/{}_goodSeeds{}.pdf'.format('diffmax_in',out_tag))



## 2D plots to understand the cut 

x = 'delta_bin'
y = 'diffmax_in'
xrange = [-8, 10]
yrange = [-1, 15]
make_scatter_plot(losses_l2tod1, x, y, xrange, yrange, "good seeds that are lost for D1L2", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.savefig('plots/seed11/cut_lostD1L2_{}{}{}.pdf'.format(y,x,out_tag))

make_scatter_plot(losses_d1tol2[losses_d1tol2.inner_z < 0], x, y, xrange, yrange, "good seeds that are lost for D1L2, negative Z", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.savefig('plots/seed11/cut_lostD1L2_negZ_{}{}{}.pdf'.format(y,x,out_tag))


xrange = [-8, 16]
yrange = [-1, 16]
make_scatter_plot(losses_l2tod1, x, y, xrange, yrange, "good seeds that are lost for L2D1", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.grid(True, ls = '--', lw = 0.4, zorder = 0)
plt.savefig('plots/seed10/cut_lostL2D1_{}{}{}.pdf'.format(y,x,out_tag))

make_scatter_plot(losses_l2tod1, x, y, xrange, yrange, "good seeds that are lost", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.grid(True, ls = '--', lw = 0.4, zorder = 0)
plt.savefig('plots/cut_lost_{}{}{}.pdf'.format(y,x,out_tag))

xrange = [-1, 16]
make_scatter_plot(losses_l2tod1[losses_l2tod1.out_of_window == False], x, y, xrange, yrange, "good seeds that are lost for L2D1 if IN window", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.grid(True, ls = '--', lw = 0.4, zorder = -0.5)
plt.savefig('plots/seed10/cut_lostL2D1_in_window_{}{}{}.pdf'.format(y,x,out_tag))


x = 'firstbin_in'
y = 'rzeff_in'
xrange = [-1, 16]
make_scatter_plot(losses_d1tol2[losses_d1tol2.out_of_window == True], x, y, xrange, yrange, "good seeds that are lost for D1L2 if out of window", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.savefig('plots/seed11/cut_lostD1L2_out_window_{}{}{}.pdf'.format(y,x,out_tag))

make_scatter_plot(losses_l2tod1[losses_l2tod1.out_of_window == True], x, y, xrange, yrange, "good seeds that are lost for L2D1 if out of window", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.grid(True, ls = '--', lw = 0.4, zorder = 0)
plt.savefig('plots/seed10/cut_lostL2D1_out_window_{}{}{}.pdf'.format(y,x,out_tag))

make_scatter_plot(losses_l2tod1[losses_l2tod1.out_of_window == False], x, y, xrange, yrange, "good seeds that are lost for L2D1 if IN window", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.grid(True, ls = '--', lw = 0.4, zorder = 0)
plt.savefig('plots/seed10/cut_lostL2D1_in_window_{}{}{}.pdf'.format(y,x,out_tag))


y = 'middle_z'
x = 'delta_bin'
make_scatter_plot(losses_l2tod1[losses_l2tod1.out_of_window == False], x, y, xrange, yrange, "good seeds that are lost for L2D1 if IN window", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.grid(True, ls = '--', lw = 0.4, zorder = 0)
plt.savefig('plots/seed10/cut_lostL2D1_in_window_{}{}{}.pdf'.format(y,x,out_tag))


x = 'diffmax_in'
y = 'rzeff_in'
make_scatter_plot(losses_l2tod1[losses_l2tod1.out_of_window == True], x, y, xrange, yrange, "good seeds that are lost for L2D1 if out of window", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.grid(True, ls = '--', lw = 0.4, zorder = 0)
plt.savefig('plots/seed10/cut_lostL2D1_out_window_{}{}{}.pdf'.format(y,x,out_tag))


y = 'inner_r'
x = 'delta_bin'
make_scatter_plot(losses_l2tod1, x, y, xrange, yrange, "good seeds that are lost for L2D1", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.savefig('plots/seed10/cut_lostL2D1_{}{}{}.pdf'.format(y,x,out_tag))

y = 'middle_z'
x = 'delta_bin'
make_scatter_plot(losses_l2tod1, x, y, xrange, yrange, "good seeds that are lost for L2D1", colormap = 'winter', alphaVal = 0.8, sizeVal=50)
plt.savefig('plots/seed10/cut_lostL2D1_{}{}{}.pdf'.format(y,x,out_tag))

