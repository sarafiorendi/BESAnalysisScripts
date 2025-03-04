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

## load input file and create pandas df
all_seeds_input = [
          'testSeeds.root:L1SeedsNtuple/tripletsTree',  
]
input_uproot = uproot.concatenate(all_seeds_input, library="np")
dataframe = pandas.DataFrame(input_uproot)


acc_seeds_input = [
          'testSeeds.root:L1AcceptedSeedsNtuple/tripletsTree',  
]
acc_input_uproot = uproot.concatenate(acc_seeds_input, library="np")
dataframe_acc = pandas.DataFrame(acc_input_uproot)


## group per event and region, and count entries (# triplets) per region
grouped = dataframe.groupby(["eventNumber", "region"]).size().reset_index(name="count")
region_counts = grouped.groupby(["region"])["count"].apply(list)

# plot the distribution of counts for each region
plt.figure(figsize=(10, 6))
for region, counts in region_counts.items():
    plt.hist(counts, bins=20, alpha=0.9, label=f"Region {region}", histtype='step')

plt.xlabel("Number of accepted triplets (second block)")
plt.ylabel("Events")
plt.legend()
plt.grid(True)
plt.savefig('ntriplets_vs_region.pdf')



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

plt.xlabel("Number of accepted triplets (second block)")
plt.ylabel("TPD instances")
plt.legend()
plt.yscale('log')

plt.text(0.95, 1.04, "50 ev, TTBar 200PU D98", fontsize=12, horizontalalignment='right', verticalalignment='top',transform=plt.gca().transAxes )
plt.grid(True)
plt.savefig('ntriplets_vs_region_v2.pdf')



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
  if '_r' in x:
    plt.xlim(20,120)
    plt.ylim(20,120)
  plt.savefig('{}_vs_{}_fail.pdf'.format(y,x))

  plt.clf()
  counts_pass = dataframe_acc.groupby([x, y]).size().reset_index(name='counts')
  plt.scatter(counts_pass[x], counts_pass[y], c=counts_pass['counts'], cmap='viridis', s=20, label='passing', alpha=0.5, edgecolors='none')
  plt.colorbar(label='Counts')  # Add color bar for reference

  plt.text(0.5, 1.05, "passing seeds", fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )
  plt.xlabel(x.replace('_', ' '))
  plt.ylabel(y.replace('_', ' '))
  if '_r' in x:
    plt.xlim(20,120)
    plt.ylim(20,120)
  plt.savefig('{}_vs_{}_pass.pdf'.format(y,x))

