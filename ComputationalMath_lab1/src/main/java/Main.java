import java.io.PrintStream;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        PrintStream out = new PrintStream(System.out);
        Scanner scanner = new Scanner(System.in);
        Reader reader = new Reader(scanner, out);
        Writer writer = new Writer(scanner, out);

        reader.read();
        writer.printMatrix(reader.getMatrix());

        Calculator calculator = new Calculator(reader.getN(), reader.getMatrix());

        long after;
        long before;
        try {
            before = System.currentTimeMillis();
            calculator.culculate();
            after = System.currentTimeMillis();

        } catch (Calculator.NoSolution e) {
            out.println("\nNo solution");
            return;
        }

        writer.printMatrix(calculator.getMatrix());
        writer.printVector("Answer: ", "x", calculator.getUnknowns());
        writer.printVector("Discrepancy: ", "", calculator.getDiscrepancy());
        writer.printDet(calculator.getDeterminant());

//        out.printf("---TIME---   %15.40f\n", (double)after - before);

        out.println( after - before);
    }
}
