import java.util.*;

public class Set {
    public static void main(String[] args) {
        java.util.Set<Integer> set = new java.util.TreeSet<>();

        set.add(30);
        set.add(10);
        set.add(20);

        set.remove(10);

        set.add(15);

        System.out.println("Contains 15? " + set.contains(15));

        for (int i : set) {
            System.out.println(i);
        }
    }
}