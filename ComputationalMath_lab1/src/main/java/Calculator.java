
public class Calculator {
    private final int n;
    private final double[][] matrix;
    private double[][] oldMatrix;
    private double determinant = 1;
    private double[] unknowns;
    private double[] discrepancy;
    private int count_change = 0; //сколько раз меняли строки местами


    public Calculator(int n, double[][] matrix) {
        this.n = n;
        this.matrix = matrix;
    }

    static class NoSolution extends Exception {
    }

    public void culculate() throws NoSolution {
        triangleForm(); //сложность = n*(n-1)+ n* (n-1)* (n-1)
        findDeterminant();
        findUnknowns();
        findDiscrepancy();

    }

    //переставить строки местами так, чтобы на главной диагонали не было 0
    //если невозможно, бросает исключение
    //сложность = n*(n-1)
    public void replaceIfMainZero() throws NoSolution {
        for (int i = 0; i < n; i++) {
            if (matrix[i][i] == 0) {

                for (int j = 0; j < n - 1; j++) { //потому что n строк проверит
                    int index = i + 1 + j; //проверку начинаем со следующей строки
                    index = (index >= n) ? index - n : i + 1;
                    //если найдена строка, в которой текущий ведущий элемент != 0
                    // и если поменять эти две строки, в найденной ведущий не станет == 0, то меняем
                    if (matrix[index][i] != 0 && matrix[i][index] != 0) {
                        double[] tmp = matrix[i];
                        matrix[i] = matrix[index];
                        matrix[index] = tmp;
                        count_change++;
                        break;
                    }
                    //если не смогли ничего поменять, то решений нет
                    if (j == n - 2) {
                        throw new NoSolution();
                    }
                }
            }
        }
    }


    private void copyMatrix() {
        oldMatrix = new double[n][n + 1];
        for (int i = 0; i < n; i++) {
            System.arraycopy(matrix[i], 0, oldMatrix[i], 0, n + 1);
        }

    }

    //привести матрицу к треугольному виду (прямой ход)
    //сложность = n*(n-1) + n* (n-1)* (n-1)
    private void triangleForm() throws NoSolution {
        copyMatrix();
        replaceIfMainZero(); //сложность n*(n-1)
        for (int str = 0; str < n - 1; str++) {
            double mainElemant = matrix[str][str];
            if (mainElemant == 0)
                throw new NoSolution();

            for (int nextStr = str + 1; nextStr < n; nextStr++) {
                double firstNoZero = matrix[nextStr][str];
                matrix[nextStr][str] = 0;
                for (int nextStlb = str + 1; nextStlb < n + 1; nextStlb++) {
                    matrix[nextStr][nextStlb] -= matrix[str][nextStlb] * (firstNoZero / mainElemant);
                    if (matrix[nextStr][nextStlb] == 2.220446049250313E-15) {
                        matrix[nextStr][nextStlb] = Math.round(matrix[nextStr][nextStlb]);
                    }
                }
            }
        }
    }

    //тк матрица имеет треугольный вид, определитель = произведение элементов главной диагонали на (-1)^count_change
    //сложность = n
    private void findDeterminant() throws NoSolution {
        for (int i = 0; i < n; i++) {
            determinant *= matrix[i][i];
        }
        determinant *= (count_change % 2 == 0) ? 1 : -1;
        if (determinant == 0)
            throw new NoSolution();

    }

    //обратный ход
    //сложность = n*n
    private void findUnknowns() {
        unknowns = new double[n];
        for (int i = n - 1; i >= 0; i--) {
            double sum = 0;
            for (int j = n - 1; j > i; j--) {
                sum += matrix[i][j] * unknowns[j];
            }
            unknowns[i] = (matrix[i][n] - sum) / matrix[i][i];

        }
    }
//сложность = n*n
    private void findDiscrepancy() {
        discrepancy = new double[n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                discrepancy[i] += oldMatrix[i][j] * unknowns[j];
            }
            discrepancy[i] -= oldMatrix[i][n];
        }
    }

    public double[][] getMatrix() {
        return matrix;
    }

    public double getDeterminant() {
        return determinant;
    }

    public double[] getUnknowns() {
        return unknowns;
    }

    public double[] getDiscrepancy() {
        return discrepancy;
    }
}
