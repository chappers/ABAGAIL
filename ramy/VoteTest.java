import com.sun.xml.internal.bind.v2.TODO;
import func.nn.backprop.BackPropagationNetwork;
import func.nn.backprop.BackPropagationNetworkFactory;
import opt.OptimizationAlgorithm;
import opt.RandomizedHillClimbing;
import opt.SimulatedAnnealing;
import opt.example.NeuralNetworkOptimizationProblem;
import opt.ga.StandardGeneticAlgorithm;
import shared.*;
import shared.filt.DiscreteToBinaryFilter;
import shared.filt.LabelSplitFilter;
import shared.filt.RandomOrderFilter;
import shared.filt.TestTrainSplitFilter;
import shared.reader.ArffDataSetReader;
import shared.reader.DataSetLabelBinarySeperator;

import javax.xml.crypto.Data;
import java.io.File;
import java.text.DecimalFormat;
import java.util.Vector;


class ErrorCount
{
    private double correct = 0;
    private double wrong = 0;

    ErrorCount(double right, double notRight)
    {
        setCorrect(right);
        setWrong(notRight);
    }

    public double getCorrect() {
        return correct;
    }

    public void setCorrect(double correct) {
        this.correct = correct;
    }

    public double getWrong() {
        return wrong;
    }

    public void setWrong(double wrong) {
        this.wrong = wrong;
    }
}

/**
 * Implementation of randomized hill climbing, simulated annealing, and genetic algorithm to
 * find optimal weights to a neural network that is classifying abalone as having either fewer 
 * or more than 15 rings. 
 *
 * @author Hannah Lau
 * @version 1.0
 */

public class VoteTest {
  //  private static Instance[] allInstances = initializeInstances();
//Ramy's NN parameters from previous assignment. iterations 40000 learning rate .01 momentum .05 -H a,o meaning one hidden layer for a' = (attribs + classes) / 2,
//'o' = classes. TODO: I need to either extract these from the data, or make the arguments. From data is better.
     //private static int inputLayer = 7, hiddenLayer = 5, outputLayer = 1, trainingIterations = 1000;
  //TODO: the old one had TWO output nodes.
    private static int inputLayer = 16, hiddenLayer = 7, outputLayer = 1, totalTrainingIterations = 1000; //for vote
    private static BackPropagationNetworkFactory factory = new BackPropagationNetworkFactory();
    
    private static ErrorMeasure measure = new SumOfSquaresError();
    private static Instance[] theInstances = null;
    private static Instance[] testInstances = null;
    //private static DataSet set = null;

    private static BackPropagationNetwork networks[] = new BackPropagationNetwork[3];
    private static NeuralNetworkOptimizationProblem[] nnop = new NeuralNetworkOptimizationProblem[3];

    private static OptimizationAlgorithm[] oa = new OptimizationAlgorithm[3];
    private static String[] oaNames = {"RHC", "SA", "GA"};
    private static String results = "";

    private static DecimalFormat df = new DecimalFormat("0.000");
    //TODO: do i need to pass in rows and columns?
    private static double cooling;
    private static int runNumber=0;
    private static int totalRuns=0;
    private static int numPercentages=1;
    private static MatlabWriter matlabWriter = null;
    private static int trainingIterations;
    private static int GA_max = 10000;
    private static int RHC_max = 10000;
    public static void doIt() {


        DataSet fullSet= loadData();
        RandomOrderFilter randomizer = new RandomOrderFilter();
        randomizer.filter(fullSet);
        TestTrainSplitFilter splitter = new TestTrainSplitFilter(33);
        splitter.filter(fullSet);

        DataSet trainingSet = splitter.getTrainingSet();
        DataSet testSet  = splitter.getTestingSet();

        theInstances = initializeInstances(trainingSet);
        testInstances =   initializeInstances(testSet);


        sampleTrainingPercentage(trainingSet);

        runNumber++;
    }

    private static int computeIncr(int total) {
        return (int) Math.ceil((total) / Math.max(1, (numPercentages - 1)));
    }

