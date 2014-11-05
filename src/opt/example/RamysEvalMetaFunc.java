package opt.example;

import dist.DiscreteUniformDistribution;
import opt.EvaluationFunction;
import opt.ga.DiscreteChangeOneMutation;
import opt.ga.GenericGeneticAlgorithmProblem;
import opt.ga.SingleCrossOver;
import opt.ga.StandardGeneticAlgorithm;
import shared.FixedIterationTrainer;
import shared.Instance;
import util.linalg.Vector;

/**
 * A function that tries to get MIMIC to optimize the params for another algo
 */
public class RamysEvalMetaFunc implements EvaluationFunction {
    /**
     * @see opt.EvaluationFunction#value(opt.OptimizationData)
     */

    public double value(Instance d)
    {
        Vector data = d.getData();
        int pop = d.getDiscrete(0);
        int keep = d.getDiscrete(1);
        int mut = d.getDiscrete(2);
        int iters = d.getDiscrete(3);
        int [] ranges = new int[4];
        ranges[0] = pop;
        ranges[1] = keep;
        ranges[2] = mut;
        ranges[3] = iters;
        CountOnesEvaluationFunction ef = new CountOnesEvaluationFunction();
        DiscreteUniformDistribution odd = new DiscreteUniformDistribution(ranges);
        DiscreteChangeOneMutation mf = new DiscreteChangeOneMutation(ranges);
        SingleCrossOver cf = new SingleCrossOver();
        GenericGeneticAlgorithmProblem gap = new GenericGeneticAlgorithmProblem(ef, odd, mf, cf);
        int k = (int) Math.ceil(pop* (double) keep /100.f);
        int m = Math.round(pop* mut/100.f);
        StandardGeneticAlgorithm ga = new StandardGeneticAlgorithm(pop, k,m,gap );
        FixedIterationTrainer fit = new FixedIterationTrainer(ga, iters);
        double val = fit.train();
        return 1.f/val;
    }

//    public double value(Instance d) {
//        Vector data = d.getData();
//        double val = 0;
//        for (int i = 0; i < data.size(); i++) {
//            if (data.get(i) == 1) {
//                val++;
//            }
//        }
//        return val;
//    }
}