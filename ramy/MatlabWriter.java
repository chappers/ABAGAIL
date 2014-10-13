//import java.lang.Runnable;
import java.lang.Double;
import java.util.*;
import java.io.IOException;
import java.lang.String;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Vector;

import com.jmatio.types.MLDouble;

import com.jmatio.io.MatFileWriter;
import com.sun.xml.internal.xsom.impl.scd.Iterators;

import static java.lang.Math.ceil;
import static java.lang.Math.min;

public class MatlabWriter {
    private String outputFile =null;

    private Map<String, ArrayList<Vector<Double> >> map = new HashMap<String, ArrayList<Vector<Double> >>();
    private int rows, columns;
    private MatlabWriter() {};

    public MatlabWriter(String out, int R, int C)
	{
        this.outputFile = out;
        this.rows = R;
        this.columns = C;
    }


    public void addValue(double val, String name, int runNumber)
    {
        if(!map.containsKey(name))
        {
            map.put(name, new ArrayList<Vector<Double>>());
        }

        if (map.get(name).size() <= runNumber)
        {
            map.get(name).add(new Vector<Double>());
        }

        map.get(name).get(runNumber).add(val);

    }

    public List<MLDouble> makeList() {
        //for (HashMap.Entry<String, Classifier> cursor : classifiers.entrySet())
        List<MLDouble> list = new ArrayList<MLDouble>();
        for (HashMap.Entry<String, ArrayList<Vector<Double>>> cursor : map.entrySet()) {
            int r, c;

            r = cursor.getValue().size();
            c = cursor.getValue().get(0).size();
            List<Double> allValues = new ArrayList<>();

            for (Vector<Double> vec : cursor.getValue()) {

                allValues.addAll(vec);
            }
            Vector<Double> theValues = new Vector<Double>();
            theValues.addAll(allValues);
            Double[] foo;
            int numel = r * c;
            foo = allValues.toArray(new Double[r * c]);
            int man = allValues.size();
            MLDouble tmp = new MLDouble(cursor.getKey(), allValues.toArray( new Double[allValues.size()]), r);
            //MLDouble tmp = new MLDouble(cursor.getKey(), theValues.toArray( new Double[theValues.size()]), r);

           list.add(tmp);
        }

        return list;
    }
       /*
        MLDouble TestMLDouble = new MLDouble("testErrorRMS", TestErrorVec.toArray(new Double[TestErrorVec.size()]), 1);

        MLDouble TrainMLDouble = new MLDouble("trainErrorRMS", TrainingErrorVec.toArray(new Double[TrainingErrorVec.size()]), 1);
        MLDouble TestMLDoublePct = new MLDouble("testErrorPercent", TestErrorPctVec.toArray(new Double[TestErrorPctVec.size()]), 1);
        MLDouble TrainMLDoublePct = new MLDouble("trainErrorPercent", TrainingErrorPctVec.toArray(new Double[TrainingErrorPctVec.size()]), 1);
        //HashMap<Integer,Long> map =
        //MLDouble TrainMLDoublePct = new MLDouble("trainingTimes",TrainingErrorPctVec.toArray(new Double[TrainingErrorPctVec.size()]), 1);
        list.add(TestMLDouble);
        list.add(TrainMLDouble);
        list.add(TrainMLDoublePct);
        list.add(TestMLDoublePct);
        */


    public  List<MLDouble> test(int runNumber) throws Exception{

        /*
        Vector<Double>  TestErrorVec = new Vector<Double> (test.numInstances());
        Vector<Double>  TrainingErrorVec = new Vector<Double> (test.numInstances());
        Vector<Double>  TrainingErrorPctVec = new Vector<Double> (test.numInstances());
        Vector<Double>  TestErrorPctVec = new Vector<Double> (test.numInstances());
        //System.out.println(runNumber + " " + train.instance(0).toString());
        int maxtrainingSetSize = mySplitter.numInstances();


        int percentBegin = 5, percentIncrement = 5;

        for(int percent=percentBegin; percent <= 100 ; percent = min(percent + percentIncrement, 101))
        {
            int tmpSize = (int) ceil(train.numInstances() * percent / 100.0);
            //System.out.println(tmpSize);
            PercentTrainAndTest TrainAndTest;
            TrainAndTest = new PercentTrainAndTest(this.classifier, tmpSize, train, test);
            double TrainingError;
            TrainingError = TrainAndTest.getTrainRMSError();
            double TestError = TrainAndTest.getTestRMSError();
            TestErrorVec.add(TestError);
            TrainingErrorVec.add(TrainingError);
            TestErrorPctVec.add(TrainAndTest.getTestErrorPct());
            TrainingErrorPctVec.add(TrainAndTest.getTrainErrorPct());
            // TrainAndTest = null;
        }

        List<MLDouble> list = new ArrayList<MLDouble>();

        MLDouble TestMLDouble = new MLDouble("testErrorRMS", TestErrorVec.toArray(new Double[TestErrorVec.size()]), 1);
        MLDouble TrainMLDouble = new MLDouble("trainErrorRMS", TrainingErrorVec.toArray(new Double[TrainingErrorVec.size()]), 1);
        MLDouble TestMLDoublePct = new MLDouble("testErrorPercent", TestErrorPctVec.toArray(new Double[TestErrorPctVec.size()]), 1);
        MLDouble TrainMLDoublePct = new MLDouble("trainErrorPercent", TrainingErrorPctVec.toArray(new Double[TrainingErrorPctVec.size()]), 1);
        //HashMap<Integer,Long> map =
        //MLDouble TrainMLDoublePct = new MLDouble("trainingTimes",TrainingErrorPctVec.toArray(new Double[TrainingErrorPctVec.size()]), 1);
        list.add(TestMLDouble);
        list.add(TrainMLDouble);
        list.add(TrainMLDoublePct);
        list.add(TestMLDoublePct);

        return list;
*/
        return null;
    }

