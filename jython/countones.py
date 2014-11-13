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
import shared.ConvergenceTrainer as ConvergenceTrainer
import opt.example.CountOnesEvaluationFunction as CountOnesEvaluationFunction
import dist.RamysMimicDistribution as RamysMimicDistribution
import opt.example.RamysEvalMetaFunc as RamysEvalMetafunc
import MatlabWriter
from array import array


"""
Commandline parameter(s):
   none
"""

DO_RHC = False
DO_SA = False
DO_GA = True
DO_MIMIC = False
TEST = False

NUM_RIGHT = 5

#GA_pop = 200*N
GA_pop = 40000


#problemSizes = range(200,0, -20)
#problemSizes.reverse()

problemSizes = [10, 20 ,30, 50, 80, 110, 150, 180, 225, 300]# 350, 400, 600, 1000, 1500, 2000]

if TEST:
    problemSizes = [10, 20,25]

maxProblem = problemSizes[-1]
#doProblem(5)

myWriter = MatlabWriter("C1s_"+str(maxProblem)+"x"+ str(NUM_RIGHT)+"correct.mat", len(problemSizes), 0)
runNum = 0

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
    global GA_pop
    global myWriter, GA_iters, GA_mut, GA_keep
    GA_keep = int(GA_pop *.75)
    GA_mut = int(GA_pop *.15)


def doProblem (num):

    makeProblem(num)

    if DO_RHC:
        start = time.time()
        RHC()
        t = time.time() -start
        myWriter.addValue(t, "RHC_experimentTime", 0)

    if DO_SA:
        start = time.time()
        SA()
        t = time.time() -start
        myWriter.addValue(t, "SA_experimentTime", 0)
    if DO_GA:
        start = time.time()
        GA()
        t = time.time() -start
        myWriter.addValue(t, "GA_experimentTime", 0)
        #print "GA_experimentTime is " + str(t)
    if DO_MIMIC:
        start = time.time()
        MIMICtest()
        t = time.time() -start
        myWriter.addValue(t, "MIMIC_experimentTime", 0)
    global runNum
    runNum +=1

def RHC():
    correctCount = 0
    RHC_iters = 1
    t=0
    while correctCount <= NUM_RIGHT:
        global rhc
        # print str(correctCount)+  " / 20 correct in RHC w/ iters " + str(RHC_iters)
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, RHC_iters)
        start = time.time()
        fitness = fit.train()
        t = time.time() - start
        myWriter.addValue(fitness, "RHC_fitness", runNum)
        myWriter.addValue(t, "RHC_searchTimes",runNum)
        v = ef.value(rhc.getOptimal())
        if v == N:
            correctCount += 1
        else:
            correctCount = 0
            RHC_iters += 1
    myWriter.addValue(t,"RHC_times",0)
    myWriter.addValue(int(RHC_iters),"RHC_iters",0)
    print str(N) + ": RHC: " + str(ef.value(rhc.getOptimal()))+" took "+str(t)+" seconds and " + str(RHC_iters) + " iterations"

def SA():
    SA_iters = 1
    correctCount = 0
    t=0
    while correctCount <= NUM_RIGHT:
        global sa
        sa = SimulatedAnnealing(1e11, .85, hcp)
        start = time.time()
        fit = FixedIterationTrainer(sa, SA_iters)
        fitness = fit.train()
        t = time.time() - start
        myWriter.addValue(fitness, "SA_fitness", runNum)
        myWriter.addValue(t, "SA_searchTimes",runNum)
        v = ef.value(sa.getOptimal())
        if v == N:
            correctCount += 1
        else:
            correctCount = 0
            SA_iters += 1
    myWriter.addValue(t,"SA_times",0)
    myWriter.addValue(int(SA_iters),"SA_iters",0)
    print str(N) + ": SA: " + str(ef.value(sa.getOptimal())) + " took "+str(t)+ " seconds and " + str(SA_iters) + " iterations"

