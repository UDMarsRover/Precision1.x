

#ifndef MoogMotorStatusWords_h
#define MoogMotorStatusWords_h

#include <vector>

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
static errorCode leftPosLimit  = {"Left Position Limit",     0b1000000000000000};  //0x8000
static errorCode rightPosLimit = {"Right Position Limit",    0b0100000000000000};  //0x4000
static errorCode histLeftLimit = {"Histogram Left Limit",    0b0010000000000000};  //0x2000
static errorCode histRightLimit= {"Histogram Right Limit",   0b0001000000000000};  //0x1000
static errorCode negHWLimit    = {"Negative Hardware Limit", 0b0000100000000000};  //0x0800
static errorCode posHWLimit    = {"Positive Hardware Limit", 0b0000010000000000};  //0x0400
static errorCode dedtError     = {"Derivitive Error",        0b0000001000000000};  //0x0200
static errorCode tempWarning   = {"Over Temperature Warning",0b0000000100000000};  //0x0100
static errorCode velocityLimit = {"Velocity Limit",          0b0000000010000000};  //0x0080
static errorCode positionLimit = {"Position Limit Error",    0b0000000001000000};  //0x0040
static errorCode tempError     = {"Over Temperature Error",  0b0000000000100000};  //0x0020
static errorCode peakOverCur   = {"Peak Over Current Error", 0b0000000000010000};  //0x0010
static errorCode servoBusVolt  = {"Servo Bus Voltage Error", 0b0000000000001000};  //0x0008
static errorCode motorInMotion = {"Rotor In Motion Status",  0b0000000000000100};  //0x0004
static errorCode motorOff      = {"Motor Coils Turned Off",  0b0000000000000010};  //0x0002
static errorCode driveReady    = {"Motor Is Ready To Use",   0b0000000000000001};  //0x0001

static std::vector<errorCode> statusWord0 = {
  leftPosLimit,
  rightPosLimit,
  histLeftLimit,
  histRightLimit,
  negHWLimit,
  posHWLimit,
  dedtError,
  tempWarning,
  peakOverCur,
  servoBusVolt,
  motorInMotion,
  motorOff,
  driveReady
};



//=================================================//
//          Define Status Word 1 Values            //
// Index Registration And Software Travel Limits   //
//=================================================//
static errorCode rtNegSoftLim        = {"Real Time Negative Soft Limit",                                           0b1000000000000000}; //0x8000
static errorCode rtPosSoftLim        = {"Real Time Positive Soft Limit",                                           0b0100000000000000}; //0x4000
static errorCode hisNegSoftOvTravLim = {"Historical Negative Software Over Travel Limit",                          0b0010000000000000}; //0x2000
static errorCode hisPosSoftOvTravLim = {"Historical Positive Software Over Travel Limit",                          0b0001000000000000}; //0x1000
static errorCode softLimMode         = {"Soft Limit Mode (Indicator): 0-Don't Stop. 1-Cause Fault. Default Is 1",  0b0000100000000000}; //0x0800
static errorCode softTravLimEn       = {"Software Travel Limits Enabled",                                          0b0000010000000000}; //0x0400
static errorCode capInState1         = {"Capture Input State 1 (Indicator)",                                       0b0000001000000000}; //0x0200
static errorCode capInState0         = {"Capture Input State 0 (Indicator)",                                       0b0000000100000000}; //0x0100
static errorCode falEdgCapENC1       = {"Falling Edge Captured ENC(1) (Historical Bit)",                           0b0000000010000000}; //0x0080
static errorCode risEdgCapENC1       = {"Rising Edge Captured ENC(1) (Historical Bit)",                            0b0000000001000000}; //0x0040
static errorCode falCapEnc1          = {"Fall Capture Encoder(1) Armed",                                           0b0000000000100000}; //0x0020
static errorCode risCapEnc1          = {"Rise Capture Encoder(1) Armed",                                           0b0000000000010000}; //0x0010
static errorCode falEdgCapENC0       = {"Falling Edge Captured ENC(0) (Historical Bit)",                           0b0000000000001000}; //0x0008
static errorCode risEdgCapENC0       = {"Rising Edge Captured ENC(0) (Historical Bit)",                            0b0000000000000100}; //0x0004
static errorCode falCapEnc0          = {"Fall Capture Encoder(0) Armed",                                           0b0000000000000010}; //0x0002
static errorCode risCapEnc0          = {"Rise Capture Encoder(0) Armed",                                           0b0000000000000001}; //0x0001

