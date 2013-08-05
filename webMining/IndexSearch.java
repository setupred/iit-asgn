package utils;

import java.io.File;
import java.io.IOException;

import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.BooleanClause;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.SimpleFSDirectory;
import org.apache.lucene.util.Version;

public class IndexSearch {
	private static StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
	static Query MakeQuery(String querystr) throws ParseException{
		BooleanQuery q ;//= new QueryParser(Version.LUCENE_40, "query", analyzer).parse(querystr);
		q = new BooleanQuery();
		String[] tmp = querystr.split(" ");
		for(String s:tmp){
			q.add(new TermQuery(new Term("query",s)),BooleanClause.Occur.SHOULD);
		}
		return q;
	}
	private static Directory dir;
	static ScoreDoc[] search(String qrStr,String IndexLoc,int hitsPerPage) throws IOException, ParseException{
		dir = new SimpleFSDirectory(new File(IndexLoc));
		IndexReader reader = IndexReader.open(dir);
		
		IndexSearcher searcher = new IndexSearcher(reader);
		TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, true);
		Query q = MakeQuery(qrStr);
		searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;
		System.out.println(hits.length+" "+qrStr);
		for(ScoreDoc hit:hits){
			System.out.println(searcher.doc(hit.doc).get("query")+":"+hit.score);
		}
		reader.close(); 
		dir.close();
		return hits;
	}
	public static void main(String[] Args) throws IOException, ParseException{
		IOHelper ioh = new IOHelper();
		String query = ioh.nline();
		search(query,"/home/stp/Downloads/Asgn/AOLlucene1",100);
	}
}