	public void writeMatFile(String OutputName, List<MLDouble> list)
			throws IOException {
		MatFileWriter writer = new MatFileWriter(OutputName, (Collection) list );
	}

    private static List<MLDouble> flattenList (List<MLDouble> L, int runs)
	{	
		HashMap<String, MLDouble> map = new HashMap<String, MLDouble>();
		HashMap<String, Integer> count = new HashMap<String, Integer>();
		int samples = L.get(0).getN();
		
		MLDouble TestMLDouble = new MLDouble("testErrorRMS",  new double[runs][samples]);
		MLDouble TrainMLDouble = new MLDouble("trainErrorRMS",new double[runs][samples]);
		MLDouble TestMLDoublePct = new MLDouble("testErrorPercent", new double[runs][samples]);
		MLDouble TrainMLDoublePct = new MLDouble("trainErrorPercent",new double[runs][samples]);
		
		map.put(TestMLDouble.name, TestMLDouble);
		map.put(TrainMLDouble.name, TrainMLDouble);

		map.put(TestMLDoublePct.name, TestMLDoublePct);
		map.put(TrainMLDoublePct.name, TrainMLDoublePct);

		count.put(TestMLDouble.name, 0);
		count.put(TrainMLDouble.name, 0);

		count.put(TestMLDoublePct.name, 0);
		count.put(TrainMLDoublePct.name, 0);

		
		
		for(int i = 0; i< L.size(); i++)
		{
			MLDouble tmp = L.get(i);
			MLDouble dest = map.get(tmp.name);
			if(dest == null)
			{
				System.err.println("ERROR! unknown map value "+tmp.name);
				continue;
			}
			
			int stored = count.get(tmp.name);
			int row = stored;
			count.put(tmp.name,  stored+1);
			for(int col = 0; col < samples; col++)
			{	double val = tmp.get(0, col);
				dest.set(val, row, col);	
			}
			
			map.put(tmp.name, dest);
		}
		
		List<MLDouble> result = new ArrayList<MLDouble>();
		Collection<MLDouble> collection = map.values();
		Set<String> s = map.keySet();
		result.addAll(map.values());
		return result;
	}

	public void runMany()
	{
		//MatlabWriter test = new MatlabWriter();
		//test.foo();
        List<MLDouble> list = new ArrayList<MLDouble>();

        int wtf =1; //(int) Math.ceil(mySplitter.numInstances() / 2.0);
        for(int i = 1; i <= wtf ; i++) {
            try {
                //mySplitter.randomizeAndSplit();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        int numRuns = 30;
        for(int i = 1; i <= numRuns ; i++)
        {

            try {
                //mySplitter.randomizeAndSplit();
            } catch (Exception e) {
                e.printStackTrace();
            }
            List<MLDouble> tmplist = null;
            try {
                tmplist = runOnce(i);
            } catch (Exception e) {
                e.printStackTrace();
            }
            list.addAll(tmplist);

        }

        List<MLDouble> finalList = flattenList(list, numRuns);
        //writeMatFile(outputFile, finalList);
        //return finalList;
        System.out.println(outputFile);

        try {
            writeMatFile(outputFile, finalList);
        } catch (IOException e) {
            e.printStackTrace();
        }
        {

        }
    }

	private List<MLDouble> runOnce(int runNumber)
			throws Exception {
		List<MLDouble> list = this.test(runNumber);
		return list;
	}

    public void write()
    {
        List<MLDouble> list  = this.makeList();
        try {
            this.writeMatFile(this.outputFile, list);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}