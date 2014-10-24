# traveling salesman algorithm implementation in jython
# This also prints the index of the points of the shortest route.
# To make a plot of the route, write the points at these indexes
# to a file and plot them in your favorite tool.
import sys

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



DO_RHC = False
DO_SA = False
DO_GA = False
DO_MIMIC = True
OUTPUT = 'rhc.mat'

# set N value.  This is the number of points
N = 25
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

rhcWriter = MatlabWriter(OUTPUT, N, 2)
rhcWriter.addValue(N,"numPoints",0)
rhc = RandomizedHillClimbing(hcp)
begin = 1
end = 50000
numSamples = 100
step = (end - begin) / numSamples
def PopulationRangeExperiment(name, ga, points, popRange, iterRange, mat):
    for idx,i in enumerate(popRange):
        helpers.IterRangeExperiment(name,ga,points,iterRange,mat,idx)

if(DO_RHC):
    path = helpers.IterRangeExperiment("RHC", rhc, points, range(begin, end, step), rhcWriter,0)

    print "RHC Inverse of Distance: " + str(ef.value(rhc.getOptimal()))
    print "Route:"
    print path
    rhcWriter.write()

if(DO_SA):
    begin = 1
    end = 10000
    numSamples = 300
    step = (end - begin) / numSamples
    SA_cooling = .695
    iterVec = range(begin, end, step)

    sa = SimulatedAnnealing(1E15, SA_cooling, hcp)
    saWriter = MatlabWriter("ts_sa.mat", N, 2)
    saWriter.addValue(N,"numPoints",0)
    path = helpers.IterRangeExperiment("SA",sa,points,iterVec, saWriter,0)
    coolingRange = helpers.floatRange(range(50000, 99999), 100000, 50)
    coolingIters = range(1, 10000, 500)
    helpers.CoolingRangeExperiment("SA_cooling", points, hcp, coolingRange, coolingIters, saWriter)

    saWriter.write();
    print "SA Inverse of Distance: " + str(ef.value(sa.getOptimal()))
    print "Route:"
    print path
    print "writing GA MATLAB matrix"
    saWriter.write()

if(DO_GA):

    #ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
    GA_population =2000
    GA_toMate =1500
    GA_toMutate=250
    GA_iters=20000;
    ga = StandardGeneticAlgorithm(GA_population, GA_toMate, GA_toMutate, gap)

    begin = 100;
    end = 2200
    step =200;
    GAiterVec = range(begin, end, step)
    populationRange = range(5, 1000, 100)
    r = len(populationRange)
    c = len(GAiterVec)
    gaWriter = MatlabWriter("ga.mat",r,c)
    gaWriter.addValue(N,"numPoints",0)
    path = helpers.IterRangeExperiment("GA",ga,points,GAiterVec, gaWriter,0)
    #PopulationRangeExperiment("GA", ga, points, populationRange, GAiterVec, gaWriter)
    #ga.populationSize=1;
    print "writing GA MATLAB matrix"
    gaWriter.write()

    #save2matlab("SA", path)

if(DO_MIMIC):

    ##  for mimic we use a sort encoding
    ef = TravelingSalesmanSortEvaluationFunction(points)
    fill = [N] * N
    ranges = array('i', fill)
    odd = DiscreteUniformDistribution(ranges)
    df = DiscreteDependencyTree(.1, ranges)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

    samplesVec = range(100, 1000, 100)
    keepVec = range(20, 1000, 50)
    iterVec = range(10,1000,100)

    r = len(samplesVec)
    c = len(iterVec)
    mimicWriter = MatlabWriter("mimic_samplesVary.mat", r,c)

    helpers.MIMICSampleRangeExperiment("MIMIC", points, pop, samplesVec,iterVec, mimicWriter)
    #mimic = MIMIC(200,20,pop)
    #path = helpers.IterRangeExperiment("MIMIC",mimic, points, range(100,200,50), mimicWriter,0)
    #fit = FixedIterationTrainer(mimic, 1000)
    #fit.train()


    mimicWriter.write()
    print "All Done! Bye now :)"
    sys.exit()
