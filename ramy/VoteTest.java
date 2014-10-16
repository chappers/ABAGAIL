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
    private static Instance[] trainingInstances = null;
    private static Instance[] testInstances = null;
    //private static DataSet set = null;

    private static BackPropagationNetwork networks[] = new BackPropagationNetwork[3];
    private static NeuralNetworkOptimizationProblem[] nnop = new NeuralNetworkOptimizationProblem[3];

    private static OptimizationAlgorithm[] oa = new OptimizationAlgorithm[3];
    private static String[] oaNames = {"RHC", "SA", "GA"};
    private static String results = "";

    private static DecimalFormat df = new DecimalFormat("0.000");
    //TODO: do i need to pass in rows and columns?

    private static int runNumber=0;
    private static int totalRuns=0;
    private static int numPercentages=1;
    private static MatlabWriter matlabWriter = null;
    private static int trainingIterations;
    public static void doIt() {


        DataSet fullSet= loadData();
        RandomOrderFilter randomizer = new RandomOrderFilter();
        randomizer.filter(fullSet);
        TestTrainSplitFilter splitter = new TestTrainSplitFilter(33);
        splitter.filter(fullSet);

        DataSet trainingSet = fullSet;//splitter.getTrainingSet();
        DataSet testSet  = fullSet; //.getTestingSet();

        trainingInstances = initializeInstances(trainingSet);
        testInstances = trainingInstances; //  initializeInstances(testSet);

        int itersBegin = 10;
        int incr = (int) Math.ceil((totalTrainingIterations ) / Math.max(1, (numPercentages - 1)));



        for (int i = itersBegin; i <= totalTrainingIterations; i+=incr)
        {
            trainingIterations = i;
            DataSet set = new DataSet(trainingInstances);
            sampleTrainingPercentage(set, 100);
        }
        runNumber++;
    }

    private static void sampleTrainingPercentage(DataSet trainingSet, int pct) {

        //set = new DataSet(trainingInstances);

        for(int i = 0; i < oa.length; i++) {
            networks[i] = factory.createClassificationNetwork(
                new int[] {inputLayer, hiddenLayer, outputLayer});
            nnop[i] = new NeuralNetworkOptimizationProblem(trainingSet, networks[i], measure);
        }

        oa[0] = new RandomizedHillClimbing(nnop[0]);
        oa[1] = new SimulatedAnnealing(1E11, .9995, nnop[1]);
        oa[2] = new StandardGeneticAlgorithm(500, 300, 100, nnop[2]);
        double trainingError[] = new double [oa.length];


        for(int i = 0; i < oa.length; i++) {
            double start = System.nanoTime(), end, trainingTime, testingTime, correct = 0, incorrect = 0;
            trainingError[i] = train(oa[i], networks[i], oaNames[i]); //trainer.train();
            end = System.nanoTime();
            trainingTime = end - start;
            trainingTime /= Math.pow(10,9);

            evalTrainingError(i);
            evalTestError(i);
        }



    }

    private static void evalTrainingError(int i)
    {
        double correct=0;
        double incorrect=0;
        double start;
        double end;
        double testingTime;
        Instance optimalInstance = oa[i].getOptimal();
        networks[i].setWeights(optimalInstance.getData());

        double predicted, actual;
        start = System.nanoTime();

        for(int j = 0; j < trainingInstances.length; j++) {
            networks[i].setInputValues(trainingInstances[j].getData());
            networks[i].run();

            predicted = Double.parseDouble(trainingInstances[j].getLabel().toString());
            actual = Double.parseDouble(networks[i].getOutputValues().toString());

            double trash = Math.abs(predicted - actual) < 0.5 ? correct++ : incorrect++;

        }
        end = System.nanoTime();
        testingTime = end - start;
        double pctError = new PercentError(correct, incorrect).invoke() ;
        testingTime /= Math.pow(10,9);
        matlabWriter.addValue(pctError, oaNames[i]+"_trainingError", runNumber);
        System.out.println("\n---------------------------\nError results for " + oaNames[i] + " with " + trainingIterations +" iterations\n");
        results +=  "Correctly classified " + correct + " instances." +
                    "\nIncorrectly classified " + incorrect + " instances.\n" + oaNames[i]+ "Percent correctly classified: "
                    + df.format(100 *(1 - pctError));// + "%\nTraining time: " + df.format(trainingTime)
                    //+ " seconds\nTesting time: " + df.format(testingTime) + " seconds\n";
        System.out.println(results);
        results = "";
    }

    private static double train(OptimizationAlgorithm oa, BackPropagationNetwork network, String oaName) {
        double x = 0;
        double tr = 0;
        if (false) // oaName.equals("RHC"))
        {
            ConvergenceTrainer C = new ConvergenceTrainer(oa, 1E-10, 1000);
            C.train();
            x = C.getIterations();
            System.out.println("Convergence trainer says " + x);
        }
        else {
            FixedIterationTrainer F = new  FixedIterationTrainer(oa, trainingIterations);
            x = F.train();

            System.out.println("Fixed trainer says " + x);
            //for (int i = 0; i < trainingIterations; i++) {
            //x = oa.train();
            //}
        }
            double error = 0;
        Instance optimalInstance = oa.getOptimal();
        network.setWeights(optimalInstance.getData());

        for(int j = 0; j < trainingInstances.length; j++) {
            network.setInputValues(trainingInstances[j].getData());
            network.run();

            Instance output = trainingInstances[j].getLabel(), example = new Instance(network.getOutputValues());
            example.setLabel(new Instance(Double.parseDouble(network.getOutputValues().toString())));
            error += measure.value(output, example);
        }
        // System.out.println(df.format(error));
        return error;
    }

//    private static Vector<ErrorCount> evalTrainingError()
//    {
//
//    }


    private  static /* Vector<ErrorCount>*/ void evalTestError(int i)
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
