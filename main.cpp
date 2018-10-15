#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <iostream>
#include <filesystem>
#include <limits.h>
using namespace std;
namespace fs = std::filesystem;
int parse_Input_File(char *filename, int *address_of_n, double **plb, double **pub,
                     double **pmu, double **pcovariance, double *address_of_lambda, double **px, double **pgrad, double **py);
int feasible(int n, double *x, double *lb, double *ub);
double computeObjFunc(int n, double lambda, double *x, double *covariance, double *mu);
double gradient(int n, double lambda, double *grad, double *x, double *mu, double *covariance);
double direction(int n, double lambda, double *grad, double *ub, double *lb, double *mu, double *covariance, double *x, double *y);
double computeY(int n, double lambda, double *x, double *y, double *mu, double *covariance);


int main(int argc, char **argv) {
    int retcode = 0, k = 0;
    int n;
    double oldF, newF, s;
    double *lb, *ub, *covariance, *mu, lambda, *x, *grad, *y, *newx;



    //char* my_path = std::filesystem::current_path();
/*    fs::path path = fs::current_path();
    std::string path_string = path.u8string();

    const char *cstr2 = path_string.c_str();
    printf("CSTR2: \n");
    printf(cstr2);
    printf("\n");

    std::string str = "string";
    char *cstr = new char[path_string.length() + 1];
    strcpy(cstr, path_string.c_str());
    printf("CSTR1: \n");
    printf(cstr);
    printf("\n");
    delete [] cstr;
    */

    /*
    *
    *  ========= CHANGE THIS DIRECTORY BEFORE RUNNING ================
    *
    */

    char *my_file = "E:/IEOR_4500/HW2/CLION_PROJ_17/example.txt";
    retcode = parse_Input_File(my_file, &n, &lb, &ub, &mu, &covariance, &lambda, &x, &grad, &y);

    feasible(n, x, lb, ub);
    printf("\nSuccesfully read data. Now computing starting values for algorithm.\n");
    oldF = computeObjFunc(n, lambda, x, covariance, mu);
    printf("\nInitial Objective value: %f ", oldF);

    k = 0;
    printf("\nk: %f", k);
    printf("\nNow attempting to compute the gradient.\n");
    gradient(n, lambda, grad, x, mu, covariance);
    direction(n, lambda, grad, ub, lb, mu, covariance, x, y);

    printf("\ny_%d: ", k);
    for (int i = 0; i < n; i++) {
        printf("%f ", *(y + i));
    }

    s = computeY(n, lambda, x, y, mu, covariance);
    printf("\ns: %f ", s);


    for (int i = 0; i < n; i++) {
        *(x + i) = (*(x + i)) + s * (*(y + i));
    }
    printf("\nx_%d: %f %f %f %f ", k, *x, *(x + 1), *(x + 2), *(x + 3));

    newF = computeObjFunc(n, lambda, x, covariance, mu);
    printf("\nnewF: %f ", newF);

    double delta = oldF - newF;
    int ii = 0;
    int max_iterations = 50000;
    while (delta >= 1e-6 && ii < max_iterations ) {
        k += 1;
        printf("\nk: %f", k);
        oldF = newF;
        gradient(n, lambda, grad, x, mu, covariance);
        direction(n, lambda, grad, ub, lb, mu, covariance, x, y);

        printf("\ny_%d: ", k);
        for (int i = 0; i < n; i++) {
            printf("%f ", *(y + i));
        }
        s = computeY(n, lambda, x, y, mu, covariance);
        printf("\ns: %f ", s);

        for (int i = 0; i < n; i++) {
            *(x + i) = (*(x + i)) + s * (*(y + i));
        }
        printf("\nx_%d: %f %f %f %f ", k, *x, *(x + 1), *(x + 2), *(x + 3));

        newF = computeObjFunc(n, lambda, x, covariance, mu);
        printf("\nnewF: %f ", newF);
        ii = ii + 1;
    }

    printf("\n");
    printf("END OF MAIN \n");


    return retcode;
}


