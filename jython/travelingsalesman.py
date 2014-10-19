# traveling salesman algorithm implementation in jython
# This also prints the index of the points of the shortest route.
# To make a plot of the route, write the points at these indexes
# to a file and plot them in your favorite tool.
from math import ceil
import sys
import os
import time

import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.TravelingSalesmanEvaluationFunction as TravelingSalesmanEvaluationFunction
import opt.example.TravelingSalesmanRouteEvaluationFunction as TravelingSalesmanRouteEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import shared.Instance as Instance
import util.ABAGAILArrays as ABAGAILArrays

import com.jmatio.types.MLDouble as MLDouble
#import matplotlib.pyplot as plt

import MatlabWriter
from array import array




"""
Commandline parameter(s):
    none
"""

# set N value.  This is the number of points
N = 10
random = Random()

points = [[0 for x in xrange(2)] for x in xrange(N)]
for i in range(0, len(points)):
    points[i][0] = random.nextDouble()
    points[i][1] = random.nextDouble()

ef = TravelingSalesmanRouteEvaluationFunction(points)
odd = DiscretePermutationDistribution(N)
nf = SwapNeighbor()
mf = SwapMutation()
cf = TravelingSalesmanCrossOver(ef)
hcp = GenericHillClimbingProblem(ef, odd, nf)
gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)


def savePath2Matlab(name, path, num, mat):
    xrow =2*(num);
    yrow = xrow+1;
    for i in range(0,len(path)):
        p = path[i]
        t= points[p]
        x = points[path[i]][0]
        y = points[path[i]][1]
        mat.addValue(x, name,xrow )
        mat.addValue(y, name,yrow )



def saveFit(name, vec, num, mat):
    for i in vec :
        mat.addValue(i,name,num)


def TrainAndSave(experiment, fit, mat, name, paramRange, runNum):
    fitVec =[]
    for idx, iters in enumerate(paramRange):
        fitness = fit.train()
        fitVec.append(fitness)
        path = []
        for x in range(0, N):
            path.append(experiment.getOptimal().getDiscrete(x))
        savePath2Matlab(name, path, idx, mat)
    # mw.addValue(iters,"RHC_iterations",idx)
    saveFit(name + "_iterations", paramRange, runNum, mat)
    saveFit(name + "_fitness", fitVec, runNum, mat)
    print fitVec
    return path


def IterRangeExperiment(name, experiment, paramRange, mat, runNum):

    t = paramRange[1]-paramRange[0]
    fit = FixedIterationTrainer(experiment,t)
    path = TrainAndSave(experiment, fit, mat, name, paramRange, runNum)
    return path

def CoolingRangeExperiment(name, coolingRange,iterRange, mat):
    for idx,i in enumerate(coolingRange):
        sa = SimulatedAnnealing(1E15, i, hcp)
        IterRangeExperiment(name,sa,iterRange,mat,idx);


def floatRange(vec, scale, num):
    tmp =  [];
    stride = int(ceil(float(len(vec)) / num))
    for x in vec[::stride]:
        tmp.append(float(x)/scale);
    return tmp


rhcWriter = MatlabWriter("ts_rhc.mat", N, 2)
rhc = RandomizedHillClimbing(hcp)
begin = 1;
end = 50000;
numSamples = 100;
step = (end - begin) / numSamples;

path = IterRangeExperiment("RHC", rhc, range(begin, end, step), rhcWriter,0)

print "RHC Inverse of Distance: " + str(ef.value(rhc.getOptimal()))
print "Route:"
print path
rhcWriter.write()

begin = 1;
end = 1000000;
numSamples = 300;
step = (end - begin) / numSamples;
SA_cooling = .695
iterVec = range(begin, end, step)

sa = SimulatedAnnealing(1E15, SA_cooling, hcp)
#saWriter = MatlabWriter("ts_sa.mat", N, 2)
path = IterRangeExperiment("SA",sa,iterVec , rhcWriter,0)
coolingRange = floatRange( range(50000, 99999 ), 100000, 50)
coolingIters = range(1, 10000, 500)
CoolingRangeExperiment("SA_cooling", coolingRange, coolingIters, rhcWriter);

#fit = FixedIterationTrainer(sa, SA_iters)
#fit.train()
print "SA Inverse of Distance: " + str(ef.value(sa.getOptimal()))
print "Route:"
#path = []
#for x in range(0,N):
#    path.append(sa.getOptimal().getDiscrete(x))
#print path


print "writing SA MATLAB matrix"
rhcWriter.write()
print "All Done! Bye now :)"
sys.exit();
#save2matlab("SA", path)

#ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
GA_population =2000
GA_toMate =1500
GA_toMutate=250
GA_iters=2000000;
ga = StandardGeneticAlgorithm(GA_population, GA_toMate, GA_toMutate, gap)
fit = FixedIterationTrainer(ga, 2000000)
fit.train()
print "GA Inverse of Distance: " + str(ef.value(ga.getOptimal()))
print "Route:"
path = []
for x in range(0,N):
    path.append(ga.getOptimal().getDiscrete(x))
print path

save2matlab("GA", path)
# for mimic we use a sort encoding
ef = TravelingSalesmanSortEvaluationFunction(points);
fill = [N] * N
ranges = array('i', fill)
odd = DiscreteUniformDistribution(ranges);
df = DiscreteDependencyTree(.1, ranges);
pop = GenericProbabilisticOptimizationProblem(ef, odd, df);

mimic = MIMIC(500, 100, pop)
fit = FixedIterationTrainer(mimic, 1000)
fit.train()
print "MIMIC Inverse of Distance: " + str(ef.value(mimic.getOptimal()))
print "Route:"
path = []
optimal = mimic.getOptimal()
fill = [0] * optimal.size()
ddata = array('d', fill)
for i in range(0,len(ddata)):
    ddata[i] = optimal.getContinuous(i)
order = ABAGAILArrays.indices(optimal.size())
ABAGAILArrays.quicksort(ddata, order)
print order
save2matlab("MIMIC", order)
mw.write();
