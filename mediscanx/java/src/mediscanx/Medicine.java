package mediscanx;

public class Medicine {
    private final String barcode;
    private final String name;
    private final String manufacturer;
    private double mrp;
    private final String composition;

    public Medicine(String barcode, String name, String manufacturer, double mrp, String composition) {
        this.barcode = barcode;
        this.name = name;
        this.manufacturer = manufacturer;
        this.mrp = mrp;
        this.composition = composition;
    }

    public String getBarcode() { return barcode; }
    public String getName() { return name; }
    public String getManufacturer() { return manufacturer; }
    public double getMrp() { return mrp; }
    public String getComposition() { return composition; }

    public void setMrp(double mrp) { this.mrp = mrp; }
}
