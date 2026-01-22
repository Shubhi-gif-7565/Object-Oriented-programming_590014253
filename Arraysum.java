import java.util.Scanner;

public class  Arraysum {
    int sum = 0;
    int arr [] = new int[6];
    public static void main(String[] args){
        Scanner s = new Scanner (System.in);
        Arraysum as = new Arraysum();

            for (int i = 0; i < 6; i++){
                as.arr[i] = s.nextInt();
                as.sum+= as.arr[i];
            }
        System.out.println(as.sum);
            
        }
    }

