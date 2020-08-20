import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.PriorityQueue;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class question_1 extends Configured implements Tool {
   public static void main(String[] args) throws Exception {
      System.out.println(Arrays.toString(args));
      int res = ToolRunner.run(new Configuration(), new question_1(), args);
      System.exit(res);
   }

   @Override
   public int run(String[] args) throws Exception {
      System.out.println(Arrays.toString(args));
      Job job = new Job(getConf(), "MutualFriendsRecommendation");
      job.setJarByClass(question_1.class);
      job.setMapOutputKeyClass(Text.class);
      job.setMapOutputValueClass(Pair.class);

      job.setMapperClass(Map.class);
      job.setReducerClass(Reduce.class);

      job.setInputFormatClass(KeyValueTextInputFormat.class);
      job.setOutputFormatClass(TextOutputFormat.class);

      FileInputFormat.addInputPath(job, new Path(args[0]));
      FileOutputFormat.setOutputPath(job, new Path(args[1]));

      job.waitForCompletion(true);

      return 0;
   }

   public static class Map extends Mapper<Text, Text, Text, Pair> {

      @Override
      public void map(Text key, Text value, Context context) throws IOException, InterruptedException {;
         if (value.getLength() != 0) {
           String[] list_friends = value.toString().split(",");
           for (int i = 0; i < list_friends.length; i ++) {
               //adding degree 1 friends 
               context.write(key, new Pair(new Text(list_friends[i]), new IntWritable(1)));
               for (int j = i + 1; j < list_friends.length; j++) {
                   //adding degree 2 friends
                   context.write(new Text(list_friends[i]), new Pair(new Text(list_friends[j]), new IntWritable(2)));
                   context.write(new Text(list_friends[j]), new Pair(new Text(list_friends[i]), new IntWritable(2)));
               }
           }
         } 
      }
   }

   public static class Reduce extends Reducer<Text, Pair, Text, Text> {
      @Override
      public void reduce(Text key, Iterable<Pair> values, Context context) throws IOException, InterruptedException {
        Iterator<Pair> itr = values.iterator();
        
        HashMap<String, Integer> hashmap = new HashMap<String, Integer>();
          while (itr.hasNext()) {
            Pair current = itr.next();
            String friend = current.getFriend();
            
            if (current.getDegree() == 1) hashmap.put(friend, -1);
            else {
            	// if friend is in hashmap, increment the count 
                if (hashmap.containsKey(friend)) {
                    // if friend is degree 1 than exclude from count. 
                    if (hashmap.get(friend) != -1) {
                        hashmap.put(friend, hashmap.get(friend) + 1);
                    }
                }
                // if friend not in hashmap, make a new entry with count 1
                else hashmap.put(friend, 1);
            }
          }

          // remove all degree 1 friend, sort top 10 with a top 10 heap (implemented by PriorityQueue) 
          PriorityQueue<Entry<String, Integer>> pq = new PriorityQueue<Entry<String, Integer>>(10, new Comparator<Entry<String, Integer>>() {

          @Override
          public int compare(Entry<String, Integer> o1,
                  Entry<String, Integer> o2) {
        	  if(o2.getValue() == o1.getValue()) {
        		  return Integer.parseInt(o1.getKey()) - Integer.parseInt(o2.getKey());
        	  }
              return o2.getValue() - o1.getValue();
          }
          });

          for (Entry<String, Integer> pairs: hashmap.entrySet()) {
            if (!pairs.getValue().equals(-1)) pq.add(pairs);
          }
          StringBuffer output = new StringBuffer();
          int count = 0;
          int size = pq.size();
          while (!pq.isEmpty()) {
            output.append(pq.poll().getKey());
            if (count >= 9 || count >= size-1) break;
            count ++;
            output.append(",");
          }
          context.write(key, new Text(output.toString()));
      }
   }


   
   public static class Pair implements Writable {
     private Text friend;
     private IntWritable degree;
  
     public Pair() {
         this.friend = new Text();
         this.degree = new IntWritable();
     }
  
     public Pair(Text friend1, IntWritable degree) {
         this.friend = friend1;
         this.degree = degree;
     }

     @Override
     public void readFields(DataInput in) throws IOException {
         this.friend.readFields(in);
         this.degree.readFields(in);
     }

     @Override
     public void write(DataOutput out) throws IOException {
         friend.write(out);
         degree.write(out);
     }
  
     public int getDegree() {
         return degree.get();
     }
  
     public String getFriend() {
         return friend.toString();
     }
   }

}