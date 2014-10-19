from math import ceil

import opt.SimulatedAnnealing as SimulatedAnnealing
import shared.FixedIterationTrainer as FixedIterationTrainer

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


def TrainAndSave(experiment,points, fit, mat, name, paramRange, runNum):
    fitVec =[]
    for idx, iters in enumerate(paramRange):
        fitness = fit.train()
        fitVec.append(fitness)
        path = []
        N = experiment.getOptimal().size();
        for x in range(0, N):
            path.append(experiment.getOptimal().getDiscrete(x))
        savePath2Matlab(name, path, points,idx, mat)
    # mw.addValue(iters,"RHC_iterations",idx)
    saveFit(name + "_iterations", paramRange, runNum, mat)
    saveFit(name + "_fitness", fitVec, runNum, mat)
    print fitVec
    return path


def floatRange(vec, scale, num):
    tmp =  [];
    stride = int(ceil(float(len(vec)) / num))
    for x in vec[::stride]:
        tmp.append(float(x)/scale);
    return tmp


def IterRangeExperiment(name, experiment, points, paramRange, mat, runNum):

    t = paramRange[1]-paramRange[0]
    fit = FixedIterationTrainer(experiment,t)
    path = TrainAndSave(experiment,points, fit, mat, name, paramRange, runNum)
    return path


def CoolingRangeExperiment(name,points, problem,coolingRange,iterRange, mat):
    for idx,i in enumerate(coolingRange):
        sa = SimulatedAnnealing(1E15, i, problem)
        IterRangeExperiment(name,sa,points,iterRange,mat,idx)