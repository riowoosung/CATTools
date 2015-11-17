import ROOT, CATTools.CatAnalyzer.CMS_lumi
import copy, sys, json, os
from CATTools.CatAnalyzer.histoHelper import *
ROOT.gROOT.SetBatch(True)

datalumi = 1915.

rootfileDir = "/cms/scratch/tt8888tt/cattools_v744/src/CATTools/CatAnalyzer/test/result_v745/files/"
datasets = json.load(open("%s/src/CATTools/CatAnalyzer/data/dataset.json" % os.environ['CMSSW_BASE']))

mcfilelist = ['TT_powheg',
              'WJets',
              'SingleTbar_tW',
              'SingleTop_tW',
              'ZZ',
              'WW',
              'WZ',
              'DYJets',
              'DYJets_10to50']
rdfilelist = ['MuonEG','DoubleEG','DoubleMuon']
channel_l = ['MuEl', 'ElEl', 'MuMu']

step = 1
channel_name = sys.argv[1]
channel = channel_l.index(channel_name)+1
plotvar = sys.argv[2]
print plotvar

#bin define
ptbin = [20, 0, 200]
etabin = [20, -2.5, 2.5]
massbin = [60, 20, 320]
njetbin = [10, 0, 10]
nbjetbin = [6, 0, 6]
rapibin = [10, -2.5, 2.5]

plotvar_l = ["ll_m", "njet", "met", "nbjet"]
x_name_l = ["M(ll) [GeV/c^{2}]", "Jet Multiplicity", "Missing Et [GeV]", "b Jet Multiplicity"]
binset_l = [massbin, njetbin, ptbin, nbjetbin]

if step >= 5:
	plotvar_l = ["top1_pt", "top1_rapi", "ttbar_pt", "ttbar_rapi", "lep1_pt", "lep1_eta", "jet1_pt", "jet1_eta"]
	binset_l = [ptbin, rapibin, ptbin, rapibin, ptbin, etabin, ptbin, etabin]
	x_name_l = ["Top p_{T} [GeV/c]", "Top Rapidity", "TTbar p_{T} [GeV/c]", "TTbar Rapidity", "lepton p_{T} [GeV/c]", "lepton #eta", "Jet p_{T} [GeV/c]", "Jet #eta"]

weight = 'weight'
#weight = 'weight/puweight'
cut = '(step>=%d && channel == %i && filtered == 1 && tri == 1)*%s'%(step,channel,weight)
print "TCut =",cut

CMS_lumi.lumi_sqrtS = "%.0f pb^{-1}, #sqrt{s} = 13 TeV "%(datalumi)
tname = "cattree/nom"

if channel == 1: ttother_tcut = "!(parton_channel==2 && ((parton_mode1==1 && parton_mode2==2) || (parton_mode1==2 && parton_mode2==1)))"
elif channel == 2: ttother_tcut = "!(parton_channel==2 && (parton_mode1==2 && parton_mode2==2))"
elif channel == 3: ttother_tcut = "!(parton_channel==2 && (parton_mode1==1 && parton_mode2==1))"
ttother_tcut = '(step>=%i && channel == %i && filtered == 1 && tri == 1 && %s)*%s'%(step,channel,ttother_tcut,weight)

binning = binset_l[plotvar_l.index(plotvar)]
x_name = "Step "+str(step)+" "+channel_name+" "+x_name_l[plotvar_l.index(plotvar)]
y_name = 'Number of Events'
if len(binning) <= 3:
	unit = ""
	if x_name.endswith(']'):
		unit = "["+x_name.split('[')[1]
	y_name = y_name + "/%g%s"%((binning[2]-binning[1])/float(binning[0]),unit)

