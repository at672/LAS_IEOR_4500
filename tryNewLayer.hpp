//
//  TryNewLayer.hpp
//  PJ3
//
//  Created by 曹真一 on 10/29/18.
//  Copyright © 2018 曹真一. All rights reserved.
//

#ifndef tryNewLayer_hpp
#define tryNewLayer_hpp

#include <iostream>

class tryNewLayer
{
public:
    tryNewLayer(int layerSize);
    void active();
    void derive();
    double *getinput();
    double *getoutput();
    double generateRandom();
    // directly use the output from last layer to calculate the new input and use setVals to caculate the output
    // only use for the first time layer construction, since we use the random weight
    void caculateInput(double *outputfromlastlayer);
    // use for the following time
    void caculateInput1(double *outputfromlastlayer);
    void setVals(double *input); // will automatically calculate output(actived values) and derivetive.
    void setweight(double *weight);
    
    
private:
    int layerSize;
    
    double *input;
    double *output;
    double *derivedVals;
    double *weight;
};

#endif /* tryNewLayer_hpp */

