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


import helpers
import MatlabWriter
from array import array




"""
Commandline parameter(s):
    none
"""

# set N value.  This is the number of points
N = 35
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

rhcWriter = MatlabWriter("ts_rhc.mat", N, 2)
rhcWriter.addValue(N,"numPoints",0);
rhc = RandomizedHillClimbing(hcp)
begin = 1;
end = 50000;
numSamples = 100;
step = (end - begin) / numSamples;

path = helpers.IterRangeExperiment("RHC", rhc, points, range(begin, end, step), rhcWriter,0)

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
path = helpers.IterRangeExperiment("SA",sa,points,iterVec, rhcWriter,0)
coolingRange = helpers.floatRange( range(50000, 99999 ), 100000, 50)
coolingIters = range(1, 10000, 500)
helpers.CoolingRangeExperiment("SA_cooling", points, hcp, coolingRange, coolingIters, rhcWriter)

#fit = FixedIterationTrainer(sa, SA_iters)
#fit.train()
print "SA Inverse of Distance: " + str(ef.value(sa.getOptimal()))
print "Route:"
print path


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
