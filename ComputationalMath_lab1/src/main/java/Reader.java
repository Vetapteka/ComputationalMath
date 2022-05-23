import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.Scanner;
import java.util.function.Function;
import java.util.function.Supplier;

public class Reader {
    Scanner scanner;
    PrintStream out;
    int n;
    double[][] matrix;

    public Reader(Scanner scanner, PrintStream out) {
        this.scanner = scanner;
        this.out = out;
    }

    public void read() {

        out.println("Select data entry method:\n" + "console:   " +
                "           0\n" + "file:                 1\n" + "automatic generation: 2");
        out.print("> ");

        int answer = (int) readNumber(Integer::parseInt, 0, 2);

        switch (answer) {
            case (0) -> {
                readN();
                out.println("Enter the matrix: ");
                readMatrix(() -> (double) readNumber(Double::parseDouble, Double.MIN_VALUE, Double.MAX_VALUE));
            }
            case (2) -> {
                readN();
                readMatrix(() -> Math.random() * 200 - 100);
            }
            case (1) -> {
                out.println("Enter file name:");
                Scanner file;
                while (true) {
                    out.print("> ");
                    try {
                        file = new Scanner(new File(scanner.next()));
                    } catch (FileNotFoundException | NullPointerException e) {
                        out.println("can't access file");
                        continue;
                    }
                    break;
                }
                try {
                    n = (int) readParsableNumber(Integer::parseInt, file.next());
                    Scanner finalFile = file;
                    readMatrix(() -> (double) readParsableNumber(Double::parseDouble, finalFile.next()));
                } catch (IllegalArgumentException e) {
                    out.println("invalid argument in the file");
                }
            }
        }

    }


    private void readN() {
        out.println("Enter the dimension of the matrix: ");
        out.print("> ");

        n = (int) readNumber(Integer::parseInt, 2, 20);
    }

    private void readMatrix(Supplier<Double> supplier) {
        matrix = new double[n][n + 1];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n + 1; j++) {
                matrix[i][j] = supplier.get();
            }
        }
    }

    private Number readNumber(Function<String, Number> parser, Number min, Number max) {
        Number res;
        while (true) {
            try {
                res = readParsableNumber(parser, scanner.next());
                if (res.floatValue() < min.floatValue() || res.floatValue() > max.floatValue())
                    throw new IllegalArgumentException();
            } catch (IllegalArgumentException e) {
                out.println("enter the number in the range " + min + ".." + max);
                out.print("> ");
                continue;
            }
            return res;
        }
    }

    private Number readParsableNumber(Function<String, Number> parser, String str) throws
            IllegalArgumentException {
        Number res;
        try {
            res = parser.apply(str);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException();
        }
        return res;
    }

    public int getN() {
        return n;
    }

    public double[][] getMatrix() {
        return matrix;
    }
}
