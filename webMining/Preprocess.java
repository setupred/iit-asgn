
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;



import utils.CleanAndStem;
import utils.FileHelper;


public class Preprocess {
	static HashMap<String,Integer> hm = new HashMap<String, Integer>();
	static HashMap<Integer,Integer> wf = new HashMap<Integer, Integer>();
	static HashMap<Long,Integer> wfb = new HashMap<Long, Integer>();
	static ArrayList<String> rev = new ArrayList<String>();

	static void makeWordIds(String fn,boolean write) throws FileNotFoundException, IOException{
		FileHelper fh = new FileHelper(fn, true);
		String line = "";
		while((line=fh.readline())!=null){
			String[] arr = line.split("\t");
			assert arr.length==2;
			int freq = Integer.parseInt(arr[1]);
			arr[0] = CleanAndStem.RSS(arr[0]);
			String[] words = arr[0].split(" ");
			//monograms
			for(String word:words){
				if(hm.containsKey(word)){
					int id = hm.get(word);
					wf.put(id,wf.get(id)+freq);
				}
				else {
					wf.put(rev.size(),freq);
					hm.put(word, rev.size());
					rev.add(word);
				}
			}
			//bigrams
			if(words.length==0) continue;
			
			long prev= hm.get(words[0]),pres;
			for(int i=1;i<words.length;i++){
				pres = hm.get(words[0]);
				long id = prev*10000000L+pres;
				int Cnt = 0;
				if(wfb.containsKey(id)){
					Cnt = wfb.get(id); 
				}
				Cnt +=  freq;
				wfb.put(id, Cnt);
				prev = pres;
			}
		}
		fh.close();
		System.out.println(rev.size()+" "+wfb.size());
		if(write){
			fh = new FileHelper("/home/stp/OQ-Final/num2words",false );
			for(int i=0;i<rev.size();i++){
				fh.write(i+" "+rev.get(i)+"\n");
			}
			fh.close();
			
			fh = new FileHelper("/home/stp/OQ-Final/wordsfreq",false );
			for(Integer word:wf.keySet()){
				fh.write(word+" "+wf.get(word)+"\n");
			}
			fh.close();
			
			fh = new FileHelper("/home/stp/OQ-Final/biwordsfreq",false );
			for(Long word:wfb.keySet()){
				fh.write(word+" "+wfb.get(word)+"\n");
			}
			fh.close();
		}
	}
	Long Limit = 1000000000L;
	
	public static void main(String args[]) throws FileNotFoundException, IOException{
		makeWordIds("/home/stp/OQ-Final/all",true);
		//System.out.println(CleanAndStem.RSS("This is a randomon shits"));
	}
}