def GA():
    correctCount = 0
    t=0
    #GA_iters=1
    attempts = 0
    threshold = .1
    iters = 0
    NUM_ITERS =10
    global ga, GA_keep, GA_mut
    ga = StandardGeneticAlgorithm(int(GA_pop), GA_keep, GA_mut, gap)
    while correctCount < 1 and attempts <= 50000:
        attempts +=1
        start = time.time()
        fit =ConvergenceTrainer(ga, threshold, NUM_ITERS)  #FixedIterationTrainer(ga, int(GA_iters))
        fitness=fit.train()
        iters += fit.getIterations()
        myWriter.addValue(fitness, "GA_fitness", runNum)
        myWriter.addValue(t, "GA_searchTimes",runNum)
        t += time.time() - start
        v = ef.value(ga.getOptimal())
        if v == N:
            correctCount+= 1
            #print "GA correct with v  " + str(v) +" correctCount = "+ str (correctCount)
        else:
            if fit.getIterations() < NUM_ITERS: #it hit its iters and still got it wrong, so the threshold was too low
                threshold /= 10
            correctCount = 0
            #GA_pop += N #5*N#*=1.2
            #GA_iters *= 1.5
           # GA_mut = int(GA_pop * .25)
           #GA_keep = int(GA_pop * .80)
    myWriter.addValue(t,"GA_times",0)
    myWriter.addValue(iters,"GA_iters",0)
    myWriter.addValue(int(GA_pop),"GA_pop",0)
    myWriter.addValue(int(GA_mut),"GA_mut",0)
    myWriter.addValue(int(GA_keep),"GA_keep",0)
    print(str(N) + ": GA: " + str(ef.value(ga.getOptimal())) + " took " + str(t) + " seconds and "
    + str(iters) + " iters w/ pop " + str(GA_pop) + " mut " + str(GA_mut) + " keep "+ str(GA_keep)+ " for fitness "
    +str(fitness)+ " in " +str(attempts) + " attempts " + " thresh " + str(threshold) )

def MIMICtest():
    correctCount = 0
    MIMIC_iters = 10
    MIMIC_samples = 5*N #max(1,int(N/10))
    MIMIC_keep = int(.1 * MIMIC_samples)
    t=0
    while correctCount <= NUM_RIGHT and MIMIC_iters <= 500:
        MIMIC_keep = int( max(.1 * MIMIC_samples, 1))
        mimic = MIMIC(int(MIMIC_samples), int(MIMIC_keep), pop)
        start = time.time()
        fit = FixedIterationTrainer(mimic, int(MIMIC_iters))
        fitness = fit.train()
        t = time.time() - start
        v = ef.value(mimic.getOptimal())
        myWriter.addValue(fitness, "MIMIC_fitness", runNum)
        myWriter.addValue(t, "MIMIC_searchTimes",runNum)
        if v==N:
            correctCount +=1
        else:
            correctCount = 0
            MIMIC_iters *=1.1
            MIMIC_samples *=1.1
    myWriter.addValue(t,"MIMIC_times",0)
    myWriter.addValue(int(MIMIC_iters),"MIMIC_iters",0)
    myWriter.addValue(int(MIMIC_samples),"MIMIC_samples",0)
    myWriter.addValue(int(MIMIC_keep),"MIMIC_keep",0)


    print(str(N) + ": MIMIC: " + str(ef.value(mimic.getOptimal())) + " took " + str(t) +
    " seconds and " + str(int(MIMIC_iters)) + " iterations and " + str(int(MIMIC_samples)) +
    " samples with keep " + str(int(MIMIC_keep)))
#TODO: iterate over problem sizes, get wall time, parameters, and fitness function evaluations




for i in problemSizes:
    myWriter.addValue(i,"ProblemSize",0)
    doProblem(i)


myWriter.write()


def mimicGATest():

    popBegin   = 1
    popEnd     = 101
    keepBegin  = 1
    keepEnd    = 90
    mutBegin   = 1
    mutEnd     = 90
    itersBegin = 1
    itersEnd   = 200

    samples = 10
    keep = 2

    problemSize = N
    mimicRange = (problemSize)
    iters = 1

    paramRanges = Vector(8)
    paramRanges.addElement(popBegin)
    paramRanges.addElement(popEnd)
    paramRanges.addElement(keepBegin)
    paramRanges.addElement(keepEnd)
    paramRanges.addElement(mutBegin)
    paramRanges.addElement(mutEnd)
    paramRanges.addElement(itersBegin)
    paramRanges.addElement(itersEnd)

    totalParamSize1 = (popEnd - popBegin +1) + (keepEnd - keepBegin +1) + (mutEnd - mutBegin +1) + (itersEnd - itersBegin +1)
    allParamValues = range(popBegin, popEnd+1)+range(keepBegin, keepEnd+1)+range(mutBegin, mutEnd+1)+range(itersBegin, itersEnd+1)
    totalParamSize = len(allParamValues)
    metaFun = RamysEvalMetafunc(ranges)
    discreteDist = RamysMimicDistribution(paramRanges) #DiscreteUniformDistribution(problemSize)
    distFunc = DiscreteDependencyTree(.1, allParamValues)
    findGA = GenericProbabilisticOptimizationProblem(metaFun, discreteDist, distFunc)
    mimic = MIMIC(samples, keep, findGA)
    fit = FixedIterationTrainer(mimic, iters)
    fit.train()
    print str(N) + ": MIMIC finds GA : " + str(ef.value(mimic.getOptimal()))

#mimicGATest()

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
