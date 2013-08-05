

import java.io.File;

import org.apache.lucene.analysis.core.StopAnalyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.search.spell.PlainTextDictionary;
import org.apache.lucene.search.spell.SpellChecker;
import org.apache.lucene.search.spell.SuggestMode;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import utils.IOHelper;

public class SimpleSuggestionService {
    public static void main(String[] args) throws Exception {
    	StopAnalyzer analyzer = new StopAnalyzer(Version.LUCENE_42,new File("/home/stp/empty"));
    	File dir = new File("/home/stp/spellchecker/");
        Directory directory = FSDirectory.open(dir);
        SpellChecker spellChecker = new SpellChecker(directory);
        String path ="/home/stp/clean";
        spellChecker.indexDictionary(
        		new PlainTextDictionary(new File(path)),new IndexWriterConfig(Version.LUCENE_42, analyzer),false);
        IOHelper ioh = new IOHelper();
        int prev=1;
        System.out.println("Please Sir:");
        while(prev==1){
        String wordForSuggestions = ioh.nline();
        
        System.out.println((spellChecker.getAccuracy()));
        
         int suggestionsNumber = 1;
	     String[] split = wordForSuggestions.split(" ");
	     for(String s: split){
	        s= s.toLowerCase();
	        s = s.trim();
	        if(spellChecker.exist(s)){
	        	System.out.print(s+ " ");
	        	continue;
	        }
	        String[] suggestions = spellChecker.suggestSimilar(s, suggestionsNumber);
	        if (suggestions!=null && suggestions.length>0) {
	            for (String word : suggestions) {
	                System.out.print(word+ " ");
	            }
	        }
	        else{System.out.print(" ?? ");}
	     
	     }
	     /*
	     for (Object w: StandardAnalyzer.STOP_WORDS_SET){
	    	 System.out.println(w.toString());
	     }
	     */
	    System.out.println();
        }
        spellChecker.close();
        directory.close();
        analyzer.close();
            
    }

}
