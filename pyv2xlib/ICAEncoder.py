from .utils import load_v2xlib
from binascii import hexlify, unhexlify
v2xlib = load_v2xlib()

def ica_encoder(msgCnt=None,
                sourceID = None,
                iCATimeStamp = None, # Optional

                partOne_exists = False,
                # if partOne_exists is True, following inputs are mandatory
                # If partOne_ecists is False, follwoing inputs should be empty
                partOne_msgCnt = None, 
                partOne_sourceID = None, 
                partOne_secMark = None, 
                partOne_lat = None, 
                partOne_long = None,
                partOne_elev = None,
                partOnePosAcc_semiMajor = None,
                partOnePosAcc_semiMinor = None,
                partOnePosAcc_orientation = None, 
                partOne_transmission = None, 
                partOne_speed = None,
                partOne_heading = None, 
                partOne_angle = None, 
                partOne_accelSet_long = None,
                partOne_accelSet_lat = None,
                partOne_accelSet_vert = None,
                partOne_accelSet_yaw = None, 
                partOne_brakes_wheelBrakes = None,
                partOne_brakes_traction = None,
                partOne_brakes_abs = None,
                partOne_brakes_scs = None,
                partOne_brakes_brakeBoost = None,
                partOne_brakes_auxBrakes = None,
                partOne_size_width = None,
                partOne_size_length = None, 

                path_exists = False,
                # if path is True, variables not commented Optional is mandatory
                # if path is False, following inputs should be empty
                path_initialPosition_exists = False, 
                path_initialPosition_utcTime_year = None, # Optional
                path_initialPosition_utcTime_month = None, # Optional
                path_initialPosition_utcTime_day = None, # Optional
                path_initialPosition_utcTime_hour = None, # Optional
                path_initialPosition_utcTime_minute = None, # Optional
                path_initialPosition_utcTime_second = None, # Optional
                path_initialPosition_utcTime_offset = None, # Optional
                path_initialPosition_long = None, 
                path_initialPosition_lat = None,
                path_initialPosition_elevation = None, # Optional
                path_initialPosition_heading = None, # Optional
                path_initialPosition_speed_transmission = None, # Optional
                path_initialPosition_speed_velocity = None, # Optional
                path_initialPosition_posAccuracy_semiMajor = None, # Optional
                path_initialPosition_posAccuracy_semiMinor = None, # Optional
                path_initialPosition_posAccuracy_orientation = None, # Optional
                path_initialPosition_timeConfidence = None, # Optional
                path_initialPosition_posConfidence_pos = None, # Optional
                path_initialPosition_posConfidence_elevation = None, # Optional
                path_initialPosition_speedConfidence_heading = None, # Optional
                path_initialPosition_speedConfidence_speed = None, # Optional
                path_initialPosition_speedConfidence_throttle = None, # Optional
                path_currGNSSstatus = None, # Optional
                path_crumbData_N = 0, # Optional
                path_crumbData_latOffset = [],
                path_crumbData_lonOffset = [],
                path_crumbData_elevationOffset = [],
                path_crumbData_timeOffset = [],
                path_crumbData_speed = [],   # Optional   
                path_crumbData_posAccuracy_semiMajor = [], # Optional   
                path_crumbData_posAccuracy_semiMinor = [],  # Optional
                path_crumbData_posAccuracy_orientation = [], # Optional
                path_crumbData_heading = [],       # Optional

                # pathPrediction - Optional
                # Either both fields are filled or empty
                pathPrediction_radiusOfCurve=None, 
                pathPrediction_confidence=None, 

                intersectionID_region=None, # Optional
                intersectionID_id=None,

                laneNumber_type=None, 
                laneNumber_value=None, 

                eventFlag_value=None,
                ):
    '''
    This function encodes ICA message.
    ICA - Broadcast to other nearby V2X devices a warning that a vehicle is likely entering
    an intersection without the right of way 
    Can be sourced by both vehicles (self-report) and infrastructure (virtual BSM from sensor data).

    Args:
        msgCnt (int): Message counter. Range: [0, 127]. Mandatory.
        sourceID (str): Source ID of the sending device (vehicle or RSU). Exactly 4 characters. Mandatory.
        iCATimeStamp (int): Number of elapsed minutes of the current year. Range: [0, 527040]. 527040 = unavailable. Optional.

        partOne_exists (bool): True if BSM core data of the offending vehicle is included. Mandatory.

        partOne_msgCnt (int): BSM message counter of the offending vehicle. Range: [0, 127]. Mandatory if partOne_exists.
        partOne_sourceID (str): Temporary ID of the offending vehicle. Exactly 4 characters. Mandatory if partOne_exists.
        partOne_secMark (int): Milliseconds within the current minute when this position was measured. Range: [0, 65535]. Mandatory if partOne_exists.
        partOne_lat (float): Latitude of the offending vehicle. Range: [-90, 90]. Unit: deg. Mandatory if partOne_exists.
        partOne_long (float): Longitude of the offending vehicle. Range: [-179.9999999, 180]. Unit: deg. Mandatory if partOne_exists.
        partOne_elev (float): Elevation of the offending vehicle. Range: [-409.5, 6143.9]. Unit: meter. Mandatory if partOne_exists.
        partOnePosAcc_semiMajor (float): Radius of the semi-major axis of the GPS uncertainty ellipse. Range: [0, 12.7]. 12.75 = unavailable. Unit: meter. Mandatory if partOne_exists.
        partOnePosAcc_semiMinor (float): Radius of the semi-minor axis of the GPS uncertainty ellipse. Range: [0, 12.7]. 12.75 = unavailable. Unit: meter. Mandatory if partOne_exists.
        partOnePosAcc_orientation (float): Orientation angle of the semi-major axis relative to true north. Range: [0, 359.9945078786]. 360 = unavailable. Unit: deg. Mandatory if partOne_exists.
        partOne_transmission (str): Transmission/gear state of the offending vehicle. One of neutral, park, forwardGears, reverseGears, unavailable. Mandatory if partOne_exists.
        partOne_speed (float): Speed of the offending vehicle. Range: [0, 163.8]. 8191 (encoded) = unavailable. Unit: m/s. Mandatory if partOne_exists.
        partOne_heading (float): Direction of travel of the offending vehicle, clockwise from north. Range: [0, 359.9875]. 28800 (encoded) = unavailable. Unit: deg. Mandatory if partOne_exists.
        partOne_angle (float): Steering wheel angle of the offending vehicle. Positive = right, negative = left. Range: [-189, 189]. 127 (encoded) = unavailable. Unit: deg. Mandatory if partOne_exists.
        partOne_accelSet_long (float): Longitudinal acceleration (forward/backward) of the offending vehicle. Positive = accelerating, negative = braking. Range: [-20, 20]. 2001 (encoded) = unavailable. Unit: m/s^2. Mandatory if partOne_exists.
        partOne_accelSet_lat (float): Lateral acceleration (left/right) of the offending vehicle. Range: [-20, 20]. 2001 (encoded) = unavailable. Unit: m/s^2. Mandatory if partOne_exists.
        partOne_accelSet_vert (float): Vertical acceleration of the offending vehicle. Range: [-24.72, 24.92]. -127 (encoded) = unavailable. Unit: m/s^2. Mandatory if partOne_exists.
        partOne_accelSet_yaw (float): Yaw rate (rotation around vertical axis) of the offending vehicle. Positive = right turn. Range: [-327.67, 327.67]. Unit: deg/s. Mandatory if partOne_exists.
        partOne_brakes_wheelBrakes (int): Bitmask indicating which wheels have brakes applied. bit0=unavailable, bit1=leftFront, bit2=leftRear, bit3=rightFront, bit4=rightRear. Range: [0, 31]. Mandatory if partOne_exists.
        partOne_brakes_traction (str): Traction control system state. One of unavailable, off, on, engaged. Mandatory if partOne_exists.
        partOne_brakes_abs (str): Anti-lock brake system state. One of unavailable, off, on, engaged. Mandatory if partOne_exists.
        partOne_brakes_scs (str): Stability control system state. One of unavailable, off, on, engaged. Mandatory if partOne_exists.
        partOne_brakes_brakeBoost (str): Brake boost assist state. One of unavailable, off, on. Mandatory if partOne_exists.
        partOne_brakes_auxBrakes (str): Auxiliary brake system state. One of unavailable, off, on. Mandatory if partOne_exists.
        partOne_size_width (int): Width of the offending vehicle. Range: [0, 1023]. Unit: cm. Mandatory if partOne_exists.
        partOne_size_length (int): Length of the offending vehicle. Range: [0, 4095]. Unit: cm. Mandatory if partOne_exists.

        path_exists (bool): True if path history of the offending vehicle is included. Mandatory.

        path_initialPosition_exists (bool): True if the anchor position for path history offsets is included. Optional within path.
        path_initialPosition_utcTime_year (int): Year of the anchor position timestamp. Range: [0, 4095]. Optional.
        path_initialPosition_utcTime_month (int): Month of the anchor position timestamp. Range: [0, 12]. Optional.
        path_initialPosition_utcTime_day (int): Day of the anchor position timestamp. Range: [0, 31]. Optional.
        path_initialPosition_utcTime_hour (int): Hour of the anchor position timestamp. Range: [0, 31]. Unit: hour. Optional.
        path_initialPosition_utcTime_minute (int): Minute of the anchor position timestamp. Range: [0, 60]. Unit: minute. Optional.
        path_initialPosition_utcTime_second (float): Second of the anchor position timestamp. Range: [0, 65.535]. Unit: second. Optional.
        path_initialPosition_utcTime_offset (int): UTC offset of the anchor position timestamp. Range: [-840, 840]. Unit: minute. Optional.
        path_initialPosition_long (float): Longitude of the path history anchor position. Range: [-179.9999999, 180]. Unit: deg. Mandatory if path_initialPosition_exists.
        path_initialPosition_lat (float): Latitude of the path history anchor position. Range: [-90, 90]. Unit: deg. Mandatory if path_initialPosition_exists.
        path_initialPosition_elevation (float): Elevation of the path history anchor position. Range: [-409.5, 6143.9]. Unit: meter. Optional.
        path_initialPosition_heading (float): Heading at the anchor position. Range: [0, 359.9875]. Unit: deg. Optional.
        path_initialPosition_speed_transmission (str): Transmission state at the anchor position. One of neutral, park, forwardGears, reverseGears, unavailable. Optional.
        path_initialPosition_speed_velocity (float): Speed at the anchor position. Range: [0, 163.8]. Unit: m/s. Optional.
        path_initialPosition_posAccuracy_semiMajor (float): Semi-major axis of GPS uncertainty ellipse at anchor position. Range: [0, 12.7]. Unit: meter. Optional.
        path_initialPosition_posAccuracy_semiMinor (float): Semi-minor axis of GPS uncertainty ellipse at anchor position. Range: [0, 12.7]. Unit: meter. Optional.
        path_initialPosition_posAccuracy_orientation (float): Orientation of GPS uncertainty ellipse at anchor position. Range: [0, 359.9945078786]. Unit: deg. Optional.
        path_initialPosition_timeConfidence (float): 95% confidence interval for the anchor position timestamp. Range: (0, 100+]. Unit: second. Optional.
        path_initialPosition_posConfidence_pos (float): 95% confidence interval for the anchor horizontal position. Range: (0, 500+]. Unit: meter. Optional.
        path_initialPosition_posConfidence_elevation (float): 95% confidence interval for the anchor elevation. Range: (0, 500+]. Unit: meter. Optional.
        path_initialPosition_speedConfidence_heading (float): 95% confidence interval for heading at anchor. Range: (0, 10+]. Unit: deg. Optional.
        path_initialPosition_speedConfidence_speed (float): 95% confidence interval for speed at anchor. Range: (0, 100+]. Unit: m/s. Optional.
        path_initialPosition_speedConfidence_throttle (float): 95% confidence interval for throttle at anchor. Range: (0, 0.1+]. Unit: percent as fraction. Optional.

        path_currGNSSstatus (int): 8-bit bitmask of GPS receiver health flags at time of recording. bit0=unavailable, bit1=isHealthy, bit2=isMonitored, bit3=baseStationType, bit4=aPDOPofUnder5, bit5=inViewOfUnder5, bit6=localCorrectionsPresent, bit7=networkCorrectionsPresent. Range: [0, 255]. Optional.
        path_crumbData_N (int): Number of path history points (breadcrumbs). Range: [1, 23]. Mandatory if path_exists.
        path_crumbData_latOffset (list): Latitude offset of each crumb from the anchor position. Positive = north. Range: [-0.0131071, 0.0131071]. -131072 (encoded) = unavailable. Unit: deg. Mandatory if path_exists.
        path_crumbData_lonOffset (list): Longitude offset of each crumb from the anchor position. Positive = east. Range: [-0.0131071, 0.0131071]. -131072 (encoded) = unavailable. Unit: deg. Mandatory if path_exists.
        path_crumbData_elevationOffset (list): Elevation offset of each crumb from the anchor position. Range: [-204.7, 204.7]. -2048 (encoded) = unavailable. Unit: meter. Mandatory if path_exists.
        path_crumbData_timeOffset (list): How far back in time each crumb was recorded relative to the anchor. Range: [0.01, 655.34]. 65535 (encoded) = unavailable. Unit: second. Mandatory if path_exists.
        path_crumbData_speed (list): Speed of the vehicle at each crumb point. Range: [0, 163.8]. 8191 (encoded) = unavailable. Unit: m/s. Optional.
        path_crumbData_posAccuracy_semiMajor (list): Semi-major axis of GPS uncertainty ellipse at each crumb. Range: [0, 12.7]. Unit: meter. Optional.
        path_crumbData_posAccuracy_semiMinor (list): Semi-minor axis of GPS uncertainty ellipse at each crumb. Range: [0, 12.7]. Unit: meter. Optional.
        path_crumbData_posAccuracy_orientation (list): Orientation of GPS uncertainty ellipse at each crumb. Range: [0, 359.9945078786]. Unit: deg. Optional.
        path_crumbData_heading (list): Coarse heading at each crumb point. Range: [0, 358.5]. Step size 1.5 deg. 240 (encoded) = unavailable. Unit: deg. Optional.

        pathPrediction_radiusOfCurve (float): Estimated radius of the offending vehicle's predicted turn. Positive = right curve, negative = left curve. 32767 (encoded) = straight path or unavailable. Range: [-3276.7, 3276.7]. Unit: meter. Optional.
        pathPrediction_confidence (float): Confidence in the path prediction. Range: [0, 100]. Unit: percent. Optional.

        intersectionID_region (int): Regional authority ID that assigned the intersection ID. Range: [0, 65535]. Optional.
        intersectionID_id (int): Unique ID of the intersection where the violation occurred within the region. Range: [0, 65535]. Values 0-255 reserved for testing. Mandatory.

        laneNumber_type (str): Whether laneNumber_value refers to an approach or a specific lane. One of approach, lane. Mandatory.
        laneNumber_value (int): Approach ID [0, 15] or Lane ID [0, 255] where the violation occurred. Mandatory.

        eventFlag_value (int): 14-bit bitmask of active vehicle events at time of violation. At least one bit should be set. bit0=eventHazardLights, bit1=eventStopLineViolation, bit2=eventABSactivated, bit3=eventTractionControlLoss, bit4=eventStabilityControlactivated, bit5=eventHazardousMaterials, bit7=eventHardBraking, bit8=eventLightsChanged, bit9=eventWipersChanged, bit10=eventFlatTire, bit11=eventDisabledVehicle, bit12=eventAirBagDeployment, bit13=eventJackKnife. Range: [0, 16383]. Mandatory.

    Returns:
        hex_ica (str): ICA message encoded as a hex string.
    '''
    ica = {}

    if msgCnt is None:
        print('msgCnt is mandatory! Please provide msgCnt. Set to 0.')
        ica['msgCnt'] = 0
    elif not isinstance(msgCnt, int):
        print('msgCnt should be an integer! But', msgCnt, 'is provided. Set to 0.')
        ica['msgCnt'] = 0
    elif msgCnt < 0 or msgCnt > 127:
        print('msgCnt should be in range [0, 127]! But', msgCnt, 'is provided. Set to 0.')
        ica['msgCnt'] = 0
    else:
        ica['msgCnt'] = msgCnt

    if sourceID is None:
        print('sourceID is mandatory! Please provide sourceID. Set to tmp.')
        ica['id'] = b'tmp\x00'
    else:
        encoded  = sourceID.encode('utf-8')
        if len(encoded) != 4:
            print('sourceID must be exactly 4 bytes! But', repr(encoded), 'is provided. Changing it to 4 bytes')
            encoded = encoded[:4].ljust(4, b'\x00')
        ica['id'] = encoded

    if iCATimeStamp is not None:
        if not isinstance(iCATimeStamp, int):
            print('iCATimeStamp should be an integer! But', iCATimeStamp, 'is provided. Remove it.')
        elif iCATimeStamp < 0 or iCATimeStamp > 527040:
            print('iCATimeStamp should be in range [0, 527040]! But', iCATimeStamp, 'is provided. Remove it.')
        else:
            ica['timeStamp'] = iCATimeStamp
    
    if partOne_exists:
        ica['partOne'] = {}
        if partOne_msgCnt is None:
            print('partOne_msgCnt is mandatory! Please provide partOne_msgCnt. Set to 0.')
            ica['partOne']['msgCnt'] = 0
        elif not isinstance(partOne_msgCnt, int):
            print('partOne_msgCnt should be an integer! But', partOne_msgCnt, 'is provided. Set to 0.')
            ica['partOne']['msgCnt'] = 0
        elif partOne_msgCnt < 0 or partOne_msgCnt > 127:
            print('partOne_msgCnt should be in range [0, 127]! But', partOne_msgCnt, 'is provided. Set to 0.')
            ica['partOne']['msgCnt'] = 0
        else:
            ica['partOne']['msgCnt'] = partOne_msgCnt

        if partOne_sourceID is None:
            print('partOne_sourceID is mandatory! Please provide partOne_sourceID. Set to tmp.')
            ica['partOne']['id'] = b'tmp\x00'
        else:
            ica['partOne']['id'] = partOne_sourceID.encode('utf-8')

        if partOne_secMark is None:
            print('partOne_secMark is mandatory! Please provide partOne_secmark. Set to 0.')
            ica['partOne']['secMark'] = 0
        elif not isinstance(partOne_secMark, int):
            print('partOne_secMark should be an integer! But', partOne_secMark, 'is provided. Set to 0.')
            ica['partOne']['secMark'] = 0
        elif partOne_secMark < 0 or partOne_secMark > 65535:
            print('partOne_secMark should be in range [0, 65535]! But', partOne_secMark, 'is provided. Remove it.')
        else:
            ica['partOne']['secMark'] = partOne_secMark
        
        if partOne_lat is None:
            print('partOne_lat is mandatory! Please provide the latitude of information source. Set to 90.0000001.')
            ica['partOne']['lat'] = 900000001
        elif partOne_lat < -90 or partOne_lat > 90:
            print('partOne_lat should be in range [-90, 90] deg! But', partOne_lat, 'is provided. Set to 90.0000001.')
            ica['partOne']['lat'] = 900000001
        else:
            ica['partOne']['lat'] = int(partOne_lat * 10 ** 7)
        if partOne_long is None:
            print('partOne_long is mandatory! Please provide the longitude of information source. Set to 180.0000001.')
            ica['partOne']['long'] = 1800000001
        elif partOne_long < -179.9999999 or partOne_long > 180:
            print('partOne_long should be in range [-179.9999999, 180] deg! But', partOne_long, 'is provided. Set to 180.0000001.')
            ica['partOne']['long'] = 1800000001
        else:
            ica['partOne']['long'] = int(partOne_long * 10 ** 7)
        if partOne_elev is None:
            print('partOne_elev is mandatory! Please provide the longitude of information source. Set to -4096.')
            ica['partOne']['elev'] = -4096
        elif partOne_elev < -409.5 or partOne_elev > 6143.9:
            print('partOne_elev should be in range [-409.5, 6143.9] deg! But', partOne_elev, 'is provided. Set to -409.6.')
            ica['partOne']['elev'] = -4096
        else:
            ica['partOne']['elev'] = int(partOne_elev * 10)

        ica['partOne']['accuracy'] = {}
        if partOnePosAcc_semiMajor is None:
            print('partOnePosAcc_semiMajor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
            ica['partOne']['accuracy']['semiMajor'] = 255
        elif partOnePosAcc_semiMajor < 0:
            print('partOnePosAcc_semiMajor should be in range [0, 12.7] m! But', partOnePosAcc_semiMajor, 'is provided. Set to 12.75.')
            ica['partOne']['accuracy']['semiMajor'] = 255
        elif partOnePosAcc_semiMajor > 12.7:
            print('partOnePosAcc_semiMajor should be in range [0, 12.7] m! But', partOnePosAcc_semiMajor, 'is provided. Set to 12.7.')
            ica['partOne']['accuracy']['semiMajor'] = 254
        else:
            ica['partOne']['accuracy']['semiMajor'] = int(partOnePosAcc_semiMajor * 20)
        if partOnePosAcc_semiMinor is None:
            print('partOnePosAcc_semiMinor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
            ica['partOne']['accuracy']['semiMinor'] = 255
        elif partOnePosAcc_semiMinor < 0:
            print('partOnePosAcc_semiMinor should be in range [0, 12.7] m! But', partOnePosAcc_semiMinor, 'is provided. Set to 12.75.')
            ica['partOne']['accuracy']['semiMinor'] = 255
        elif partOnePosAcc_semiMinor > 12.7:
            print('partOnePosAcc_semiMinor should be in range [0, 12.7] m! But', partOnePosAcc_semiMinor, 'is provided. Set to 12.7.')
            ica['partOne']['accuracy']['semiMinor'] = 254
        else:
            ica['partOne']['accuracy']['semiMinor'] = int(partOnePosAcc_semiMinor * 20)
        if partOnePosAcc_orientation is None:
            print('partOnePosAcc_orientation is mandatory! Please provide the orientation of the angle of the semi-major axis of an ellipsoid. Set to 12.75.')
            ica['partOne']['accuracy']['orientation'] = 65535
        elif partOnePosAcc_orientation < 0 or partOnePosAcc_orientation > 359.9945078786:
            print('partOnePosAcc_orientation should be in range [0, 359.9945078786] deg! But', partOnePosAcc_orientation, 'is provided. Set to 360.')
            ica['partOne']['accuracy']['orientation'] = 65535
        else:
            ica['partOne']['accuracy']['orientation'] = int(partOnePosAcc_orientation / 360 * 65535)

        if partOne_transmission is None:
            print('partOne_transmission is mandatory! Please corresponding tranmission state. Set to unavailable')
            ica['partOne']['transmission'] = 'unavailable'
        elif partOne_transmission in ['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']:
            ica['partOne']['transmission'] = partOne_transmission
        else:
            print('partOne_transmission should be one of neutral, park, forwardGears, reverseGears, unavailable! But', partOne_transmission, 'is provided. Set to unavailable.')
            ica['partOne']['transmission'] = 'unavailable'

        if partOne_speed is None:
            print('partOne_speed is mandatory! Please provide the speed of the object. Set to 8191.')
            ica['partOne']['speed'] = 8191
        elif not isinstance(partOne_speed, (int, float)):
            print('partOne_speed should be a number! But', partOne_speed, 'is provided. Set to 8191.')
            ica['partOne']['speed'] = 8191
        elif partOne_speed < 0 or partOne_speed > 163.8:
            print('partOne_speed should be in range [0, 163.8] m/s! But', partOne_speed, 'is provided. Set to 8191.')
            ica['partOne']['speed'] = 8191
        else:
            ica['partOne']['speed'] = int(partOne_speed * 50)

        if partOne_heading is None:
            print('partOne_heading is mandatory! Please provide the current heading of the sending device. Set to 28800')
            ica['partOne']['heading'] = 28800
        elif not isinstance(partOne_heading, (int, float)):
            print('partOne_heading should be a number! But', partOne_heading, 'is provided. Set to 28800.')
            ica['partOne']['heading'] = 28800
        elif partOne_heading < 0 or partOne_heading > 359.9875:
            print('partOne_heading should be in range [0, 359.9875] deg! But', partOne_heading, 'is provided. Set to 28800.')
            ica['partOne']['heading'] = 28800
        else:
            ica['partOne']['heading'] = int(partOne_heading / 0.0125)
        
        if partOne_angle is None:
            print('partOne_angle is mandatory! Please provide the angle of the driver\'s steering angle. Set to 127')
            ica['partOne']['angle'] = 127
        elif not isinstance(partOne_angle, (int, float)):
            print('partOne_angle should be a number! But', partOne_angle, 'is provided. Set to 127.')
            ica['partOne']['angle'] = 127
        elif partOne_angle < -189 or partOne_angle > 189:
            print('partOne_angle should be in range [-189, 189]! But', partOne_angle, 'is provided. Set to 127.')
            ica['partOne']['angle'] = 127
        else:
            ica['partOne']['angle'] = int(partOne_angle / 1.5)

        ica['partOne']['accelSet'] = {}
        if partOne_accelSet_long is None:
            print('partOne_accelSet_long is mandatory! Please provide partOne_accelSet_long. Set to 2001.')
            ica['partOne']['accelSet']['long'] = 2001
        elif not isinstance(partOne_accelSet_long, (int, float)):
            print('partOne_accelSet_long should be a number! But', partOne_accelSet_long, 'is provided. Set to 2001.')
            ica['partOne']['accelSet']['long'] = 2001
        elif partOne_accelSet_long < -20:
            ica['partOne']['accelSet']['long'] = -2000
        elif partOne_accelSet_long > 20:
            ica['partOne']['accelSet']['long'] = 2000
        else:
            ica['partOne']['accelSet']['long'] = int(partOne_accelSet_long * 100)

        if partOne_accelSet_lat is None:
            print('partOne_accelSet_lat is mandatory! Please provide partOne_accelSet_lat. Set to 2001.')
            ica['partOne']['accelSet']['lat'] = 2001
        elif not isinstance(partOne_accelSet_lat, (int, float)):
            print('partOne_accelSet_lat should be a number! But', partOne_accelSet_lat, 'is provided. Set to 2001.')
            ica['partOne']['accelSet']['lat'] = 2001
        elif partOne_accelSet_lat < -20:
            ica['partOne']['accelSet']['lat'] = -2000
        elif partOne_accelSet_lat > 20:
            ica['partOne']['accelSet']['lat'] = 2000
        else:
            ica['partOne']['accelSet']['lat'] = int(partOne_accelSet_lat * 100)

        if partOne_accelSet_vert is None:
            print('partOne_accelSet_vert is mandatory! Please provide partOne_accelSet_vert. Set to -127.')
            ica['partOne']['accelSet']['vert'] = -127
        elif not isinstance(partOne_accelSet_vert, (int, float)):
            print('partOne_accelSet_vert should be a number! But', partOne_accelSet_vert, 'is provided. Set to -127.')
            ica['partOne']['accelSet']['vert'] = -127
        elif partOne_accelSet_vert <= -2.52 * 9.80665:
            ica['partOne']['accelSet']['vert'] = -126
        elif partOne_accelSet_vert >= 2.54 * 9.80665:
            ica['partOne']['accelSet']['vert'] = 127
        else:
            ica['partOne']['accelSet']['vert'] = int(partOne_accelSet_vert / 9.80665 * 50)

        if partOne_accelSet_yaw is None:
            print('partOne_accelSet_yaw is mandatory! Please provide partOne_accelSet_yaw. Set to 0.')
            ica['partOne']['accelSet']['yaw'] = 0
        elif not isinstance(partOne_accelSet_yaw, (int, float)):
            print('partOne_accelSet_yaw should be a number! But', partOne_accelSet_yaw, 'is provided. Set to 0.')
            ica['partOne']['accelSet']['yaw'] = 0
        elif partOne_accelSet_yaw < -327.67:
            ica['partOne']['accelSet']['yaw'] = -32767
        elif partOne_accelSet_yaw > 327.67:
            ica['partOne']['accelSet']['yaw'] = 32767
        else:
            ica['partOne']['accelSet']['yaw'] = int(partOne_accelSet_yaw * 100)

        ica['partOne']['brakes'] = {}
        if partOne_brakes_wheelBrakes is None:
            print('partOne_brakes_wheelBrakes is mandatory! Please provide partOne_brakes_wheelBrakes. Set to unavailable.')
            ica['partOne']['brakes']['wheelBrakes'] = (1, 5)
        elif not isinstance(partOne_brakes_wheelBrakes, int):
            print('partOne_brakes_wheelBrakes should be an integer! But', partOne_brakes_wheelBrakes, 'is provided. Set to unavailable.')
            ica['partOne']['brakes']['wheelBrakes'] = (1, 5)
        elif partOne_brakes_wheelBrakes < 0 or partOne_brakes_wheelBrakes > 31:
            print('partOne_brakes_wheelBrakes should be in range [0, 31]! But', partOne_brakes_wheelBrakes, 'is provided. Set to unavailable.')
            ica['partOne']['brakes']['wheelBrakes'] = (1, 5)
        else:
            ica['partOne']['brakes']['wheelBrakes'] = (partOne_brakes_wheelBrakes, 5)

        if partOne_brakes_traction is None:
            print('partOne_brakes_traction is mandatory! Please provide partOne_brakes_traction. Set to unavailable.')
            ica['partOne']['brakes']['traction'] = 'unavailable'
        elif partOne_brakes_traction in ['unavailable', 'off', 'on', 'engaged']:
            ica['partOne']['brakes']['traction'] = partOne_brakes_traction
        else:
            print('partOne_brakes_traction should be one of unavailable, off, on, or engaged! But', partOne_brakes_traction, 'is provided. Set to unavailable.')
            ica['partOne']['brakes']['traction'] = 'unavailable'

        if partOne_brakes_abs is None:
            print('partOne_brakes_abs is mandatory! Please provide partOne_brakes_abs. Set to unavailable.')
            ica['partOne']['brakes']['abs'] = 'unavailable'
        elif partOne_brakes_abs in ['unavailable', 'off', 'on', 'engaged']:
            ica['partOne']['brakes']['abs'] = partOne_brakes_abs
        else:
            print('partOne_brakes_abs should be one of unavailable, off, on, or engaged! But', partOne_brakes_abs, 'is provided. Set to unavailable.')
            ica['partOne']['brakes']['abs'] = 'unavailable'

        if partOne_brakes_scs is None:
            print('partOne_brakes_scs is mandatory! Please provide partOne_brakes_scs. Set to unavailable.')
            ica['partOne']['brakes']['scs'] = 'unavailable'
        elif partOne_brakes_scs in ['unavailable', 'off', 'on', 'engaged']:
            ica['partOne']['brakes']['scs'] = partOne_brakes_scs
        else:
            print('partOne_brakes_scs should be one of unavailable, off, on, or engaged! But', partOne_brakes_scs, 'is provided. Set to unavailable.')
            ica['partOne']['brakes']['scs'] = 'unavailable'

        if partOne_brakes_brakeBoost is None:
            print('partOne_brakes_brakeBoost is mandatory! Please provide partOne_brakes_brakeBoost. Set to unavailable.')
            ica['partOne']['brakes']['brakeBoost'] = 'unavailable'
        elif partOne_brakes_brakeBoost in ['unavailable', 'off', 'on']:
            ica['partOne']['brakes']['brakeBoost'] = partOne_brakes_brakeBoost
        else:
            print('partOne_brakes_brakeBoost should be one of unavailable, off, or on! But', partOne_brakes_brakeBoost, 'is provided. Set to unavailable.')
            ica['partOne']['brakes']['brakeBoost'] = 'unavailable'

        if partOne_brakes_auxBrakes is None:
            print('partOne_brakes_auxBrakes is mandatory! Please provide partOne_brakes_auxBrakes. Set to unavailable.')
            ica['partOne']['brakes']['auxBrakes'] = 'unavailable'
        elif partOne_brakes_auxBrakes in ['unavailable', 'off', 'on']:
            ica['partOne']['brakes']['auxBrakes'] = partOne_brakes_auxBrakes
        else:
            print('partOne_brakes_auxBrakes should be one of unavailable, off, or on! But', partOne_brakes_auxBrakes, 'is provided. Set to unavailable.')
            ica['partOne']['brakes']['auxBrakes'] = 'unavailable'

        ica['partOne']['size'] = {}
        if partOne_size_length is None:
            print('partOne_size_length is mandatory! Please provide partOne_size_length. Set to 0')
            ica['partOne']['size']['length'] = 0
        elif not isinstance(partOne_size_length, int):
            print('partOne_size_length should be an integer! But', partOne_size_length, 'is provided. Set to 0')
            ica['partOne']['size']['length'] = 0
        elif partOne_size_length < 0 or partOne_size_length > 4095:
            print('partOne_size_length should be in a range [0, 4095]! But', partOne_size_length, 'provided. Set to 0')
            ica['partOne']['size']['length'] = 0
        else:
            ica['partOne']['size']['length'] = partOne_size_length
        if partOne_size_width is None:
            print('partOne_size_width is mandatory! Please provide partOne_size_width. Set to 0')
            ica['partOne']['size']['width'] = 0
        elif not isinstance(partOne_size_width, int):
            print('partOne_size_width should be an integer! But', partOne_size_width, 'is provided. Set to 0')
            ica['partOne']['size']['width'] = 0
        elif partOne_size_width < 0 or partOne_size_width > 1023:
            print('partOne_size_width should be in a range [0, 1023]! But', partOne_size_width, 'provided. Set to 0')
            ica['partOne']['size']['width'] = 0
        else:
            ica['partOne']['size']['width'] = partOne_size_width
    else:
        print('partOne BSM Core data is not provided.')

    if path_exists:
        ica['path'] = {}
        if path_initialPosition_exists:
            ica['path']['initialPosition'] = {}
            utcTime = {}
            if path_initialPosition_utcTime_year is not None:
                if not isinstance(path_initialPosition_utcTime_year, int):
                    print('path_initialPosition_utcTime_year should be an integer! But', path_initialPosition_utcTime_year, 'is provided. Remove it.')
                elif path_initialPosition_utcTime_year < 0 or path_initialPosition_utcTime_year > 4095:
                    print('path_initialPosition_utcTime_year should be in range [0, 4095]! But', path_initialPosition_utcTime_year, 'is provided. Remove it.')
                else:
                    utcTime['year'] = path_initialPosition_utcTime_year
            if path_initialPosition_utcTime_month is not None:
                if not isinstance(path_initialPosition_utcTime_month, int):
                    print('path_initialPosition_utcTime_month should be an integer! But', path_initialPosition_utcTime_month, 'is provided. Remove it.')
                elif path_initialPosition_utcTime_month < 0 or path_initialPosition_utcTime_month > 12:
                    print('path_initialPosition_utcTime_month should be in range [0, 12]! But', path_initialPosition_utcTime_month, 'is provided. Remove it.')
                else:
                    utcTime['month'] = path_initialPosition_utcTime_month
            if path_initialPosition_utcTime_day is not None:
                if not isinstance(path_initialPosition_utcTime_day, int):
                    print('path_initialPosition_utcTime_day should be an integer! But', path_initialPosition_utcTime_day, 'is provided. Remove it.')
                elif path_initialPosition_utcTime_day < 0 or path_initialPosition_utcTime_day > 31:
                    print('path_initialPosition_utcTime_day should be in range [0, 31]! But', path_initialPosition_utcTime_day, 'is provided. Remove it.')
                else:
                    utcTime['day'] = path_initialPosition_utcTime_day
            if path_initialPosition_utcTime_hour is not None:
                if not isinstance(path_initialPosition_utcTime_hour, int):
                    print('path_initialPosition_utcTime_hour should be an integer! But', path_initialPosition_utcTime_hour, 'is provided. Remove it.')
                elif path_initialPosition_utcTime_hour < 0 or path_initialPosition_utcTime_hour > 31:
                    print('path_initialPosition_utcTime_hour should be in range [0, 31] h! But', path_initialPosition_utcTime_hour, 'is provided. Remove it.')
                else:
                    utcTime['hour'] = path_initialPosition_utcTime_hour
            if path_initialPosition_utcTime_minute is not None:
                if not isinstance(path_initialPosition_utcTime_minute, int):
                    print('path_initialPosition_utcTime_minute should be an integer! But', path_initialPosition_utcTime_minute, 'is provided. Remove it.')
                elif path_initialPosition_utcTime_minute < 0 or path_initialPosition_utcTime_minute > 60:
                    print('path_initialPosition_utcTime_minute should be in range [0, 60] min! But', path_initialPosition_utcTime_minute, 'is provided. Remove it.')
                else:
                    utcTime['minute'] = path_initialPosition_utcTime_minute
            if path_initialPosition_utcTime_second is not None:
                if path_initialPosition_utcTime_second < 0 or path_initialPosition_utcTime_second > 65.535:
                    print('path_initialPosition_utcTime_second should be in range [0, 65.535] s! But', path_initialPosition_utcTime_second, 'is provided. Remove it.')
                else:
                    utcTime['second'] = int(path_initialPosition_utcTime_second * 10**3)
            if path_initialPosition_utcTime_offset is not None:
                if not isinstance(path_initialPosition_utcTime_offset, int):
                    print('path_initialPosition_utcTime_offset should be an integer! But', path_initialPosition_utcTime_offset, 'is provided. Remove it.')
                elif path_initialPosition_utcTime_offset < -840 or path_initialPosition_utcTime_offset > 840:
                    print('path_initialPosition_utcTime_offset should be in range [-840, 840] min! But', path_initialPosition_utcTime_offset, 'is provided. Remove it.')
                else:
                    utcTime['offset'] = path_initialPosition_utcTime_offset
            if utcTime:
                ica['path']['initialPosition']['utcTime'] = utcTime
        
            if path_initialPosition_long is None:
                print('path_initialPosition_long is mandatory if initialPosition is included! Set to 180.0000001.')
                ica['path']['initialPosition']['long'] = 1800000001
            elif path_initialPosition_long < -179.9999999 or path_initialPosition_long > 180:
                print('path_initialPosition_long should be in range [-179.9999999, 180] deg! But', path_initialPosition_long, 'is provided. Set to 180.0000001.')
                ica['path']['initialPosition']['long'] = 1800000001
            else:
                ica['path']['initialPosition']['long'] = int(path_initialPosition_long * 10 ** 7)

            if path_initialPosition_lat is None:
                print('path_initialPosition_lat is mandatory if initialPosition is included! Set to 90.0000001.')
                ica['path']['initialPosition']['lat'] = 900000001
            elif path_initialPosition_lat < -90 or path_initialPosition_lat > 90:
                print('path_initialPosition_lat should be in range [-90, 90] deg! But', path_initialPosition_lat, 'is provided. Set to 90.0000001.')
                ica['path']['initialPosition']['lat'] = 900000001
            else:
                ica['path']['initialPosition']['lat'] = int(path_initialPosition_lat * 10 ** 7)

            if path_initialPosition_elevation is not None:
                if path_initialPosition_elevation < -409.5 or path_initialPosition_elevation > 6143.9:
                    print('path_initialPosition_elevation should be in range [-409.5, 6143.9] m! But', path_initialPosition_elevation, 'is provided. Remove it.')
                    ica['path']['initialPosition']['elevation'] = -4096
                else:
                    ica['path']['initialPosition']['elevation'] = int(path_initialPosition_elevation * 10)

            if path_initialPosition_heading is not None:
                if path_initialPosition_heading < 0 or path_initialPosition_heading > 359.9875:
                    print('path_initialPosition_heading should be in range [0, 359.9875] deg! But', path_initialPosition_heading, 'is provided. Remove it.')
                else:
                    ica['path']['initialPosition']['heading'] = int(path_initialPosition_heading / 0.0125)

            if path_initialPosition_speed_transmission is not None or path_initialPosition_speed_velocity is not None:
                ica['path']['initialPosition']['speed'] = {}
                if path_initialPosition_speed_transmission is None:
                    print('path_initialPosition_speed_transmission is mandatory! Please provide. Set to unvailable.')
                    ica['path']['initialPosition']['speed']['transmisson'] = 'unavailable'
                elif path_initialPosition_speed_transmission in ['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']:
                    ica['path']['initialPosition']['speed']['transmisson'] = path_initialPosition_speed_transmission
                else:
                    print('path_initialPosition_speed_transmission should be one of neutral, park, forwardGears, reverseGears, or unavailable! But', path_initialPosition_speed_transmission, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['speed']['transmisson'] = 'unavailable'

                if path_initialPosition_speed_velocity is None:
                    print('path_initialPosition_speed_velocity is mandatory! Please provide the speed. Set to unvailable.')
                    ica['path']['initialPosition']['speed']['speed'] = 8191
                elif not isinstance(path_initialPosition_speed_velocity, (int, float)):
                    print('path_initialPosition_speed_velocity should be a number! But', path_initialPosition_speed_velocity, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['speed']['speed'] = 8191
                elif path_initialPosition_speed_velocity < 0 or path_initialPosition_speed_velocity > 163.8:
                    print('path_initialPosition_speed_velocity should be in range [0, 163.8] m/s! But', path_initialPosition_speed_velocity, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['speed']['speed'] = 8191
                else:
                    ica['path']['initialPosition']['speed']['speed'] = int(path_initialPosition_speed_velocity * 50)
            
            if path_initialPosition_posAccuracy_semiMinor is not None or path_initialPosition_posAccuracy_semiMajor is not None or path_initialPosition_posAccuracy_orientation is not None:
                ica['path']['initialPosition']['posAccuracy'] = {}
                if path_initialPosition_posAccuracy_semiMajor is None:
                    print('path_initialPosition_posAccuracy_semiMajor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
                    ica['path']['initialPosition']['posAccuracy']['semiMajor'] = 255
                elif path_initialPosition_posAccuracy_semiMajor < 0:
                    print('path_initialPosition_posAccuracy_semiMajor should be in range [0, 12.7] m! But', path_initialPosition_posAccuracy_semiMajor, 'is provided. Set to 12.75.')
                    ica['path']['initialPosition']['posAccuracy']['semiMajor'] = 255
                elif path_initialPosition_posAccuracy_semiMajor > 12.7:
                    print('path_initialPosition_posAccuracy_semiMajor should be in range [0, 12.7] m! But', path_initialPosition_posAccuracy_semiMajor, 'is provided. Set to 12.7.')
                    ica['path']['initialPosition']['posAccuracy']['semiMajor'] = 254
                else:
                    ica['path']['initialPosition']['posAccuracy']['semiMajor'] = int(path_initialPosition_posAccuracy_semiMajor * 20)
                if path_initialPosition_posAccuracy_semiMinor is None:
                    print('path_initialPosition_posAccuracy_semiMinor is mandatory! Please provide the radius of the semi-minor axis of an ellipsoid. Set to 12.75.')
                    ica['path']['initialPosition']['posAccuracy']['semiMinor'] = 255
                elif path_initialPosition_posAccuracy_semiMinor < 0:
                    print('path_initialPosition_posAccuracy_semiMinor should be in range [0, 12.7] m! But', path_initialPosition_posAccuracy_semiMinor, 'is provided. Set to 12.75.')
                    ica['path']['initialPosition']['posAccuracy']['semiMinor'] = 255
                elif path_initialPosition_posAccuracy_semiMinor > 12.7:
                    print('path_initialPosition_posAccuracy_semiMinor should be in range [0, 12.7] m! But', path_initialPosition_posAccuracy_semiMinor, 'is provided. Set to 12.7.')
                    ica['path']['initialPosition']['posAccuracy']['semiMinor'] = 254
                else:
                    ica['path']['initialPosition']['posAccuracy']['semiMinor'] = int(path_initialPosition_posAccuracy_semiMinor * 20)
                if path_initialPosition_posAccuracy_orientation is None:
                    print('path_initialPosition_posAccuracy_orientation is mandatory! Please provide the orientation of the angle of the semi-major axis of an ellipsoid. Set to 360.')
                    ica['path']['initialPosition']['posAccuracy']['orientation'] = 65535
                elif path_initialPosition_posAccuracy_orientation < 0 or path_initialPosition_posAccuracy_orientation > 359.9945078786:
                    print('path_initialPosition_posAccuracy_orientation should be in range [0, 359.9945078786] deg! But', path_initialPosition_posAccuracy_orientation, 'is provided. Set to 360.')
                    ica['path']['initialPosition']['posAccuracy']['orientation'] = 65535
                else:
                    ica['path']['initialPosition']['posAccuracy']['orientation'] = int(path_initialPosition_posAccuracy_orientation / 360 * 65535)

            if path_initialPosition_timeConfidence is not None:
                if path_initialPosition_timeConfidence <= 0:
                    print('path_initialPosition_timeConfidence should be greater than 0 s! But', path_initialPosition_timeConfidence, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['timeConfidence'] = 'unavailable'
                elif 0 < path_initialPosition_timeConfidence <= 1e-11:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-01'
                elif 1e-11 < path_initialPosition_timeConfidence <= 2e-11:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-02'
                elif 2e-11 < path_initialPosition_timeConfidence <= 5e-11:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-05'
                elif 5e-11 < path_initialPosition_timeConfidence <= 1e-10:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-1'
                elif 1e-10 < path_initialPosition_timeConfidence <= 2e-10:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-2'
                elif 2e-10 < path_initialPosition_timeConfidence <= 5e-10:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-5'
                elif 5e-10 < path_initialPosition_timeConfidence <= 1e-9:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-001'
                elif 1e-9 < path_initialPosition_timeConfidence <= 2e-9:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-002'
                elif 2e-9 < path_initialPosition_timeConfidence <= 5e-9:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-005'
                elif 5e-9 < path_initialPosition_timeConfidence <= 1e-8:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-01'
                elif 1e-8 < path_initialPosition_timeConfidence <= 2e-8:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-02'
                elif 2e-8 < path_initialPosition_timeConfidence <= 5e-8:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-05'
                elif 5e-8 < path_initialPosition_timeConfidence <= 1e-7:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-1'
                elif 1e-7 < path_initialPosition_timeConfidence <= 2e-7:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-2'
                elif 2e-7 < path_initialPosition_timeConfidence <= 5e-7:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-000-5'
                elif 5e-7 < path_initialPosition_timeConfidence <= 1e-6:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-001'
                elif 1e-6 < path_initialPosition_timeConfidence <= 2e-6:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-002'
                elif 2e-6 < path_initialPosition_timeConfidence <= 5e-6:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-005'
                elif 5e-6 < path_initialPosition_timeConfidence <= 1e-5:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-01'
                elif 1e-5 < path_initialPosition_timeConfidence <= 2e-5:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-02'
                elif 2e-5 < path_initialPosition_timeConfidence <= 5e-5:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-05'
                elif 5e-5 < path_initialPosition_timeConfidence <= 1e-4:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-1'
                elif 1e-4 < path_initialPosition_timeConfidence <= 2e-4:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-2'
                elif 2e-4 < path_initialPosition_timeConfidence <= 5e-4:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-000-5'
                elif 5e-4 < path_initialPosition_timeConfidence <= 1e-3:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-001'
                elif 1e-3 < path_initialPosition_timeConfidence <= 2e-3:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-002'
                elif 2e-3 < path_initialPosition_timeConfidence <= 5e-3:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-005'
                elif 5e-3 < path_initialPosition_timeConfidence <= 1e-2:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-010'
                elif 1e-2 < path_initialPosition_timeConfidence <= 2e-2:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-020'
                elif 2e-2 < path_initialPosition_timeConfidence <= 5e-2:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-050'
                elif 5e-2 < path_initialPosition_timeConfidence <= 1e-1:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-100'
                elif 1e-1 < path_initialPosition_timeConfidence <= 2e-1:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-200'
                elif 2e-1 < path_initialPosition_timeConfidence <= 5e-1:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-000-500'
                elif 5e-1 < path_initialPosition_timeConfidence <= 1:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-001-000'
                elif 1 < path_initialPosition_timeConfidence <= 2:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-002-000'
                elif 2 < path_initialPosition_timeConfidence <= 10:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-010-000'
                elif 10 < path_initialPosition_timeConfidence <= 20:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-020-000'
                elif 20 < path_initialPosition_timeConfidence <= 50:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-050-000'
                elif 50 < path_initialPosition_timeConfidence <= 100:
                    ica['path']['initialPosition']['timeConfidence'] = 'time-100-000'
                elif 100 < path_initialPosition_timeConfidence:
                    ica['path']['initialPosition']['timeConfidence'] = 'unavailable'

            if path_initialPosition_posConfidence_pos is not None or path_initialPosition_posConfidence_elevation is not None:
                ica['path']['initialPosition']['posConfidence'] = {}
                if path_initialPosition_posConfidence_pos is None:
                    print('path_initialPosition_posConfidence_pos is mandatory! Please provide. Set to unavailable')
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'unavailable'
                elif path_initialPosition_posConfidence_pos <= 0:
                    print('path_initialPosition_posConfidence_pos should be greater than 0 m! But', path_initialPosition_posConfidence_pos, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'unavailable'
                elif 0 < path_initialPosition_posConfidence_pos <= 0.01:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a1cm'
                elif 0.01 < path_initialPosition_posConfidence_pos <= 0.02:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a2cm'
                elif 0.02 < path_initialPosition_posConfidence_pos <= 0.05:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a5cm'
                elif 0.05 < path_initialPosition_posConfidence_pos <= 0.1:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a10cm'
                elif 0.1 < path_initialPosition_posConfidence_pos <= 0.2:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a20cm'
                elif 0.2 < path_initialPosition_posConfidence_pos <= 0.5:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a50cm'
                elif 0.5 < path_initialPosition_posConfidence_pos <= 1:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a1m'
                elif 1 < path_initialPosition_posConfidence_pos <= 2:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a2m'
                elif 2 < path_initialPosition_posConfidence_pos <= 5:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a5m'
                elif 5 < path_initialPosition_posConfidence_pos <= 10:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a10m'
                elif 10 < path_initialPosition_posConfidence_pos <= 20:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a20m'
                elif 20 < path_initialPosition_posConfidence_pos <= 50:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a50m'
                elif 50 < path_initialPosition_posConfidence_pos <= 100:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a100m'
                elif 100 < path_initialPosition_posConfidence_pos <= 200:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a200m'
                elif 200 < path_initialPosition_posConfidence_pos <= 500:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'a500m'
                else:
                    ica['path']['initialPosition']['posConfidence']['pos'] = 'unavailable'

                if path_initialPosition_posConfidence_elevation is None:
                    print('path_initialPosition_posConfidence_elevation is mandatory! Please provide. Set to unavailable.')
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'unavailable'
                elif path_initialPosition_posConfidence_elevation <= 0:
                    print('path_initialPosition_posConfidence_elevation should be greater than 0 m! But', path_initialPosition_posConfidence_elevation, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'unavailable'
                elif path_initialPosition_posConfidence_elevation <= 0.01:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-000-01'
                elif path_initialPosition_posConfidence_elevation <= 0.02:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-000-02'
                elif path_initialPosition_posConfidence_elevation <= 0.05:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-000-05'
                elif path_initialPosition_posConfidence_elevation <= 0.10:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-000-10'
                elif path_initialPosition_posConfidence_elevation <= 0.20:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-000-20'
                elif path_initialPosition_posConfidence_elevation <= 0.50:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-000-50'
                elif path_initialPosition_posConfidence_elevation <= 1.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-001-00'
                elif path_initialPosition_posConfidence_elevation <= 2.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-002-00'
                elif path_initialPosition_posConfidence_elevation <= 5.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-005-00'
                elif path_initialPosition_posConfidence_elevation <= 10.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-010-00'
                elif path_initialPosition_posConfidence_elevation <= 20.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-020-00'
                elif path_initialPosition_posConfidence_elevation <= 50.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-050-00'
                elif path_initialPosition_posConfidence_elevation <= 100.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-100-00'
                elif path_initialPosition_posConfidence_elevation <= 200.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-200-00'
                elif path_initialPosition_posConfidence_elevation <= 500.00:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'elev-500-00'
                else:
                    ica['path']['initialPosition']['posConfidence']['elevation'] = 'unavailable'
                
            
            if path_initialPosition_speedConfidence_heading is not None or path_initialPosition_speedConfidence_speed is not None or path_initialPosition_speedConfidence_throttle is not None:
                ica['path']['initialPosition']['speedConfidence'] = {}
                if path_initialPosition_speedConfidence_heading is None:
                    print('path_initialPosition_speedConfidence_heading is mandatory! Please provide. Set to unavailable')
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'unavailable'
                elif path_initialPosition_speedConfidence_heading <= 0:
                    print('path_initialPosition_speedConfidence_heading should be greater than 0 deg! But', path_initialPosition_speedConfidence_heading, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'unavailable'
                elif 0 < path_initialPosition_speedConfidence_heading <= 0.01:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'prec0-01deg'
                elif 0.01 < path_initialPosition_speedConfidence_heading <= 0.0125:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'prec0-0125deg'
                elif 0.0125 < path_initialPosition_speedConfidence_heading <= 0.05:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'prec0-05deg'
                elif 0.05 < path_initialPosition_speedConfidence_heading <= 0.1:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'prec0-1deg'
                elif 0.1 < path_initialPosition_speedConfidence_heading <= 1:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'prec01deg'
                elif 1 < path_initialPosition_speedConfidence_heading <= 5:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'prec05deg'
                elif 5 < path_initialPosition_speedConfidence_heading <= 10:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'prec10deg'
                else:
                    ica['path']['initialPosition']['speedConfidence']['heading'] = 'unavailable'

                if path_initialPosition_speedConfidence_speed is None:
                    print('path_initialPosition_speedConfidence_speed is mandatory! Please provide. Set to unavailable')
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'unavailable'
                elif path_initialPosition_speedConfidence_speed <= 0:
                    print('path_initialPosition_speedConfidence_speed should be greater than 0 m/s! But', path_initialPosition_speedConfidence_speed, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'unavailable'
                elif 0 < path_initialPosition_speedConfidence_speed <= 0.01:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'prec0-01ms'
                elif 0.01 < path_initialPosition_speedConfidence_speed <= 0.05:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'prec0-05ms'
                elif 0.05 < path_initialPosition_speedConfidence_speed <= 0.1:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'prec0-1ms'
                elif 0.1 < path_initialPosition_speedConfidence_speed <= 1:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'prec1ms'
                elif 1 < path_initialPosition_speedConfidence_speed <= 5:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'prec5ms'
                elif 5 < path_initialPosition_speedConfidence_speed <= 10:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'prec10ms'
                elif 10 < path_initialPosition_speedConfidence_speed <= 100:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'prec100ms'
                else:
                    ica['path']['initialPosition']['speedConfidence']['speed'] = 'unavailable'

                if path_initialPosition_speedConfidence_throttle is None:
                    print('path_initialPosition_speedConfidence_throttle is mandatory! Please provide. Set to unavailable')
                    ica['path']['initialPosition']['speedConfidence']['throttle'] = 'unavailable'
                elif path_initialPosition_speedConfidence_throttle <= 0:
                    print('path_initialPosition_speedConfidence_throttle should be greater than 0 m/s! But', path_initialPosition_speedConfidence_throttle, 'is provided. Set to unavailable.')
                    ica['path']['initialPosition']['speedConfidence']['throttle'] = 'unavailable'
                elif 0 < path_initialPosition_speedConfidence_throttle <= 0.005:
                    ica['path']['initialPosition']['speedConfidence']['throttle'] = 'prec0-5percent'
                elif 0.005 < path_initialPosition_speedConfidence_throttle <= 0.01:
                    ica['path']['initialPosition']['speedConfidence']['throttle'] = 'prec1percent'
                elif 0.01 < path_initialPosition_speedConfidence_throttle <= 0.1:
                    ica['path']['initialPosition']['speedConfidence']['throttle'] = 'prec10percent'
                else:
                    ica['path']['initialPosition']['speedConfidence']['throttle'] = 'unavailable'

        if path_currGNSSstatus is not None:
            if not isinstance(path_currGNSSstatus, int):
                print('path_currGNSSstatus should be an integer bitmask! But', path_currGNSSstatus, 'is provided. Remove it.')
            elif path_currGNSSstatus < 0 or path_currGNSSstatus > 255:
                print('path_currGNSSstatus should be in range [0, 255] (8 bits)! But', path_currGNSSstatus, 'is provided. Remove it.')
            else:
                ica['path']['currGNSSstatus'] = (path_currGNSSstatus, 8)

        ica['path']['crumbData'] = []
        if path_crumbData_N < 1 or path_crumbData_N > 23:
            print('path_crumbData_N should be in range [1, 23]! But', path_crumbData_N, 'is provided. Path cannot be encoded without at least 1 crumb point.')
            del ica['path']
        else:
            for i in range(path_crumbData_N):
                crumb = {}

                if len(path_crumbData_latOffset) <= i:
                    print('Expect', path_crumbData_N, 'path_crumbData_latOffset but there are only', len(path_crumbData_latOffset), 'of it!')
                    break
                elif path_crumbData_latOffset[i] is None:
                    print('path_crumbData_latOffset is mandatory! Please provide path_crumbData_latOffset. Set to unavailable.')
                    crumb['latOffset'] = -131072
                elif path_crumbData_latOffset[i] >= 0.0131071:
                    crumb['latOffset'] = 131071
                elif path_crumbData_latOffset[i] <= -0.0131071:
                    crumb['latOffset'] = -131071
                else:
                    crumb['latOffset'] = int(path_crumbData_latOffset[i] * 10**7)

                if len(path_crumbData_lonOffset) <= i:
                    print('Expect', path_crumbData_N, 'path_crumbData_lonOffset but there are only', len(path_crumbData_lonOffset), 'of it!')
                    break
                elif path_crumbData_lonOffset[i] is None:
                    print('path_crumbData_lonOffset is mandatory! Please provide path_crumbData_lonOffset. Set to unavailable.')
                    crumb['lonOffset'] = -131072
                elif path_crumbData_lonOffset[i] >= 0.0131071:
                    crumb['lonOffset'] = 131071
                elif path_crumbData_lonOffset[i] <= -0.0131071:
                    crumb['lonOffset'] = -131071
                else:
                    crumb['lonOffset'] = int(path_crumbData_lonOffset[i] * 10**7)

                if len(path_crumbData_elevationOffset) <= i:
                    print('Expect', path_crumbData_N, 'path_crumbData_elevationOffset but there are only', len(path_crumbData_elevationOffset), 'of it!')
                    break
                elif path_crumbData_elevationOffset[i] is None:
                    print('path_crumbData_elevationOffset is mandatory! Please provide path_crumbData_elevationOffset. Set to unavailable.')
                    crumb['elevationOffset'] = -2048
                elif path_crumbData_elevationOffset[i] >= 204.7:
                    crumb['elevationOffset'] = 2047
                elif path_crumbData_elevationOffset[i] <= -204.7:
                    crumb['elevationOffset'] = -2047
                else:
                    crumb['elevationOffset'] = int(path_crumbData_elevationOffset[i] * 10)

                if len(path_crumbData_timeOffset) <= i:
                    print('Expect', path_crumbData_N, 'path_crumbData_timeOffset but there are only', len(path_crumbData_timeOffset), 'of it!')
                    break
                elif path_crumbData_timeOffset[i] is None:
                    print('path_crumbData_timeOffset is mandatory! Please provide path_crumbData_timeOffset. Set to unavailable.')
                    crumb['timeOffset'] = 65535
                elif path_crumbData_timeOffset[i] >= 655.34:
                    crumb['timeOffset'] = 65534
                elif path_crumbData_timeOffset[i] < 0.01:
                    print('path_crumbData_timeOffset[', i, '] should be >= 0.01s! Set to unavailable.')
                    crumb['timeOffset'] = 65535
                else:
                    crumb['timeOffset'] = int(path_crumbData_timeOffset[i] * 100)

                if len(path_crumbData_speed) > i:
                    if path_crumbData_speed[i] < 0 or path_crumbData_speed[i] > 163.8:
                        print('path_crumbData_speed[', i, '] should be in range [0, 163.8] m/s! Set to unavailable.')
                        crumb['speed'] = 8191
                    else:
                        crumb['speed'] = int(path_crumbData_speed[i] * 50)

                if len(path_crumbData_posAccuracy_semiMajor) > i and len(path_crumbData_posAccuracy_semiMinor) > i and len(path_crumbData_posAccuracy_orientation) > i:
                    crumb['posAccuracy'] = {}
                    sM = path_crumbData_posAccuracy_semiMajor[i]
                    sm = path_crumbData_posAccuracy_semiMinor[i]
                    orient = path_crumbData_posAccuracy_orientation[i]
                    crumb['posAccuracy']['semiMajor'] = 255 if sM is None or sM < 0 else (254 if sM > 12.7 else int(sM * 20))
                    crumb['posAccuracy']['semiMinor'] = 255 if sm is None or sm < 0 else (254 if sm > 12.7 else int(sm * 20))
                    crumb['posAccuracy']['orientation'] = 65535 if orient is None or orient < 0 or orient > 359.9945078786 else int(orient / 360 * 65535)

                if len(path_crumbData_heading) > i:
                    if path_crumbData_heading[i] is None or path_crumbData_heading[i] < 0 or path_crumbData_heading[i] > 358.5:
                        crumb['heading'] = 240
                    else:
                        crumb['heading'] = int(path_crumbData_heading[i] / 1.5)

                ica['path']['crumbData'].append(crumb)

            if len(ica['path']['crumbData']) < 1:
                print('No valid crumb points were built (mismatch occurred before the first entry completed). Path cannot be encoded')
                del ica['path']
    else:
        print('Path history data is not provided.')
    
    if pathPrediction_confidence is not None or pathPrediction_radiusOfCurve is not None:
        ica['pathPrediction'] = {}
        if pathPrediction_radiusOfCurve is None:
            print('pathPrediction_radiusOfCurve is mandatory! Please provide pathPrediction_radiusOfCurve. Set to 32767.')
            ica['pathPrediction']['radiusOfCurve'] = 32767
        elif not isinstance(pathPrediction_radiusOfCurve, (int, float)):
            print('pathPrediction_radisuOfCurve should be a number! But', pathPrediction_radiusOfCurve, 'is provided. Set to 32767.')
            ica['pathPrediction']['radiusOfCurve'] = 32767
        elif pathPrediction_radiusOfCurve >= 3276.7:
            print('pathPrediction_radiusOfCurve should be in range [-3276.7, 3276.7]! But', pathPrediction_radiusOfCurve, 'is provided. Set to 32767.')
            ica['pathPrediction']['radiusOfCurve'] = 32767
        elif pathPrediction_radiusOfCurve <= -3276.7:
            print('pathPrediction_radiusOfCurve should be in range [-3276.7, 3276.7]! But', pathPrediction_radiusOfCurve, 'is provided. Set to -32767.')
            ica['pathPrediction']['radiusOfCurve'] = -32767
        else:
            ica['pathPrediction']['radiusOfCurve'] = int(pathPrediction_radiusOfCurve * 10)

        if pathPrediction_confidence is None:
            print('pathPrediction_confidence is mandatory! Please provide pathPrediction_confidence. Set to 0.')
            ica['pathPrediction']['confidence'] = 0
        elif not isinstance(pathPrediction_confidence, (int, float)):
            print('pathPrediction_confidence should be a number! But', pathPrediction_confidence, 'is provided. Set to 0.')
            ica['pathPrediction']['confidence'] = 0
        elif pathPrediction_confidence < 0:
            print('pathPrediction_confidence should be in range [0, 100]! But', pathPrediction_confidence, 'is provided. Set to 0.')
            ica['pathPrediction']['confidence'] = 0
        elif pathPrediction_confidence > 100:
            print('pathPrediction_confidence should be in range [0, 100]! But', pathPrediction_confidence, 'is provided. Set to 200 (max).')
            ica['pathPrediction']['confidence'] = 200
        else:
            ica['pathPrediction']['confidence'] = int(pathPrediction_confidence * 2)


    ica['intersectionID'] = {}
    if intersectionID_id is None:
        print('intersectionID_id is mandatory! Please provide intersectionID_id. Set to 0.')
        ica['intersectionID']['id'] = 0
    elif not isinstance(intersectionID_id, int):
        print('intersectionID_id should be an integer! But', intersectionID_id, 'is provided. Set to 0.')
        ica['intersectionID']['id'] = 0
    elif intersectionID_id < 0 or intersectionID_id > 65535:
        print('intersectionID_id should be in range [0, 65535]! But', intersectionID_id, 'is provided. Set to 0.')
        ica['intersectionID']['id'] = 0
    else:
        ica['intersectionID']['id'] = intersectionID_id

    if intersectionID_region is not None:
        if not isinstance(intersectionID_region, int):
            print('intersectionID_region should be an integer! But', intersectionID_region, 'is provided. Set to 0.')
            ica['intersectionID']['region'] = 0
        elif intersectionID_region < 0 or intersectionID_region > 65535:
            print('intersectionID_region should be in range [0, 65535]! But', intersectionID_region, 'is provided. Set to 0.')
            ica['intersectionID']['region'] = 0
        else:
            ica['intersectionID']['region'] = intersectionID_region

    if laneNumber_type is None or laneNumber_value is None:
        print('laneNumber is mandatory! Please provide laneNumber_type and laneNumber_value. Set to approach 0.')
        ica['laneNumber'] = ('approach', 0)
    elif laneNumber_type not in ['approach', 'lane']:
        print('laneNumber_type should be one of approach or lane! But', laneNumber_type, 'is provided. Set to approach 0.')
        ica['laneNumber'] = ('approach', 0)
    elif not isinstance(laneNumber_value, int):
        print('laneNumber_value should be an integer! But', laneNumber_value, 'is provided. Set to approach 0.')
        ica['laneNumber'] = ('approach', 0)
    elif laneNumber_type == 'approach':
        if laneNumber_value < 0 or laneNumber_value > 15:
            print('laneNumber_value (approach) should be in range [0, 15]! But', laneNumber_value, 'is provided. Set to 0.')
            ica['laneNumber'] = ('approach', 0)
        else:
            ica['laneNumber'] = ('approach', laneNumber_value)
    else:  
        if laneNumber_value < 0 or laneNumber_value > 255:
            print('laneNumber_value (lane) should be in range [0, 255]! But', laneNumber_value, 'is provided. Set to 0.')
            ica['laneNumber'] = ('lane', 0)
        else:
            ica['laneNumber'] = ('lane', laneNumber_value)

    if eventFlag_value is None:
        print('eventFlag_value is mandatory! Please provide eventFlag_value. Set to 0.')
        ica['eventFlag'] = (0, 14)
    elif not isinstance(eventFlag_value, int):
        print('eventFlag_value should be an integer bitmask! But', eventFlag_value, 'is provided. Set to 0.')
        ica['eventFlag'] = (0, 14)
    elif eventFlag_value < 0 or eventFlag_value > 16383:
        print('eventFlag_value should be in range [0, 16383] (14 bits)! But', eventFlag_value, 'is provided. Set to 0.')
        ica['eventFlag'] = (0, 14)
    else:
        if eventFlag_value == 0:
            print('Warning: eventFlag is 0 (no flags set). Per spec guidance, this field should typically only be present when at least one event flag is active.')
        ica['eventFlag'] = (eventFlag_value, 14)

    header_ica = {
        'messageId' : 23,
        'value' : ("IntersectionCollision", ica)
    }

    header_ica_msg = v2xlib.MessageFrame.MessageFrame
    header_ica_msg.set_val(header_ica)
    hex_ica = hexlify(header_ica_msg.to_uper())

    return hex_ica.decode('utf-8')