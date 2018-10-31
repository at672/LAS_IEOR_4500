//
//  TryNewLayer.cpp
//  PJ3
//
//  Created by 曹真一 on 10/29/18.
//  Copyright © 2018 曹真一. All rights reserved.
//

//#include "TryNewLayer.hpp"
#include "tryNewLayer.hpp"
#include <math.h>
#include <random>

tryNewLayer::tryNewLayer(int layerSize){
    this->layerSize = layerSize;
    this->input = new double[this->layerSize];
    this->output = new double[this->layerSize];
    this->derivedVals = new double[this->layerSize];
    
}

void tryNewLayer::active(){
    for(int i = 0; i < layerSize; i++){
        this->output[i] = 1 / (1 + exp(- this->input[i]));
    }
}

void tryNewLayer::derive(){
    for(int i = 0; i < layerSize; i++){
        this->derivedVals[i] = this->output[i] * (1 - this->output[i]);
    }
}

double * tryNewLayer::getinput(){
    return this->input;
}

double * tryNewLayer::getoutput(){
    return this->output;
}

double tryNewLayer::generateRandom(){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0,1);
    
    return dis(gen);
}

void tryNewLayer::caculateInput(double *outputfromlastlayer){
    // directly use the output from last layer to calculate the new input for this layer and use setVals() to caculate the output
    //only use for the first time layer construction, since we use the random weight
    double *newinput;
    for (int j = 0; j<sizeof(layerSize);j++){
        double *temp;
        for (int i = 0; i<sizeof(outputfromlastlayer); i++){
            double weight = this->generateRandom();
            temp[i] = weight*outputfromlastlayer[i];
            newinput[j]+=temp[i];
        }
    }
    this->setVals(newinput);
}

void tryNewLayer::caculateInput1(double *outputfromlastlayer){
    // directly use the output from last layer to calculate the new input for this layer and use setVals() to caculate the output
    // use for the following time, using the input weight
    // before using this function, we need to setweight()
    double *newinput;
    for (int j = 0; j<sizeof(layerSize);j++){
        double *temp;
        for (int i = 0; i<sizeof(outputfromlastlayer); i++){
            temp[i] = weight[i]*outputfromlastlayer[i];
            newinput[j]+=temp[i];
        }
    }
    this->setVals(newinput);
}

void tryNewLayer::setVals(double *input){
    for(int i = 0; i < this->layerSize; i++){
        this->input[i] = input[i];
    }
    this->active(); // update output
    this->derive(); // update derive
}

void tryNewLayer::setweight(double *weight){
    this->weight = weight;
}
