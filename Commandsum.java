public class Commandsum {
    public static void main(String[] args) {

        int sum = 0;

        if (args.length == 0) {
            System.out.println("Please provide array elements as command-line arguments.");
            return;
        }

        for (int i = 0; i < args.length; i++) {
            sum += Integer.parseInt(args[i]);
        }

        System.out.println("Sum of array elements = " + sum);
    }
}