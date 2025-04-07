import os, sys
import matplotlib.pyplot as plt
import pandas, uproot
import pdb
import numpy as np

region_label_dict = {
 0 :"A",
 1 :"B",
 2 :"C",
 3 :"D",
 4 :"E",
 5 :"F",
 6 :"G",
 7 :"H",
 8 :"I",
 9 :"J",
}

# input_file = 'testSeeds_50ev.root'
# out_tag = '_50ev'
# input_file = 'testSeeds_cutOnInner_50ev.root'
# out_tag = '_cutOnInner_50ev'

# input_file = 'testSeeds_20DisplSUSY.root'
# out_tag = '_displSUSY_20ev'
# input_file = 'testSeeds_cutOnInner_20DisplSUSY.root'
# out_tag = '_displSUSY_cutOnInner_20ev'

# input_file = 'testSeeds_20DisplSUSY_no_cut_mirror_updateVMRouter_v5_deltaRhalfOK.root' ## new original
# out_tag = '_displSUSY_newOriginal_20ev'

input_file = 'testSeeds_20DisplSUSY_inner_cut_mirror_updateVMRouter_v5_deltaRhalfOK_myLUTonPS.root' ## new with cuts
out_tag = '_displSUSY_deltaRhalfOK_myLUTonPS_20ev_seed10'

## load input file and create pandas df
all_seeds_input = [
          input_file + ':L1SeedsNtuple/tripletsTree',  
]
input_uproot = uproot.concatenate(all_seeds_input, library="np")
dataframe = pandas.DataFrame(input_uproot)


acc_seeds_input = [
          input_file + ':L1AcceptedSeedsNtuple/tripletsTree',  
]
acc_input_uproot = uproot.concatenate(acc_seeds_input, library="np")
dataframe_acc = pandas.DataFrame(acc_input_uproot)

## only seed 10
# dataframe_acc = dataframe_acc[dataframe_acc.middle_layerdisk == 1 &&  dataframe_acc.inner_layerdisk == 6]
# dataframe = dataframe[(dataframe.middle_layerdisk == 1) & (dataframe.inner_layerdisk == 6)]

## group per event and region, and count entries (# triplets) per region
grouped = dataframe.groupby(["eventNumber", "region"]).size().reset_index(name="count")
region_counts = grouped.groupby(["region"])["count"].apply(list)

# plot the distribution of counts for each region
plt.figure(figsize=(10, 6))
for region, counts in region_counts.items():
    plt.hist(counts, bins=20, alpha=0.9, label=f"Region {region}", histtype='step')

plt.xlabel("Number of tested triplets (second block)")
plt.ylabel("Events")
plt.legend()
plt.grid(True)
plt.savefig('plots/ntriplets_vs_region{}.pdf'.format(out_tag))



plt.clf()
## group per event and region/sector/tpdunit, and count entries (# triplets) per sub-region
grouped = dataframe.groupby(["eventNumber", "region", "sector", "tpdunit"]).size().reset_index(name="count")
region_combined_counts = grouped.groupby("region")["count"].apply(list)

plt.figure(figsize=(8, 6))

# plot the distribution of counts for each region (all sectors treated equally, same as tpdunit)
for region, counts in region_combined_counts.items():
#     print(f"Region {region}: Counts {counts}")
    ave = np.mean(counts)
    reg_label = region_label_dict[region]
    plt.hist(counts, bins=20, alpha=0.9, label=f"region {reg_label} (avg {ave:.2f})", histtype='step')

plt.xlabel("Number of tested triplets (second block)")
plt.ylabel("TPD instances")
plt.legend()
plt.yscale('log')
plt.xlim(-40,2000)

