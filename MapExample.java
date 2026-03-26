import java.util.*;

public class MapExample {
    public static void main(String[] args) {

        // Creating Map
        Map<Integer, String> m = new HashMap<>();

        // Insertion
        m.put(101, "Apple");
        m.put(102, "Banana");
        m.put(103, "Mango");

        // Display map
        System.out.println("Original Map: " + m);

        // Deletion
        m.remove(102);

        // Updation
        m.put(103, "Orange");

        // Searching
        if (m.containsKey(101)) {
            System.out.println("Key 101 exists");
        }

        if (m.containsValue("Orange")) {
            System.out.println("Value Orange exists");
        }

        // Traversal using keySet
        System.out.println("Traversing using keySet:");
        for (Integer key : m.keySet()) {
            System.out.println("Key: " + key + " Value: " + m.get(key));
        }

        // Traversal using entrySet (BEST METHOD)
        System.out.println("Traversing using entrySet:");
        for (Map.Entry<Integer, String> entry : m.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }

        // Extra methods
        System.out.println("Map size: " + m.size());
        System.out.println("Is map empty? " + m.isEmpty());
    }
}