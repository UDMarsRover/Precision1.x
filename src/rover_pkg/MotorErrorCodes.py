# Define Status Word 0 Values
statusWord0 = {
    0x8000: "Left Position Limit",
    0x4000: "Right Position Limit",
    0x2000: "Histogram Left Limit",
    0x1000: "Histogram Right Limit",
    0x0800: "Negative Hardware Limit",
    0x0400: "Positive Hardware Limit",
    0x0200: "Derivitive Error",
    0x0100: "Over Temperature Warning",
    0x0080: "Velocity Limit",
    0x0040: "Position Limit Error",
    0x0020: "Over Temperature Error",
    0x0010: "Peak Over Current Error",
    0x0008: "Servo Bus Voltage Error",
    0x0004: "Rotor In Motion Status",
    0x0002: "Motor Coils Turned Off",
    0x0001: "Motor Is Ready To Use"
}

# Define Status Word 1 Values
statusWord1 = {
    0x8000: "Real Time Negative Soft Limit",
    0x4000: "Real Time Positive Soft Limit",
    0x2000: "Historical Negative Software Over Travel Limit",
    0x1000: "Historical Positive Software Over Travel Limit",
    0x0800: "Soft Limit Mode (Indicator): 0-Don't Stop. 1-Cause Fault. Default Is 1",
    0x0400: "Software Travel Limits Enabled",
    0x0200: "Capture Input State 1 (Indicator)",
    0x0100: "Capture Input State 0 (Indicator)",
    0x0080: "Falling Edge Captured ENC(1) (Historical Bit)",
    0x0040: "Rising Edge Captured ENC(1) (Historical Bit)",
    0x0020: "Fall Capture Encoder(1) Armed",
    0x0010: "Rise Capture Encoder(1) Armed",
    0x0008: "Falling Edge Captured ENC(0) (Historical Bit)",
    0x0004: "Rising Edge Captured ENC(0) (Historical Bit)",
    0x0002: "Fall Capture Encoder(0) Armed",
    0x0001: "Rise Capture Encoder(0) Armed"
}

# Define Status Word 2 Values
statusWord2 = {
    0x8000: "Program Checksum Error",
    0x4000: "Command Syntax Error",
    0x2000: "EE Busy",
    0x1000: "EE Write Buffer Overflow",
    0x0800: "Trace In Progress",
    0x0400: "Program Running",
    0x0200: "ADB Bad Checksum",
    0x0100: "Watchdog Event",
    0x0080: "I2C Running Error",
    0x0040: "Ethernet Error",
    0x0020: "Reserved 5",
    0x0010: "CAN Port Error",
    0x0008: "Reserved 3",
    0x0004: "USB Error ",
    0x0002: "Error on Communications Channel 1",
    0x0001: "Error on Communicatoins Channel 0"
}

# Define Status Word 3 Values
statusWord3 = {
    0x8000: "Velocity Target Reached",
    0x4000: "External Go Enabled",
    0x2000: "Brake OK",
    0x1000: "Brake Asserted",
    0x0800: "Modulo Rollover",
    0x0400: "Peak Current Saturation",
    0x0200: "Reserved 9",
    0x0100: "Relative Position Mode",
    0x0080: "I/O Fault Latch",
    0x0040: "Torque Direction",
    0x0020: "Velocity Direction",
    0x0010: "KG Enabled",
    0x0008: "Wraparound Occured",
    0x0004: "Voltage Saturation",
    0x0002: "Torque Saturation",
    0x0001: "Reserved 0"
}

# Define Status Word 4 Values
statusWord4 = {
    0x0008: "Timer 3",
    0x0004: "Timer 2",
    0x0002: "Timer 1",
    0x0001: "Timer 0"
}

# Define Status Word 5 Values
statusWord5 = {
    0x8000: "Enable Interrupts",
    0x0080: "Interrupt 7 Enabled",
    0x0040: "Interrupt 6 Enabled",
    0x0020: "Interrupt 5 Enabled",
    0x0010: "Interrupt 4 Enabled",
    0x0008: "Interrupt 3 Enabled",
    0x0004: "Interrupt 2 Enabled",
    0x0002: "Interrupt 1 Enabled",
    0x0001: "Interrupt 0 Enabled"
}

# Define Status Word 6 Values
statusWord6 = {
    0x8000: "Regen Active",
    0x4000: "High Bus Voltage",
    0x2000: "Low Bus Voltage",
    0x1000: "ABS Battery Fault",
    0x0800: "MTB Active",
    0x0400: "Inverted",
    0x0200: "TOB enabled",
    0x0100: "Angle Match",
    0x0080: "Drive Enable Fault",
    0x0040: "MDH Mode Active",
    0x0020: "Velocity Direction",
    0x0010: "Reserved 4",
    0x0008: "Vector Control",
    0x0004: "sineMode",
    0x0002: "Enhanced Trap Mode",
    0x0001: "Trap Mode"
}

# Define Status Word 7 Values
statusWord7 = {
    0x8000: "TS WAIT",
    0x4000: "Traverse Lower Dwell in Progress",
    0x2000: "Traverse Direction, 0:FWD, 1:Rev",
    0x1000: "TG2 Dwell (or higher Dwell in progress)",
    0x0800: "TG2 Decel/Decend",
    0x0400: "TG2 Slewing",
    0x0200: "TG2 Accel/Ascend",
    0x0100: "TG2 in Progress",
    0x0010: "TG1 Reserved or Dwell",
    0x0008: "TG1 Decel/Descend",
    0x0004: "TG1 Slewing",
    0x0002: "TG1 Accel",
    0x0001: "Tg1 in Progress"
}

# Define Status Word 8 Values
statusWord8 = {
    0x8000: "IP Mode 1",
    0x4000: "IP Mode 0",
    0x2000: "IP User Bit 5",
    0x1000: "IP User Bit 4",
    0x0800: "IP User Bit 3",
    0x0400: "IP User Bit 2",
    0x0200: "IP User Bit 1",
    0x0100: "IP User Bit 0",
    0x0080: "Cam Mode 1",
    0x0040: "Cam Mode 0",
    0x0020: "Cam User Bit 5",
    0x0010: "Cam User Bit 4",
    0x0008: "Cam User Bit 3",
    0x0004: "Cam User Bit 2",
    0x0002: "Cam User Bit 1",
    0x0001: "Cam User Bit 0"
}

# Define Status Word 10 Values
statusWord10 = {
    0x0020: "RxPDO 5 arrived",
    0x0010: "RxPDO 4 arrived",
    0x0008: "RxPDO 3 arrived",
    0x0004: "RxPDO 2 arrived",
    0x0002: "RxPDO 1 arrived",
    0x0001: "Master Enabled"
}
