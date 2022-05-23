import java.io.PrintStream;
import java.util.Scanner;

public class Writer {
    Scanner scanner;
    PrintStream out;

    public Writer(Scanner scanner, PrintStream out) {
        this.scanner = scanner;
        this.out = out;
    }

    public void printMatrix(double[][] matrix) {
        printDelim();
        out.println("matrix: ");
        int n = matrix[1].length - 1;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n + 1; j++) {
                String delim = (j == n - 1) ? " | " : "  ";
                out.print(matrix[i][j] + delim);
            }
            out.println();
        }
    }

    public void printVector(String massage, String str, double[] vector) {
        printDelim();
        out.println(massage);
        for (int i = 0; i < vector.length; i++) {
            out.print(str + i + "=");
//            out.printf("%15.3f\n", vector[i]);
            out.println(vector[i]);
        }

    }

    public void printDet(double det) {
        printDelim();
        out.printf("Determinant: %21.3f\n", det);
    }
    private void printDelim(){
        out.println("-------------------------------------------------");

    }
}
