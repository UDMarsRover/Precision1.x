/**
 * @file udmrt_sensor.cpp
 * @author Greg Molskow
 * @brief This file contains the necessary imports for a basic sensor that is integrated into ROS1 using the rosserial arduino library. This file was created with the intention of providing a base to build a variety of custom sensors quickly and easily in a uniform fashion.
 * @version 0.1
 * @date 2024-07-09
 * 
 * @copyright Copyright (c) 2024
 * 
 */


#ifndef UDMRT_SENSOR
#define UDMRT_SENSOR

#include <ros.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/KeyValue.h>
#include <sensor_msgs/NavSatFix.h> // GPS

#define DIAGNOSTIC_STATUS_LENGTH 1
#define OK diagnostic_msgs::DiagnosticStatus::OK;
#define WARN diagnostic_msgs::DiagnosticStatus::WARN;
#define ERROR diagnostic_msgs::DiagnosticStatus::ERROR;
#define STALE diagnostic_msgs::DiagnosticStatus::STALE;


template <typename ros_data_type> class UDMRT_Sensor{
    /**
     * @brief This class is meant to be a parent class to all UDMRT sensors that are connected to a Arduino Nano BLE sense 33. This class initializes the required publishers and sets up the required values for the diagnostics topic. The goal of this class is to standardize the creation of custom sensors and to make development and debugging more streamlined.
     * 
     * NOTE: The "updateData()" and the "updateDiagnostic()" functions are intended to be created by the child class and are required for operation. These functions are not created here as the data and diagnostic collection will be different for each sensor.
     * 
     */


    public:
        UDMRT_Sensor( char* name, char* dataTopic, char* diagnosticTopic):
        data_pub(dataTopic, &data_msg),
        diag_pub(diagnosticTopic,&diag_msg){
            /**
             * @brief The constructor for the UDMRT_Sensor class
             * 
             * @param name The name of the sensor
             * @param dataTopic The topic where the sensor data will be pushed
             * @param diagnosticTopic The topic where the diagnostic data will be pushed
             * 
             */
            diag_msg.values_length = DIAGNOSTIC_STATUS_LENGTH;
            diag_msg.name = name;
        }

        void init(ros::NodeHandle* node){
            node->advertise(UDMRT_Sensor::diag_pub);
            node->advertise(UDMRT_Sensor::data_pub);
        }

    private:
        ros::Publisher diag_pub;
        ros::Publisher data_pub;
        ros_data_type data_msg;
        diagnostic_msgs::DiagnosticStatus diag_msg;
        diagnostic_msgs::KeyValue key;
        
        void publishData(){
            UDMRT_Sensor::updateData();
            UDMRT_Sensor::data_pub.publish(&data_msg);
        }
        
        void publishDiag(){
            UDMRT_Sensor::updateDiagnostics();
            UDMRT_Sensor::diag_pub.publish(&diag_msg);
        }

        void updateData();

        void updateDiagnostics();


};

#endif