int parse_Input_File(char *filename, int *address_of_n, double **plb, double **pub,
                     double **pmu, double **pcovariance, double *address_of_lambda, double **px, double **pgrad, double **py) {
    int readcode = 0, fscancode;
    char buffer[100];	// In stack. 100 bytes, each byte one character.
    int n, i, j, lamb;
    double *lb = NULL, *ub = NULL, *mu = NULL, *covariance = NULL, *x = NULL, *y = NULL, *grad = NULL;

    FILE *datafile = NULL;

    datafile = fopen(filename, "r");
    if (datafile == NULL) {
        perror("ERROR: Cannot open the specified file.\n");
        readcode = 1;// Read fail. No indentation needed.
        return readcode;
    }

    fscanf(datafile, "%s", buffer);	// Read 1 word at a time. (different from python). Now, buffer == "n"
    fscancode = fscanf(datafile, "%s", buffer);	// Now, buffer == 4
    if (fscancode == EOF) {	// EOF: in <stdio.h>
        perror("ERROR: EOF reached prematurely in input file. \n");
        readcode = 4;
        return readcode;
    }

    n = *address_of_n = atoi(buffer);	// *address_of_n is 1 argument we pass in this function.
    /*int atoi (const char * str); Convert string to integer*/

    printf("n = %d\n", n);

    lb = (double *)calloc(n, sizeof(double));
    *plb = lb;
    ub = (double *)calloc(n, sizeof(double));
    *pub = ub;
    mu = (double *)calloc(n, sizeof(double));
    *pmu = mu;
    covariance = (double *)calloc(n*n, sizeof(double));
    *pcovariance = covariance;
    x = (double *)calloc(n, sizeof(double));
    *px = x;
    y = (double *)calloc(n, sizeof(double));
    *py = y;
    grad = (double *)calloc(n, sizeof(double));
    *pgrad = grad;

    if (!lb || !ub || !mu || !covariance) {
        perror("ERROR: Insufficient memory available for allocation of arrays (lower, upper, mu, covariance). \n");
        readcode = 3;
    }

    fscanf(datafile, "%s", buffer);

    for (j = 0; j < n; j++) {
        fscanf(datafile, "%s", buffer);
        fscanf(datafile, "%s", buffer);
        lb[j] = atof(buffer);
        fscanf(datafile, "%s", buffer);
        ub[j] = atof(buffer);
        fscanf(datafile, "%s", buffer);
        mu[j] = atof(buffer);
        printf("j = %d lb = %g ub = %g mu = %g\n", j, lb[j], ub[j], mu[j]);
        x[j] = 0.0;
    }

    fscanf(datafile, "%s", buffer);
    fscanf(datafile, "%s", buffer);
    lamb = *address_of_lambda = atoi(buffer);

    fscanf(datafile, "%s", buffer); /* reading 'covariance'*/

    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            fscanf(datafile, "%s", buffer);
            covariance[i*n + j] = atof(buffer);
        }
    }

    fscanf(datafile, "%s", buffer);
    if (strcmp(buffer, "END") != 0) {
        printf("WARNING: Possible error in data file: 'END' missing.\n");
    }

    fclose(datafile);
    return readcode;	// Initial as 0.
}


// Step 1: Achieve feasibility
int feasible(int n, double *x, double *lb, double *ub) {
    int returncode = 0;
    double lsum = 0.0, usum = 0.0, xsum = 0.0;

    for (int i = 0; i < n; i++) {
        lsum += *(lb + i);
        usum += *(ub + i);
    }

    // Check whether lower bounds and upper bounds feasible.
    if (lsum > 1) {
        printf("Not feasible. Lower bounds sum to > 1");
        returncode = 1;
        return returncode;
    }
    if (usum < 1) {
        printf("Not feasible. Upper bounds sum to < 1");
        returncode = 1;
        return returncode;
    }

    // Initial value of x: lower bounds
    for (int i = 0; i < n; i++) {
        *(x + i) = *(lb + i);
    }
    xsum = lsum;

    for (int j = 0; j < n; j++) {
        if (xsum + (*(ub + j) - *(lb + j)) >= 1.0) {
            *(x + j) = 1.0 - xsum + *(lb + j);	// Increase x[j] so that sumx = 1.
            break;
        }
        else {
            *(x + j) = *(ub + j);	// Bring x[j] to upper bound.
            xsum += *(ub + j) - *(lb + j);
        }
    }

    printf("\nx_0: ");
    for (int j = 0; j < n; j++) {
        printf("%f ", *(x + j));
    }

    return returncode;
}

