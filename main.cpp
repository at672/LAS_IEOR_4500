//
//  main.cpp
//  PJ3
//
//  Created by 曹真一 on 10/22/18.
//  Copyright © 2018 曹真一. All rights reserved.
//


#include <iostream>
#include <vector>
//#include "Neuron.h"
//#include "Matrix.hpp"
//#include "NeuralN.hpp"
#include "tryNewLayer.hpp"
using namespace std;

int main(int argc, char **argv){
    /*
     Matrix *m = new Matrix(3, 2, true);
     m->print2Console();
     cout << "---------------------" << endl;
     
     Matrix *mT = m->transpose();
     mT->print2Console();
     return 0;
     
     vector<int> topology;
     topology.push_back(3);
     topology.push_back(2);
     topology.push_back(3);
     
     vector<double> input;
     input.push_back(1.0);
     input.push_back(2.0);
     input.push_back(3.0);
     
     NeuralN *nn = new NeuralN(topology);
     nn->setCurrentInput(input);
     */
    /*
     we should have some code calculating the size of data here
     */
    
    // topology: how many layers; how many neurons in each layer
    // input X
    // ouput Y (used for calculate errors)
    int topology[4] = {504,90,90,504};
    int topologySize;
    topologySize = sizeof(topology)/sizeof(*topology);
    /*
    // matrix generating function
    int** m1 = new int*[topology[0]];
    for(int i = 0; i < topology[0]; ++i){
        m1[i] = new int[topology[1]];
    }
    // ++ random generate;
    
     feedforward function
     input: Xi
     output: prediction
     */
    
    /* loss function*/
    /*
    // contruct the graph
    tryNewLayer *layers = new tryNewLayer[topologySize];
    for(int i = 0; i < topologySize; i++){
        if (i == 0){
            layers[i] = tryNewLayer(x);
        }
    }
    return 0;
    */
}


double *feedForward(double *xInput, int *topology){
    //the first hidden layer
    tryNewLayer layer1(sizeof(xInput));
    layer1.caculateInput(xInput);
    double *output1 = layer1.getoutput();
    
    //the second hidden layer
    tryNewLayer layer2(sizeof(topology[1]));
    layer2.caculateInput(output1);
    double *output2 = layer2.getoutput();
    
    //the output layer
    tryNewLayer layer3(sizeof(topology[2]));
    layer3.caculateInput(output2);
    double *output3 = layer3.getoutput();
    
    return output3;
}

double loss(double *realY, double *caculateY){
    //loss function
    double sum = 0;
    for (int i = 0; i < sizeof(realY); i++){
        sum += (realY[i]-caculateY[i])*(realY[i]-caculateY[i]);
    }
    return sum;
}
