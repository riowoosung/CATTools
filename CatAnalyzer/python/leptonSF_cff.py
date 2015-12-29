import FWCore.ParameterSet.Config as cms

muonSFTight = cms.PSet(
    etabins = cms.vdouble(-2.4, -2.1, -1.2, -0.9, 0, 0.9, 1.2, 2.1, 2.4),
    ptbins = cms.vdouble(20, 25, 30, 40, 50, 60, 1e9),
    values = cms.vdouble(
        0.9752116203308105, 0.9738101959228516, 0.9983288645744324, 0.9877836108207703, 
        0.9848297238349915, 0.978645384311676, 0.9905462265014648, 0.9802553653717041, 
        0.9861794114112854, 0.9798933267593384, 0.9923668503761292, 0.9785045385360718, 
        0.987443208694458, 0.980233907699585, 0.9927627444267273, 0.9778544902801514, 
        0.9834294319152832, 0.9773300886154175, 0.9886322021484375, 0.9654409885406494, 
        0.9863178730010986, 0.9795225858688354, 0.9950451850891113, 0.9689615368843079, 
    ),
    errors = cms.vdouble(
        0.0030660638813280626+0.01, 0.004502934246978295+0.01, 0.002331323348626783+0.01, 0.004915740433340289+0.01, 
        0.0016307213764927449+0.01, 0.0027064755458685794+0.01, 0.001402578599690647+0.01, 0.003173276637083633+0.01, 
        0.0006187187412138267+0.01, 0.001057081371390319+0.01, 0.0005653311393042486+0.01, 0.0015542030446523895+0.01, 
        0.000494159746725046+0.01, 0.000819615406448897+0.01, 0.0004155573807947332+0.01, 0.001456799997296391+0.01, 
        0.0011818999573518245+0.01, 0.001955436343316424+0.01, 0.0011254961157344963+0.01, 0.003709169009223743+0.01, 
        0.002073330940717176+0.01, 0.0035622593553725837+0.01, 0.002673833447209764+0.01, 0.011084748199568817+0.01, 
    ),
)

electronSFWP90 = cms.PSet(
    etabins = cms.vdouble(-2.5, -1.5, -1.0, 0, 1.0, 1.5, 2.5),
    ptbins = cms.vdouble(15, 25, 35, 45, 55, 1e9),
    values = cms.vdouble(
        0.96, 0.95, 0.98, 0.99, 0.99, 0.97,
        0.98, 0.97, 0.97, 0.99, 0.99, 0.98,
        0.98, 0.99, 0.99, 0.99, 0.99, 0.98,
        0.98, 0.99, 0.99, 0.99, 0.99, 0.99,
        0.99, 0.99, 0.99, 1.00, 0.99, 0.99,
    ),
    errors = cms.vdouble(
        0.02, 0.06, 0.01, 0.01, 0.02, 0.01, 
        0.01, 0.01, 0.02, 0.01, 0.01, 0.01, 
        0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 
        0.01, 0.0, 0.01, 0.0, 0.01, 0.01, 
        0.01, 0.02, 0.01, 0.0, 0.02, 0.02,
    ),
)

