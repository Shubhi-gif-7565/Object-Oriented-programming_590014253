import java.util.Scanner;
import java.util.HashSet;

public class duplicate {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of elements: ");
        int n = sc.nextInt();

        int[] arr = new int[n];
        HashSet<Integer> set = new HashSet<>();

        System.out.println("Enter elements:");
        boolean hasDuplicate = false;

        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();

            if (!set.add(arr[i])) {
                hasDuplicate = true;
            }
        }

        if (hasDuplicate) {
            System.out.println("Array contains duplicates");
        } else {
            System.out.println("Array does not contain duplicates");
        }

        sc.close();
    }
}