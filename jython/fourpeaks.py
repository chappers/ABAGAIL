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
"""
Commandline parameter(s):
   none
"""

DO_RHC = True
DO_SA = True
DO_GA = True
DO_MIMIC = True

test = False
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

    rhcWriter = MatlabWriter(filepath+"RHC_"+str(N)+".mat", N, 2)
    rhcWriter.addValue(N,"numPoints",0)

    start = time.time()
    helpers.IterRangeExperiment("RHC", rhc, ranges, range(begin, end, step), rhcWriter, 0)
    t= time.time() - start

    rhcWriter.addValue(t, "RHC_runtime", 0)
    rhcWriter.write()

#    fit = FixedIterationTrainer(rhc, 200000)
#    fit.train()
#    print "RHC: " + str(ef.value(rhc.getOptimal()))

if DO_SA:
    cooling = .95
    SA_iters = 20000
    sa = SimulatedAnnealing(1E11, cooling, hcp)
    fit = FixedIterationTrainer(sa, SA_iters)
    fit.train()
    print "SA: " + str(ef.value(sa.getOptimal()))

if DO_GA:
    ga = StandardGeneticAlgorithm(200, 100, 10, gap)
    fit = FixedIterationTrainer(ga, 1000)
    fit.train()
    print "GA: " + str(ef.value(ga.getOptimal()))

if DO_MIMIC:
    mimic = MIMIC(200, 20, pop)
    fit = FixedIterationTrainer(mimic, 1000)
    fit.train()
    print "MIMIC: " + str(ef.value(mimic.getOptimal()))
