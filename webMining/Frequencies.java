package utils;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import utils.FileHelper;


public class Frequencies {
	static HashMap<String,Integer> hm = new HashMap<String, Integer>();
	static HashMap<Integer,Integer> wf = new HashMap<Integer, Integer>();
	static HashMap<Long,Integer> wfb = new HashMap<Long, Integer>();
	static ArrayList<String> rev = new ArrayList<String>();
	
	public static void load() throws FileNotFoundException, IOException{
		FileHelper fh = new FileHelper("/home/stp/OQ-Final/num2words",true );
		String line;
		while((line=fh.readline())!=null){
			String[] arr = line.split(" ");
			if(arr.length<2) continue;
			hm.put(arr[1], Integer.parseInt(arr[0]));
		}		
		fh.close();
		
		fh = new FileHelper("/home/stp/OQ-Final/wordsfreq",true );
		while((line=fh.readline())!=null){
			String[] arr = line.split(" ");
			if(arr.length<2) continue;
			wf.put(Integer.parseInt(arr[0]), Integer.parseInt(arr[1]));
		}	
		fh.close();
		
		fh = new FileHelper("/home/stp/OQ-Final/biwordsfreq",true );
		while((line=fh.readline())!=null){
			String[] arr = line.split(" ");
			if(arr.length<2) continue;
			wfb.put(Long.parseLong(arr[0]), Integer.parseInt(arr[1]));
		}	
		fh.close();
	}
	public static int getFreq(String s1,String s2){
		long i1 = hm.get(s1);
		long i2 = hm.get(s2);
		long id = i1*10000000L+i2;
		if(wfb.containsKey(id)) return wfb.get(id);
		return 0;
	}
	
	public static int getFreq(String s){
		Integer id = hm.get(s);
		if(wf.containsKey(id)) return wf.get(id);
		return 0;
	}
	public static void main(String[] arg) throws FileNotFoundException, IOException{
		load();
	}
}