//=================================================//
//          Define Status Word 2 Values            //
//        Communications, Program, and Memory      //
//=================================================//
static errorCode prgmCheckSum  = {"Program Checksum Error",           0b1000000000000000};  //0x8000
static errorCode commandError  = {"Command Syntax Error",             0b0100000000000000};  //0x4000
static errorCode eeBusy        = {"EE Busy",                          0b0010000000000000};  //0x2000
static errorCode eeWriteBuff   = {"EE Write Buffer Overflow",         0b0001000000000000};  //0x1000
static errorCode traceInprog   = {"Trace In Progress",                0b0000100000000000};  //0x0800
static errorCode progRunning   = {"Program Running",                  0b0000010000000000};  //0x0400
static errorCode adbBad        = {"ADB Bad Checksum",                 0b0000001000000000};  //0x0200
static errorCode watchdogEvent = {"Watchdog Event",                   0b0000000100000000};  //0x0100
static errorCode i2cRunning    = {"I2C Running Error",                0b0000000010000000};  //0x0080
static errorCode ethernetError = {"Ethernet Error",                   0b0000000001000000};  //0x0040
static errorCode reserved5     = {"Reserved 5",                       0b0000000000100000};  //0x0020
static errorCode canPortErr    = {"CAN Port Error",                   0b0000000000010000};  //0x0010
static errorCode reserved3     = {"Reserved 3",                       0b0000000000001000};  //0x0008
static errorCode USBerr        = {"USB Error ",                       0b0000000000000100};  //0x0004
static errorCode ComChnl1Err   = {"Error on Communications Channel 1",0b0000000000000010};  //0x0002
static errorCode ComChnl0Err   = {"Error on Communicatoins Channel 0",0b0000000000000001};  //0x0001


//=================================================//
//          Define Status Word 3 Values            //
// PID State, Brake, Move Generation Indicators    //
//=================================================//
static errorCode velTarRea   = {"Velocity Target Reached", 0b1000000000000000}; //0x8000
static errorCode exGoEn      = {"External Go Enabled",     0b0100000000000000}; //0x4000
static errorCode braOK       = {"Brake OK",                0b0010000000000000}; //0x2000
static errorCode braAss      = {"Brake Asserted",          0b0001000000000000}; //0x1000
static errorCode modRoll     = {"Modulo Rollover",         0b0000100000000000}; //0x0800
static errorCode peaCurSat   = {"Peak Current Saturation", 0b0000010000000000}; //0x0400
static errorCode res9        = {"Reserved 9",              0b0000001000000000}; //0x0200
static errorCode relPosMode  = {"Relative Position Mode",  0b0000000100000000}; //0x0100
static errorCode ioFauLat    = {"I/O Fault Latch",         0b0000000010000000}; //0x0080
static errorCode torDir      = {"Torque Direction",        0b0000000001000000}; //0x0040
static errorCode velDir      = {"Velocity Direction",      0b0000000000100000}; //0x0020
static errorCode kgEn        = {"KG Enabled",              0b0000000000010000}; //0x0010
static errorCode wrapOcc     = {"Wraparound Occured",      0b0000000000001000}; //0x0008
static errorCode volSat      = {"Voltage Saturation",      0b0000000000000100}; //0x0004
static errorCode torSat      = {"Torque Saturation",       0b0000000000000010}; //0x0002
static errorCode res0        = {"Reserved 0",              0b0000000000000001}; //0x0001


//=================================================//
//          Define Status Word 4 Values            //
//               Interrupt Timers                  //
//=================================================//
static errorCode timer3   = {"Timer 3",   0b0000000000001000};//0x0008
static errorCode timer2   = {"Timer 2",   0b0000000000000100}; //0x0004
static errorCode timer1   = {"Timer 1",   0b0000000000000010}; //0x0002
static errorCode timer0   = {"Timer 0",   0b0000000000000001}; //0x0001



//=================================================//
//          Define Status Word 5 Values            //
//          Interrupt Status Indicators            //
//=================================================//
static errorCode enIntrpts   = {"Enable Interrupts",       0b1000000000000000}; //0x8000
static errorCode enIntrpt7   = {"Interrupt 7 Enabled",     0b0000000010000000}; //0x0080
static errorCode enIntrpt6   = {"Interrupt 6 Enabled",     0b0000000001000000}; //0x0040
static errorCode enIntrpt5   = {"Interrupt 5 Enabled",     0b0000000000100000}; //0x0020
static errorCode enIntrpt4   = {"Interrupt 4 Enabled",     0b0000000000010000}; //0x0010
static errorCode enIntrpt3   = {"Interrupt 3 Enabled",     0b0000000000001000}; //0x0008
static errorCode enIntrpt2   = {"Interrupt 2 Enabled",     0b0000000000000100}; //0x0004
static errorCode enIntrpt1   = {"Interrupt 1 Enabled",     0b0000000000000010}; //0x0002
static errorCode enIntrpt0   = {"Interrupt 0 Enabled",     0b0000000000000001}; //0x0001



