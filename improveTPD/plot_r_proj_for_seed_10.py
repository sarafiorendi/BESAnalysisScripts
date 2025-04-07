import os, sys
import matplotlib.pyplot as plt
import pandas, uproot
import pdb
import numpy as np
from matplotlib import ticker

# data = pandas.read_csv('seed10_rminmax_tryExtZ0.csv')  
data = pandas.read_csv('check_lut_seed10.csv')  
out_tag = '_v4'

plt.figure(figsize=(10, 6))
plt.clf()
fig, ax = plt.subplots()
'''
r,z,rmin,rmax,rbin1,rbin2,rbin1lut,rbin2lut
'''

def add_labels(x,y, xrange, yrange, text):
    plt.xlabel(x.replace('_', ' '))
    plt.ylabel(y.replace('_', ' '))
    plt.text(0.5, 1.05, text, fontsize=12, horizontalalignment='center', verticalalignment='top',transform=plt.gca().transAxes )


def make_scatter_plot(df, x, y, xrange, yrange, text):
    plt.clf()
    counts = df.groupby([x, y]).size().reset_index(name='counts')
    plt.scatter(counts[x], counts[y], c=counts['counts'], cmap='viridis', s=20, label='failing', alpha=0.3, edgecolors='none')
    plt.colorbar(label='Counts')  # Add color bar for reference
    add_labels(x,y, xrange, yrange, text)


data['deltar_cm'] = data.rmax - data.rmin
data['deltar_bin'] = data.rbin2 - data.rbin1

xrange = [0,1] # not used

x = 'z'
y = 'rmin'
plt.clf()
make_scatter_plot(data, x, y, xrange, xrange, "seed 10")
plt.xlabel('middle stub z')
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))

x = 'z'
y = 'rmax'
plt.clf()
make_scatter_plot(data, x, y, xrange, xrange, "seed 10")
plt.xlabel('middle stub z')
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))


x = 'z'
y = 'deltar_cm'
plt.clf()
make_scatter_plot(data, x, y, xrange, xrange, "seed 10")
plt.xlabel('middle stub z')
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))

y = 'deltar_bin'
xrange = [0,1] # not used
plt.clf()
make_scatter_plot(data, x, y, xrange, xrange, "seed 10")
plt.xlabel('middle stub z')
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))

x = 'rmin'
y = 'rmax'
plt.clf()
make_scatter_plot(data, x, y, xrange, xrange, "seed 10")
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))


x = 'z'
y = 'rmin'
plt.clf()
counts = data.groupby([x, y]).size().reset_index(name='counts')
plt.scatter(counts[x], counts[y], c=counts['counts'], cmap='winter', s=20, label='rmin', alpha=0.3, edgecolors='none')

counts2 = data.groupby([x, 'rmax']).size().reset_index(name='counts')
plt.scatter(counts2[x], counts2['rmax'], c=counts2['counts'], cmap='summer', s=20, label='rmax', alpha=0.3, edgecolors='none')
plt.legend()
add_labels(x,y, xrange, xrange, "seed 10")
plt.xlabel('middle stub z')
plt.savefig('plots/lut_{}_and_rmax_vs_{}_bins{}.pdf'.format(y,x,out_tag))


x = 'r'
y = 'rmin'

plt.clf()
counts = data.groupby([x, y]).size().reset_index(name='counts')
plt.scatter(counts[x], counts[y], c=counts['counts'], cmap='winter', s=20, label='rmin', alpha=0.3, edgecolors='none')
add_labels(x,y, xrange, xrange, "seed 10")
plt.xlabel('middle stub r')
plt.savefig('plots/lut_{}_and_vs_{}_bins{}.pdf'.format(y,x,out_tag))


x = 'r'
y = 'rmax'

plt.clf()
counts = data.groupby([x, y]).size().reset_index(name='counts')
plt.scatter(counts[x], counts[y], c=counts['counts'], cmap='winter', s=20, label='rmin', alpha=0.3, edgecolors='none')
add_labels(x,y, xrange, xrange, "seed 10")
plt.xlabel('middle stub r')
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))


x = 'rbin1lut'
y = 'rbin1'

plt.clf()
counts = data.groupby([x, y]).size().reset_index(name='counts')
plt.scatter(counts[x], counts[y], c=counts['counts'], cmap='winter', s=20, label='rmin', alpha=0.3, edgecolors='none')
add_labels(x,y, xrange, xrange, "seed 10")
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))


x = 'rbin2lut'
y = 'rbin2'

plt.clf()
counts = data.groupby([x, y]).size().reset_index(name='counts')
plt.scatter(counts[x], counts[y], c=counts['counts'], cmap='winter', s=20, label='rmin', alpha=0.3, edgecolors='none')
add_labels(x,y, xrange, xrange, "seed 10")
plt.savefig('plots/lut_{}_vs_{}_bins{}.pdf'.format(y,x,out_tag))