#DY estimation
dyratio = [[0 for x in range(7)] for x in range(4)]
dyratio[1][step] = 1.
if channel !=1:
    scale = 1.
    dycut = ""
    if step == 1: dycut = "(step1==1)*"
    if step == 2: dycut = "(step1==1)*"
    if step == 3: dycut = "(step1==1)*(step3==1)*"
    if step == 4: dycut = "(step1==1)*(step3==1)*(step4==1)*"
    if step >= 5: dycut = "(step1==1)*(step3==1)*(step4==1)*(step5==1)*"

    rfname = rootfileDir + 'DYJets' +".root"
    data = findDataSet('DYJets', datasets)
    scale = datalumi*data["xsec"]
    wentries = getWeightedEntries(rfname, tname, "tri", weight)
    scale = scale/wentries
    
    mc_ee_in = makeTH1(rfname,tname,"mc_ee_in", binning, plotvar, dycut+'(filtered==1 && channel==2 && step2==0)*(%s)'%(weight), scale)
    mc_mm_in = makeTH1(rfname,tname,"mc_mm_in", binning, plotvar, dycut+'(filtered==1 && channel==3 && step2==0)*(%s)'%(weight), scale)
    mc_ee_out = makeTH1(rfname,tname,"mc_ee_in", binning, plotvar, dycut+'(filtered==1 && channel==2 && step2==1)*(%s)'%(weight), scale)
    mc_mm_out = makeTH1(rfname,tname,"mc_mm_in", binning, plotvar, dycut+'(filtered==1 && channel==3 && step2==1)*(%s)'%(weight), scale)

    rfname = rootfileDir + 'DYJets_10to50' +".root"
    data = findDataSet('DYJets_10to50', datasets)
    scale = datalumi*data["xsec"]
    wentries = getWeightedEntries(rfname, tname, "tri", weight)
    scale = scale/wentries
    mc_ee_in.Add(makeTH1(rfname,tname,"mc_ee_in", binning, plotvar, dycut+'(filtered==1 && channel==2 && step2==0)*(%s)'%(weight), scale))
    mc_mm_in.Add(makeTH1(rfname,tname,"mc_mm_in", binning, plotvar, dycut+'(filtered==1 && channel==3 && step2==0)*(%s)'%(weight), scale))
    mc_ee_out.Add(makeTH1(rfname,tname,"mc_ee_in", binning, plotvar, dycut+'(filtered==1 && channel==2 && step2==1)*(%s)'%(weight), scale))
    mc_mm_out.Add(makeTH1(rfname,tname,"mc_mm_in", binning, plotvar, dycut+'(filtered==1 && channel==3 && step2==1)*(%s)'%(weight), scale))
    
    rfname = rootfileDir+rdfilelist[1-1]+".root"
    rd_em_in = makeTH1(rfname, tname,'rd_ee_in', binning, plotvar, dycut+'(filtered==1 && channel==1 && ((ll_m > 76) && (ll_m < 106)))')
    rfname = rootfileDir + rdfilelist[2-1] +".root"
    rd_ee_in = makeTH1(rfname, tname,'rd_ee_in', binning, plotvar, dycut+'(filtered==1 && channel==2 && step2 ==0)')
    rfname = rootfileDir + rdfilelist[3-1] +".root"
    rd_mm_in = makeTH1(rfname, tname,'rd_ee_in', binning, plotvar, dycut+'(filtered==1 && channel==3 && step2 ==0)')

    dyest = drellYanEstimation(mc_ee_in.Integral(), mc_ee_out.Integral(), mc_mm_in.Integral(), mc_mm_out.Integral(),
                               rd_ee_in.Integral(), rd_mm_in.Integral(), rd_em_in.Integral())
    print "DY estimation for", step, "ee =",dyest[0], "mm =",dyest[1]   
    dyratio[2][step] = dyest[0]
    dyratio[3][step] = dyest[1]

mchistList = []
for i, mcname in enumerate(mcfilelist):
	data = findDataSet(mcname, datasets)
	scale = datalumi*data["xsec"]
	colour = data["colour"]
	title = data["title"]
	if 'DYJets' in mcname:
		scale = scale*dyratio[channel][step]

	rfname = rootfileDir + mcname +".root"
	wentries = getWeightedEntries(rfname, tname, "tri", weight)
	scale = scale/wentries
	
	mchist = makeTH1(rfname, tname, title, binning, plotvar, cut, scale)
	mchist.SetLineColor(colour)
	mchist.SetFillColor(colour)
	mchistList.append(mchist)
	if 'TT_powheg' == mcname:
		ttothers = makeTH1(rfname, tname, title+' others', binning, plotvar, ttother_tcut, scale)
		ttothers.SetLineColor(906)
		ttothers.SetFillColor(906)
		mchistList.append(ttothers)
		mchist.Add(ttothers, -1)

rfname = rootfileDir + rdfilelist[channel-1] +".root"
rdhist = makeTH1(rfname, tname, 'data', binning, plotvar, cut)

outfile = "%s_s%d_%s.png"%(channel_name,step,plotvar)
drawTH1(outfile, CMS_lumi, mchistList, rdhist, x_name, y_name, True)
print outfile 
