# import numpy
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i"  , "--input"     , dest = "input"     ,  help = "input file"       , default = ''                        )
parser.add_argument("-c"  , "--compare"   , dest = "compfile"  ,  help = "file to compare"  , default = ''                        )
parser.add_argument("-d"  , "--diff"      , dest = "diff"      ,  help = "plot differences" , default = False, action='store_true')
parser.add_argument("-m"  , "--mc"        , dest = "mc"        ,  help = "comparison is mc" , default = False, action='store_true')
parser.add_argument("-l"  , "--leg"       , dest = "leg"       ,  help = "legend labels"    , default = ''                        )
parser.add_argument("-o"  , "--outtag"    , dest = "ouffiletag",  help = "tag for out pdf file"    , default = 'default'                        )
parser.add_argument("-s"  , "--seed"      , dest = "seed"      ,  help = "seed number"      , default = 'All'                        )

options = parser.parse_args()
if not options.input:   
  parser.error('Input filename not given')

import ROOT
from   ROOT  import TFile, TTree, gDirectory, TH1F, TCanvas, TLegend, TEfficiency, gPad, gStyle, gROOT, TGaxis, TPad, TGraphErrors, TPaveText
from   array import array
from   math  import sqrt, isnan
from   copy  import deepcopy as dc

gStyle.SetOptStat('emr')
gStyle.SetTitleAlign(23)
gStyle.SetPadLeftMargin(0.16)
gStyle.SetPadBottomMargin(0.16)
TGaxis.SetMaxDigits(3)

gROOT.SetBatch(True)
import pdb; 

namefiles = options.input.split(',')
nfiles   = len(namefiles)
files    = []

print ('number of input files is ' + str(nfiles))

for i in range(0, nfiles):
  print ('opening file ' + str(i) + ': ' + namefiles[i])
  files.append(TFile.Open(namefiles[i]   , 'r') )


pt_bins  = [  0, 15, 18, 20, 22, 25, 30, 40, 50, 60, 80, 120] 
eta_bins = [-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4]

colorlist = [ROOT.kBlack, ROOT.kRed, ROOT.kOrange, ROOT.kGreen+2, ROOT.kAzure+1, ROOT.kViolet, ROOT.kBlue, ROOT.kGray, ROOT.kMagenta+3, ROOT.kOrange+2, ROOT.kYellow]


def doHisto(file, var, thecolor, i, marker=8, toReplace=[]):
#   pdb.set_trace()
  if len(toReplace)==0:
      pEff = file.Get(var[0])
  else:    
      pEff = file.Get(var[0].replace(toReplace[0],toReplace[1]))
  pEff.SetLineColor  (thecolor)
  pEff.SetMarkerColor(thecolor)
  pEff.SetMarkerStyle(marker  )
  pEff.SetMarkerSize(0.8)

  pEff.SetTitle(";" + var[1] + ";" + var[2])
  return pEff


ytitlez = 'z0 resolution'
ytitlep = 'pt resolution'
ytitlep2 = 'pt resolution/pt'
ytitlee = 'efficiency'

yrange = (0., 1.2)
if options.seed != 'All':
  yrange = (0., 0.5)
  
variables = [
#  numerator          # x axis title        # y title   # nbins    # x range      # y range      # pdf name                     # legend position         #y range ratio          
#  ('resVsEta_z0_68'    , '|#eta|'              , ytitlez,    30   , (  0   , 30   ), (0.00 , 3),     'resVsEta68',     (0.2 , 0.7, 0.75, 0.88),  (0.501, 1.05 )), 
#  ('resVsPt2_z0_68'    , 'pt'                  , ytitlez,    30   , (  0   , 30   ), (0.00 , 3),    'z0resVsPt68',    (0.2 , 0.7, 0.75, 0.88),  (0.501, 1.05 )), 
#  ('resVsPt2_ptRel_68' , 'pt'                  , ytitlep2,   30   , (  0   , 30   ), (0.00 , 1.5 ), 'relpTresVsPt68',   (0.2 , 0.7, 0.75, 0.88),  (0.501, 1.05 )), 
#  ('eff_pt'            , 'p_{T}'               , ytitlee,    30   , (  0   , 20   ), (0.3   ,1.1),     'effVsPt',      (0.2 , 0.7, 0.75, 0.88),  (0.501, 1.05 )), 
#  ('eff_eta'           , '#eta'                , ytitlee,   100   , ( -3.  , 3    ), (0.3   ,1.1),     'effVsEta',      (0.2 , 0.7, 0.75, 0.88),  (0.5  , 1.05  )),
#  ('eff_d0'            , 'd0'                  , ytitlee,    50   , ( -10. ,  10. ), (0.   ,.5),    'effVsD0',       (0.2 , 0.5, 0.25, 0.38),  (0.5  , 1.05  )),
#  ('eff_z0'            , 'z0'                  , ytitlee,    50   , ( -10. ,  10. ), (0.   ,.5),    'effVsZ0',       (0.2 , 0.5, 0.25, 0.38),  (0.5  , 1.05  )),
 ('eff_pt'            , 'p_{T}'               , ytitlee,    30   , (  0   , 20   ), yrange,    'effVsPt',       (0.2 , 0.7, 0.75, 0.88),  (0.501, 1.05 )), 
 ('eff_eta'           , '|#eta|'              , ytitlee,   100   , ( -3.  , 3    ), yrange,    'effVsEta',      (0.2 , 0.7, 0.75, 0.88),  (0.5  , 1.05  )),
 ('eff_d0'            , 'd0'                  , ytitlee,    50   , ( -10. ,  10. ), yrange,    'effVsD0',       (0.2 , 0.7, 0.78, 0.88),  (0.5  , 1.05  )),
 ('eff_z0'            , 'z0'                  , ytitlee,    50   , ( -10. ,  10. ), yrange,    'effVsZ0',       (0.2 , 0.7, 0.75, 0.88),  (0.5  , 1.05  )),
#  ('duplicatefrac_pt' , 'p_{T} [GeV]'          , 'duplicate fraction',    50   , ( 0. ,  25 ), (0.   , .07),    'dupVsPt',       (0.2 , 0.5, 0.75, 0.88),  (0.5  , 1.05  )),
] 