    private static void sampleTrainingPercentage(DataSet trainingSet) {

        //set = new DataSet(trainingInstances);

        for(int i = 0; i < oa.length; i++) {
            networks[i] = factory.createClassificationNetwork(
                new int[] {inputLayer, hiddenLayer, outputLayer});
            nnop[i] = new NeuralNetworkOptimizationProblem(trainingSet, networks[i], measure);
        }
        oa[0] = new RandomizedHillClimbing(nnop[0]);
        cooling = .9995;
        oa[1] = new SimulatedAnnealing(1E11, cooling, nnop[1]);
        oa[2] = new StandardGeneticAlgorithm(500, 300, 100, nnop[2]);
        double trainingError[] = new double [oa.length];

        for(int i = 0; i < oa.length; i++)
        {
            int itersBegin = 1;

            Boolean doingSA = "SA".equals(oaNames[i]);
            int howMany = GA_max;

            if(doingSA ) {
                howMany = totalTrainingIterations;
            }
            int incr = 100; //computeIncr(howMany);

           // for (int j = itersBegin; j <= howMany+incr; j+=incr)
            double err = 1;
            double THRESHOLD = 0;
            double start = System.nanoTime(), end, trainingTime, testingTime, correct = 0, incorrect = 0;
            int iterCount =0;
            double pctError = 100;
            int perfectCount = 0;
            while ( pctError >0 && (perfectCount) < 100)
            {
                if(pctError == 0)
                    perfectCount++;

                err = train(oa[i], incr);
                iterCount += incr;
                pctError= evalPercentError(oaNames[i]+"_trainingError", oa[i], networks[i], theInstances, iterCount);

                double testError= evalPercentError(oaNames[i]+"_testError", oa[i], networks[i], testInstances, iterCount);
            }
            printResults(i, iterCount, correct, incorrect, pctError, err);
            end = System.nanoTime();
            trainingTime = end - start;
            trainingTime /= Math.pow(10, 9);
            matlabWriter.addValue(trainingTime, oaNames[i] + "_Time", runNumber);

            //evalTestError(i);
        }
    }

    private static void printResults(int i, int howMany, double correct, double incorrect, double pctError, double err) {
        System.out.println("\nRun " + runNumber + "/" + totalRuns + " : " + howMany + " iterations" +
                "\n---------------------------\nError results for " + oaNames[i] + " " + err);
        results +=  "Correctly classified " + correct + " instances." +
                "\nIncorrectly classified " + incorrect + " instances.\n" + oaNames[i]+ "Percent correctly classified: "
                + df.format(100 *(1 - pctError));// + "%\nTraining time: " + df.format(trainingTime)
        //+ " seconds\nTesting time: " + df.format(testingTime) + " seconds\n";
        System.out.println(results);
        results = "";
    }

    private static double evalPercentError(String name, OptimizationAlgorithm oa, BackPropagationNetwork network, Instance[] theInstances, int iters)
    {
        double correct=0;
        double incorrect=0;
        double start;
        double end;
        double testingTime;

        Instance optimalInstance = oa.getOptimal();
        network.setWeights(optimalInstance.getData());

        double predicted, actual;

        for(int j = 0; j < theInstances.length; j++) {
            network.setInputValues(theInstances[j].getData());
            network.run();

            predicted = Double.parseDouble(theInstances[j].getLabel().toString());
            actual = Double.parseDouble(network.getOutputValues().toString());

            double trash = Math.abs(predicted - actual) < 0.5 ? correct++ : incorrect++;

        }

        double pctError = new PercentError(correct, incorrect).invoke() ;

        matlabWriter.addValue(pctError, name, runNumber);
        matlabWriter.addValue(iters, name+"Iterations", runNumber);
        return pctError;
    }

