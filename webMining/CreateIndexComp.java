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


public class CreateIndexComp {
	
	private static Directory dir;
	private static IndexWriter write;
	private static IndexWriterConfig config;
	private static StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
	private static boolean string_text = false;
	public static void createIndex(String filesDir,String IndDir) throws IOException{
		List<String> filesLst =  FileHelper.getFiles(filesDir,"");
		dir = new SimpleFSDirectory(new File(IndDir));
	    config = new IndexWriterConfig(Version.LUCENE_40, analyzer);
	    write = new IndexWriter(dir, config);
		for(String f:filesLst){
			indexq(filesDir+"/"+f);
		}
		write.close();
		config.clone();
		dir.close();
	}
	private static void indexq(String f) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader(f));
		System.out.println(f);
		String line;
		while((line=br.readLine())!=null){
			if(line.charAt(line.length()-1)=='\t')line+=" ";
			String[] sarr = line.split("\t",2);
			//System.out.println(line);
			if(sarr.length!=2) {
				System.out.println(sarr.length);
				continue;
			}
			Document doc = new Document();
	        if(!string_text)doc.add(new TextField("query", sarr[0], Field.Store.YES));
	        else doc.add(new StringField("query", sarr[0], Field.Store.YES));
	        doc.add(new StringField("resultURL", sarr[1], Field.Store.YES));
	        write.addDocument(doc);
		}
	}
	private static String words(String string) {
		string.replace("http://", "");
		string.replace("https://", "");
		int start  = string.indexOf("/");
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
		if(Args.length!=5){
			Args = new String[5];
			Args[1]="/home/stp/Downloads/ModAOLData-Final";
			Args[2]="/home/stp/Downloads/AOLlucene1";
			
			Args[3]="/home/stp/Downloads/ModAOLData-rFinal";
			Args[4]="/home/stp/Downloads/AOLlucene2";
		}
		List<String> lst = FileHelper.getFiles(Args[1],"");
		for (String s: lst){
			System.out.println(s);
		}
		
		System.out.println(Args[1]+Args[2]);
		System.out.println(Args[3]+Args[4]);
		
		Date td = new Date();
		System.out.println(td);
		createIndex(Args[1],Args[2]);
		System.out.println(-td.getTime() + (new Date()).getTime());
		System.out.println("Index1 Done");
		
		td = new Date();
		System.out.println(td);
		createIndex(Args[3],Args[4]);
		System.out.println(-td.getTime() + (new Date()).getTime());
		System.out.println("Index2 Done");
	}
}