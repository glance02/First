import java.io.*;

public class chapter8 {
    public static void main(String[] args) throws Exception {
        // BufferedReaderDemo();
        
        // InputStreamDemo();
        // FileReaderDemo();
    }
    
    //用buffered包装的字符流输入
    public static void BufferedReaderDemo() throws Exception{
        try(
            BufferedReader br=new BufferedReader(new FileReader("file.txt"));
        ){
            String line;
            while((line=br.readLine())!=null){
                System.out.println(line);
            }
        }
    }

    public static void FileWriterDemo() throws Exception{
        try(
            FileWriter fw=new FileWriter("file.txt",true);
        ){
            fw.write("I'll never forgive you. \n");
        }
    }

    public static void FileReaderDemo() throws Exception{
        try(
            FileReader fr=new FileReader("file.txt");
        ){
            char[] buffer = new char[1024];
            int c;
            while((c=fr.read(buffer))!=-1){
                System.out.print(new String(buffer,0,c));
            }
        }
    }

    //字节流输出（指输出到文件）
    public static void OutputStreamDemo() throws Exception{
        try(FileOutputStream fos=new FileOutputStream("file.txt",true)){
            byte[] bytes="love me more please. \n".getBytes();
            fos.write(bytes);
        }
    }

    //字节流输入（指输入给程序）    
    public static void InputStreamDemo() throws Exception{
        try(FileInputStream fis=new FileInputStream("file.txt")){
            byte[] buffer =new byte[1024];
            int len;
            while((len=fis.read(buffer))!=-1){
                System.out.println(new String(buffer,0,len));
            }
        }
    }
}
