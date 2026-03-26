
import java.util.TreeMap;
import java.util.Map;
public class Sorted {
    public static void main(String[] args) {

        TreeMap<Integer, String> map = new TreeMap<>();

        // INSERTION
        map.put(3, "C");
        map.put(1, "A");
        map.put(2, "B");

        // TRAVERSING
        System.out.println("Traversing:");
        for (Map.Entry<Integer, String> entry : map.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }

        // SEARCHING
        System.out.println("Search key 2: " + map.get(2));

        // UPDATING
        map.put(2, "Z");

        // DELETION
        map.remove(1);

        System.out.println("Final Map: " + map);
    }
}