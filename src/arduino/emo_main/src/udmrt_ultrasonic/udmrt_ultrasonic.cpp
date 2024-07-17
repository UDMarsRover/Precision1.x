#ifndef UDMRT_ULTRASONIC_CPP
#define UDMRT_ULTRASONIC_CPP

#include "udmrt_ultrasonic.h"

UDMRT_Ultrasonic::UDMRT_Ultrasonic(char* name, 
                         ros::NodeHandle* node,
                         int trigger_pin,
                         int echo_pin,
                         int max_distance,
                         int min_distance,
                         double alpha_value):
    UDMRT_Sensor<sensor_msgs::Range>(name,node),
    ultrasonicSensor(trigger_pin,echo_pin,max_distance){

    alphaValue = alpha_value;
    data_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
    data_msg.min_range = min_distance;
    data_msg.max_range = max_distance;

}

void UDMRT_Ultrasonic::updateData(){
    // convert microseconds to cm
    currentDistance = (ultrasonicSensor.ping() * 0.034) / 2;
    if (data_msg.min_range <= currentDistance <= data_msg.max_range) {
        currentDistance = expFilter(alphaValue,data_msg.range, currentDistance);
        data_msg.range = currentDistance;
    }
    
    if (data_msg.range <= 30) errorState(data_msg.range,"2","Within 30 CM");
    else if (data_msg.radiation_type <= 50) warningState(data_msg.range,"1","Within 50 CM");
    else okState();
}

void UDMRT_Ultrasonic::spin(){
    updateData();
    UDMRT_Sensor::spin();
}


#endif