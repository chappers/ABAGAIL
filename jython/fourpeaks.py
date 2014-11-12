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
import time
import helpers as helpers
from array import array
import MatlabWriter
#from travelingsalesman import PopulationRangeExperiment
"""
Commandline parameter(s):
   none
"""

DO_RHC =   False #True
DO_SA =    False #True
DO_GA =    True
DO_MIMIC = True
test =     False
N=200
T=N/5
fill = [2] * N
ranges = array('i', fill)

ef = FourPeaksEvaluationFunction(T)
odd = DiscreteUniformDistribution(ranges)
nf = DiscreteChangeOneNeighbor(ranges)
mf = DiscreteChangeOneMutation(ranges)
cf = SingleCrossOver()
df = DiscreteDependencyTree(.1, ranges)
hcp = GenericHillClimbingProblem(ef, odd, nf)
gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
rhc = RandomizedHillClimbing(hcp)
filepath = "4P/"

def PopulationRangeExperiment(name,  points, popRange, mateRange, mutRange, iterRange, mat):
    lastRow = -1
    for idx,i in enumerate(popRange):
        for jdx, j in enumerate(mateRange):
            print('.')
            for kdx, k in enumerate(mutRange):
                row = idx * len(mateRange)*len(mutRange) + jdx*len(mutRange)+ kdx
                if row < lastRow:
                    print "ERROR in ROW CALC!"
                lastRow = row
                if j > i or k > i:
                    #print "skipping bad values for i,j,k "
                    continue
                ga = StandardGeneticAlgorithm(i, j, k, gap)
                helpers.IterRangeExperiment(name, ga, points, iterRange, mat, row)


def makeFileName(file,N):
    res = filepath + file + "_" + str(N)+ ".mat"
    return res


if DO_RHC:
    if test:
        begin = 1
        end = 500
        numSamples = 10
    else:
        begin = 1
        end = 50000
        numSamples = 100

    step = (end - begin) / numSamples

    f = makeFileName("RHC", N)
    rhcWriter = MatlabWriter(f, N, 2)
    rhcWriter.addValue(N,"numPoints",0)

    start = time.time()
    helpers.IterRangeExperiment("RHC", rhc, ranges, range(begin, end, step), rhcWriter, 0)
    t=time.time() - start

    rhcWriter.addValue(t, "RHC_runtime", 0)
    rhcWriter.write()

    print "RHC done..." + str(f)
    # fit = FixedIterationTrainer(rhc, 200000)
    # fit.train()
    # print "RHC: " + str(ef.value(rhc.getOptimal()))

if DO_SA:
    if test:
        begin = 1
        end = 100
        numSamples = 10
        coolingRange = helpers.floatRange(range(50000, 99999), 100000, 10)
        coolingIters = range(1, 200, 10)
    else:
        begin = 1
        end = 100000
        numSamples = 300
        coolingRange = helpers.floatRange(range(50000, 99999), 100000, 50)
        coolingIters = range(1, 100000, 500)

    f = makeFileName("SA", N)
    saWriter = MatlabWriter(f, N, 2)
    saWriter.addValue(N,"numPoints",0)
    #path = helpers.IterRangeExperiment("SA",sa,points,iterVec, saWriter, 0)
    start = time.time()
    helpers.CoolingRangeExperiment("SA", ranges, hcp, coolingRange, coolingIters, saWriter)
    t = time.time() -start
    saWriter.addValue(t,"SA_runtime", 0)
    saWriter.write()
    print "SA done..."  + str(f)

    # cooling = .95
    # sa = SimulatedAnnealing(1E11, cooling, hcp)
    # fit = FixedIterationTrainer(sa, 2000)
    # fit.train()
    # print "SA: " + str(ef.value(sa.getOptimal()))

if DO_GA:
    begin = 100
    end = 2200
    step =200
    if test:
        GAiterVec = range(1, 10, 2)
        populationRange = range(5, 100, 10)
        mateRange = range(1, 10, 5)
        mutationRange = range(1, 10, 5)
    else:
        GAiterVec = range(begin, end, step)
        populationRange = range(5, 10000, 500)
        mateRange = range(5, 9000, 500)
        mutationRange = range(5, 9000, 500)


    f = makeFileName("GA", N)
    gaWriter = MatlabWriter(f,N,2)
    gaWriter.addValue(N,"numPoints",0)
    start = time.time()
    PopulationRangeExperiment("GA", ranges, populationRange,mateRange,mutationRange, GAiterVec, gaWriter)

    t = time.time() -start
    gaWriter.addValue(t,"GA_runtime", 0)
    gaWriter.write()

    print "GA done..."  + str(f)
    # ga = StandardGeneticAlgorithm(200, 100, 10, gap)
    # fit = FixedIterationTrainer(ga, 1000)
    # fit.train()
    # print "GA: " + str(ef.value(ga.getOptimal()))

if DO_MIMIC:

    if test:
        samplesVec = range(1, 10, 2)
        keepVec = range(1, 8, 2)
        iterVec = range(10, 101, 10)
    else:
        samplesVec = range(5000, 20001, 5000)
        keepVec = range(1000, 20001, 5000)
        iterVec = range(1000, 100001, 10000)


    f = makeFileName("MIMIC", N)
    mimicWriter = MatlabWriter(f,N,2)
    mimicWriter.addValue(N,"numPoints",0)

    start = time.time()
    helpers.MIMICAllRangeExperiment("MIMIC", ranges, pop, samplesVec, keepVec, iterVec, mimicWriter)
    t = time.time() -start

    mimicWriter.addValue(t,"MIMIC_runtime", 0)
    mimicWriter.write()

    print "MIMIC done: wrote " + str(f)
    # mimic = MIMIC(200, 20, pop)
    # fit = FixedIterationTrainer(mimic, 1000)
    # fit.train()
    #print "MIMIC: " + str(ef.value(mimic.getOptimal()))
