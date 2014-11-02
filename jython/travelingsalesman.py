# traveling salesman algorithm implementation in jython
# This also prints the index of the points of the shortest route.
# To make a plot of the route, write the points at these indexes
# to a file and plot them in your favorite tool.


import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution

import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.TravelingSalesmanRouteEvaluationFunction as TravelingSalesmanRouteEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import util.ABAGAILArrays as ABAGAILArrays
import getopt, sys

import helpers
import MatlabWriter
from array import array
import getopt as getopt
import time

def PopulationRangeExperiment(name,  points, popRange, mateRange, mutRange, iterRange, mat):
    lastRow = -1
    for idx,i in enumerate(popRange):
        for jdx, j in enumerate(mateRange):
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


DO_RHC = True
DO_SA = True
DO_GA = True
DO_MIMIC = True

test = False
# set N value.  This is the number of points
N = 4
random = Random(3)
for arg in sys.argv:
    print arg

foo = len(sys.argv)
bar = sys.argv[foo-1]
print "got N as "+ str(bar)

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

    rhcWriter = MatlabWriter("RHC_"+str(N)+".mat", N, 2)
    rhcWriter.addValue(N,"numPoints",0)
    rhc = RandomizedHillClimbing(hcp)

    start = time.time()
    helpers.IterRangeExperiment("RHC", rhc, points, range(begin, end, step), rhcWriter, 0)
    t= time.time() - start

    rhcWriter.addValue(t, "RHC_runtime", 0)
    rhcWriter.write()
    print "RHC done"
if DO_SA:
    if test:
        begin = 1
        end = 100
        numSamples = 10
        coolingRange = helpers.floatRange(range(50000, 99999), 100000, 10)
        coolingIters = range(1, 200, 10)
    else:
        begin = 1
        end = 10000
        numSamples = 300
        coolingRange = helpers.floatRange(range(50000, 99999), 100000, 50)
        coolingIters = range(1, 10000, 500)


    #    step = (end - begin) / numSamples
#    SA_cooling = .695
#    iterVec = range(begin, end, step)
#    sa = SimulatedAnnealing(1E15, SA_cooling, hcp)

    saWriter = MatlabWriter("SA_"+str(N)+".mat", N, 2)
    saWriter.addValue(N,"numPoints",0)
    #path = helpers.IterRangeExperiment("SA",sa,points,iterVec, saWriter, 0)
    start = time.time()
    helpers.CoolingRangeExperiment("SA", points, hcp, coolingRange, coolingIters, saWriter)
    t = time.time() -start
    saWriter.addValue(t,"SA_runtime", 0)
    print "SA done"


    saWriter.write()

if DO_GA:
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
    #ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
    GA_population =2000
    GA_toMate =1500
    GA_toMutate=250
    GA_iters=20000
    ga = StandardGeneticAlgorithm(GA_population, GA_toMate, GA_toMutate, gap)

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

    r = len(populationRange)
    c = len(GAiterVec)
    gaWriter = MatlabWriter("GA_"+str(N)+".mat",r,c)
    gaWriter.addValue(N,"numPoints",0)

    #path = helpers.IterRangeExperiment("GA",ga,points,GAiterVec, gaWriter,0)
    start = time.time()
    PopulationRangeExperiment("GA", points, populationRange,mateRange,mutationRange, GAiterVec, gaWriter)
    t= time.time() - start
    print "writing GA MATLAB matrix"
    gaWriter.addValue(t,"GA_runtime",0)
    gaWriter.write()

    #save2matlab("SA", path)

if DO_MIMIC:

    ##  for mimic we use a sort encoding
    ef = TravelingSalesmanSortEvaluationFunction(points)
    fill = [N] * N
    ranges = array('i', fill)
    odd = DiscreteUniformDistribution(ranges)
    df = DiscreteDependencyTree(.1, ranges)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)


    if test:
        samplesVec = range(5, 200, 50)
        keepVec = range(1, 200, 50)
        iterVec = range(1, 100, 50)
    else:
        samplesVec = range(5, 2000, 50)
        keepVec = range(1, 1900, 300)
        iterVec = range(1, 10000, 500)

    r = len(samplesVec)*len(iterVec)
    c = len(iterVec)
    mimicWriter = MatlabWriter("MIMIC_"+str(N)+".mat", r,c)
    mimicWriter.addValue(N,"numPoints",0)
    #helpers.MIMICSampleRangeExperiment("MIMIC", points, pop, samplesVec,iterVec, mimicWriter)
    start = time.time()
    helpers.MIMICAllRangeExperiment("MIMIC", points, pop, samplesVec, keepVec, iterVec, mimicWriter)
    t= time.time() - start
    mimicWriter.addValue(t,"MIMIC_runtime", 0)
    mimicWriter.write()
    print "All Done! Bye now :)"
    sys.exit()