import pdb

c2 = TCanvas('c2', 'c2', 600,600)
c1 = TCanvas('c1', 'c1', 600,600)
if options.diff:
  stackPad = ROOT.TPad('stackPad', 'stackPad', 0.,  .25, 1., 1.  , 0, 0)  
  ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0. , 1.,  .3, 0, 0)  
else:
  stackPad = ROOT.TPad('stackPad', 'stackPad', 0,  0. , 1., 1.  , 0, 0)  
  ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0. , 0.00001, 0.00001  , 0, 0)  

## define baseline legend
leg_labels = []
if options.leg:
  for i in range(len(files)):
    leg_labels.append(options.leg.split(',')[i])

for var in variables:

  c1.cd()
  stackPad.Draw()
  ratioPad.Draw()

#   pdb.set_trace()  
#   l = TLegend(var[7][0], var[7][2], var[7][1], var[7][3], 'DisplacedMu Pt 2-10 50mm, PU200, seed 9')
  l = TLegend(var[7][0], var[7][2], var[7][1], var[7][3], 'DisplacedSUSY 50mm, PU200, seed {}'.format(options.seed))
  l.SetBorderSize(1)
  l.SetTextSize(0.023)
  
  eff_list = [] 
  for i, ifile in enumerate(files):
    c2.cd() 
    eff_list.append(dc(doHisto(ifile , var, colorlist[i], i)))
    
    if '_68' in var[0]:
        if i==0:
            sec_leg = TLegend( .66, .75, .75, .88 )
#             sec_leg = TLegend( .8, .2, .9, .35 )
            sec_leg.SetBorderSize(1)
            sec_leg.SetTextSize(0.022)
            sec_leg.AddEntry(eff_list[-1], '68%', 'p')

        eff_list.append(dc(doHisto(ifile , var, colorlist[i], i, 26, ['68','90'])))
        eff_list[-1].SetLineStyle(2)
        eff_list[-1].SetLineWidth(1)
        if i==0:  sec_leg.AddEntry(eff_list[-1], '90%', 'p')

        eff_list.append(dc(doHisto(ifile , var, colorlist[i], i, 25, ['68','99'])))
        eff_list[-1].SetLineStyle(3)
        eff_list[-1].SetLineWidth(1)
        if i==0:  sec_leg.AddEntry(eff_list[-1], '99%', 'p')
        
  c1.cd()
  stackPad.cd()
  
  drawOption = 'PL'*('res' in var[0]) + 'EP'*('res' not in var[0])
  for i,k in enumerate(eff_list):
    if (i == 0):
      k.Draw(drawOption)
      c1.Update()
      c1.Modified()

      k.GetYaxis().SetRangeUser(var[5][0],var[5][1])             
      k.GetXaxis().SetLabelSize(0.04)
      k.GetYaxis().SetLabelSize(0.04)   
      k.GetXaxis().SetTitleSize(0.04)
      k.GetYaxis().SetTitleSize(0.04)
      k.GetYaxis().SetTitleOffset(1.5)
      k.GetXaxis().SetTitleOffset(1.2)

    else:
      k.Draw(drawOption + 'SAME')

    if options.leg and '68' not in var[0]:
        l.AddEntry(k , leg_labels[i]  , "pel")
    elif options.leg and i%3==0:
#         pdb.set_trace()
        l.AddEntry(k , leg_labels[int(i/3)]  , "pel")
    
  if options.leg: l.Draw()
  if '_68' in var[0] :
      sec_leg.Draw()


  gPad.SetGridx(True)
  gPad.SetGridy(True)

  c1.SaveAs("plots/" +  var[6] + "_D98_%s.pdf"%options.ouffiletag)