plt.text(0.95, 1.04, "20 ev, DisplSUSY 200PU D98", fontsize=12, horizontalalignment='right', verticalalignment='top',transform=plt.gca().transAxes )
# plt.text(0.95, 1.04, "20 ev, DisplSUSY 200PU D98, seed 10", fontsize=12, horizontalalignment='right', verticalalignment='top',transform=plt.gca().transAxes )
plt.grid(True)
plt.savefig('plots/ntriplets_vs_region_v2{}.pdf'.format(out_tag))


exit(0)


## now compare all seeds to selected ones
sel_cols = ['eventNumber', 'inner_r', 'middle_r', 'outer_r', 
                           'inner_z', 'middle_z', 'outer_z', 
                           'inner_bend', 'middle_bend', 'outer_bend', 
#                            'inner_rzbin','middle_rzbin', 'outer_rzbin', 
                           'inner_index', 'middle_index', 'outer_index', 
                           'inner_layerdisk', 'middle_layerdisk', 'outer_layerdisk',
                           'sector', 'region', 
#            'tpdunit'
]

## check if duplicate rows in more inclusive df
duplicate_rows = dataframe[dataframe.duplicated()]
# print("Duplicate Rows:")
# print(duplicate_rows)

## find failing seeds
df_red = dataframe[sel_cols]
df_acc_red = dataframe_acc[sel_cols]
df_fail = pandas.concat([df_acc_red, df_red]).drop_duplicates(keep=False)

## now go back to original df and select failing seeds with full info
full_fail = dataframe.merge(df_fail, on=sel_cols, how='inner')

## plot distributions for failing seeds
plt.clf()
fig, ax = plt.subplots()

pair_list = [
  ['inner_bend', 'middle_bend'],
  ['outer_bend', 'middle_bend'],
  ['inner_bend', 'outer_bend'],
  ['inner_r', 'middle_r'],
  ['outer_r', 'middle_r'],
  ['inner_r', 'outer_r'],
  ['inner_z', 'middle_z'],
  ['outer_z', 'middle_z'],
  ['inner_z', 'outer_z'],
  ['inner_layerdisk', 'middle_layerdisk'],
  ['outer_layerdisk', 'middle_layerdisk'],
  ['inner_layerdisk', 'outer_layerdisk'],
  ['inner_rzbin', 'middle_rzbin'],
  ['outer_rzbin', 'middle_rzbin'],
  ['inner_rzbin', 'outer_rzbin'],
]

for pair in pair_list:
  x = pair[0]
  y = pair[1]
# for x,y in pair_dict.items():
  print (y, 'vs', x)
  plt.clf()

  counts_fail = full_fail.groupby([x, y]).size().reset_index(name='counts')
  plt.scatter(counts_fail[x], counts_fail[y], c=counts_fail['counts'], cmap='viridis', s=20, label='failing', alpha=0.5, edgecolors='none')
  plt.colorbar(label='Counts')  # Add color bar for reference

  # ax.legend()
  # ax.grid(True)
  plt.text(0.5, 1.05, "failing seeds", fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )
  plt.xlabel(x.replace('_', ' '))
  plt.ylabel(y.replace('_', ' '))
  if '_r' in x[-2:]:
    plt.xlim(20,120)
    plt.ylim(20,120)
  plt.savefig('plots/{}_vs_{}_fail{}.pdf'.format(y,x,out_tag))

  plt.clf()
  if 'rzbin' in x:  continue
  counts_pass = dataframe_acc.groupby([x, y]).size().reset_index(name='counts')
  plt.scatter(counts_pass[x], counts_pass[y], c=counts_pass['counts'], cmap='viridis', s=20, label='passing', alpha=0.5, edgecolors='none')
  plt.colorbar(label='Counts')  # Add color bar for reference

  plt.text(0.5, 1.05, "passing seeds", fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )
  plt.xlabel(x.replace('_', ' '))
  plt.ylabel(y.replace('_', ' '))
  if '_r' in x[-2:]:
    plt.xlim(20,120)
    plt.ylim(20,120)
  plt.savefig('plots/{}_vs_{}_pass{}.pdf'.format(y,x,out_tag))

