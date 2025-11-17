import java.util.*;
import java.io.*;

public class t2 {
    public static void main(String[] args) {
        // 随机生成字符串序列
        List<String> strings = generateRandomStrings(10, 5);

        System.out.println("原始字符串序列：");
        System.out.println(strings);

        // 使用Collections.sort()和Lambda表达式进行倒序字典排序
        Collections.sort(strings, (s1, s2) -> s2.compareTo(s1));

        System.out.println("倒序字典排序后的字符串序列：");
        System.out.println(strings);

        // 将排序后的数据写到文件中
        writeStringsToFile(strings, "a.data");

        // 从文件中读取数据并显示
        readStringsFromFile("a.data");
    }

    // 随机生成指定数量和长度的字符串序列
    public static List<String> generateRandomStrings(int count, int length) {
        List<String> strings = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < count; i++) {
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j < length; j++) {
                char c = (char) ('a' + random.nextInt(26)); // 生成随机小写字母
                sb.append(c);
            }
            strings.add(sb.toString());
        }
        return strings;
    }

    // 将字符串序列写到文件中，使用缓冲处理流提高效率
    public static void writeStringsToFile(List<String> strings, String filename) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (String str : strings) {
                writer.write(str);
                writer.newLine();
            }
            System.out.println("\n数据已成功写入文件 " + filename);
        } catch (IOException e) {
            System.out.println("写入文件时出错：" + e.getMessage());
            e.printStackTrace();
        }
    }

    // 从文件中读取字符串序列
    public static void readStringsFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            System.out.println("\n从文件 " + filename + " 读取的数据：");
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.out.println("读取文件时出错：" + e.getMessage());
            e.printStackTrace();
        }
    }
}