//=================================================//
//          Define Status Word 6 Values            //
//                  Drive Modes                    //
//=================================================//
static errorCode rgnAct      = {"Regen Active",            0b1000000000000000}; //0x8000
static errorCode hghBusVolt  = {"High Bus Voltage",        0b0100000000000000}; //0x4000
static errorCode lowBusVolt  = {"Low Bus Voltage",         0b0010000000000000}; //0x2000
static errorCode ABSbatFlt   = {"ABS Battery Fault",       0b0001000000000000}; //0x1000
static errorCode MTBact      = {"MTB Active",              0b0000100000000000}; //0x0800
static errorCode invd        = {"Inverted",                0b0000010000000000}; //0x0400
static errorCode enTOB       = {"TOB enabled",             0b0000001000000000}; //0x0200
static errorCode angleMatch  = {"Angle Match",             0b0000000100000000}; //0x0100
static errorCode driveEnFault= {"Drive Enable Fault",      0b0000000010000000}; //0x0080
static errorCode MDHmodeAct  = {"MDH Mode Active",         0b0000000001000000}; //0x0040
static errorCode fdbckFault  = {"Velocity Direction",      0b0000000000100000}; //0x0020
static errorCode reserved4   = {"Reserved 4",              0b0000000000010000}; //0x0010
static errorCode vectorCntrl = {"Vector Control",          0b0000000000001000}; //0x0008
static errorCode sineMode    = {"sineMode",                0b0000000000000100}; //0x0004
static errorCode enhcdTrapMd = {"Enhanced Trap Mode",      0b0000000000000010}; //0x0002
static errorCode trapMd      = {"Trap Mode",               0b0000000000000001}; //0x0001


//=================================================//
//          Define Status Word 7 Values            //
//                  Drive Modes                    //
//=================================================//
static errorCode TSwait            = {"TS WAIT",                                0b1000000000000000}; //0x8000
static errorCode tvrsLwrDwellInPrgs= {"Traverse Lower Dwell in Progress",       0b0100000000000000}; //0x4000
static errorCode tvrsDirdction     = {"Traverse Direction, 0:FWD, 1:Rev",       0b0010000000000000}; //0x2000
static errorCode TG2dwell          = {"TG2 Dwell (or higher Dwell in progress)",0b0001000000000000}; //0x1000
static errorCode TG2Decel          = {"TG2 Decel/Decend",                       0b0000100000000000}; //0x0800
static errorCode TG2slewing        = {"TG2 Slewing",                            0b0000010000000000}; //0x0400
static errorCode TG2Accel          = {"TG2 Accel/Ascend",                       0b0000001000000000}; //0x0200
static errorCode TG2inProg         = {"TG2 in Progress",                        0b0000000100000000}; //0x0100
static errorCode TG1dwell          = {"TG1 Reserved or Dwell",                  0b0000000000010000}; //0x0010
static errorCode TG1decel          = {"TG1 Decel/Descend",                      0b0000000000001000}; //0x0008
static errorCode TG1slewing        = {"TG1 Slewing",                            0b0000000000000100}; //0x0004
static errorCode TG1accel          = {"TG1 Accel",                              0b0000000000000010}; //0x0002
static errorCode TG1inPrgs         = {"Tg1 in Progress",                        0b0000000000000001}; //0x0001



//=================================================//
//          Define Status Word 8 Values            //
//                 Cam Support                     //
//=================================================//
static errorCode ipMode1     = {"IP Mode 1",               0b1000000000000000}; //0x8000
static errorCode ipMode0     = {"IP Mode 0",               0b0100000000000000}; //0x4000
static errorCode ipUserBit5  = {"IP User Bit 5",           0b0010000000000000}; //0x2000
static errorCode ipUserBit4  = {"IP User Bit 4",           0b0001000000000000}; //0x1000
static errorCode ipUserBit3  = {"IP User Bit 3",           0b0000100000000000}; //0x0800
static errorCode ipUserBit2  = {"IP User Bit 2",           0b0000010000000000}; //0x0400
static errorCode ipUserBit1  = {"IP User Bit 1",           0b0000001000000000}; //0x0200
static errorCode ipUserBit0  = {"IP User Bit 0",           0b0000000100000000}; //0x0100
static errorCode camMode1    = {"Cam Mode 1",              0b0000000010000000}; //0x0080
static errorCode camMode0    = {"Cam Mode 0",              0b0000000001000000}; //0x0040
static errorCode camUserBit5 = {"Cam User Bit 5",          0b0000000000100000}; //0x0020
static errorCode camUserBit4 = {"Cam User Bit 4",          0b0000000000010000}; //0x0010
static errorCode camUserBit3 = {"Cam User Bit 3",          0b0000000000001000}; //0x0008
static errorCode camUserBit2 = {"Cam User Bit 2",          0b0000000000000100}; //0x0004
static errorCode camUserBit1 = {"Cam User Bit 1",          0b0000000000000010}; //0x0002
static errorCode camUserBit0 = {"Cam User Bit 0",          0b0000000000000001}; //0x0001



//=================================================//
//            Define Status Word 10 Values         //
//             RxPDO Arrival Notification          //
//=================================================//
static errorCode RxPDO5ari   = {"RxPDO 5 arrived",          0b0000000000100000}; //0x0020
static errorCode RxPDO4ari   = {"RxPDO 4 arrived",          0b0000000000010000}; //0x0010
static errorCode RxPDO3ari   = {"RxPDO 3 arrived",          0b0000000000001000}; //0x0008
static errorCode RxPDO2ari   = {"RxPDO 2 arrived",          0b0000000000000100}; //0x0004
static errorCode RxPDO1ari   = {"RxPDO 1 arrived",          0b0000000000000010}; //0x0002
static errorCode MasterEnb   = {"Master Enabled",           0b0000000000000001}; //0x0001

#endif