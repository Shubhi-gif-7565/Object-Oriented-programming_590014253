import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class useappend {
    public static void main(String[] args) {

        String filename = "sample.txt";

        try {
            // STEP 1: Create & write initial content
            FileWriter fw = new FileWriter(filename);
            fw.write("This is the original content.\n");
            fw.close();

            // STEP 2: Read BEFORE update
            System.out.println("Before Update:");
            FileReader fr1 = new FileReader(filename);
            int ch;
            while ((ch = fr1.read()) != -1) {
                System.out.print((char) ch);
            }
            fr1.close();

            // STEP 3: Append new content (instead of overwrite)
            FileWriter fw2 = new FileWriter(filename, true); // append mode
            fw2.write("This content is APPENDED.\nJava File Handling Demo.");
            fw2.close();

            // STEP 4: Read AFTER update
            System.out.println("\n\nAfter Update:");
            FileReader fr2 = new FileReader(filename);
            while ((ch = fr2.read()) != -1) {
                System.out.print((char) ch);
            }
            fr2.close();

        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
