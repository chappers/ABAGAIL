from math import ceil

import opt.SimulatedAnnealing as SimulatedAnnealing
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import util.ABAGAILArrays as ABAGAILArrays

import opt.prob.MIMIC as MIMIC
from array import array

#from opt.SimulatedAnnealing import SimulatedAnnealing as SimulatedAnnealing
#from shared.FixedIterationTrainer import FixedIterationTrainer as FixedIterationTrainer


__author__ = 'Ramy'


def savePath2Matlab(name, path, points, num, mat):
    xrow =2*(num)
    yrow = xrow+1
    for i in range(0,len(path)):
        p = path[i]
        t= points[p]
        x = points[path[i]][0]
        y = points[path[i]][1]
        mat.addValue(x, name,xrow )
        mat.addValue(y, name,yrow )
    #print path


def saveFit(name, vec, num, mat):
    for i in vec :
        mat.addValue(i,name,num)


def TrainAndSave(experiment,points, fit, mat, name, runNum):
    fitVec =[]
    # for idx, iters in enumerate(paramRange):
    fitness = fit.train()
    fitVec.append(fitness)
    path = []
    if(isinstance(experiment, MIMIC)):
        path = doMIMICExtraction(experiment)
    else:
        N = experiment.getOptimal().size()
        for x in range(0, N):
            path.append(experiment.getOptimal().getDiscrete(x))
    savePath2Matlab(name, path, points,runNum, mat)
    # mw.addValue(iters,"RHC_iterations",idx)
    saveFit(name + "_fitness", fitVec, runNum, mat)
    #    print fitVec
    return path


def floatRange(vec, scale, num):
    tmp =  [];
    stride = int(ceil(float(len(vec)) / num))
    for x in vec[::stride]:
        tmp.append(float(x)/scale);
    return tmp


def IterRangeExperiment(name, experiment, points, paramRange, mat, runNum):
    totalSoFar =0
    for idx, i in enumerate(paramRange):
        num = i-totalSoFar
        fit = FixedIterationTrainer(experiment,num)
        totalSoFar+=num;
        path = TrainAndSave(experiment,points, fit, mat, name, runNum)
    saveFit(name + "_iterations", paramRange, runNum, mat)
    return path


def CoolingRangeExperiment(name,points, problem,coolingRange,iterRange, mat):
    for idx,i in enumerate(coolingRange):
        sa = SimulatedAnnealing(1E15, i, problem)
        IterRangeExperiment(name,sa,points,iterRange,mat,idx)
    saveFit(name + "_coolingValues", coolingRange, 0, mat)
def MIMICSampleRangeExperiment(name, points,problem, sampleRange, iterRange, mat):
    for idx,i in enumerate(sampleRange):
        mimic = MIMIC(i, 20, problem)
        IterRangeExperiment(name, mimic, points, iterRange, mat, idx)
    saveFit(name + "_numSamples", sampleRange,0, mat )

def doMIMICExtraction(mimic):
        optimal = mimic.getOptimal()
        fill = [0] * optimal.size()
        ddata = array('d', fill)
        for i in range(0,len(ddata)):
            ddata[i] = optimal.getContinuous(i)
        order = ABAGAILArrays.indices(optimal.size())
        ABAGAILArrays.quicksort(ddata, order)
        print order
        return order


#
# def getArgs():
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], 'rsgmo:', ['rhc','sa','ga','MIMIC','output='])
#     except getopt.GetoptError, err:
#         print str(err)
#         sys.exit(2)
#     output = None
#     verbose = False
#     for o, a in opts:
#         if o == "-r":
#             DO_RHC = True
#         elif o == "s":
#             DO_SA = True
#         elif o == "g":
#             DO_GA = True
#         elif o == "m":
#             DO_MIMIC = True
#         elif o in ("-o","--output"):
#             output = a
#         else:
#             assert False,"unhandled option"
#
# getArgs()
