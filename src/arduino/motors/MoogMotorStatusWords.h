
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
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define DEDTERROR         0b0000001000000000  //0x0200
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define TEMPERATUREWARN   0b0000000100000000  //0x0100
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define VELOCITYLIMIT     0b0000000010000000  //0x0080
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define POSITION          0b0000000001000000  //0x0040
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define TEMPERATUREERROR  0b0000000000100000  //0x0020
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define PEAKOVERCURRENT   0b0000000000010000  //0x0010
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define SERVOBUSVOLTAGE   0b0000000000001000  //0x0008
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define MOVING            0b0000000000000100  //0x0004
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define MOTOROFF          0b0000000000000010  //0x0002
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};
#define DRIVEREADY        0b0000000000000001  //0x0001
errorCode leftPosLimit = {"Left Position Limit", 0b1000000000000000};



//=================================================//
//          Define Status Word 1 Values            //
//=================================================//


//=================================================//
//          Define Status Word 2 Values            //
//=================================================//


//=================================================//
//          Define Status Word 3 Values            //
//=================================================//