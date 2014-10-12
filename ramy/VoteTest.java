import shared.DataSet;
import shared.DataSetDescription;
import shared.filt.DiscreteToBinaryFilter;
import shared.filt.TestTrainSplitFilter;
import shared.reader.ArffDataSetReader;
import shared.filt.LabelSplitFilter;
import shared.reader.DataSetLabelBinarySeperator;

import func.nn.backprop.BackPropagationNetwork;
import func.nn.backprop.BackPropagationNetworkFactory;
import opt.OptimizationAlgorithm;
import opt.RandomizedHillClimbing;
import opt.SimulatedAnnealing;
import opt.example.NeuralNetworkOptimizationProblem;
import opt.ga.StandardGeneticAlgorithm;
import shared.ErrorMeasure;
import shared.Instance;
import shared.SumOfSquaresError;

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
    private static int inputLayer = 16, hiddenLayer = 7, outputLayer = 1, trainingIterations = 100; //for vote
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

    public static void doIt() {
        DataSet fullSet= loadData();
        int pct = 10;
        TestTrainSplitFilter splitter = new TestTrainSplitFilter(pct);
        splitter.filter(fullSet);
        DataSet trainingSet = splitter.getTrainingSet();
        DataSet testSet  = splitter.getTestingSet();

        trainingInstances = initializeInstances(trainingSet);
        testInstances = initializeInstances(testSet);
        //set = new DataSet(trainingInstances);

        for(int i = 0; i < oa.length; i++) {
            networks[i] = factory.createClassificationNetwork(
                new int[] {inputLayer, hiddenLayer, outputLayer});
            nnop[i] = new NeuralNetworkOptimizationProblem(trainingSet, networks[i], measure);
        }

        oa[0] = new RandomizedHillClimbing(nnop[0]);
        oa[1] = new SimulatedAnnealing(1E11, .95, nnop[1]);
        oa[2] = new StandardGeneticAlgorithm(200, 100, 10, nnop[2]);

        for(int i = 0; i < oa.length; i++) {
            double start = System.nanoTime(), end, trainingTime, testingTime, correct = 0, incorrect = 0;
            train(oa[i], networks[i], oaNames[i]); //trainer.train();
            end = System.nanoTime();
            trainingTime = end - start;
            trainingTime /= Math.pow(10,9);

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
            testingTime /= Math.pow(10,9);

            results +=  "\nResults for " + oaNames[i] + ": \nCorrectly classified " + correct + " instances." +
                        "\nIncorrectly classified " + incorrect + " instances.\nPercent correctly classified: "
                        + df.format(correct/(correct+incorrect)*100) + "%\nTraining time: " + df.format(trainingTime)
                        + " seconds\nTesting time: " + df.format(testingTime) + " seconds\n";
        }
        evalTestError();

        System.out.println(results);
    }

    private static void train(OptimizationAlgorithm oa, BackPropagationNetwork network, String oaName) {
        System.out.println("\nError results for " + oaName + "\n---------------------------");

        for(int i = 0; i < trainingIterations; i++) {
            oa.train();

            double error = 0;
            for(int j = 0; j < trainingInstances.length; j++) {
                network.setInputValues(trainingInstances[j].getData());
                network.run();

                Instance output = trainingInstances[j].getLabel(), example = new Instance(network.getOutputValues());
                example.setLabel(new Instance(Double.parseDouble(network.getOutputValues().toString())));
                error += measure.value(output, example);
            }

            System.out.println(df.format(error));
        }
    }
    private static Vector<ErrorCount> evalTestError()
    {
        int nn = 0;
        double correct =0, wrong = 0;
        Vector<ErrorCount> results = new Vector<ErrorCount>(oa.length);
        for (int i = 0; i < oa.length; i++)
        {
            for (int j = 0; j < testInstances.length;j++)
            {
                double truth  = Double.parseDouble( testInstances[j].getLabel().toString());
                networks[i].setInputValues(testInstances[j].getData());
                double predicted = Double.parseDouble(networks[i].getOutputValues().toString());
                double trash = Math.abs(predicted - truth) < 0.5 ? correct++ : wrong++;
            }
            results.add(i, new ErrorCount(correct,wrong));
            System.out.println("test Error is " + correct + "/" + wrong + " : " + df.format(correct / (correct + wrong) * 100) + " %correct");
        }
        return results;
    }
    private static DataSet loadData()
    {
        ArffDataSetReader dsr = new ArffDataSetReader(new File("").getAbsolutePath() +"/vote.arff");
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
            System.out.println(set);
            System.out.println(new DataSetDescription(set));
            int numInstances = set.size();
            int numAttributes = set.getLabelDataSet().getDescription().getAttributeCount();
            attributes = new double[numInstances][][];

            for(int i = 0; i < attributes.length; i++) {
              //  Scanner scan = new Scanner(br.readLine());
               // scan.useDelimiter(",");

                attributes[i] = new double[2][];
                attributes[i][0] = new double[numAttributes]; // 7 attributes
                attributes[i][1] = new double[1];

                for(int j = 0; j < numAttributes; j++)
                    attributes[i][0][j] =  set.get(i).getContinuous(j);//Double.parseDouble(scan.next());

                attributes[i][1][0] = set.get(i).getContinuous();// Double.parseDouble(scan.next());
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
        System.out.print("Hello World. Main called here. ");
        doIt();

    }

}
