# RO Controller -
#
# Hardware:  WiPy 3.0;  RO-Controller ROv3_ELPM-v2
# Versions
# 1.0       2022.Mar.16 - Initial
#           2022.Mar.21 - STP08 Control functions finished.

# ==========================================================================
# ==========================================================================
# STP08 - Support Functions
# ==========================================================================
# Include everthing below these lines to "Main Routine"
# [Do not include - Main Routine.  Included here as example only.]
# ==========================================================================
# ==========================================================================

import pycom    # import the entire pycom library.
import time   # import the entire 'time' library.
# import machine # import the entire 'machine' library

#import tok.py      # Import 'constants' or 'tokens' for RO Controller.  <<< Optional - use tok.py if desired.

# Import only some functions from the following libraries.
from time import sleep   # import just the 'sleep' function from the 'time' library.
from time import sleep_ms
from time import sleep_us
from machine import Pin  # import just the 'Pin' function from the 'machine' library.

# ==========================================================================
# ==========================================================================
# INITIALIZATION STUFF
# ==========================================================================
pycom.heartbeat(False)  # Turns the heartbeat function off / WiPy 3.0 Module.

# ==========================================================================
# ==========================================================================
# INDICATOR CONTROL FUNCTIONS
# ==========================================================================

# Read / Write the STP08 Inidicator Control Chip.
# Only on/off control is possible.
# When a channel is 'on', 10mA is delivered to the indicator.
#
# The STP08 is controlled via a 3 wire serial port.
# Pins are as on the WiPy 3.0 Module.
#    LE: pin 23 - GPIO 26, "P21";
#   CLK: pin 22 - GPIO 33, "P20";
#   SDI: pin 21 - GPIO 32, "P19";
#
# Shift MSBit (OUT7 / Indicator 8) first into the STP08.
# LE: Low - shift data in without affecting output.
#     Low to High edge: latch bits to output register (update 'indictors' status).
# CLK: Rising edge shifts SDI bit into the STP08 (LE state doesn't matter).
#
# A '1' in a bit position turns the corresponding indicator on.
# The STP08 chip powers on with all indicators off.
#
# The STP08 is 1 byte wide.
#       Bit         Function
#       0 (LSB)     D20: Red status LED
#       1           D21: Green status LED
#       2           D22
#       3           D23
#       4           D24
#       5           D25
#       6           D26
#       7 (MSB)     D27   -  [most significant bit]


# -------------------------------------------------------------------------
# Low level STP08 Driver - not to be directly called by the user.
# 'data': 8 bit value to output to the STP08.
# !!!!!  NOTE: to make this faster, use the Python SPI function!!!
#              or create own 'ser_delay()' function...
stp_le  = Pin("P21",mode=Pin.OUT, value=0)
stp_clk = Pin("P20",mode=Pin.OUT, value=0)
stp_sdi = Pin("P19",mode=Pin.OUT, value=0)

# Note: 'time.sleep_us(1) is supposed to give a near 1uS delay.
#       However, actually measure 10uS.  (2022.Mar.21 - TL).
#       [Also - writing own delay routine - shortest delay could get was about 25uS]
def indicatorsUpdate( data_in ):
    # Make sure LE and CLK are at their idle level.
    stp_le(0)   # Make sure LE is low.
    stp_clk(0)  # Make sure CLK is low.

    indicator_o = data_in

    # Output the upper 7 bits of the byte.
    i=7
    while i > 0:
        bity = indicator_o & 0x80
        indicator_o = indicator_o << 1
        if (bity != 0): stp_sdi(1)
        else: stp_sdi(0)
        time.sleep_us(1)    # Actually only want a 0.1uS delay here...
        stp_clk(1)
        time.sleep_us(1)    # Actually only want a 0.1uS delay here...
        stp_clk(0)
        i = i - 1

    # Now output the last bit.
    bity = indicator_o & 0x80
    if (bity != 0): stp_sdi(1)
    else: stp_sdi(0)
    time.sleep_us(1)    # Actually only want a 0.1uS delay here...
    stp_clk(1)
    time.sleep_us(1)    # Actually only want a 0.1uS delay here...
    stp_clk(0)
    stp_le(1)
    time.sleep_us(1)    # Actually only want a 0.1uS delay here...
    stp_le(0)
    return
# -------------------------------------------------------------------------

# User Functions:
# These next functions are to be called whenever an indicator value
# needs to be changed.

# Variable to keep track of the state of the indicators.
# A '0' forces the indicator off.
# A '1' turns the indicator on - supplies it with 10mA.
l_indicators = 0x00   # Default value - all indicators off.

# Turn all indicators off.
def indicatorsClear():
    global l_indicators
    l_indicators = 0x00
    indicatorsUpdate( l_indicators )
    return

# To turn an indicator on:
# Example call:   indicatorOn( INDICATE_3 )
def indicatorOff( indict ):
    global l_indicators
    mask = 1 << indict
    l_indicators &= (~mask)
    indicatorsUpdate( l_indicators )
    return

# To turn an indicator off:
# Example call:   indicatorOff( INDICATE_3 )
def indicatorOn( indict ):
    global l_indicators
    mask = 1 << indict
    l_indicators |= mask
    indicatorsUpdate( l_indicators )
    return


# ==========================================================================
# ==========================================================================
# ==========================================================================
# ==========================================================================
# MAIN ROUTINE
# - Code below this line is for example only and should not be included in
#   the final program.
# ==========================================================================
rgbl = 0
while True:
    ind = 0
 #   indicatorOn( INDICATE_1 )
  #  time.sleep_ms(2000)
 #   indicatorOff( INDICATE_1 )
    while ind < 8:
        indicatorOn( ind )
        time.sleep_ms(200)
        indicatorOff( ind )
        ind = ind + 1
        if (rgbl == 0):
            rgbl = 1
            pycom.rgbled(0x1F0000)
        elif (rgbl == 1):
            rgbl = 0
            pycom.rgbled(0x001F00)
#        elif (rgbl == 2):
#            rgbl = 0
#            pycom.rgbled(0x00001F)

    time.sleep_ms(50)
    pycom.rgbled(0x00001F)
    time.sleep_ms(500)

