
#define okSTAT    0b0 // Need To Set
#define warnSTAT  0b0 // Need To Set
#define errorSTAT 0b0 // Need To Set

struct errorCode {
  String name;
  int code;
};

//=================================================//
//          Define Status Word 0 Values            //
//=================================================//
#define LEFTPOSLIMIT      0b1000000000000000  //0x8000
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};   //0x8000
#define RIGHTPOSLIMIT     0b0100000000000000  //0x4000
errorCode rightPosLimit = {"Right Position Limit", 0b1000000000000000};
#define HISTLEFTLIMIT     0b0010000000000000  //0x2000
errorCode histLeftLimit = {"Histogram Left Limit", 0b1000000000000000};
#define HISTRIGHTLIMIT    0b0001000000000000  //0x1000
errorCode histRightLimit = {"Histogram Right Limit", 0b1000000000000000};
#define NEGATIVEHWLIMIT   0b0000100000000000  //0x0800
errorCode negHWLimit = {"Negative Hardware Limit", 0b1000000000000000};
#define POSITIVEHWLIMIT   0b0000010000000000  //0x0400

#define DEDTERROR         0b0000001000000000  //0x0200

#define TEMPERATUREWARN   0b0000000100000000  //0x0100

#define VELOCITYLIMIT     0b0000000010000000  //0x0080

#define POSITION          0b0000000001000000  //0x0040

#define TEMPERATUREERROR    //0x0020

#define PEAKOVERCURRENT     //0x0010

#define SERVOBUSVOLTAGE   0b0000000000001000  //0x0008

#define MOVING            0b0000000000000100  //0x0004

#define MOTOROFF          0b0000000000000010  //0x0002

#define DRIVEREADY        0b0000000000000001  //0x0001




//=================================================//
//          Define Status Word 1 Values            //
// Index Registration And Software Travel Limits   //
//=================================================//
errorCode rtNegSoftLim        = {"Real Time Negative Soft Limit",                                           0b1000000000000000} //0x8000
errorCode rtPosSoftLim        = {"Real Time Positive Soft Limit",                                           0b0100000000000000} //0x4000
errorCode hisNegSoftOvTravLim = {"Historical Negative Software Over Travel Limit",                          0b0010000000000000} //0x2000
errorCode hisPosSoftOvTravLim = {"Historical Positive Software Over Travel Limit",                          0b0001000000000000} //0x1000
errorCode softLimMode         = {"Soft Limit Mode (Indicator): 0-Don't Stop. 1-Cause Fault. Default Is 1",  0b0000100000000000} //0x0800
errorCode softTravLimEn       = {"Software Travel Limits Enabled",                                          0b0000010000000000} //0x0400
errorCode capInState1         = {"Capture Input State 1 (Indicator)",                                       0b0000001000000000} //0x0200
errorCode capInState0         = {"Capture Input State 0 (Indicator)",                                       0b0000000100000000} //0x0100
errorCode falEdgCapENC1       = {"Falling Edge Captured ENC(1) (Historical Bit)",                           0b0000000010000000} //0x0080
errorCode risEdgCapENC1       = {"Rising Edge Captured ENC(1) (Historical Bit)",                            0b0000000001000000} //0x0040
errorCode falCapEnc1          = {"Fall Capture Encoder(1) Armed",                                           0b0000000000100000} //0x0020
errorCode risCapEnc1          = {"Rise Capture Encoder(1) Armed",                                           0b0000000000010000} //0x0010
errorCode falEdgCapENC0       = {"Falling Edge Captured ENC(0) (Historical Bit)",                           0b0000000000001000} //0x0008
errorCode risEdgCapENC0       = {"Rising Edge Captured ENC(0) (Historical Bit)",                            0b0000000000000100} //0x0004
errorCode falCapEnc0          = {"Fall Capture Encoder(0) Armed",                                           0b0000000000000010} //0x0002
errorCode risCapEnc0          = {"Rise Capture Encoder(0) Armed",                                           0b0000000000000001} //0x0001

//=================================================//
//          Define Status Word 2 Values            //
//=================================================//


//=================================================//
//          Define Status Word 3 Values            //
// PID State, Brake, Move Generation Indicators    //
//=================================================//
errorCode velTarRea   = {"Velocity Target Reached", 0b1000000000000000} //0x8000
errorCode exGoEn      = {"External Go Enabled",     0b0100000000000000} //0x4000
errorCode braOK       = {"Brake OK",                0b0010000000000000} //0x2000
errorCode braAss      = {"Brake Asserted",          0b0001000000000000} //0x1000
errorCode modRoll     = {"Modulo Rollover",         0b0000100000000000} //0x0800
errorCode peaCurSat   = {"Peak Current Saturation", 0b0000010000000000} //0x0400
errorCode res9        = {"Reserved 9",              0b0000001000000000} //0x0200
errorCode relPosMode  = {"Relative Position Mode",  0b0000000100000000} //0x0100
errorCode ioFauLat    = {"I/O Fault Latch",         0b0000000010000000} //0x0080
errorCode torDir      = {"Torque Direction",        0b0000000001000000} //0x0040
errorCode velDir      = {"Velocity Direction",      0b0000000000100000} //0x0020
errorCode kgEn        = {"KG Enabled",              0b0000000000010000} //0x0010
errorCode wrapOcc     = {"Wraparound Occured",      0b0000000000001000} //0x0008
errorCode volSat      = {"Voltage Saturation",      0b0000000000000100} //0x0004
errorCode torSat      = {"Torque Saturation",       0b0000000000000010} //0x0002
errorCode res0        = {"Reserved 0",              0b0000000000000001} //0x0001