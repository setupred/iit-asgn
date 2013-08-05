package utils;
import java.util.HashSet;


public class CleanAndStem {
	static HashSet<String> stop = new HashSet<String>();
	private static Stemmer  stem = new Stemmer();
	public static void init(){
		
		if(stop.size()!=0) return;
		String[] ENGLISH_STOP_WORDS = {
				"a", "an", "and", "are", "as", "at", "be", "but", "by",
				"for", "if", "in", "into", "is", "it",
				"no", "not", "of", "on", "or", "such",
				"that", "the", "their", "then", "there", "these",
				"they", "this", "to", "was", "will", "with"
				};
		for(String s:ENGLISH_STOP_WORDS){
			stop.add(s);
		}
	}
	static String processSentence(String query){
		String ret="";
		query =  query.toLowerCase();
		for(int i=0;i<query.length();i++){
			char c = query.charAt(i);
			if('a'<=c && c<='z'){}
			else c = ' ';
			ret+=c;
		}
		while(true){
			String news = ret.replace("  ", " ");
			if(news==ret) {
				ret = news;
				break;
			}
			ret= news;
		}
		return ret;
	}
	public static String RSS(String sentence){
	    init();
		sentence  = processSentence(sentence);
	    String[] arr = sentence.split(" ");
	    String ret="";
	    for(String s: arr){
	    	if(stop.contains(s)) continue;
	    	stem.add((s).toCharArray(), s.length());
	    	stem.stem();
	    	ret+= (stem.toString()+ " ");
	    }
	    return ret;
	}
}
