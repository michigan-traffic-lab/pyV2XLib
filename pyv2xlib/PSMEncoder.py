from binascii import hexlify, unhexlify
from .utils import load_v2xlib
v2xlib = load_v2xlib()

def psm_encoder(
        basicType = None,
        secMark = None,
        msgCnt = None,
        sourceID = None,
        position_lat = None,
        position_long = None,
        position_elevation = None,
        accuracy_semiMajor = None,
        accuracy_semiMinor = None,
        accuracy_orientation = None, # Optional
        speed = None,
        heading = None,

        # Either all mandatory or all empty
        accelSet_lat = None,
        accelSet_long = None,
        accelSet_vert = None,
        accelSet_yaw = None,

        # if path is True, variables not commented Optional is mandatory
        # if path is False, following inputs should be empty
        pathHistory_exists = False,
        pathHistory_initialPosition_exists = False, 
        pathHistory_initialPosition_utcTime_year = None, # Optional
        pathHistory_initialPosition_utcTime_month = None, # Optional
        pathHistory_initialPosition_utcTime_day = None, # Optional
        pathHistory_initialPosition_utcTime_hour = None, # Optional
        pathHistory_initialPosition_utcTime_minute = None, # Optional
        pathHistory_initialPosition_utcTime_second = None, # Optional
        pathHistory_initialPosition_utcTime_offset = None, # Optional
        pathHistory_initialPosition_long = None, 
        pathHistory_initialPosition_lat = None,
        pathHistory_initialPosition_elevation = None, # Optional
        pathHistory_initialPosition_heading = None, # Optional
        pathHistory_initialPosition_speed_transmission = None, # Optional
        pathHistory_initialPosition_speed_velocity = None, # Optional
        pathHistory_initialPosition_posAccuracy_semiMajor = None, # Optional
        pathHistory_initialPosition_posAccuracy_semiMinor = None, # Optional
        pathHistory_initialPosition_posAccuracy_orientation = None, # Optional
        pathHistory_initialPosition_timeConfidence = None,# Optional
        pathHistory_initialPosition_posConfidence_pos = None,# Optional
        pathHistory_initialPosition_posConfidence_elevation = None, # Optional
        pathHistory_initialPosition_speedConfidence_heading = None, # Optional
        pathHistory_initialPosition_speedConfidence_speed = None, # Optional
        pathHistory_initialPosition_speedConfidence_throttle = None, # Optional
        pathHistory_currGNSSstatus = None,# Optional
        pathHistory_crumbData_N = 0, # Optional
        pathHistory_crumbData_latOffset = [],
        pathHistory_crumbData_lonOffset = [],
        pathHistory_crumbData_elevationOffset = [],
        pathHistory_crumbData_timeOffset = [],
        pathHistory_crumbData_speed = [], # Optional
        pathHistory_crumbData_posAccuracy_semiMajor = [], # Optional
        pathHistory_crumbData_posAccuracy_semiMinor = [], # Optional
        pathHistory_crumbData_posAccuracy_orientation = [], # Optional
        pathHistory_crumbData_heading = [], # Optional

        # pathPrediction - optional
        # Either both is filled or empty
        pathPrediction_radiusOfCurve = None,
        pathPrediction_confidence = None,

        # All the following are optional
        propulsion_type = None,
        propulsion_value = None,
        useState = None,
        crossRequest = None,
        crossState = None,
        clusterSize = None,
        clusterRadius = None,
        eventResponderType = None,
        activityType = None,
        activitySubType = None,
        assistType = None,
        sizing = None,
        attachment = None,
        attachmentRadius = None,
        animalType = None
):
    """
    This function encodes PSM message.

    Args:
        basicType (str): Type of the personal device user. One of unavailable, aPEDESTRIAN, aPEDALCYCLIST, aPUBLICSAFETYWORKER, anANIMAL. Mandatory.
        secMark (int): Milliseconds within the current minute when this position was measured. Range: [0, 65535]. 65535 = unavailable. Mandatory.
        msgCnt (int): Message counter. Range: [0, 127]. Mandatory.
        sourceID (str): Temporary ID of the sending device. Exactly 4 characters. Mandatory.

        position_lat (float): Latitude of the VRU. Range: [-90, 90]. Unit: deg. Mandatory.
        position_long (float): Longitude of the VRU. Range: [-179.9999999, 180]. Unit: deg. Mandatory.
        position_elevation (float): Elevation of the VRU above the WGS-84 ellipsoid. Range: [-409.5, 6143.9]. Unit: meter. Optional.

        accuracy_semiMajor (float): Radius of the semi-major axis of the GPS uncertainty ellipse. Range: [0, 12.7]. 12.75 = unavailable. Unit: meter. Mandatory.
        accuracy_semiMinor (float): Radius of the semi-minor axis of the GPS uncertainty ellipse. Range: [0, 12.7]. 12.75 = unavailable. Unit: meter. Mandatory.
        accuracy_orientation (float): Orientation angle of the semi-major axis relative to true north. Range: [0, 359.9945078786]. 360 = unavailable. Unit: deg. Mandatory.

        speed (float): Speed of the VRU. Range: [0, 163.80]. 8191 (encoded) = unavailable. Unit: m/s. Mandatory.
        heading (float): Direction of travel of the VRU, clockwise from north. Range: [0, 359.9875]. 28800 (encoded) = unavailable. Unit: deg. Mandatory.

        accelSet_long (float): Longitudinal acceleration of the VRU. Positive = forward, negative = braking. Range: [-20, 20]. 2001 (encoded) = unavailable. Unit: m/s^2. Optional.
        accelSet_lat (float): Lateral acceleration of the VRU. Positive = rightward, negative = leftward. Range: [-20, 20]. 2001 (encoded) = unavailable. Unit: m/s^2. Optional.
        accelSet_vert (float): Vertical acceleration of the VRU. Positive = downward (SAE convention). Range: [-24.72, 24.92]. -127 (encoded) = unavailable. Unit: m/s^2. Optional.
        accelSet_yaw (float): Yaw rate of the VRU. Positive = clockwise/right turn. Range: [-327.67, 327.67]. Unit: deg/s. Optional.

        pathHistory_exists (bool): True if path history of the VRU is included. Default False. Optional.
        pathHistory_initialPosition_exists (bool): True if the anchor position for path history offsets is included. Optional within pathHistory.
        pathHistory_initialPosition_utcTime_year (int): Year of the anchor position timestamp. Range: [0, 4095]. Optional.
        pathHistory_initialPosition_utcTime_month (int): Month of the anchor position timestamp. Range: [0, 12]. Optional.
        pathHistory_initialPosition_utcTime_day (int): Day of the anchor position timestamp. Range: [0, 31]. Optional.
        pathHistory_initialPosition_utcTime_hour (int): Hour of the anchor position timestamp. Range: [0, 31]. Unit: hour. Optional.
        pathHistory_initialPosition_utcTime_minute (int): Minute of the anchor position timestamp. Range: [0, 60]. Unit: minute. Optional.
        pathHistory_initialPosition_utcTime_second (float): Second of the anchor position timestamp. Range: [0, 65.535]. Unit: second. Optional.
        pathHistory_initialPosition_utcTime_offset (int): UTC offset of the anchor position timestamp. Range: [-840, 840]. Unit: minute. Optional.
        pathHistory_initialPosition_long (float): Longitude of the path history anchor position. Range: [-179.9999999, 180]. Unit: deg. Mandatory if pathHistory_initialPosition_exists.
        pathHistory_initialPosition_lat (float): Latitude of the path history anchor position. Range: [-90, 90]. Unit: deg. Mandatory if pathHistory_initialPosition_exists.
        pathHistory_initialPosition_elevation (float): Elevation of the anchor position. Range: [-409.5, 6143.9]. Unit: meter. Optional.
        pathHistory_initialPosition_heading (float): Heading at the anchor position. Range: [0, 359.9875]. Unit: deg. Optional.
        pathHistory_initialPosition_speed_transmission (str): Transmission state at the anchor position. One of neutral, park, forwardGears, reverseGears, unavailable. Optional.
        pathHistory_initialPosition_speed_velocity (float): Speed at the anchor position. Range: [0, 163.80]. Unit: m/s. Optional.
        pathHistory_initialPosition_posAccuracy_semiMajor (float): Semi-major axis of GPS uncertainty ellipse at anchor. Range: [0, 12.7]. Unit: meter. Optional.
        pathHistory_initialPosition_posAccuracy_semiMinor (float): Semi-minor axis of GPS uncertainty ellipse at anchor. Range: [0, 12.7]. Unit: meter. Optional.
        pathHistory_initialPosition_posAccuracy_orientation (float): Orientation of GPS uncertainty ellipse at anchor. Range: [0, 359.9945078786]. Unit: deg. Optional.
        pathHistory_initialPosition_timeConfidence (float): 95% confidence interval for the anchor position timestamp. Range: (0, 100+]. Unit: second. Optional.
        pathHistory_initialPosition_posConfidence_pos (float): 95% confidence interval for the anchor horizontal position. Range: (0, 500+]. Unit: meter. Optional.
        pathHistory_initialPosition_posConfidence_elevation (float): 95% confidence interval for the anchor elevation. Range: (0, 500+]. Unit: meter. Optional.
        pathHistory_initialPosition_speedConfidence_heading (float): 95% confidence interval for heading at anchor. Range: (0, 10+]. Unit: deg. Optional.
        pathHistory_initialPosition_speedConfidence_speed (float): 95% confidence interval for speed at anchor. Range: (0, 100+]. Unit: m/s. Optional.
        pathHistory_initialPosition_speedConfidence_throttle (float): 95% confidence interval for throttle at anchor. Range: (0, 0.1+]. Unit: percent as fraction. Optional.
        pathHistory_currGNSSstatus (int): 8-bit bitmask of GPS receiver health flags. bit0=unavailable, bit1=isHealthy, bit2=isMonitored, bit3=baseStationType, bit4=aPDOPofUnder5, bit5=inViewOfUnder5, bit6=localCorrectionsPresent, bit7=networkCorrectionsPresent. Range: [0, 255]. Optional.
        pathHistory_crumbData_N (int): Number of path history breadcrumb points. Range: [1, 23]. Mandatory if pathHistory_exists.
        pathHistory_crumbData_latOffset (list): Latitude offset of each crumb from the anchor. Positive = north. Range: [-0.0131071, 0.0131071]. -131072 (encoded) = unavailable. Unit: deg. Mandatory if pathHistory_exists.
        pathHistory_crumbData_lonOffset (list): Longitude offset of each crumb from the anchor. Positive = east. Range: [-0.0131071, 0.0131071]. -131072 (encoded) = unavailable. Unit: deg. Mandatory if pathHistory_exists.
        pathHistory_crumbData_elevationOffset (list): Elevation offset of each crumb from the anchor. Range: [-204.7, 204.7]. -2048 (encoded) = unavailable. Unit: meter. Mandatory if pathHistory_exists.
        pathHistory_crumbData_timeOffset (list): How far back in time each crumb was recorded from the anchor. Range: [0.01, 655.34]. 65535 (encoded) = unavailable. Unit: second. Mandatory if pathHistory_exists.
        pathHistory_crumbData_speed (list): Speed of the VRU at each crumb point. Range: [0, 163.80]. 8191 (encoded) = unavailable. Unit: m/s. Optional.
        pathHistory_crumbData_posAccuracy_semiMajor (list): Semi-major axis of GPS uncertainty ellipse at each crumb. Range: [0, 12.7]. Unit: meter. Optional.
        pathHistory_crumbData_posAccuracy_semiMinor (list): Semi-minor axis of GPS uncertainty ellipse at each crumb. Range: [0, 12.7]. Unit: meter. Optional.
        pathHistory_crumbData_posAccuracy_orientation (list): Orientation of GPS uncertainty ellipse at each crumb. Range: [0, 359.9945078786]. Unit: deg. Optional.
        pathHistory_crumbData_heading (list): Coarse heading at each crumb point. Range: [0, 358.5]. Step size 1.5 deg. 240 (encoded) = unavailable. Unit: deg. Optional.

        pathPrediction_radiusOfCurve (float): Estimated radius of the VRU's predicted path. Positive = right curve, negative = left curve. 32767 (encoded) = straight/unavailable. Range: [-3276.7, 3276.7]. Unit: meter. Optional.
        pathPrediction_confidence (float): Confidence in the path prediction. Range: [0, 100]. Unit: percent. Optional.

        propulsion_type (str): Type of propulsion method. One of human, animal, motor. Optional.
        propulsion_value (str): Specific propulsion state for the chosen type. Optional.
            If propulsion_type = human: one of unavailable, otherTypes, onFoot, skateboard, pushOrKickScooter, wheelchair.
            If propulsion_type = animal: one of unavailable, otherTypes, animalMounted, animalDrawnCarriage.
            If propulsion_type = motor: one of unavailable, otherTypes, wheelChair, bicycle, scooter, selfBalancingDevice.

        useState (str): Current usage state of the personal device. One of unavailable, other, idle, listeningToAudio, typing, calling, playingGames, reading, viewing. Optional.
        crossRequest (bool): True if the VRU is requesting to cross the road. Optional.
        crossState (bool): True if the VRU is currently crossing the road. Optional.
        clusterSize (str): Size of the VRU cluster. One of unavailable, small, medium, large. Optional.
        clusterRadius (int): Radius of the VRU cluster centered on the reported position. Range: [0, 100]. Unit: meter. Optional.
        eventResponderType (str): Type of emergency/event responder. One of unavailable, towOperator, fireAndEMSWorker, aDOTWorker, lawEnforcement, hazmatResponder, animalControlWorker, otherPersonnel. Optional.
        activityType (int): 6-bit bitmask describing the type of road worker activity. bit0=unavailable, bit1=workingOnRoad, bit2=settingUpClosures, bit3=respondingToEvents, bit4=directingTraffic, bit5=otherActivities. Range: [0, 63]. Optional.
        activitySubType (int): 7-bit bitmask for additional activity detail. Range: [0, 127]. Optional.
        assistType (int): 6-bit bitmask describing type of assistance being provided. Range: [0, 63]. Optional.
        sizing (int): 5-bit bitmask describing the physical size/equipment of the VRU. Range: [0, 31]. Optional.
        attachment (str): Type of attachment carried by or attached to the VRU. One of unavailable, stroller, bicycleTrailer, cart, wheelchair, otherWalkAssistAttachments, pet. Optional.
        attachmentRadius (int): Radius of the attachment from the VRU's reported position. Range: [0, 200]. Unit: decimeter. Optional.
        animalType (str): Type of animal if basicType is anANIMAL. One of unavailable, serviceUse, pet, farm. Optional.

    Returns:
        hex_psm (str): PSM message encoded as a hex string.
    """
    psm = {}

    if basicType is None:
        print('basicType is mandatory! Please provide the type of the pedestrian. Set to unavailable.')
        psm['basicType'] = 'unavailable'
    elif basicType in ['unavailable', 'aPEDESTRIAN', 'aPEDALCYCLIST', 'aPUBLICSAFETYWORKER', 'anANIMAL']:
        psm['basicType'] = basicType
    else:
        print('basicType should be one of unavailable, aPEDESTRIAN, aPEDALCYCLIST, aPUBLICSAFETYWORKER, anANIMAL! But', basicType, 'is provided. Set to unavailable.')
        psm['basicType'] = 'unavailable'
    
    if secMark is None:
        print('secMark is mandatory! Please provide the second elapsed. Set to 65535.')
        psm['secMark'] = 65535
    elif not isinstance(secMark, int):
        print('secMark should be an integer! But', secMark, 'is provided. Set to 0.')
        psm['secMark'] = 0
    elif secMark < 0 or secMark > 65535:
        print('secMark should be in range [0, 65535]! But', secMark, 'is provided. Remove it.')
        psm['secMark'] = 65535
    else:
        psm['secMark'] = secMark

    if msgCnt is None:
        print('msgCnt is mandatory! Please provide msgCnt. Set to 0.')
        psm['msgCnt'] = 0
    elif not isinstance(msgCnt, int):
        print('msgCnt should be an integer! But', msgCnt, 'is provided. Set to 0.')
        psm['msgCnt'] = 0
    elif msgCnt < 0 or msgCnt > 127:
        print('msgCnt should be in range [0, 127]! But', msgCnt, 'is provided. Set to 0.')
        psm['msgCnt'] = 0
    else:
        psm['msgCnt'] = msgCnt

    if sourceID is None:
        print('sourceID is mandatory! Please provide sourceID. Set to tmp.')
        psm['id'] = b'tmp\x00'
    else:
        encoded = sourceID.encode('utf-8')
        if len(encoded) != 4:
            print('sourceID must be exactly 4 bytes! But', repr(encoded), 'is provided. Changing it to 4 bytes')
            encoded = encoded[:4].ljust(4, b'\x00')
        psm['id'] = encoded
    
    psm['position'] = {}
    if position_lat is None:
        print('position_lat is mandatory! Please provide the latitude of information source. Set to 90.0000001.')
        psm['position']['lat'] = 900000001
    elif position_lat < -90 or position_lat > 90:
        print('position_lat should be in range [-90, 90] deg! But', position_lat, 'is provided. Set to 90.0000001.')
        psm['position']['lat'] = 900000001
    else:
        psm['position']['lat'] = int(position_lat * 10 ** 7)

    if position_long is None:
        print('position_long is mandatory! Please provide the longitude of information source. Set to 180.0000001.')
        psm['position']['long'] = 1800000001
    elif position_long < -179.9999999 or position_long > 180:
        print('position_long should be in range [-179.9999999, 180] deg! But', position_long, 'is provided. Set to 180.0000001.')
        psm['position']['long'] = 1800000001
    else:
        psm['position']['long'] = int(position_long * 10 ** 7)

    if position_elevation is not None:
        if position_elevation < -409.5 or position_elevation > 6143.9:
            print('position_elevation should be in range [-409.5, 6143.9] m! But', position_elevation, 'is provided. Set to -409.6.')
            psm['position']['elevation'] = -4096
        else:
            psm['position']['elevation'] = int(position_elevation * 10)

    psm['accuracy'] = {}
    if accuracy_semiMajor is None:
        print('accuracy_semiMajor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
        psm['accuracy']['semiMajor'] = 255
    elif accuracy_semiMajor < 0:
        print('accuracy_semiMajor should be in range [0, 12.7] m! But', accuracy_semiMajor, 'is provided. Set to 12.75.')
        psm['accuracy']['semiMajor'] = 255
    elif accuracy_semiMajor > 12.7:
        print('accuracy_semiMajor should be in range [0, 12.7] m! But', accuracy_semiMajor, 'is provided. Set to 12.7.')
        psm['accuracy']['semiMajor'] = 254
    else:
        psm['accuracy']['semiMajor'] = int(accuracy_semiMajor * 20)

    if accuracy_semiMinor is None:
        print('accuracy_semiMinor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
        psm['accuracy']['semiMinor'] = 255
    elif accuracy_semiMinor < 0:
        print('accuracy_semiMinor should be in range [0, 12.7] m! But', accuracy_semiMinor, 'is provided. Set to 12.75.')
        psm['accuracy']['semiMinor'] = 255
    elif accuracy_semiMinor > 12.7:
        print('accuracy_semiMinor should be in range [0, 12.7] m! But', accuracy_semiMinor, 'is provided. Set to 12.7.')
        psm['accuracy']['semiMinor'] = 254
    else:
        psm['accuracy']['semiMinor'] = int(accuracy_semiMinor * 20)

    if accuracy_orientation is None:
        print('accuracy_orientation is mandatory! Please provide the orientation of the angle of the semi-major axis of an ellipsoid. Set to 12.75.')
        psm['accuracy']['orientation'] = 65535
    elif accuracy_orientation < 0 or accuracy_orientation > 359.9945078786:
        print('accuracy_orientation should be in range [0, 359.9945078786] deg! But', accuracy_orientation, 'is provided. Set to 360.')
        psm['accuracy']['orientation'] = 65535
    else:
        psm['accuracy']['orientation'] = int(accuracy_orientation / 360 * 65535)

    if speed is None:
        print('speed is mandatory! Please provide the speed of the object. Set to 8191.')
        psm['speed'] = 8191
    elif not isinstance(speed, (int, float)):
        print('speed should be a number! But', speed, 'is provided. Set to 8191.')
        psm['speed'] = 8191
    elif speed < 0 or speed > 163.80:
        print('speed should be in range [0, 163.80] m/s! But', speed, 'is provided. Set to 8191.')
        psm['speed'] = 8191
    else:
        psm['speed'] = int(speed * 50)

    if heading is None:
        print('heading is mandatory! Please provide the current heading of the sending device. Set to 28800')
        psm['heading'] = 28800
    elif not isinstance(heading, (int, float)):
        print('heading should be a number! But', heading, 'is provided. Set to 28800.')
        psm['heading'] = 28800
    elif heading < 0 or heading > 359.9875:
        print('heading should be in range [0, 359.9875] deg! But', heading, 'is provided. Set to 28800.')
        psm['heading'] = 28800
    else:
        psm['heading'] = int(heading / 0.0125)

    if accelSet_long is not None or accelSet_lat is not None or accelSet_vert is not None or accelSet_yaw is not None:
        psm['accelSet'] = {}
        if accelSet_long is None:
            print('accelSet_long is mandatory! Please provide accelSet_long. Set to 2001.')
            psm['accelSet']['long'] = 2001
        elif not isinstance(accelSet_long, (int, float)):
            print('accelSet_long should be a number! But', accelSet_long, 'is provided. Set to 2001.')
            psm['accelSet']['long'] = 2001
        elif accelSet_long < -20:
            psm['accelSet']['long'] = -2000
        elif accelSet_long > 20:
            psm['accelSet']['long'] = 2000
        else:
            psm['accelSet']['long'] = int(accelSet_long * 100)

        if accelSet_lat is None:
            print('accelSet_lat is mandatory! Please provide accelSet_lat. Set to 2001.')
            psm['accelSet']['lat'] = 2001
        elif not isinstance(accelSet_lat, (int, float)):
            print('accelSet_lat should be a number! But', accelSet_lat, 'is provided. Set to 2001.')
            psm['accelSet']['lat'] = 2001
        elif accelSet_lat < -20:
            psm['accelSet']['lat'] = -2000
        elif accelSet_lat > 20:
            psm['accelSet']['lat'] = 2000
        else:
            psm['accelSet']['lat'] = int(accelSet_lat * 100)

        if accelSet_vert is None:
            print('accelSet_vert is mandatory! Please provide accelSet_vert. Set to -127.')
            psm['accelSet']['vert'] = -127
        elif not isinstance(accelSet_vert, (int, float)):
            print('accelSet_vert should be a number! But', accelSet_vert, 'is provided. Set to -127.')
            psm['accelSet']['vert'] = -127
        elif accelSet_vert <= -2.52 * 9.80665:
            psm['accelSet']['vert'] = -126
        elif accelSet_vert >= 2.54 * 9.80665:
            psm['accelSet']['vert'] = 127
        else:
            psm['accelSet']['vert'] = int(accelSet_vert / 9.80665 * 50)

        if accelSet_yaw is None:
            print('accelSet_yaw is mandatory! Please provide accelSet_yaw. Set to 0.')
            psm['accelSet']['yaw'] = 0
        elif not isinstance(accelSet_yaw, (int, float)):
            print('accelSet_yaw should be a number! But', accelSet_yaw, 'is provided. Set to 0.')
            psm['accelSet']['yaw'] = 0
        elif accelSet_yaw < -327.67:
            psm['accelSet']['yaw'] = -32767
        elif accelSet_yaw > 327.67:
            psm['accelSet']['yaw'] = 32767
        else:
            psm['accelSet']['yaw'] = int(accelSet_yaw * 100)

    if pathHistory_exists:
        psm['pathHistory'] = {}
        if pathHistory_initialPosition_exists:
            psm['pathHistory']['initialPosition'] = {}
            utcTime = {}
            if pathHistory_initialPosition_utcTime_year is not None:
                if not isinstance(pathHistory_initialPosition_utcTime_year, int):
                    print('pathHistory_initialPosition_utcTime_year should be an integer! But', pathHistory_initialPosition_utcTime_year, 'is provided. Remove it.')
                elif pathHistory_initialPosition_utcTime_year < 0 or pathHistory_initialPosition_utcTime_year > 4095:
                    print('pathHistory_initialPosition_utcTime_year should be in range [0, 4095]! But', pathHistory_initialPosition_utcTime_year, 'is provided. Remove it.')
                else:
                    utcTime['year'] = pathHistory_initialPosition_utcTime_year
            if pathHistory_initialPosition_utcTime_month is not None:
                if not isinstance(pathHistory_initialPosition_utcTime_month, int):
                    print('pathHistory_initialPosition_utcTime_month should be an integer! But', pathHistory_initialPosition_utcTime_month, 'is provided. Remove it.')
                elif pathHistory_initialPosition_utcTime_month < 0 or pathHistory_initialPosition_utcTime_month > 12:
                    print('pathHistory_initialPosition_utcTime_month should be in range [0, 12]! But', pathHistory_initialPosition_utcTime_month, 'is provided. Remove it.')
                else:
                    utcTime['month'] = pathHistory_initialPosition_utcTime_month
            if pathHistory_initialPosition_utcTime_day is not None:
                if not isinstance(pathHistory_initialPosition_utcTime_day, int):
                    print('pathHistory_initialPosition_utcTime_day should be an integer! But', pathHistory_initialPosition_utcTime_day, 'is provided. Remove it.')
                elif pathHistory_initialPosition_utcTime_day < 0 or pathHistory_initialPosition_utcTime_day > 31:
                    print('pathHistory_initialPosition_utcTime_day should be in range [0, 31]! But', pathHistory_initialPosition_utcTime_day, 'is provided. Remove it.')
                else:
                    utcTime['day'] = pathHistory_initialPosition_utcTime_day
            if pathHistory_initialPosition_utcTime_hour is not None:
                if not isinstance(pathHistory_initialPosition_utcTime_hour, int):
                    print('pathHistory_initialPosition_utcTime_hour should be an integer! But', pathHistory_initialPosition_utcTime_hour, 'is provided. Remove it.')
                elif pathHistory_initialPosition_utcTime_hour < 0 or pathHistory_initialPosition_utcTime_hour > 31:
                    print('pathHistory_initialPosition_utcTime_hour should be in range [0, 31] h! But', pathHistory_initialPosition_utcTime_hour, 'is provided. Remove it.')
                else:
                    utcTime['hour'] = pathHistory_initialPosition_utcTime_hour
            if pathHistory_initialPosition_utcTime_minute is not None:
                if not isinstance(pathHistory_initialPosition_utcTime_minute, int):
                    print('pathHistory_initialPosition_utcTime_minute should be an integer! But', pathHistory_initialPosition_utcTime_minute, 'is provided. Remove it.')
                elif pathHistory_initialPosition_utcTime_minute < 0 or pathHistory_initialPosition_utcTime_minute > 60:
                    print('pathHistory_initialPosition_utcTime_minute should be in range [0, 60] min! But', pathHistory_initialPosition_utcTime_minute, 'is provided. Remove it.')
                else:
                    utcTime['minute'] = pathHistory_initialPosition_utcTime_minute
            if pathHistory_initialPosition_utcTime_second is not None:
                if pathHistory_initialPosition_utcTime_second < 0 or pathHistory_initialPosition_utcTime_second > 65.535:
                    print('pathHistory_initialPosition_utcTime_second should be in range [0, 65.535] s! But', pathHistory_initialPosition_utcTime_second, 'is provided. Remove it.')
                else:
                    utcTime['second'] = int(pathHistory_initialPosition_utcTime_second * 10**3)
            if pathHistory_initialPosition_utcTime_offset is not None:
                if not isinstance(pathHistory_initialPosition_utcTime_offset, int):
                    print('pathHistory_initialPosition_utcTime_offset should be an integer! But', pathHistory_initialPosition_utcTime_offset, 'is provided. Remove it.')
                elif pathHistory_initialPosition_utcTime_offset < -840 or pathHistory_initialPosition_utcTime_offset > 840:
                    print('pathHistory_initialPosition_utcTime_offset should be in range [-840, 840] min! But', pathHistory_initialPosition_utcTime_offset, 'is provided. Remove it.')
                else:
                    utcTime['offset'] = pathHistory_initialPosition_utcTime_offset
            if utcTime:
                psm['pathHistory']['initialPosition']['utcTime'] = utcTime

            if pathHistory_initialPosition_long is None:
                print('pathHistory_initialPosition_long is mandatory if initialPosition is included! Set to 180.0000001.')
                psm['pathHistory']['initialPosition']['long'] = 1800000001
            elif pathHistory_initialPosition_long < -179.9999999 or pathHistory_initialPosition_long > 180:
                print('pathHistory_initialPosition_long should be in range [-179.9999999, 180] deg! But', pathHistory_initialPosition_long, 'is provided. Set to 180.0000001.')
                psm['pathHistory']['initialPosition']['long'] = 1800000001
            else:
                psm['pathHistory']['initialPosition']['long'] = int(pathHistory_initialPosition_long * 10 ** 7)

            if pathHistory_initialPosition_lat is None:
                print('pathHistory_initialPosition_lat is mandatory if initialPosition is included! Set to 90.0000001.')
                psm['pathHistory']['initialPosition']['lat'] = 900000001
            elif pathHistory_initialPosition_lat < -90 or pathHistory_initialPosition_lat > 90:
                print('pathHistory_initialPosition_lat should be in range [-90, 90] deg! But', pathHistory_initialPosition_lat, 'is provided. Set to 90.0000001.')
                psm['pathHistory']['initialPosition']['lat'] = 900000001
            else:
                psm['pathHistory']['initialPosition']['lat'] = int(pathHistory_initialPosition_lat * 10 ** 7)

            if pathHistory_initialPosition_elevation is not None:
                if pathHistory_initialPosition_elevation < -409.5 or pathHistory_initialPosition_elevation > 6143.9:
                    print('pathHistory_initialPosition_elevation should be in range [-409.5, 6143.9] m! But', pathHistory_initialPosition_elevation, 'is provided. Remove it.')
                    psm['pathHistory']['initialPosition']['elevation'] = -4096
                else:
                    psm['pathHistory']['initialPosition']['elevation'] = int(pathHistory_initialPosition_elevation * 10)

            if pathHistory_initialPosition_heading is not None:
                if pathHistory_initialPosition_heading < 0 or pathHistory_initialPosition_heading > 359.9875:
                    print('pathHistory_initialPosition_heading should be in range [0, 359.9875] deg! But', pathHistory_initialPosition_heading, 'is provided. Remove it.')
                else:
                    psm['pathHistory']['initialPosition']['heading'] = int(pathHistory_initialPosition_heading / 0.0125)

            if pathHistory_initialPosition_speed_transmission is not None or pathHistory_initialPosition_speed_velocity is not None:
                psm['pathHistory']['initialPosition']['speed'] = {}
                if pathHistory_initialPosition_speed_transmission is None:
                    print('pathHistory_initialPosition_speed_transmission is mandatory! Please provide. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speed']['transmisson'] = 'unavailable'
                elif pathHistory_initialPosition_speed_transmission in ['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']:
                    psm['pathHistory']['initialPosition']['speed']['transmisson'] = pathHistory_initialPosition_speed_transmission
                else:
                    print('pathHistory_initialPosition_speed_transmission should be one of neutral, park, forwardGears, reverseGears, or unavailable! But', pathHistory_initialPosition_speed_transmission, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speed']['transmisson'] = 'unavailable'

                if pathHistory_initialPosition_speed_velocity is None:
                    print('pathHistory_initialPosition_speed_velocity is mandatory! Please provide the speed. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speed']['speed'] = 8191
                elif not isinstance(pathHistory_initialPosition_speed_velocity, (int, float)):
                    print('pathHistory_initialPosition_speed_velocity should be a number! But', pathHistory_initialPosition_speed_velocity, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speed']['speed'] = 8191
                elif pathHistory_initialPosition_speed_velocity < 0 or pathHistory_initialPosition_speed_velocity > 163.80:
                    print('pathHistory_initialPosition_speed_velocity should be in range [0, 163.80] m/s! But', pathHistory_initialPosition_speed_velocity, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speed']['speed'] = 8191
                else:
                    psm['pathHistory']['initialPosition']['speed']['speed'] = int(pathHistory_initialPosition_speed_velocity * 50)

            if pathHistory_initialPosition_posAccuracy_semiMinor is not None or pathHistory_initialPosition_posAccuracy_semiMajor is not None or pathHistory_initialPosition_posAccuracy_orientation is not None:
                psm['pathHistory']['initialPosition']['posAccuracy'] = {}
                if pathHistory_initialPosition_posAccuracy_semiMajor is None:
                    print('pathHistory_initialPosition_posAccuracy_semiMajor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMajor'] = 255
                elif pathHistory_initialPosition_posAccuracy_semiMajor < 0:
                    print('pathHistory_initialPosition_posAccuracy_semiMajor should be in range [0, 12.7] m! But', pathHistory_initialPosition_posAccuracy_semiMajor, 'is provided. Set to 12.75.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMajor'] = 255
                elif pathHistory_initialPosition_posAccuracy_semiMajor > 12.7:
                    print('pathHistory_initialPosition_posAccuracy_semiMajor should be in range [0, 12.7] m! But', pathHistory_initialPosition_posAccuracy_semiMajor, 'is provided. Set to 12.7.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMajor'] = 254
                else:
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMajor'] = int(pathHistory_initialPosition_posAccuracy_semiMajor * 20)

                if pathHistory_initialPosition_posAccuracy_semiMinor is None:
                    print('pathHistory_initialPosition_posAccuracy_semiMinor is mandatory! Please provide the radius of the semi-minor axis of an ellipsoid. Set to 12.75.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMinor'] = 255
                elif pathHistory_initialPosition_posAccuracy_semiMinor < 0:
                    print('pathHistory_initialPosition_posAccuracy_semiMinor should be in range [0, 12.7] m! But', pathHistory_initialPosition_posAccuracy_semiMinor, 'is provided. Set to 12.75.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMinor'] = 255
                elif pathHistory_initialPosition_posAccuracy_semiMinor > 12.7:
                    print('pathHistory_initialPosition_posAccuracy_semiMinor should be in range [0, 12.7] m! But', pathHistory_initialPosition_posAccuracy_semiMinor, 'is provided. Set to 12.7.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMinor'] = 254
                else:
                    psm['pathHistory']['initialPosition']['posAccuracy']['semiMinor'] = int(pathHistory_initialPosition_posAccuracy_semiMinor * 20)

                if pathHistory_initialPosition_posAccuracy_orientation is None:
                    print('pathHistory_initialPosition_posAccuracy_orientation is mandatory! Please provide the orientation of the angle of the semi-major axis of an ellipsoid. Set to 360.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['orientation'] = 65535
                elif pathHistory_initialPosition_posAccuracy_orientation < 0 or pathHistory_initialPosition_posAccuracy_orientation > 359.9945078786:
                    print('pathHistory_initialPosition_posAccuracy_orientation should be in range [0, 359.9945078786] deg! But', pathHistory_initialPosition_posAccuracy_orientation, 'is provided. Set to 360.')
                    psm['pathHistory']['initialPosition']['posAccuracy']['orientation'] = 65535
                else:
                    psm['pathHistory']['initialPosition']['posAccuracy']['orientation'] = int(pathHistory_initialPosition_posAccuracy_orientation / 360 * 65535)

            if pathHistory_initialPosition_timeConfidence is not None:
                if pathHistory_initialPosition_timeConfidence <= 0:
                    print('pathHistory_initialPosition_timeConfidence should be greater than 0 s! But', pathHistory_initialPosition_timeConfidence, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'unavailable'
                elif 0 < pathHistory_initialPosition_timeConfidence <= 1e-11:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-01'
                elif 1e-11 < pathHistory_initialPosition_timeConfidence <= 2e-11:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-02'
                elif 2e-11 < pathHistory_initialPosition_timeConfidence <= 5e-11:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-05'
                elif 5e-11 < pathHistory_initialPosition_timeConfidence <= 1e-10:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-1'
                elif 1e-10 < pathHistory_initialPosition_timeConfidence <= 2e-10:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-2'
                elif 2e-10 < pathHistory_initialPosition_timeConfidence <= 5e-10:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-000-5'
                elif 5e-10 < pathHistory_initialPosition_timeConfidence <= 1e-9:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-001'
                elif 1e-9 < pathHistory_initialPosition_timeConfidence <= 2e-9:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-002'
                elif 2e-9 < pathHistory_initialPosition_timeConfidence <= 5e-9:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-005'
                elif 5e-9 < pathHistory_initialPosition_timeConfidence <= 1e-8:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-01'
                elif 1e-8 < pathHistory_initialPosition_timeConfidence <= 2e-8:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-02'
                elif 2e-8 < pathHistory_initialPosition_timeConfidence <= 5e-8:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-05'
                elif 5e-8 < pathHistory_initialPosition_timeConfidence <= 1e-7:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-1'
                elif 1e-7 < pathHistory_initialPosition_timeConfidence <= 2e-7:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-2'
                elif 2e-7 < pathHistory_initialPosition_timeConfidence <= 5e-7:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-000-5'
                elif 5e-7 < pathHistory_initialPosition_timeConfidence <= 1e-6:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-001'
                elif 1e-6 < pathHistory_initialPosition_timeConfidence <= 2e-6:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-002'
                elif 2e-6 < pathHistory_initialPosition_timeConfidence <= 5e-6:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-005'
                elif 5e-6 < pathHistory_initialPosition_timeConfidence <= 1e-5:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-01'
                elif 1e-5 < pathHistory_initialPosition_timeConfidence <= 2e-5:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-02'
                elif 2e-5 < pathHistory_initialPosition_timeConfidence <= 5e-5:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-05'
                elif 5e-5 < pathHistory_initialPosition_timeConfidence <= 1e-4:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-1'
                elif 1e-4 < pathHistory_initialPosition_timeConfidence <= 2e-4:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-2'
                elif 2e-4 < pathHistory_initialPosition_timeConfidence <= 5e-4:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-000-5'
                elif 5e-4 < pathHistory_initialPosition_timeConfidence <= 1e-3:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-001'
                elif 1e-3 < pathHistory_initialPosition_timeConfidence <= 2e-3:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-002'
                elif 2e-3 < pathHistory_initialPosition_timeConfidence <= 5e-3:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-005'
                elif 5e-3 < pathHistory_initialPosition_timeConfidence <= 1e-2:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-010'
                elif 1e-2 < pathHistory_initialPosition_timeConfidence <= 2e-2:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-020'
                elif 2e-2 < pathHistory_initialPosition_timeConfidence <= 5e-2:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-050'
                elif 5e-2 < pathHistory_initialPosition_timeConfidence <= 1e-1:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-100'
                elif 1e-1 < pathHistory_initialPosition_timeConfidence <= 2e-1:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-200'
                elif 2e-1 < pathHistory_initialPosition_timeConfidence <= 5e-1:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-000-500'
                elif 5e-1 < pathHistory_initialPosition_timeConfidence <= 1:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-001-000'
                elif 1 < pathHistory_initialPosition_timeConfidence <= 2:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-002-000'
                elif 2 < pathHistory_initialPosition_timeConfidence <= 10:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-010-000'
                elif 10 < pathHistory_initialPosition_timeConfidence <= 20:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-020-000'
                elif 20 < pathHistory_initialPosition_timeConfidence <= 50:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-050-000'
                elif 50 < pathHistory_initialPosition_timeConfidence <= 100:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'time-100-000'
                elif 100 < pathHistory_initialPosition_timeConfidence:
                    psm['pathHistory']['initialPosition']['timeConfidence'] = 'unavailable'

            if pathHistory_initialPosition_posConfidence_pos is not None or pathHistory_initialPosition_posConfidence_elevation is not None:
                psm['pathHistory']['initialPosition']['posConfidence'] = {}
                if pathHistory_initialPosition_posConfidence_pos is None:
                    print('pathHistory_initialPosition_posConfidence_pos is mandatory! Please provide. Set to unavailable')
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'unavailable'
                elif pathHistory_initialPosition_posConfidence_pos <= 0:
                    print('pathHistory_initialPosition_posConfidence_pos should be greater than 0 m! But', pathHistory_initialPosition_posConfidence_pos, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'unavailable'
                elif 0 < pathHistory_initialPosition_posConfidence_pos <= 0.01:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a1cm'
                elif 0.01 < pathHistory_initialPosition_posConfidence_pos <= 0.02:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a2cm'
                elif 0.02 < pathHistory_initialPosition_posConfidence_pos <= 0.05:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a5cm'
                elif 0.05 < pathHistory_initialPosition_posConfidence_pos <= 0.1:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a10cm'
                elif 0.1 < pathHistory_initialPosition_posConfidence_pos <= 0.2:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a20cm'
                elif 0.2 < pathHistory_initialPosition_posConfidence_pos <= 0.5:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a50cm'
                elif 0.5 < pathHistory_initialPosition_posConfidence_pos <= 1:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a1m'
                elif 1 < pathHistory_initialPosition_posConfidence_pos <= 2:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a2m'
                elif 2 < pathHistory_initialPosition_posConfidence_pos <= 5:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a5m'
                elif 5 < pathHistory_initialPosition_posConfidence_pos <= 10:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a10m'
                elif 10 < pathHistory_initialPosition_posConfidence_pos <= 20:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a20m'
                elif 20 < pathHistory_initialPosition_posConfidence_pos <= 50:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a50m'
                elif 50 < pathHistory_initialPosition_posConfidence_pos <= 100:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a100m'
                elif 100 < pathHistory_initialPosition_posConfidence_pos <= 200:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a200m'
                elif 200 < pathHistory_initialPosition_posConfidence_pos <= 500:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'a500m'
                else:
                    psm['pathHistory']['initialPosition']['posConfidence']['pos'] = 'unavailable'

                if pathHistory_initialPosition_posConfidence_elevation is None:
                    print('pathHistory_initialPosition_posConfidence_elevation is mandatory! Please provide. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'unavailable'
                elif pathHistory_initialPosition_posConfidence_elevation <= 0:
                    print('pathHistory_initialPosition_posConfidence_elevation should be greater than 0 m! But', pathHistory_initialPosition_posConfidence_elevation, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'unavailable'
                elif pathHistory_initialPosition_posConfidence_elevation <= 0.01:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-000-01'
                elif pathHistory_initialPosition_posConfidence_elevation <= 0.02:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-000-02'
                elif pathHistory_initialPosition_posConfidence_elevation <= 0.05:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-000-05'
                elif pathHistory_initialPosition_posConfidence_elevation <= 0.10:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-000-10'
                elif pathHistory_initialPosition_posConfidence_elevation <= 0.20:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-000-20'
                elif pathHistory_initialPosition_posConfidence_elevation <= 0.50:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-000-50'
                elif pathHistory_initialPosition_posConfidence_elevation <= 1.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-001-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 2.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-002-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 5.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-005-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 10.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-010-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 20.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-020-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 50.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-050-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 100.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-100-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 200.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-200-00'
                elif pathHistory_initialPosition_posConfidence_elevation <= 500.00:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'elev-500-00'
                else:
                    psm['pathHistory']['initialPosition']['posConfidence']['elevation'] = 'unavailable'

            if pathHistory_initialPosition_speedConfidence_heading is not None or pathHistory_initialPosition_speedConfidence_speed is not None or pathHistory_initialPosition_speedConfidence_throttle is not None:
                psm['pathHistory']['initialPosition']['speedConfidence'] = {}
                if pathHistory_initialPosition_speedConfidence_heading is None:
                    print('pathHistory_initialPosition_speedConfidence_heading is mandatory! Please provide. Set to unavailable')
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'unavailable'
                elif pathHistory_initialPosition_speedConfidence_heading <= 0:
                    print('pathHistory_initialPosition_speedConfidence_heading should be greater than 0 deg! But', pathHistory_initialPosition_speedConfidence_heading, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'unavailable'
                elif 0 < pathHistory_initialPosition_speedConfidence_heading <= 0.01:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'prec0-01deg'
                elif 0.01 < pathHistory_initialPosition_speedConfidence_heading <= 0.0125:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'prec0-0125deg'
                elif 0.0125 < pathHistory_initialPosition_speedConfidence_heading <= 0.05:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'prec0-05deg'
                elif 0.05 < pathHistory_initialPosition_speedConfidence_heading <= 0.1:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'prec0-1deg'
                elif 0.1 < pathHistory_initialPosition_speedConfidence_heading <= 1:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'prec01deg'
                elif 1 < pathHistory_initialPosition_speedConfidence_heading <= 5:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'prec05deg'
                elif 5 < pathHistory_initialPosition_speedConfidence_heading <= 10:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'prec10deg'
                else:
                    psm['pathHistory']['initialPosition']['speedConfidence']['heading'] = 'unavailable'

                if pathHistory_initialPosition_speedConfidence_speed is None:
                    print('pathHistory_initialPosition_speedConfidence_speed is mandatory! Please provide. Set to unavailable')
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'unavailable'
                elif pathHistory_initialPosition_speedConfidence_speed <= 0:
                    print('pathHistory_initialPosition_speedConfidence_speed should be greater than 0 m/s! But', pathHistory_initialPosition_speedConfidence_speed, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'unavailable'
                elif 0 < pathHistory_initialPosition_speedConfidence_speed <= 0.01:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'prec0-01ms'
                elif 0.01 < pathHistory_initialPosition_speedConfidence_speed <= 0.05:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'prec0-05ms'
                elif 0.05 < pathHistory_initialPosition_speedConfidence_speed <= 0.1:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'prec0-1ms'
                elif 0.1 < pathHistory_initialPosition_speedConfidence_speed <= 1:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'prec1ms'
                elif 1 < pathHistory_initialPosition_speedConfidence_speed <= 5:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'prec5ms'
                elif 5 < pathHistory_initialPosition_speedConfidence_speed <= 10:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'prec10ms'
                elif 10 < pathHistory_initialPosition_speedConfidence_speed <= 100:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'prec100ms'
                else:
                    psm['pathHistory']['initialPosition']['speedConfidence']['speed'] = 'unavailable'

                if pathHistory_initialPosition_speedConfidence_throttle is None:
                    print('pathHistory_initialPosition_speedConfidence_throttle is mandatory! Please provide. Set to unavailable')
                    psm['pathHistory']['initialPosition']['speedConfidence']['throttle'] = 'unavailable'
                elif pathHistory_initialPosition_speedConfidence_throttle <= 0:
                    print('pathHistory_initialPosition_speedConfidence_throttle should be greater than 0 m/s! But', pathHistory_initialPosition_speedConfidence_throttle, 'is provided. Set to unavailable.')
                    psm['pathHistory']['initialPosition']['speedConfidence']['throttle'] = 'unavailable'
                elif 0 < pathHistory_initialPosition_speedConfidence_throttle <= 0.005:
                    psm['pathHistory']['initialPosition']['speedConfidence']['throttle'] = 'prec0-5percent'
                elif 0.005 < pathHistory_initialPosition_speedConfidence_throttle <= 0.01:
                    psm['pathHistory']['initialPosition']['speedConfidence']['throttle'] = 'prec1percent'
                elif 0.01 < pathHistory_initialPosition_speedConfidence_throttle <= 0.1:
                    psm['pathHistory']['initialPosition']['speedConfidence']['throttle'] = 'prec10percent'
                else:
                    psm['pathHistory']['initialPosition']['speedConfidence']['throttle'] = 'unavailable'

        if pathHistory_currGNSSstatus is not None:
            if not isinstance(pathHistory_currGNSSstatus, int):
                print('pathHistory_currGNSSstatus should be an integer bitmask! But', pathHistory_currGNSSstatus, 'is provided. Remove it.')
            elif pathHistory_currGNSSstatus < 0 or pathHistory_currGNSSstatus > 255:
                print('pathHistory_currGNSSstatus should be in range [0, 255] (8 bits)! But', pathHistory_currGNSSstatus, 'is provided. Remove it.')
            else:
                psm['pathHistory']['currGNSSstatus'] = (pathHistory_currGNSSstatus, 8)

        psm['pathHistory']['crumbData'] = []
        if pathHistory_crumbData_N < 1 or pathHistory_crumbData_N > 23:
            print('pathHistory_crumbData_N should be in range [1, 23]! But', pathHistory_crumbData_N, 'is provided. Path cannot be encoded without at least 1 crumb point.')
        else:
            for i in range(pathHistory_crumbData_N):
                crumb = {}

                if len(pathHistory_crumbData_latOffset) <= i:
                    print('Expect', pathHistory_crumbData_N, 'pathHistory_crumbData_latOffset but there are only', len(pathHistory_crumbData_latOffset), 'of it!')
                    break
                elif pathHistory_crumbData_latOffset[i] is None:
                    print('pathHistory_crumbData_latOffset is mandatory! Please provide pathHistory_crumbData_latOffset. Set to unavailable.')
                    crumb['latOffset'] = -131072
                elif pathHistory_crumbData_latOffset[i] >= 0.0131071:
                    crumb['latOffset'] = 131071
                elif pathHistory_crumbData_latOffset[i] <= -0.0131071:
                    crumb['latOffset'] = -131071
                else:
                    crumb['latOffset'] = int(pathHistory_crumbData_latOffset[i] * 10**7)

                if len(pathHistory_crumbData_lonOffset) <= i:
                    print('Expect', pathHistory_crumbData_N, 'pathHistory_crumbData_lonOffset but there are only', len(pathHistory_crumbData_lonOffset), 'of it!')
                    break
                elif pathHistory_crumbData_lonOffset[i] is None:
                    print('pathHistory_crumbData_lonOffset is mandatory! Please provide pathHistory_crumbData_lonOffset. Set to unavailable.')
                    crumb['lonOffset'] = -131072
                elif pathHistory_crumbData_lonOffset[i] >= 0.0131071:
                    crumb['lonOffset'] = 131071
                elif pathHistory_crumbData_lonOffset[i] <= -0.0131071:
                    crumb['lonOffset'] = -131071
                else:
                    crumb['lonOffset'] = int(pathHistory_crumbData_lonOffset[i] * 10**7)

                if len(pathHistory_crumbData_elevationOffset) <= i:
                    print('Expect', pathHistory_crumbData_N, 'pathHistory_crumbData_elevationOffset but there are only', len(pathHistory_crumbData_elevationOffset), 'of it!')
                    break
                elif pathHistory_crumbData_elevationOffset[i] is None:
                    print('pathHistory_crumbData_elevationOffset is mandatory! Please provide pathHistory_crumbData_elevationOffset. Set to unavailable.')
                    crumb['elevationOffset'] = -2048
                elif pathHistory_crumbData_elevationOffset[i] >= 204.7:
                    crumb['elevationOffset'] = 2047
                elif pathHistory_crumbData_elevationOffset[i] <= -204.7:
                    crumb['elevationOffset'] = -2047
                else:
                    crumb['elevationOffset'] = int(pathHistory_crumbData_elevationOffset[i] * 10)

                if len(pathHistory_crumbData_timeOffset) <= i:
                    print('Expect', pathHistory_crumbData_N, 'pathHistory_crumbData_timeOffset but there are only', len(pathHistory_crumbData_timeOffset), 'of it!')
                    break
                elif pathHistory_crumbData_timeOffset[i] is None:
                    print('pathHistory_crumbData_timeOffset is mandatory! Please provide pathHistory_crumbData_timeOffset. Set to unavailable.')
                    crumb['timeOffset'] = 65535
                elif pathHistory_crumbData_timeOffset[i] >= 655.34:
                    crumb['timeOffset'] = 65534
                elif pathHistory_crumbData_timeOffset[i] < 0.01:
                    print('pathHistory_crumbData_timeOffset[', i, '] should be >= 0.01s! Set to unavailable.')
                    crumb['timeOffset'] = 65535
                else:
                    crumb['timeOffset'] = int(pathHistory_crumbData_timeOffset[i] * 100)

                if len(pathHistory_crumbData_speed) > i:
                    if pathHistory_crumbData_speed[i] < 0 or pathHistory_crumbData_speed[i] > 163.80:
                        print('pathHistory_crumbData_speed[', i, '] should be in range [0, 163.80] m/s! Set to unavailable.')
                        crumb['speed'] = 8191
                    else:
                        crumb['speed'] = int(pathHistory_crumbData_speed[i] * 50)

                if len(pathHistory_crumbData_posAccuracy_semiMajor) > i and len(pathHistory_crumbData_posAccuracy_semiMinor) > i and len(pathHistory_crumbData_posAccuracy_orientation) > i:
                    crumb['posAccuracy'] = {}
                    sM = pathHistory_crumbData_posAccuracy_semiMajor[i]
                    sm = pathHistory_crumbData_posAccuracy_semiMinor[i]
                    orient = pathHistory_crumbData_posAccuracy_orientation[i]
                    crumb['posAccuracy']['semiMajor'] = 255 if sM is None or sM < 0 else (254 if sM > 12.7 else int(sM * 20))
                    crumb['posAccuracy']['semiMinor'] = 255 if sm is None or sm < 0 else (254 if sm > 12.7 else int(sm * 20))
                    crumb['posAccuracy']['orientation'] = 65535 if orient is None or orient < 0 or orient > 359.9945078786 else int(orient / 360 * 65535)

                if len(pathHistory_crumbData_heading) > i:
                    if pathHistory_crumbData_heading[i] is None or pathHistory_crumbData_heading[i] < 0 or pathHistory_crumbData_heading[i] > 358.5:
                        crumb['heading'] = 240
                    else:
                        crumb['heading'] = int(pathHistory_crumbData_heading[i] / 1.5)

                psm['pathHistory']['crumbData'].append(crumb)
    else:
        print('Path history data is not provided.')

    if pathPrediction_confidence is not None or pathPrediction_radiusOfCurve is not None:
        psm['pathPrediction'] = {}
        if pathPrediction_radiusOfCurve is None:
            print('pathPrediction_radiusOfCurve is mandatory! Please provide pathPrediction_radiusOfCurve. Set to 32767.')
            psm['pathPrediction']['radiusOfCurve'] = 32767
        elif not isinstance(pathPrediction_radiusOfCurve, (int, float)):
            print('pathPrediction_radiusOfCurve should be a number! But', pathPrediction_radiusOfCurve, 'is provided. Set to 32767.')
            psm['pathPrediction']['radiusOfCurve'] = 32767
        elif pathPrediction_radiusOfCurve >= 3276.7:
            print('pathPrediction_radiusOfCurve should be in range [-3276.7, 3276.7]! But', pathPrediction_radiusOfCurve, 'is provided. Set to 32767.')
            psm['pathPrediction']['radiusOfCurve'] = 32767
        elif pathPrediction_radiusOfCurve <= -3276.7:
            print('pathPrediction_radiusOfCurve should be in range [-3276.7, 3276.7]! But', pathPrediction_radiusOfCurve, 'is provided. Set to -32767.')
            psm['pathPrediction']['radiusOfCurve'] = -32767
        else:
            psm['pathPrediction']['radiusOfCurve'] = int(pathPrediction_radiusOfCurve * 10)

        if pathPrediction_confidence is None:
            print('pathPrediction_confidence is mandatory! Please provide pathPrediction_confidence. Set to 0.')
            psm['pathPrediction']['confidence'] = 0
        elif not isinstance(pathPrediction_confidence, (int, float)):
            print('pathPrediction_confidence should be a number! But', pathPrediction_confidence, 'is provided. Set to 0.')
            psm['pathPrediction']['confidence'] = 0
        elif pathPrediction_confidence < 0:
            print('pathPrediction_confidence should be in range [0, 100]! But', pathPrediction_confidence, 'is provided. Set to 0.')
            psm['pathPrediction']['confidence'] = 0
        elif pathPrediction_confidence > 100:
            print('pathPrediction_confidence should be in range [0, 100]! But', pathPrediction_confidence, 'is provided. Set to 200 (max).')
            psm['pathPrediction']['confidence'] = 200
        else:
            psm['pathPrediction']['confidence'] = int(pathPrediction_confidence * 2)

    if propulsion_type is not None or propulsion_value is not None:
        if propulsion_type is None:
            print('propulsion_type is mandatory if propulsion is provided! Remove propulsion.')
        elif propulsion_value is None:
            print('propulsion_value is mandatory if propulsion is provided! Remove propulsion.')
        elif propulsion_type == 'human':
            if propulsion_value in ['unavailable', 'otherTypes', 'onFoot', 'skateboard', 'pushOrKickScooter', 'wheelchair']:
                psm['propulsion'] = ('human', propulsion_value)
            else:
                print('propulsion_value for human should be one of unavailable, otherTypes, onFoot, skateboard, pushOrKickScooter, wheelchair! But', propulsion_value, 'is provided. Set to unavailable.')
                psm['propulsion'] = ('human', 'unavailable')
        elif propulsion_type == 'animal':
            if propulsion_value in ['unavailable', 'otherTypes', 'animalMounted', 'animalDrawnCarriage']:
                psm['propulsion'] = ('animal', propulsion_value)
            else:
                print('propulsion_value for animal should be one of unavailable, otherTypes, animalMounted, animalDrawnCarriage! But', propulsion_value, 'is provided. Set to unavailable.')
                psm['propulsion'] = ('animal', 'unavailable')
        elif propulsion_type == 'motor':
            if propulsion_value in ['unavailable', 'otherTypes', 'wheelChair', 'bicycle', 'scooter', 'selfBalancingDevice']:
                psm['propulsion'] = ('motor', propulsion_value)
            else:
                print('propulsion_value for motor should be one of unavailable, otherTypes, wheelChair, bicycle, scooter, selfBalancingDevice! But', propulsion_value, 'is provided. Set to unavailable.')
                psm['propulsion'] = ('motor', 'unavailable')
        else:
            print('propulsion_type should be one of human, animal, or motor! But', propulsion_type, 'is provided. Remove propulsion.')

    if useState is not None:
        if not isinstance(useState, int):
            print('useState should be an integer bitmask! But', useState, 'is provided. Remove it.')
        elif useState < 0 or useState > 511: 
            print('useState should be in range [0, 511] (9 bits)! But', useState, 'is provided. Remove it.')
        else:
            psm['useState'] = (useState, 9)

    if crossRequest is not None:
        if not isinstance(crossRequest, bool):
            print('crossRequest should be a boolean! But', crossRequest, 'is provided. Remove it.')
        else:
            psm['crossRequest'] = crossRequest

    if crossState is not None:
        if not isinstance(crossState, bool):
            print('crossState should be a boolean! But', crossState, 'is provided. Remove it.')
        else:
            psm['crossState'] = crossState

    if clusterSize is not None:
        if clusterSize in ['unavailable', 'small', 'medium', 'large']:
            psm['clusterSize'] = clusterSize
        else:
            print('clusterSize should be one of unavailable, small, medium, large! But', clusterSize, 'is provided. Set to unavailable.')
            psm['clusterSize'] = 'unavailable'

    if clusterRadius is not None:
        if not isinstance(clusterRadius, int):
            print('clusterRadius should be an integer! But', clusterRadius, 'is provided. Remove it.')
        elif clusterRadius < 0 or clusterRadius > 100:
            print('clusterRadius should be in range [0, 100] m! But', clusterRadius, 'is provided. Remove it.')
        else:
            psm['clusterRadius'] = clusterRadius

    if eventResponderType is not None:
        if eventResponderType in ['unavailable', 'towOperator', 'fireAndEMSWorker', 'aDOTWorker', 'lawEnforcement', 'hazmatResponder', 'animalControlWorker', 'otherPersonnel']:
            psm['eventResponderType'] = eventResponderType
        else:
            print('eventResponderType should be one of unavailable, towOperator, fireAndEMSWorker, aDOTWorker, lawEnforcement, hazmatResponder, animalControlWorker, otherPersonnel! But', eventResponderType, 'is provided. Set to unavailable')
            psm['eventResponderType'] = 'unavailable'
    
    if activityType is not None:
        if not isinstance(activityType, int):
            print('activityType should be an integer bitmask! But', activityType, 'is provided. Remove it')
        elif activityType < 0 or activityType > 63:
            print('activityType should be in a range [0, 63] (6 bit)! But', activityType, 'is porvided. Remove it')
        else:
            psm['activityType'] = (activityType, 6)
    
    if activitySubType is not None:
        if not isinstance(activitySubType, int):
            print('activitySubType should be an integer bitmask! But', activitySubType, 'is provided. Remove it')
        elif activitySubType < 0 or activitySubType > 127:
            print('activitySubType should be in a range [0, 127] (7 bit)! But', activitySubType, 'is porvided. Remove it')
        else:
            psm['activitySubType'] = (activitySubType, 7)

    if assistType is not None:
        if not isinstance(assistType, int):
            print('assistType should be an integer bitmask! But', assistType, 'is provided. Remove it')
        elif assistType < 0 or assistType > 63:
            print('assistType should be in a range [0, 63] (6 bit)! But', assistType, 'is porvided. Remove it')
        else:
            psm['assistType'] = (assistType, 6)

    if sizing is not None:
        if not isinstance(sizing, int):
            print('sizing should be an integer bitmask! But', sizing, 'is provided. Remove it')
        elif sizing < 0 or sizing > 31:
            print('sizing should be in a range [0, 31] (5 bit)! But', sizing, 'is porvided. Remove it')
        else:
            psm['sizing'] = (sizing, 5)

    if attachment is not None:
        if attachment in ['unavailable', 'stroller', 'bicycleTrailer', 'cart', 'wheelchair', 'otherWalkAssistAttachments', 'pet']:
            psm['attachment'] = attachment
        else:
            print('attachment should be one of unavailable, stroller, bicycleTrailer, cart, wheelchair, otherWalkAssistAttachments, pet! But', attachment, 'is provided. Set to unavailable')
            psm['attachment'] = 'unavailable'

    if attachmentRadius is not None:
        if not isinstance(attachmentRadius, int):
            print('attachmentRadius should be an integer! But', attachmentRadius, 'is provided. Remove it.')
        elif attachmentRadius < 0 or attachmentRadius > 200:
            print('attachmentRadius should be in range [0, 200] decimeter! But', attachmentRadius, 'is provided. Remove it.')
        else:
            psm['attachmentRadius'] = attachmentRadius

    if animalType is not None:
        if animalType in ['unavailable', 'serviceUse', 'pet', 'farm']:
            psm['animalType'] = animalType
        else:
            print('animalType should be one of unavailable, serviceUse, pet, farm! But', animalType, 'is provided. Set to unavailable')
            psm['animalType'] = 'unavailable'

    header_psm = {
        'messageId': 32,
        'value': ('PersonalSafetyMessage', psm)
    }

    header_psm_msg = v2xlib.MessageFrame.MessageFrame
    header_psm_msg.set_val(header_psm)
    hex_psm = hexlify(header_psm_msg.to_uper())
    return hex_psm.decode('utf-8')