/**
Template taken from team Proof (ICPC World Finalists 2011,2012)
Used by Team Cubes
**/
package utils;

import java.io.*;
import java.util.*;
import java.math.*;
public class IOHelper
{
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer tokenizer = null;
    int ni() throws IOException{
        return Integer.parseInt(ns());
    }
    long nl() throws IOException{
        return Long.parseLong(ns());
    }
    double nd() throws IOException{
        return Double.parseDouble(ns());
    }
    String ns() throws IOException{
        while (tokenizer == null || !tokenizer.hasMoreTokens())
            tokenizer = new StringTokenizer(br.readLine());
        return tokenizer.nextToken();
    }
    public String nline() throws IOException{
        tokenizer = null;
        return br.readLine();
    }
    
}