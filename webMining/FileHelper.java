package utils;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class FileHelper {
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
	
	

    FileInputStream fstream;
    DataInputStream  in;
    BufferedReader br;
    PrintWriter outfile;
    boolean input;
    public FileHelper(String str, boolean inp) throws FileNotFoundException, IOException{
        input = inp; 
        
        if(inp){
            fstream = new FileInputStream(str);
            in = new DataInputStream(fstream);
            br = new BufferedReader(new InputStreamReader(in));
        }
        else{
            outfile = new PrintWriter(new FileWriter(str));
        }
    }
    public void write(String wrstr){
        if(input) {
            return;
        }
        outfile.write(wrstr);
    }
    public String readline() throws IOException{
        if(input){
            return br.readLine();
        }
        else{
            return null;
        }
    }
    public void close() throws IOException{
        if(input){
            br.close();
            in.close();
            fstream.close();
        }
        else{
            outfile.close();
        }
    }
}

