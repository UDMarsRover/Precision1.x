#ifndef UDMRT_THERMISOR_CPP
#define UDMRT_THERMISOR_CPP

#include "udmrt_thermistor.h"

UDMRT_Thermistor::UDMRT_Thermistor(char* name, 
                         ros::NodeHandle* node,
                         int inputPin,
                         int thermistor_value,
                         int r_2_value,
                         int b_coefficient):
    UDMRT_Sensor<sensor_msgs::Temperature>(name,node){
        in = inputPin;
        thermVal = thermistor_value;
        r2 = r_2_value;
        bCoeff = b_coefficient;
    }