// Calculate the value of the objective function.
double computeObjFunc(int n, double lambda, double *x, double *covariance, double *mu) {
    double term1 = 0.0, term2 = 0.0, term3 = 0.0, obj;
    for (int i = 0; i < n; i++) {
        term1 += (*(covariance + i * (n + 1))) * pow(*(x + i), 2);
        term3 += (*(mu + i)) * (*(x + i));
        for (int j = i + 1; j < n; j++) {
            term2 += *(covariance + i * n + j) * (*(x + i)) * (*(x + j));
        }
    }
    //printf("term1:%f term2:%f term3:%f", term1, term2, term3);
    obj = lambda * (term1 + 2 * term2) - term3;
    return obj;
}

// Step 2: Improvement phase
double gradient(int n, double lambda, double *grad, double *x, double *mu, double *covariance) {
    double num = 0.0;
    for (int i = 0; i < n; i++) {
        num = (2 * lambda * (*(covariance + i * (n + 1))) *(*(x + i))) - (*(mu + i));
        for (int j = 0; j < n; j++) {
            if (j != i) {
                num += 2 * lambda * (*(covariance + i * n + j)) * (*(x + j));
            }
        }
        *(grad + i) = num;
    }
    return 0;
}

double direction(int n, double lambda, double *grad, double *ub, double *lb, double *mu, double *covariance, double *x, double *y) {
    double sum = 0.0;
    int temp = 0;

    // Sort the index in descending order.
    int index[] = { 0,1,2,3 };
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (*(grad + index[i]) < *(grad + index[j])) {
                temp = index[i];
                index[i] = index[j];
                index[j] = temp;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        sum = 0.0;
        for (int j = 0; j < n; j++) {
            if (j < i) {	// higher ranked go to lower bound
                *(y + index[j]) = *(lb + index[j]) - *(x + index[j]);
                sum += *(lb + index[j]) - *(x + index[j]);
            }
            else if (j > i) {	// lower ranked go to upper bound
                *(y + index[j]) = *(ub + index[j]) - *(x + index[j]);
                sum += *(ub + index[j]) - *(x + index[j]);
            }
        }
        *(y + index[i]) = (0 - sum);
        if ((*(y + index[i]) >= *(lb + index[i]) - *(x + index[i])) && (*(y + index[i]) <= *(ub + index[i]) - *(x + index[i]))) {
            return 0;
        }
    }

    printf("Error!Cannot find feasible y!!!");
    exit(0);
}

double computeY(int n, double lambda, double *x, double *y, double *mu, double *covariance) {
    double numerator = 0.0, denominator = 0.0, s = 0.0;
    for (int i = 0; i < n; i++) {
        numerator += (*(mu + i)) * (*(y + i)) - 2 * lambda * (*(covariance + i * n + i) * (*(x + i)) * (*(y + i)));
        denominator += 2 * lambda * (*(covariance + i * n + i)) * (*(y + i)) * (*(y + i));
        for (int j = i + 1; j < n; j++) {
            numerator -= 2 * lambda * (*(covariance + i * n + j)) * ((*(y + i)) * (*(x + j)) + (*(y + j)) * (*(x + i)));
            denominator += 4 * lambda * (*(covariance + i * n + j)) * (*(y + i)) * (*(y + j));
        }
    }
    s = numerator / denominator;
    return s;
}