//
//  main.c
//  PJ2Q1
//
//  Created by 曹真一 on 10/13/18.
//  Copyright © 2018 曹真一. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int readit(char *nameoffile, int *addressofn, double **, double **, double **, double **, double **);

int main(int argc, char **argv)
{
    int retcode = 0;
    int n;
    double *lb, *ub, *covariance, *mu, *lambda;
    /*
    if (argc != 2){
        printf("usage: qp1 filename\n");  retcode = 1;
        goto BACK;
    }
    */
    retcode = readit("example.txt", &n, &lb, &ub, &mu, &covariance, &lambda);
    //printf(lb[0]);
    BACK:
    return retcode;
}

int readit(char *filename, int *address_of_n, double **plb, double **pub,
           double **pmu, double **pcovariance, double **plambda)
{
    int readcode = 0, fscancode;
    FILE *datafile = NULL;
    char buffer[100];
    int n, i, j;
    double *lb = NULL, *ub = NULL, *mu = NULL, *covariance = NULL, *lambda = NULL;
    
    datafile = fopen(filename, "r");
    if (!datafile){
        printf("cannot open file %s\n", filename);
        readcode = 2;  goto BACK;
    }
    
    printf("reading data file %s\n", filename);
    
    fscanf(datafile, "%s", buffer);
    fscancode = fscanf(datafile, "%s", buffer);
    if (fscancode == EOF){
        printf("problem: premature file end at ...\n");
        readcode = 4; goto BACK;
    }
    
    n = *address_of_n = atoi(buffer);
    
    printf("n = %d\n", n);
    
    lb = (double *)calloc(n, sizeof(double));
    *plb = lb;
    ub = (double *)calloc(n, sizeof(double));
    *pub = ub;
    mu = (double *)calloc(n, sizeof(double));
    *pmu = mu;
    lambda = (double *)calloc(1, sizeof(double));
    *plambda = lambda;
    covariance = (double *)calloc(n*n, sizeof(double));
    *pcovariance = covariance;
    
    if (!lb || !ub || !mu || !lambda || !covariance){
        printf("not enough memory for lb ub mu covariance\n"); readcode = 3; goto BACK;
    }
    
    //fscanf(datafile, "%s", buffer);
    //lambda = atof(buffer);
    
    for (j = 0; j < n; j++){
        fscanf(datafile, "%s", buffer);
        fscanf(datafile, "%s", buffer);
        lb[j] = atof(buffer);
        fscanf(datafile, "%s", buffer);
        ub[j] = atof(buffer);
        fscanf(datafile, "%s", buffer);
        mu[j] = atof(buffer);
        printf("j = %d lb = %g ub = %g mu = %g\n", j, lb[j], ub[j], mu[j]);
    }
    
    fscanf(datafile, "%s", buffer);
    fscanf(datafile, "%s", buffer);
    
    
    fscanf(datafile, "%s", buffer); /* reading 'covariance'*/
    
    for (i = 0; i < n; i++){
        for (j = 0; j < n; j++){
            fscanf(datafile, "%s", buffer);
            covariance[i*n + j] = atof(buffer);
        }
    }
    
    
    fscanf(datafile, "%s", buffer);
    if (strcmp(buffer, "END") != 0){
        printf("possible error in data file: 'END' missing\n");
    }
    
    
    fclose(datafile);
    
    BACK:
    
    return readcode;
}