    private static double train(OptimizationAlgorithm oa, int howMany)
    {
        double x = 0;
        double tr = 0;
 //      double yo = Math.log(1E-11 / 1E11) / Math.log(cooling);

        FixedIterationTrainer F = new FixedIterationTrainer(oa, howMany);
        x = F.train();

        return x;
    }
/*
    private  static Vector<ErrorCount> void evalTestError(int i)
    {
        double correct =0, wrong = 0;
        Vector<ErrorCount> results = new Vector<ErrorCount>(oa.length);
        //for (int i = 0; i < oa.length; i++)
        //{
            Instance optimalInstance = oa[i].getOptimal();
            networks[i].setWeights(optimalInstance.getData());

            for (int j = 0; j < testInstances.length;j++)
            {
                double truth  = Double.parseDouble( testInstances[j].getLabel().toString());
                networks[i].setInputValues(testInstances[j].getData());
                networks[i].run();

                double predicted = Double.parseDouble(networks[i].getOutputValues().toString());
                double trash = Math.abs(predicted - truth) < 0.5 ? correct++ : wrong++;
            }
            //results.add(i, new ErrorCount(correct,wrong));
            double pctError = new PercentError(correct,wrong).invoke();
            matlabWriter.addValue(pctError, oaNames[i] + "_testError",runNumber);
            System.out.println("\n---------------------------\nTest results for " + oaNames[i] + " with " + trainingIterations +" iterations\n");
            System.out.println("test Error is " + correct + "vs" + wrong + " : " + 100*(1-pctError)+ " %correct");
//        }

  //      return results;
    }
    */
    private static DataSet loadData()
    {
       // ArffDataSetReader dsr = new ArffDataSetReader(new File("").getAbsolutePath() +"/vote.arff");
        String file = new String("vote.arff");
        ArffDataSetReader dsr = new ArffDataSetReader(new File("") + file);
        // read in the raw data
        DataSet fullDataSet = null;
        try {
            fullDataSet = dsr.read();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return  fullDataSet;
    }
    private static Instance[] initializeInstances(DataSet set) {
        double[][][] attributes = null;

        try {

            // split out the label
            LabelSplitFilter lsf = new LabelSplitFilter();
            lsf.filter(set);
            DiscreteToBinaryFilter ctdf = new DiscreteToBinaryFilter();
            ctdf.filter(set);
            DataSetLabelBinarySeperator.seperateLabels(set);
            //System.out.println(set);
            //System.out.println(new DataSetDescription(set));
            int numInstances = set.size();
            int numAttributes = set.getDescription().getAttributeCount(); //set.getLabelDataSet().getDescription().getAttributeCount();
            attributes = new double[numInstances][][];

            for(int i = 0; i < attributes.length; i++) {
              //  Scanner scan = new Scanner(br.readLine());
               // scan.useDelimiter(",");

                attributes[i] = new double[2][];
                attributes[i][0] = new double[numAttributes]; // 7 attributes
                attributes[i][1] = new double[1];

                for(int j = 0; j < numAttributes; j++)
                    attributes[i][0][j] =  set.get(i).getContinuous(j);//Double.parseDouble(scan.next());

                Instance p = set.get(i).getLabel();
                attributes[i][1][0] = p.getContinuous();

            }

        }
        catch(Exception e) {
            e.printStackTrace();
        }

        Instance[] instances = new Instance[attributes.length];

        for(int i = 0; i < instances.length; i++) {
            instances[i] = new Instance(attributes[i][0]);
            // classifications range from 0 to 30; split into 0 - 14 and 15 - 30
            //TODO: what  is this? Needs a fix.
            int label =attributes[i][1][0] < .5 ? 0 : 1 ;
            instances[i].setLabel( new Instance(label));
        }

        return instances;
    }

    public static void main(String[] args)
    {
        if(args.length < 4)
        {
            System.err.println("Error! Usage is #runs #samples #iters outfile.mat");
            System.exit(1);
        }
        //int junkArg = Integer.parseInt(args[0]);
        int numRuns = Integer.parseInt(args[0]);
        int numSamples = Integer.parseInt(args[1]);
        int numIters = Integer.parseInt(args[2]);
        String outfile = new String(args[3]);

        System.out.print("Hello World. Main called here. ");
        totalTrainingIterations = numIters;
        totalRuns =numRuns; numPercentages= numSamples;
        matlabWriter = new MatlabWriter(outfile, numPercentages, totalRuns);
        for (int i = 0; i < totalRuns; i++) {
            doIt();
        }

        matlabWriter.write();
    }

    private static class PercentError {
        private double correct;
        private double incorrect;

        public PercentError(double correct, double incorrect) {
            this.correct = correct;
            this.incorrect = incorrect;
        }

        public double invoke() {
            return (1- correct/(correct+incorrect));
        }
    }
}
