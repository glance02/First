import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ImageCopyComparison {

    /**
     * 使用基本字节流复制文件
     * @param sourcePath 源文件路径
     * @param targetPath 目标文件路径
     * @return 复制耗时（毫秒）
     */
    public static long copyWithByteStream(String sourcePath, String targetPath) {
        long startTime = System.currentTimeMillis();
        
        try (FileInputStream fis = new FileInputStream(sourcePath);
             FileOutputStream fos = new FileOutputStream(targetPath)) {
            
            int byteData;
            while ((byteData = fis.read()) != -1) {
                fos.write(byteData);
            }
            
        } catch (IOException e) {
            System.err.println("字节流复制出错: " + e.getMessage());
            return -1;
        }
        
        long endTime = System.currentTimeMillis();
        return endTime - startTime;
    }

    /**
     * 使用字节缓冲流复制文件
     * @param sourcePath 源文件路径
     * @param targetPath 目标文件路径
     * @return 复制耗时（毫秒）
     */
    public static long copyWithBufferedStream(String sourcePath, String targetPath) {
        long startTime = System.currentTimeMillis();
        
        try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream(sourcePath));
             BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(targetPath))) {
            
            byte[] buffer = new byte[8192]; // 8KB缓冲区
            int bytesRead;
            
            while ((bytesRead = bis.read(buffer)) != -1) {
                bos.write(buffer, 0, bytesRead);
            }
            
        } catch (IOException e) {
            System.err.println("字节缓冲流复制出错: " + e.getMessage());
            return -1;
        }
        
        long endTime = System.currentTimeMillis();
        return endTime - startTime;
    }

    /**
     * 获取文件大小
     * @param filePath 文件路径
     * @return 文件大小（字节）
     */
    public static long getFileSize(String filePath) {
        try {
            Path path = Paths.get(filePath);
            return Files.size(path);
        } catch (IOException e) {
            System.err.println("获取文件大小出错: " + e.getMessage());
            return -1;
        }
    }

    /**
     * 验证文件是否相同
     * @param file1Path 第一个文件路径
     * @param file2Path 第二个文件路径
     * @return 如果文件相同返回true，否则返回false
     */
    public static boolean verifyFilesIdentical(String file1Path, String file2Path) {
        try (FileInputStream fis1 = new FileInputStream(file1Path);
             FileInputStream fis2 = new FileInputStream(file2Path)) {
            
            int byte1, byte2;
            while (true) {
                byte1 = fis1.read();
                byte2 = fis2.read();
                
                if (byte1 != byte2) {
                    return false;
                }
                
                if (byte1 == -1) { // 到达文件末尾
                    break;
                }
            }
            
            return true;
            
        } catch (IOException e) {
            System.err.println("验证文件相同性出错: " + e.getMessage());
            return false;
        }
    }

    public static void main(String[] args) {
        // 选择一个图片文件作为测试
        String sourceImage = "java备考.assets/image-20251107202901007.png";
        String targetImage1 = "image_copy_byte_stream.png";
        String targetImage2 = "image_copy_buffered_stream.png";
        
        // 检查源文件是否存在
        if (!new File(sourceImage).exists()) {
            System.err.println("源图片文件不存在: " + sourceImage);
            System.out.println("请将代码中的sourceImage变量修改为您系统上存在的图片文件路径");
            return;
        }
        
        // 获取源文件大小
        long fileSize = getFileSize(sourceImage);
        System.out.println("源文件: " + sourceImage);
        System.out.println("文件大小: " + fileSize + " 字节 (" + (fileSize / 1024.0) + " KB)");
        System.out.println();
        
        // 使用基本字节流复制
        System.out.println("=== 使用基本字节流复制 ===");
        long byteStreamTime = copyWithByteStream(sourceImage, targetImage1);
        if (byteStreamTime >= 0) {
            System.out.println("复制完成，耗时: " + byteStreamTime + " 毫秒");
            boolean identical1 = verifyFilesIdentical(sourceImage, targetImage1);
            System.out.println("文件验证: " + (identical1 ? "成功" : "失败"));
        }
        System.out.println();
        
        // 使用字节缓冲流复制
        System.out.println("=== 使用字节缓冲流复制 ===");
        long bufferedStreamTime = copyWithBufferedStream(sourceImage, targetImage2);
        if (bufferedStreamTime >= 0) {
            System.out.println("复制完成，耗时: " + bufferedStreamTime + " 毫秒");
            boolean identical2 = verifyFilesIdentical(sourceImage, targetImage2);
            System.out.println("文件验证: " + (identical2 ? "成功" : "失败"));
        }
        System.out.println();
        
        // 性能比较
        System.out.println("=== 性能比较 ===");
        if (byteStreamTime >= 0 && bufferedStreamTime >= 0) {
            double speedup = (double) byteStreamTime / bufferedStreamTime;
            System.out.println("基本字节流耗时: " + byteStreamTime + " 毫秒");
            System.out.println("字节缓冲流耗时: " + bufferedStreamTime + " 毫秒");
            System.out.println("字节缓冲流比基本字节流快 " + String.format("%.2f", speedup) + " 倍");
            
            if (bufferedStreamTime < byteStreamTime) {
                System.out.println("字节缓冲流性能更优");
            } else if (bufferedStreamTime > byteStreamTime) {
                System.out.println("基本字节流性能更优（可能是小文件或系统缓存影响）");
            } else {
                System.out.println("两种方式性能相同");
            }
        }
        
        System.out.println("\n提示：您可以使用系统自带的图片查看工具打开复制得到的文件验证复制是否成功");
    }
}
