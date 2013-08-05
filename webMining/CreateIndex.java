package utils;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.SimpleFSDirectory;
import org.apache.lucene.util.Version;

import java.io.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class CreateIndex {
	public static List<String> getFiles(String sfile,String sw) {
		List<String> ret = new ArrayList<String>();
		File file = new File(sfile);
	    if (!file.exists()) {
	      System.out.println(file + " does not exist.");
	    }
	    else if (file.isDirectory()) {
	      for (File f : file.listFiles()) {
	        if(f.getName().startsWith(sw)) ret.add(f.getName());
	      }
	    } 
	    else {
	      String filename = file.getName().toLowerCase();
	      if (filename.startsWith(sw)) {
	        ret.add(filename);
	      } else {
	        System.out.println("Skipped " + filename);
	      }
	    }
		return ret;
	  }
	private static Directory dir;
	private static IndexWriter write;
	private static IndexWriterConfig config;
	private static StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
	
	public static void createIndex(String filesDir,String IndDir) throws IOException{
		List<String> filesLst =  getFiles(filesDir,"clean-user-ct-test");
		dir = new SimpleFSDirectory(new File(IndDir));
	    config = new IndexWriterConfig(Version.LUCENE_40, analyzer);
	    write = new IndexWriter(dir, config);
		for(String f:filesLst){
			index(filesDir+"/"+f);
		}
		write.close();
		config.clone();
		dir.close();
	}
	private static void index(String f) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader(f));
		System.out.println(f);
		String line;
		while((line=br.readLine())!=null){
			if(line.charAt(line.length()-1)=='\t')line+=" ";
			String[] sarr = line.split("\t");
			//System.out.println(line);
			if(sarr.length!=2) {
				continue;
			}
			Document doc = new Document();

	        //===================================================
	        // add contents of file
	        //===================================================
	        
	        doc.add(new TextField("query", sarr[0], Field.Store.YES));
	        doc.add(new TextField("resultWords", words(sarr[1]), Field.Store.YES));
	        doc.add(new StringField("resultURL", sarr[1], Field.Store.YES));
	        //doc.add(new StringField("filename", f.getName(), Field.Store.YES));
	        write.addDocument(doc);
		}
	}
	private static String words(String string) {
		int start  = string.lastIndexOf("/");
		if(start==-1 || start==string.length() || start==6 ) return "";
		string =  string.substring(start+1);
		String ret="";
		for(int i=start;i<string.length();i++){
			if((string.charAt(i)>='a' && string.charAt(i)<='z' ) || (string.charAt(i)>='A' && string.charAt(i)<='Z' )){
				ret+=string.charAt(i);
			}
			else ret+=" "; 
		}
		return ret;
	}
	public static void main(String[] Args) throws IOException{
		if(Args.length!=3){
			Args = new String[3];
			Args[1]="/home/stp/Downloads/AOL-user-ct-collection";
			Args[2]="/home/stp/Downloads/AOLlucene";
		}
		List<String> lst = getFiles(Args[1],"clean-user-ct-test");
		for (String s: lst){
			System.out.println(s);
		}
		System.out.println(Args[1]+Args[2]);
		Date td = new Date();
		System.out.println(td);
		createIndex(Args[1],Args[2]);		
		System.out.println(-td.getTime() + (new Date()).getTime());
	}
}
