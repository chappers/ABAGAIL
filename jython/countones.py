from hmac import new
from math import ceil
import sys
import os
import time

import java.io.FileReader as FileReader
import java.io.File as File
from java.lang import Integer
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
from java.util import Vector
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
import opt.example.CountOnesEvaluationFunction as CountOnesEvaluationFunction
import dist.RamysMimicDistribution as RamysMimicDistribution
import opt.example.RamysEvalMetaFunc as RamysEvalMetafunc
from array import array


"""
Commandline parameter(s):
   none
"""


def makeProblem(num):
    global N
    N = num
    global fill
    fill = [2] * N
    global ranges
    ranges = array('i', fill)
    global ef
    ef = CountOnesEvaluationFunction()
    global odd
    odd = DiscreteUniformDistribution(ranges)
    global nf
    nf = DiscreteChangeOneNeighbor(ranges)
    global mf
    mf = DiscreteChangeOneMutation(ranges)
    global cf
    cf = SingleCrossOver()
    global df
    df = DiscreteDependencyTree(.1, ranges)
    global hcp
    hcp = GenericHillClimbingProblem(ef, odd, nf)
    global gap
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
    global pop
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)



def doProblem (num):

    makeProblem(num)

    correctCount = 0
    RHC_iters = 1
    while correctCount <= 20:
        global rhc
        # print str(correctCount)+  " / 20 correct in RHC w/ iters " + str(RHC_iters)
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, RHC_iters)
        fit.train()
        v = ef.value(rhc.getOptimal())
        if v == N:
            correctCount += 1
        else:
            correctCount = 0
            RHC_iters += 1

    print str(N) + ": RHC: " + str(ef.value(rhc.getOptimal()))+ " took " + str(RHC_iters)


    SA_iters = 1
    correctCount = 0
    while correctCount <= 20:
        global sa
        sa = SimulatedAnnealing(1e11, .85, hcp)
        fit = FixedIterationTrainer(sa, SA_iters)
        fit.train()
        v = ef.value(sa.getOptimal())
        if v == N:
            correctCount += 1
        else:
            correctCount = 0
            SA_iters += 1

    print str(N) + ": SA: " + str(ef.value(sa.getOptimal())) + " took " + str(SA_iters)

    correctCount = 0
    GA_iters = 1
    GA_pop = 500
    GA_keep = int( ceil(GA_pop *.9))
    GA_mut = int(.01 * GA_pop)
    while correctCount <= 20 and GA_iters <= 5000:
        global ga
        ga = StandardGeneticAlgorithm(GA_pop, GA_keep, GA_mut, gap)
        fit = FixedIterationTrainer(ga, GA_iters)
        fit.train()
        v = ef.value(ga.getOptimal())
        if v == N:
            correctCount+= 1
            #print "GA correct with v  " + str(v) +" correctCount = "+ str (correctCount)
        else:
            #print "GA wrong w/ iters " + str(GA_iters)
            correctCount = 0
            GA_pop +=10
            GA_iters += 10
            GA_mut = int( GA_pop * .25)
            GA_keep = int(GA_pop * .80)

    print str(N) + ": GA: " + str(ef.value(ga.getOptimal())) + " took " + str(GA_iters)


    mimic = MIMIC(50, 5, pop)
    fit = FixedIterationTrainer(mimic, 100)
    fit.train()
    print str(N) + ": MIMIC: " + str(ef.value(mimic.getOptimal()))



problemSizes = range(200,0, -5)
problemSizes.reverse()

doProblem(10)
#for i in problemSizes:
#    doProblem(i)




def mimicGATest():

    popBegin   = 100
    popEnd     = 1000
    keepBegin  = 10
    keepEnd    = 95
    mutBegin   = 1
    mutEnd     = 95
    itersBegin = 100
    itersEnd   = 10000

    samples = 800
    keep = 500

    problemSize = N
    mimicRange = (problemSize)
    iters = 1000

    paramRanges = Vector(8)
    paramRanges.addElement(popBegin)
    paramRanges.addElement(popEnd)
    paramRanges.addElement(keepBegin)
    paramRanges.addElement(keepEnd)
    paramRanges.addElement(mutBegin)
    paramRanges.addElement(mutEnd)
    paramRanges.addElement(itersBegin)
    paramRanges.addElement(itersEnd)

    discreteDist = RamysMimicDistribution(paramRanges) #DiscreteUniformDistribution(problemSize)
    distFunc = RamysEvalMetafunc() # DiscreteDependencyTree(.1, mimicRange)
    findGA = GenericProbabilisticOptimizationProblem(ef, discreteDist, distFunc)
    mimic = MIMIC(samples, keep, findGA)
    fit = FixedIterationTrainer(mimic, iters)
    fit.train()
    print str(N) + ": MIMIC finds GA : " + str(ef.value(mimic.getOptimal()))

mimicGATest()

#
# makeProblem(80)
#
# rhc = RandomizedHillClimbing(hcp)
# fit = FixedIterationTrainer(rhc, 8000)
# fit.train()
# print str(N) + ": RHC: " + str(ef.value(rhc.getOptimal()))
#
# sa = SimulatedAnnealing(1e11, .85, hcp)
# fit = FixedIterationTrainer(sa, 8000)
# fit.train()
# print str(N) + ": SA: " + str(ef.value(sa.getOptimal()))
#
# ga = StandardGeneticAlgorithm(1000, 800, 50, gap)
# fit = FixedIterationTrainer(ga, 800)
# fit.train()
# print str(N) + ": GA: " + str(ef.value(ga.getOptimal()))
#
# mimic = MIMIC(500, 10, pop)
# fit = FixedIterationTrainer(mimic, 800)
# fit.train()
# print str(N) + ": MIMIC: " + str(ef.value(mimic.getOptimal()))
