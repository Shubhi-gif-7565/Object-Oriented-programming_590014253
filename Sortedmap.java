//Insertion, Delection,Update,Travse,Searching 


import java.util.*;

public class Sortedmap {
    public static void main(String[] args) {
        java.util.SortedMap<Integer, String> sm = new java.util.TreeMap<>();

        // Insertion
        sm.put(5, "E");
        sm.put(1, "A");
        sm.put(3, "C");
        sm.put(2, "B");

        // Display sorted map
        System.out.println("SortedMap: " + sm);

        // Deletion
        sm.remove(3);

        // Updation
        sm.put(2, "Z");

        // Searching
        if (sm.containsKey(1)) {
            System.out.println("Key 1 found");
        } else {
            System.out.println("Key not found");
        }

        // Special SortedMap methods
        System.out.println("First Key: " + sm.firstKey());
        System.out.println("Last Key: " + sm.lastKey());

        // Traversal using values() (different way)
        System.out.println("Values in map:");
        for (String value : sm.values()) {
            System.out.println(value);
        }

        // Extra methods
        System.out.println("Map size: " + sm.size());
    }
}
