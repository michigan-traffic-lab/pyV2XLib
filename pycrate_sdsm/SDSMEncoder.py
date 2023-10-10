from pycrate_sdsm import SDSM
from binascii import hexlify, unhexlify


def sdsm_encoder(msgCnt=None,
                 sourceID=None,
                 equipmentType=None,
                 sDSMTimeStamp_year = None,  # optional
                 sDSMTimeStamp_month = None,  # optional
                 sDSMTimeStamp_day=None,  # optional
                 sDSMTimeStamp_hour=None,  # optional
                 sDSMTimeStamp_minute=None,  # optional
                 sDSMTimeStamp_second=None,  # optional
                 sDSMTimeStamp_offset=None,  # optional
                 refPos_lat=None,
                 refPos_long=None,
                 refPos_elevation=None,  # optional
                 refPosXYConf_semiMajor=None,
                 refPosXYConf_semiMinor=None,
                 refPosXYConf_orientation=None,
                 refPosElConf=None,  # optional
                 objects_N=0,
                 objects_detObjCommon_objType=[],
                 objects_detObjCommon_objTypeCfd=[],
                 objects_detObjCommon_objectID=[],
                 objects_detObjCommon_measurementTime=[],
                 objects_detObjCommon_timeConfidence=[],
                 objects_detObjCommon_pos_offsetX=[],
                 objects_detObjCommon_pos_offsetY=[],
                 objects_detObjCommon_pos_offsetZ=[],  # optional
                 objects_detObjCommon_posConfidence_pos=[],
                 objects_detObjCommon_posConfidence_elevation=[],
                 objects_detObjCommon_speed=[],
                 objects_detObjCommon_speedConfidence=[],
                 objects_detObjCommon_speedZ=[],  # optional
                 objects_detObjCommon_speedConfidenceZ=[],  # optional
                 objects_detObjCommon_heading=[],
                 objects_detObjCommon_headingConf=[],
                 objects_detObjCommon_accel4way_lat=[],  # optional
                 objects_detObjCommon_accel4way_long=[],  # optional
                 objects_detObjCommon_accel4way_vert=[],  # optional
                 objects_detObjCommon_accel4way_yaw=[],  # optional
                 objects_detObjCommon_accCfdX=[],  # optional
                 objects_detObjCommon_accCfdY=[],  # optional
                 objects_detObjCommon_accCfdZ=[],  # optional
                 objects_detObjCommon_accCfdYaw=[],  # optional

                 objects_detObjOptData_type=[],
                 objects_detObjOptData_detVeh_lights=[],  # optional
                 objects_detObjOptData_detVeh_vehAttitude_pitch=[],  # optional
                 objects_detObjOptData_detVeh_vehAttitude_roll=[],  # optional
                 objects_detObjOptData_detVeh_vehAttitude_yaw=[],  # optional
                 objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence=[],  # optional
                 objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence=[],  # optional
                 objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence=[],  # optional
                 objects_detObjOptData_detVeh_vehAngleVel_pitchRate=[],  # optional
                 objects_detObjOptData_detVeh_vehAngleVel_rollRate=[],  # optional
                 objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence=[],  # optional
                 objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence=[],  # optional
                 objects_detObjOptData_detVeh_size_width=[],  # optional
                 objects_detObjOptData_detVeh_size_length=[],  # optional
                 objects_detObjOptData_detVeh_height=[],  # optional
                 objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence=[],  # optional
                 objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence=[],  # optional
                 objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence=[],  # optional
                 objects_detObjOptData_detVeh_vehicleClass=[],  # optional
                 objects_detObjOptData_detVeh_classConf=[],  # optional
                 objects_detObjOptData_detVRU_basicType=[],  # optional
                 objects_detObjOptData_detVRU_propulsion=[],  # optional
                 objects_detObjOptData_detVRU_propulsion_human=[],  # optional
                 objects_detObjOptData_detVRU_propulsion_animal=[],  # optional
                 objects_detObjOptData_detVRU_propulsion_motor=[],  # optional
                 objects_detObjOptData_detVRU_attachment=[],  # optional
                 objects_detObjOptData_detVRU_radius=[],  # optional
                 objects_detObjOptData_detObst_obstSize_width=[],  # optional
                 objects_detObjOptData_detObst_obstSize_length=[],  # optional
                 objects_detObjOptData_detObst_obstSize_height=[],  # optional
                 objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence=[],  # optional
                 objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence=[],  # optional
                 objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence=[],  # optional
                 ):
    '''
    This function encodes SDSM message.

    Args:
        msgCnt (int): Message counter. Range: [0, 127]. Mandatory.
        sourceID (bytes): Source ID. Range: [0, 255]. Mandatory.
        equipmentType (str): Equipment type. One of unknown, rsu, obu, or vru. Mandatory.
        sDSMTimeStamp_year (int): Year of the timestamp. Range: [0, 4095]. Optional.
        sDSMTimeStamp_month (int): Month of the timestamp. Range: [0, 12]. Optional.
        sDSMTimeStamp_day (int): Day of the timestamp. Range: [0, 31]. Optional.
        sDSMTimeStamp_hour (int): Hour of the timestamp. Range: [0, 31]. Unit: hour. Optional.
        sDSMTimeStamp_minute (int): Minute of the timestamp. Range: [0, 60]. Unit: minute. Optional.
        sDSMTimeStamp_second (float): Second of the timestamp. Range: [0, 65.535]. Unit: second. Optional.
        sDSMTimeStamp_offset (int): Offset of the timestamp. Range: [-840, 840]. Unit: minute. Optional.
        refPos_lat (float): Latitude of the information source. Range: [-90, 90]. Unit: deg. Mandatory.
        refPos_long (float): Longitude of the information source. Range: [-180, 180]. Unit: deg. Mandatory.
        refPos_elevation (float): Elevation of the information source. Range: [-409.6, 6143.9]. Unit: meter. Optional.
        refPosXYConf_semiMajor (float): Radius of the semi-major axis of an ellipsoid. Range: [0, 12.7]. Unit: meter. Mandatory.
        refPosXYConf_semiMinor (float): Radius of the semi-minor axis of an ellipsoid. Range: [0, 12.7]. Unit: meter. Mandatory.
        refPosXYConf_orientation (float): Orientation of the angle of the semi-major axis of an ellipsoid. Range: [0, 359.9945078786]. Unit: deg. Mandatory.
        refPosElConf (float): Elevation confidence. Range: [0, 550]. Unit: meter. Optional.
        objects_N (int): Number of detected objects. Range: [1, 127]. Mandatory.
        objects_detObjCommon_objType (list): Object type. One of unknown, vehicle, vru, or animal. Mandatory.
        objects_detObjCommon_objTypeCfd (list): Object type confidence. Range: [0, 101]. Unit: percent. Mandatory.
        objects_detObjCommon_objectID (list): Object ID. Range: [0, 65535]. Mandatory.
        objects_detObjCommon_measurementTime (list): Measurement time. Range: [-1.5, 1.5]. Unit: second. Mandatory.
        objects_detObjCommon_timeConfidence (list): Time confidence. Range: [0, 110]. Unit: percent. Mandatory.
        objects_detObjCommon_pos_offsetX (list): Offset of the object position in X-axis. Range: [-3276.7, 3276.7]. Unit: meter. Mandatory.
        objects_detObjCommon_pos_offsetY (list): Offset of the object position in Y-axis. Range: [-3276.7, 3276.7]. Unit: meter. Mandatory.
        objects_detObjCommon_pos_offsetZ (list): Offset of the object position in Z-axis. Range: [-3276.7, 3276.7]. Unit: meter. Optional.
        objects_detObjCommon_posConfidence_pos (list): Position confidence. Range: [0, 550]. Unit: meter. Mandatory.
        objects_detObjCommon_posConfidence_elevation (list): Elevation confidence. Range: [0, 550]. Unit: meter. Mandatory.
        objects_detObjCommon_speed (list): Speed of the object. Range: [0, 163.8]. Unit: m/s. Mandatory.
        objects_detObjCommon_speedConfidence (list): Speed confidence. Range: [0, 110]. Unit: percent. Mandatory.
        objects_detObjCommon_speedZ (list): Speed of the object in Z-axis. Range: [0, 163.82]. Unit: m/s. Optional.
        objects_detObjCommon_speedConfidenceZ (list): Speed confidence in Z-axis. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjCommon_heading (list): Heading of the object. Range: [0, 360]. Unit: deg. Mandatory.
        objects_detObjCommon_headingConf (list): Heading confidence. Range: [0, 12]. Unit: deg. Mandatory.
        objects_detObjCommon_accel4way_lat (list): Lateral acceleration of the object. Range: [-20, 20.01]. Unit: m/s^2. Optional.
        objects_detObjCommon_accel4way_long (list): Longitudinal acceleration of the object. Range: [-20, 20.01]. Unit: m/s^2. Optional.
        objects_detObjCommon_accel4way_vert (list): Vertical acceleration of the object. Range: [-24.9174, 24.9174]. Unit: m/s^2. Optional.
        objects_detObjCommon_accel4way_yaw (list): Yaw rate of the object. Range: [-327.67, 327.67]. Unit: deg/s. Optional.
        objects_detObjCommon_accCfdX (list): Lateral acceleration confidence. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjCommon_accCfdY (list): Longitudinal acceleration confidence. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjCommon_accCfdZ (list): Vertical acceleration confidence. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjCommon_accCfdYaw (list): Yaw rate confidence. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjOptData_type (list): Object type. One of Veh, VRU, or Obst. Optional.
        objects_detObjOptData_detVeh_lights (list): Light status. One of 0, 1, 2, 3, 4, 5, 6, 7, or 8. Optional.
        objects_detObjOptData_detVeh_vehAttitude_pitch (list): Pitch of the vehicle. Range: [-90, 90]. Unit: deg. Optional.
        objects_detObjOptData_detVeh_vehAttitude_roll (list): Roll of the vehicle. Range: [-180, 180]. Unit: deg. Optional.
        objects_detObjOptData_detVeh_vehAttitude_yaw (list): Yaw of the vehicle. Range: [-180, 180]. Unit: deg. Optional.
        objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence (list): Pitch confidence. Range: [0, 12]. Unit: deg. Optional.
        objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence (list): Roll confidence. Range: [0, 12]. Unit: deg. Optional.
        objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence (list): Yaw confidence. Range: [0, 12]. Unit: deg. Optional.
        objects_detObjOptData_detVeh_vehAngleVel_pitchRate (list): Pitch rate of the vehicle. Range: [-327.67, 327.67]. Unit: deg/s. Optional.
        objects_detObjOptData_detVeh_vehAngleVel_rollRate (list): Roll rate of the vehicle. Range: [-327.67, 327.67]. Unit: deg/s. Optional.
        objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence (list): Pitch rate confidence. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence (list): Roll rate confidence. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjOptData_detVeh_size_width (list): Width of the vehicle. Range: [0, 15.99]. Unit: meter. Optional.
        objects_detObjOptData_detVeh_size_length (list): Length of the vehicle. Range: [0, 15.99]. Unit: meter. Optional.
        objects_detObjOptData_detVeh_height (list): Height of the vehicle. Range: [0, 6.35]. Unit: meter. Optional.
        objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence (list): Vehicle width confidence. Range: [0, 120]. Unit: percent. Optional.
        objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence (list): Vehicle length confidence. Range: [0, 120]. Unit: percent. Optional.
        objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence (list): Vehicle height confidence. Range: [0, 120]. Unit: percent. Optional.
        objects_detObjOptData_detVeh_vehicleClass (list): Vehicle class. Range: [0, 255]. Optional.
        objects_detObjOptData_detVeh_classConf (list): Vehicle class confidence. Range: [0, 110]. Unit: percent. Optional.
        objects_detObjOptData_detVRU_basicType (list): Basic type of the VRU. Range: [0, 255]. Optional.
        objects_detObjOptData_detVRU_propulsion (list): Propulsion of the VRU. Range: [0, 255]. Optional.
        objects_detObjOptData_detVRU_propulsion_human (list): Propulsion of the VRU. Range: [0, 255]. Optional.
        objects_detObjOptData_detVRU_propulsion_animal (list): Propulsion of the VRU. Range: [0, 255]. Optional.
        objects_detObjOptData_detVRU_propulsion_motor (list): Propulsion of the VRU. Range: [0, 255]. Optional.
        objects_detObjOptData_detVRU_attachment (list): Attachment of the VRU. Range: [0, 255]. Optional.
        objects_detObjOptData_detVRU_radius (list): Radius of the VRU. Range: [0, 255]. Optional.
        objects_detObjOptData_detObst_obstSize_width (list): Width of the obstacle. Range: [0, 15.99]. Unit: meter. Optional.
        objects_detObjOptData_detObst_obstSize_length (list): Length of the obstacle. Range: [0, 15.99]. Unit: meter. Optional.
        objects_detObjOptData_detObst_obstSize_height (list): Height of the obstacle. Range: [0, 6.35]. Unit: meter. Optional.
        objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence (list): Obstacle width confidence. Range: [0, 120]. Unit: percent. Optional.
        objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence (list): Obstacle length confidence. Range: [0, 120]. Unit: percent. Optional.
        objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence (list): Obstacle height confidence. Range: [0, 120]. Unit: percent. Optional.

    Returns:
        sdsm (bytes): SDSM message.
    '''
    # convert input to correct format
    sdsm = {}

    if msgCnt is None:
        print('msgCnt is mandatory! Please provide msgCnt. Set to 0.')
        sdsm['msgCnt'] = 0
    elif not isinstance(msgCnt, int):
        print('msgCnt should be an integer! But', msgCnt, 'is provided. Set to 0.')
        sdsm['msgCnt'] = 0
    elif msgCnt < 0 or msgCnt > 127:
        print('msgCnt should be in range [0, 127]! But', msgCnt, 'is provided. Set to 0.')
        sdsm['msgCnt'] = 0
    else:
        sdsm['msgCnt'] = msgCnt

    if sourceID is None:
        print('sourceID is mandatory! Please provide sourceID. Set to tmp.')
        sdsm['sourceID'] = b'tmp'
    else:
        sdsm['sourceID'] = sourceID

    if equipmentType is None:
        print('equipmentType is mandatory! Please provide equipmentType. Set to unknown.')
        sdsm['sourceID'] = b'unknown'
    elif equipmentType in ['unknown', 'rsu', 'obu', 'vru']:
        sdsm['equipmentType'] = equipmentType
    else:
        print('equipmentType should be one of unknown, rsu, obu, or vru! But', equipmentType, 'is provided. Set to unknown.')
        sdsm['equipmentType'] = 'unknown'

    sdsm['sDSMTimeStamp'] = {}
    if sDSMTimeStamp_year is not None:
        if not isinstance(sDSMTimeStamp_year, int):
            print('sDSMTimeStamp_year should be an integer! But', sDSMTimeStamp_year, 'is provided. Remove it.')
        elif sDSMTimeStamp_year < 0 or sDSMTimeStamp_year > 4095:
            print('sDSMTimeStamp_year should be in range [0, 4095]! But', sDSMTimeStamp_year, 'is provided. Remove it.')
        else:
            sdsm['sDSMTimeStamp']['year'] = sDSMTimeStamp_year
    if sDSMTimeStamp_month is not None:
        if not isinstance(sDSMTimeStamp_month, int):
            print('sDSMTimeStamp_month should be an integer! But', sDSMTimeStamp_month, 'is provided. Remove it.')
        elif sDSMTimeStamp_month < 0 or sDSMTimeStamp_month > 12:
            print('sDSMTimeStamp_month should be in range [0, 12]! But', sDSMTimeStamp_month, 'is provided. Remove it.')
        else:
            sdsm['sDSMTimeStamp']['month'] = sDSMTimeStamp_month
    if sDSMTimeStamp_day is not None:
        if not isinstance(sDSMTimeStamp_day, int):
            print('sDSMTimeStamp_day should be an integer! But', sDSMTimeStamp_day, 'is provided. Remove it.')
        elif sDSMTimeStamp_day < 0 or sDSMTimeStamp_day > 31:
            print('sDSMTimeStamp_day should be in range [0, 31]! But', sDSMTimeStamp_day, 'is provided. Remove it.')
        else:
            sdsm['sDSMTimeStamp']['day'] = sDSMTimeStamp_day
    if sDSMTimeStamp_hour is not None:
        if not isinstance(sDSMTimeStamp_hour, int):
            print('sDSMTimeStamp_hour should be an integer! But', sDSMTimeStamp_hour, 'is provided. Remove it.')
        elif sDSMTimeStamp_hour < 0 or sDSMTimeStamp_hour > 31:
            print('sDSMTimeStamp_hour should be in range [0, 31] h! But', sDSMTimeStamp_hour, 'is provided. Remove it.')
        else:
            sdsm['sDSMTimeStamp']['hour'] = sDSMTimeStamp_hour
    if sDSMTimeStamp_minute is not None:
        if not isinstance(sDSMTimeStamp_minute, int):
            print('sDSMTimeStamp_minute should be an integer! But', sDSMTimeStamp_minute, 'is provided. Remove it.')
        elif sDSMTimeStamp_minute < 0 or sDSMTimeStamp_minute > 60:
            print('sDSMTimeStamp_minute should be in range [0, 60] min! But', sDSMTimeStamp_minute, 'is provided. Remove it.')
        else:
            sdsm['sDSMTimeStamp']['minute'] = sDSMTimeStamp_minute
    if sDSMTimeStamp_second is not None:
        if sDSMTimeStamp_second < 0 or sDSMTimeStamp_second > 65.535:
            print('sDSMTimeStamp_second should be in range [0, 65.535] s! But', sDSMTimeStamp_second, 'is provided. Remove it.')
        else:
            sdsm['sDSMTimeStamp']['second'] = int(sDSMTimeStamp_second * 10**3)
    if sDSMTimeStamp_offset is not None:
        if not isinstance(sDSMTimeStamp_offset, int):
            print('sDSMTimeStamp_offset should be an integer! But', sDSMTimeStamp_offset, 'is provided. Remove it.')
        elif sDSMTimeStamp_offset < -840 or sDSMTimeStamp_offset > 840:
            print('sDSMTimeStamp_offset should be in range [-840, 840] min! But', sDSMTimeStamp_offset, 'is provided. Remove it.')
        else:
            sdsm['sDSMTimeStamp']['offset'] = sDSMTimeStamp_offset

    sdsm['refPos'] = {}
    if refPos_lat is None:
        print('refPos_lat is mandatory! Please provide the latitude of information source. Set to 90.0000001.')
        sdsm['refPos']['lat'] = 900000001
    elif refPos_lat < -90 or refPos_lat > 90:
        print('refPos_lat should be in range [-90, 90] deg! But', refPos_lat, 'is provided. Set to 90.0000001.')
        sdsm['refPos']['lat'] = 900000001
    else:
        sdsm['refPos']['lat'] = int(refPos_lat * 10 ** 7)
    if refPos_long is None:
        print('refPos_long is mandatory! Please provide the longitude of information source. Set to 180.0000001.')
        sdsm['refPos']['long'] = 1800000001
    elif refPos_long < -179.9999999 or refPos_long > 180:
        print('refPos_long should be in range [-179.9999999, 180] deg! But', refPos_long, 'is provided. Set to 180.0000001.')
        sdsm['refPos']['long'] = 1800000001
    else:
        sdsm['refPos']['long'] = int(refPos_long * 10 ** 7)
    if refPos_elevation is not None:
        if refPos_elevation < -409.5 or refPos_elevation > 6143.9:
            print('refPos_elevation should be in range [-409.5, 6143.9] deg! But', refPos_elevation, 'is provided. Set to -409.6.')
            sdsm['refPos']['elevation'] = -4096
        else:
            sdsm['refPos']['elevation'] = int(refPos_elevation * 10)
    
    sdsm['refPosXYConf'] = {}
    if refPosXYConf_semiMajor is None:
        print('refPosXYConf_semiMajor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
        sdsm['refPosXYConf']['semiMajor'] = 255
    elif refPosXYConf_semiMajor < 0:
        print('refPosXYConf_semiMajor should be in range [0, 12.7] m! But', refPosXYConf_semiMajor, 'is provided. Set to 12.75.')
        sdsm['refPosXYConf']['semiMajor'] = 255
    elif refPosXYConf_semiMajor > 12.7:
        print('refPosXYConf_semiMajor should be in range [0, 12.7] m! But', refPosXYConf_semiMajor, 'is provided. Set to 12.7.')
        sdsm['refPosXYConf']['semiMajor'] = 254
    else:
        sdsm['refPosXYConf']['semiMajor'] = int(refPosXYConf_semiMajor * 20)
    if refPosXYConf_semiMinor is None:
        print('refPosXYConf_semiMinor is mandatory! Please provide the radius of the semi-minor axis of an ellipsoid. Set to 12.75.')
        sdsm['refPosXYConf']['semiMinor'] = 255
    elif refPosXYConf_semiMinor < 0:
        print('refPosXYConf_semiMinor should be in range [0, 12.7] m! But', refPosXYConf_semiMinor, 'is provided. Set to 12.75.')
        sdsm['refPosXYConf']['semiMinor'] = 255
    elif refPosXYConf_semiMinor > 12.7:
        print('refPosXYConf_semiMinor should be in range [0, 12.7] m! But', refPosXYConf_semiMinor, 'is provided. Set to 12.7.')
        sdsm['refPosXYConf']['semiMinor'] = 254
    else:
        sdsm['refPosXYConf']['semiMinor'] = int(refPosXYConf_semiMinor * 20)
    if refPosXYConf_orientation is None:
        print('refPosXYConf_orientation is mandatory! Please provide the orientation of the angle of the semi-major axis of an ellipsoid. Set to 12.75.')
        sdsm['refPosXYConf']['orientation'] = 65535
    elif refPosXYConf_orientation < 0 or refPosXYConf_orientation > 359.9945078786:
        print('refPosXYConf_orientation should be in range [0, 359.9945078786] deg! But', refPosXYConf_orientation, 'is provided. Set to 360.')
        sdsm['refPosXYConf']['orientation'] = 65535
    else:
        sdsm['refPosXYConf']['orientation'] = int(refPosXYConf_orientation / 360 * 65535)

    if refPosElConf is not None:
        if refPosElConf <= 0:
            print('refPosElConf should be greater than 0 m! But', refPosElConf, 'is provided. Remove it.')
        elif 0 < refPosElConf <= 0.01:
            sdsm['refPosElConf'] = 'elev-000-01'
        elif 0.01 < refPosElConf <= 0.02:
            sdsm['refPosElConf'] = 'elev-000-02'
        elif 0.02 < refPosElConf <= 0.05:
            sdsm['refPosElConf'] = 'elev-000-05'
        elif 0.05 < refPosElConf <= 0.1:
            sdsm['refPosElConf'] = 'elev-000-10'
        elif 0.1 < refPosElConf <= 0.2:
            sdsm['refPosElConf'] = 'elev-000-20'
        elif 0.2 < refPosElConf <= 0.5:
            sdsm['refPosElConf'] = 'elev-000-50'
        elif 0.5 < refPosElConf <= 1:
            sdsm['refPosElConf'] = 'elev-001-00'
        elif 1 < refPosElConf <= 2:
            sdsm['refPosElConf'] = 'elev-002-00'
        elif 2 < refPosElConf <= 5:
            sdsm['refPosElConf'] = 'elev-005-00'
        elif 5 < refPosElConf <= 10:
            sdsm['refPosElConf'] = 'elev-010-00'
        elif 10 < refPosElConf <= 20:
            sdsm['refPosElConf'] = 'elev-020-00'
        elif 20 < refPosElConf <= 50:
            sdsm['refPosElConf'] = 'elev-050-00'
        elif 50 < refPosElConf <= 100:
            sdsm['refPosElConf'] = 'elev-100-00'
        elif 100 < refPosElConf <= 200:
            sdsm['refPosElConf'] = 'elev-200-00'
        elif 200 < refPosElConf <= 500:
            sdsm['refPosElConf'] = 'elev-500-00'
        elif 500 < refPosElConf:
            sdsm['refPosElConf'] = 'unavailable'

    sdsm['objects'] = []
    for i in range(objects_N):
        detected_object = {}
        detected_object['detObjCommon'] = {}

        if len(objects_detObjCommon_objType) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_objType but there are only', len(objects_detObjCommon_objType), 'of it!')
            break
        elif objects_detObjCommon_objType[i] not in ['unknown', 'vehicle', 'vru', 'animal']:
            print('Object', i, ': objects_detObjCommon_objType should be one of unknown, vehicle, vru, or animal! But', objects_detObjCommon_objType[i], 'is provided. Set to unknown.')
            detected_object['detObjCommon']['objType'] = 'unknown'
        else:
            detected_object['detObjCommon']['objType'] = objects_detObjCommon_objType[i]
        
        if len(objects_detObjCommon_objTypeCfd) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_objTypeCfd but there are only', len(objects_detObjCommon_objTypeCfd), 'of it!')
            break
        elif not isinstance(objects_detObjCommon_objTypeCfd[i], int):
            print('Object', i, ': objects_detObjCommon_objTypeCfd should be an integer! But', objects_detObjCommon_objTypeCfd[i], 'is provided. Set to 0 (unknown).')
            detected_object['detObjCommon']['objTypeCfd'] = 0
        elif objects_detObjCommon_objTypeCfd[i] < 0 or objects_detObjCommon_objTypeCfd[i] > 101:
            print('Object', i, ': objects_detObjCommon_objTypeCfd should be in range [0, 101]! But', objects_detObjCommon_objTypeCfd[i], 'is provided. Set to 0 (unknown).')
            detected_object['detObjCommon']['objTypeCfd'] = 0
        else:
            detected_object['detObjCommon']['objTypeCfd'] = objects_detObjCommon_objTypeCfd[i]

        if len(objects_detObjCommon_objectID) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_objectID but there are only', len(objects_detObjCommon_objectID), 'of it!')
            break
        elif not isinstance(objects_detObjCommon_objectID[i], int):
            print('Object', i, ': objects_detObjCommon_objectID should be an integer! But', objects_detObjCommon_objectID[i], 'is provided. Set to 0.')
            detected_object['detObjCommon']['objectID'] = 0
        elif objects_detObjCommon_objectID[i] < 0 or objects_detObjCommon_objectID[i] > 65535:
            print('Object', i, ': objects_detObjCommon_objectID should be in range [0, 65535]! But', objects_detObjCommon_objectID[i], 'is provided. Set to 0.')
            detected_object['detObjCommon']['objectID'] = 0
        else:
            detected_object['detObjCommon']['objectID'] = objects_detObjCommon_objectID[i]
        
        if len(objects_detObjCommon_measurementTime) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_measurementTime but there are only', len(objects_detObjCommon_measurementTime), 'of it!')
            break
        elif objects_detObjCommon_measurementTime[i] < -1.5 or objects_detObjCommon_measurementTime[i] > 1.5:
            print('Object', i, ': objects_detObjCommon_measurementTime should be in range [-1.5, 1.5] s! But', objects_detObjCommon_measurementTime[i], 'is provided. Set to 0.')
            detected_object['detObjCommon']['measurementTime'] = 0
        else:
            detected_object['detObjCommon']['measurementTime'] = int(objects_detObjCommon_measurementTime[i] * 1000)
        
        if len(objects_detObjCommon_timeConfidence) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_timeConfidence but there are only', len(objects_detObjCommon_timeConfidence), 'of it!')
            break
        elif objects_detObjCommon_timeConfidence[i] <= 0:
            print('Object', i, ': objects_detObjCommon_timeConfidence should be greater than 0 s! But', objects_detObjCommon_timeConfidence[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['timeConfidence'] = 'unavailable'
        elif 0 < objects_detObjCommon_timeConfidence[i] <= 1e-11:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-000-01'
        elif 1e-11 < objects_detObjCommon_timeConfidence[i] <= 2e-11:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-000-02'
        elif 2e-11 < objects_detObjCommon_timeConfidence[i] <= 5e-11:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-000-05'
        elif 5e-11 < objects_detObjCommon_timeConfidence[i] <= 1e-10:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-000-1'
        elif 1e-10 < objects_detObjCommon_timeConfidence[i] <= 2e-10:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-000-2'
        elif 2e-10 < objects_detObjCommon_timeConfidence[i] <= 5e-10:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-000-5'
        elif 5e-10 < objects_detObjCommon_timeConfidence[i] <= 1e-9:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-001'
        elif 1e-9 < objects_detObjCommon_timeConfidence[i] <= 2e-9:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-002'
        elif 2e-9 < objects_detObjCommon_timeConfidence[i] <= 5e-9:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-005'
        elif 5e-9 < objects_detObjCommon_timeConfidence[i] <= 1e-8:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-01'
        elif 1e-8 < objects_detObjCommon_timeConfidence[i] <= 2e-8:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-02'
        elif 2e-8 < objects_detObjCommon_timeConfidence[i] <= 5e-8:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-05'
        elif 5e-8 < objects_detObjCommon_timeConfidence[i] <= 1e-7:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-1'
        elif 1e-7 < objects_detObjCommon_timeConfidence[i] <= 2e-7:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-2'
        elif 2e-7 < objects_detObjCommon_timeConfidence[i] <= 5e-7:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-000-5'
        elif 5e-7 < objects_detObjCommon_timeConfidence[i] <= 1e-6:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-001'
        elif 1e-6 < objects_detObjCommon_timeConfidence[i] <= 2e-6:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-002'
        elif 2e-6 < objects_detObjCommon_timeConfidence[i] <= 5e-6:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-005'
        elif 5e-6 < objects_detObjCommon_timeConfidence[i] <= 1e-5:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-01'
        elif 1e-5 < objects_detObjCommon_timeConfidence[i] <= 2e-5:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-02'
        elif 2e-5 < objects_detObjCommon_timeConfidence[i] <= 5e-5:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-05'
        elif 5e-5 < objects_detObjCommon_timeConfidence[i] <= 1e-4:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-1'
        elif 1e-4 < objects_detObjCommon_timeConfidence[i] <= 2e-4:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-2'
        elif 2e-4 < objects_detObjCommon_timeConfidence[i] <= 5e-4:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-000-5'
        elif 5e-4 < objects_detObjCommon_timeConfidence[i] <= 1e-3:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-001'
        elif 1e-3 < objects_detObjCommon_timeConfidence[i] <= 2e-3:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-002'
        elif 2e-3 < objects_detObjCommon_timeConfidence[i] <= 5e-3:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-005'
        elif 5e-3 < objects_detObjCommon_timeConfidence[i] <= 1e-2:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-010'
        elif 1e-2 < objects_detObjCommon_timeConfidence[i] <= 2e-2:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-020'
        elif 2e-2 < objects_detObjCommon_timeConfidence[i] <= 5e-2:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-050'
        elif 5e-2 < objects_detObjCommon_timeConfidence[i] <= 1e-1:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-100'
        elif 1e-1 < objects_detObjCommon_timeConfidence[i] <= 2e-1:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-200'
        elif 2e-1 < objects_detObjCommon_timeConfidence[i] <= 5e-1:
            detected_object['detObjCommon']['timeConfidence'] = 'time-000-500'
        elif 5e-1 < objects_detObjCommon_timeConfidence[i] <= 1:
            detected_object['detObjCommon']['timeConfidence'] = 'time-001-000'
        elif 1 < objects_detObjCommon_timeConfidence[i] <= 2:
            detected_object['detObjCommon']['timeConfidence'] = 'time-002-000'
        elif 2 < objects_detObjCommon_timeConfidence[i] <= 10:
            detected_object['detObjCommon']['timeConfidence'] = 'time-010-000'
        elif 10 < objects_detObjCommon_timeConfidence[i] <= 20:
            detected_object['detObjCommon']['timeConfidence'] = 'time-020-000'
        elif 20 < objects_detObjCommon_timeConfidence[i] <= 50:
            detected_object['detObjCommon']['timeConfidence'] = 'time-050-000'
        elif 50 < objects_detObjCommon_timeConfidence[i] <= 100:
            detected_object['detObjCommon']['timeConfidence'] = 'time-100-000'
        elif 100 < objects_detObjCommon_timeConfidence[i]:
            detected_object['detObjCommon']['timeConfidence'] = 'unavailable'
        
        detected_object['detObjCommon']['pos'] = {}
        if len(objects_detObjCommon_pos_offsetX) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_pos_offsetX but there are only', len(objects_detObjCommon_pos_offsetX), 'of it!')
            break
        elif objects_detObjCommon_pos_offsetX[i] < -3276.7 or objects_detObjCommon_pos_offsetX[i] > 3276.7:
            print('Object', i, ': objects_detObjCommon_pos_offsetX should be in range [-3276.7, 3276.7] s! But', objects_detObjCommon_pos_offsetX[i], 'is provided. Set to 0.')
            detected_object['detObjCommon']['pos']['offsetX'] = 0
        else:
            detected_object['detObjCommon']['pos']['offsetX'] = int(objects_detObjCommon_pos_offsetX[i] * 10)
        
        if len(objects_detObjCommon_pos_offsetY) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_pos_offsetY but there are only', len(objects_detObjCommon_pos_offsetY), 'of it!')
            break
        elif objects_detObjCommon_pos_offsetY[i] < -3276.7 or objects_detObjCommon_pos_offsetY[i] > 3276.7:
            print('Object', i, ': objects_detObjCommon_pos_offsetY should be in range [-3276.7, 3276.7] s! But', objects_detObjCommon_pos_offsetY[i], 'is provided. Set to 0.')
            detected_object['detObjCommon']['pos']['offsetY'] = 0
        else:
            detected_object['detObjCommon']['pos']['offsetY'] = int(objects_detObjCommon_pos_offsetY[i] * 10)
        
        if len(objects_detObjCommon_pos_offsetZ) > i:
            if objects_detObjCommon_pos_offsetZ[i] < -3276.7 or objects_detObjCommon_pos_offsetZ[i] > 3276.7:
                print('Object', i, ': objects_detObjCommon_pos_offsetZ should be in range [-3276.7, 3276.7] s! But', objects_detObjCommon_pos_offsetZ[i], 'is provided. Remove it.')
                detected_object['detObjCommon']['pos']['offsetZ'] = 0
            else:
                detected_object['detObjCommon']['pos']['offsetZ'] = int(objects_detObjCommon_pos_offsetZ[i] * 10)
        
        detected_object['detObjCommon']['posConfidence'] = {}
        if len(objects_detObjCommon_posConfidence_pos) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_posConfidence_pos but there are only', len(objects_detObjCommon_posConfidence_pos), 'of it!')
            break
        elif objects_detObjCommon_posConfidence_pos[i] <= 0:
            print('Object', i, ': objects_detObjCommon_posConfidence_pos should be greater than 0 m! But', objects_detObjCommon_posConfidence_pos[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['posConfidence']['pos'] = 'unavailable'
        elif 0 < objects_detObjCommon_posConfidence_pos[i] <= 0.01:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a1cm'
        elif 0.01 < objects_detObjCommon_posConfidence_pos[i] <= 0.02:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a2cm'
        elif 0.02 < objects_detObjCommon_posConfidence_pos[i] <= 0.05:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a5cm'
        elif 0.05 < objects_detObjCommon_posConfidence_pos[i] <= 0.1:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a10cm'
        elif 0.1 < objects_detObjCommon_posConfidence_pos[i] <= 0.2:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a20cm'
        elif 0.2 < objects_detObjCommon_posConfidence_pos[i] <= 0.5:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a50cm'
        elif 0.5 < objects_detObjCommon_posConfidence_pos[i] <= 1:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a1m'
        elif 1 < objects_detObjCommon_posConfidence_pos[i] <= 2:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a2m'
        elif 2 < objects_detObjCommon_posConfidence_pos[i] <= 5:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a5m'
        elif 5 < objects_detObjCommon_posConfidence_pos[i] <= 10:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a10m'
        elif 10 < objects_detObjCommon_posConfidence_pos[i] <= 20:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a20m'
        elif 20 < objects_detObjCommon_posConfidence_pos[i] <= 50:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a50m'
        elif 50 < objects_detObjCommon_posConfidence_pos[i] <= 100:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a100m'
        elif 100 < objects_detObjCommon_posConfidence_pos[i] <= 200:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a200m'
        elif 200 < objects_detObjCommon_posConfidence_pos[i] <= 500:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'a500m'
        elif 500 < objects_detObjCommon_posConfidence_pos[i]:
            detected_object['detObjCommon']['posConfidence']['pos'] = 'unavailable'
        if len(objects_detObjCommon_posConfidence_elevation) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_posConfidence_elevation but there are only', len(objects_detObjCommon_posConfidence_elevation), 'of it!')
            break
        elif objects_detObjCommon_posConfidence_elevation[i] <= 0:
            print('Object', i, ': objects_detObjCommon_posConfidence_elevation should be greater than 0 m! But', objects_detObjCommon_posConfidence_elevation[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'unavailable'
        elif 0 < objects_detObjCommon_posConfidence_elevation[i] <= 0.01:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-000-01'
        elif 0.01 < objects_detObjCommon_posConfidence_elevation[i] <= 0.02:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-000-02'
        elif 0.02 < objects_detObjCommon_posConfidence_elevation[i] <= 0.05:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-000-05'
        elif 0.05 < objects_detObjCommon_posConfidence_elevation[i] <= 0.1:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-000-10'
        elif 0.1 < objects_detObjCommon_posConfidence_elevation[i] <= 0.2:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-000-20'
        elif 0.2 < objects_detObjCommon_posConfidence_elevation[i] <= 0.5:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-000-50'
        elif 0.5 < objects_detObjCommon_posConfidence_elevation[i] <= 1:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-001-00'
        elif 1 < objects_detObjCommon_posConfidence_elevation[i] <= 2:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-002-00'
        elif 2 < objects_detObjCommon_posConfidence_elevation[i] <= 5:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-005-00'
        elif 5 < objects_detObjCommon_posConfidence_elevation[i] <= 10:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-010-00'
        elif 10 < objects_detObjCommon_posConfidence_elevation[i] <= 20:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-020-00'
        elif 20 < objects_detObjCommon_posConfidence_elevation[i] <= 50:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-050-00'
        elif 50 < objects_detObjCommon_posConfidence_elevation[i] <= 100:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-100-00'
        elif 100 < objects_detObjCommon_posConfidence_elevation[i] <= 200:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-200-00'
        elif 200 < objects_detObjCommon_posConfidence_elevation[i] <= 500:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'elev-500-00'
        elif 500 < objects_detObjCommon_posConfidence_elevation[i]:
            detected_object['detObjCommon']['posConfidence']['elevation'] = 'unavailable'
        
        if len(objects_detObjCommon_speed) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_speed but there are only', len(objects_detObjCommon_speed), 'of it!')
            break
        elif objects_detObjCommon_speed[i] < 0 or objects_detObjCommon_speed[i] > 163.8:
            print('Object', i, ': objects_detObjCommon_speed should be in range [0, 163.8] m/s! But', objects_detObjCommon_speed[i], 'is provided. Set to 163.82 (unavailable).')
            detected_object['detObjCommon']['speed'] = 8191
        else:
            detected_object['detObjCommon']['speed'] = int(objects_detObjCommon_speed[i] * 50)
        
        if len(objects_detObjCommon_speedConfidence) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_speedConfidence but there are only', len(objects_detObjCommon_speedConfidence), 'of it!')
            break
        elif objects_detObjCommon_speedConfidence[i] <= 0:
            print('Object', i, ': objects_detObjCommon_speedConfidence should be greater than 0 m/s! But', objects_detObjCommon_speedConfidence[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['speedConfidence'] = 'unavailable'
        elif 0 < objects_detObjCommon_speedConfidence[i] <= 0.01:
            detected_object['detObjCommon']['speedConfidence'] = 'prec0-01ms'
        elif 0.01 < objects_detObjCommon_speedConfidence[i] <= 0.05:
            detected_object['detObjCommon']['speedConfidence'] = 'prec0-05ms'
        elif 0.05 < objects_detObjCommon_speedConfidence[i] <= 0.1:
            detected_object['detObjCommon']['speedConfidence'] = 'prec0-1ms'
        elif 0.1 < objects_detObjCommon_speedConfidence[i] <= 1:
            detected_object['detObjCommon']['speedConfidence'] = 'prec1ms'
        elif 1 < objects_detObjCommon_speedConfidence[i] <= 5:
            detected_object['detObjCommon']['speedConfidence'] = 'prec5ms'
        elif 5 < objects_detObjCommon_speedConfidence[i] <= 10:
            detected_object['detObjCommon']['speedConfidence'] = 'prec10ms'
        elif 10 < objects_detObjCommon_speedConfidence[i] <= 100:
            detected_object['detObjCommon']['speedConfidence'] = 'prec100ms'
        elif 100 < objects_detObjCommon_speedConfidence[i]:
            detected_object['detObjCommon']['speedConfidence'] = 'unavailable'

        if len(objects_detObjCommon_speedZ) > i:
            if objects_detObjCommon_speedZ[i] < 0 or objects_detObjCommon_speedZ[i] > 163.8:
                print('Object', i, ': objects_detObjCommon_speedZ should be in range [0, 163.8] m/s! But', objects_detObjCommon_speedZ[i], 'is provided. Set to 163.82 (unavailable).')
                detected_object['detObjCommon']['speedZ'] = 8191
            else:
                detected_object['detObjCommon']['speedZ'] = int(objects_detObjCommon_speedZ[i] * 50)
        
        if len(objects_detObjCommon_speedConfidenceZ) > i:
            if objects_detObjCommon_speedConfidence[i] <= 0:
                print('Object', i, ': objects_detObjCommon_speedConfidence should be greater than 0 m/s! But', objects_detObjCommon_speedConfidence[i], 'is provided. Set to unavailable.')
                detected_object['detObjCommon']['speedConfidenceZ'] = 'unavailable'
            elif 0 < objects_detObjCommon_speedConfidence[i] <= 0.01:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'prec0-01ms'
            elif 0.01 < objects_detObjCommon_speedConfidence[i] <= 0.05:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'prec0-05ms'
            elif 0.05 < objects_detObjCommon_speedConfidence[i] <= 0.1:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'prec0-1ms'
            elif 0.1 < objects_detObjCommon_speedConfidence[i] <= 1:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'prec1ms'
            elif 1 < objects_detObjCommon_speedConfidence[i] <= 5:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'prec5ms'
            elif 5 < objects_detObjCommon_speedConfidence[i] <= 10:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'prec10ms'
            elif 10 < objects_detObjCommon_speedConfidence[i] <= 100:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'prec100ms'
            elif 100 < objects_detObjCommon_speedConfidence[i]:
                detected_object['detObjCommon']['speedConfidenceZ'] = 'unavailable'
        
        if len(objects_detObjCommon_heading) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_heading but there are only', len(objects_detObjCommon_heading), 'of it!')
            break
        elif objects_detObjCommon_heading[i] < 0 or objects_detObjCommon_heading[i] > 359.9875:
            print('Object', i, ': objects_detObjCommon_heading should be in range [0, 359.9875] deg! But', objects_detObjCommon_heading[i], 'is provided. Set to 360 (unavailable).')
            detected_object['detObjCommon']['heading'] = 28800
        else:
            detected_object['detObjCommon']['heading'] = int(objects_detObjCommon_heading[i] / 0.0125)
        
        if len(objects_detObjCommon_headingConf) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_headingConf but there are only', len(objects_detObjCommon_headingConf), 'of it!')
            break
        elif objects_detObjCommon_headingConf[i] <= 0:
            print('Object', i, ': objects_detObjCommon_headingConf should be greater than 0 deg! But', objects_detObjCommon_headingConf[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['headingConf'] = 'unavailable'
        elif 0 < objects_detObjCommon_headingConf[i] <= 0.0125:
            detected_object['detObjCommon']['headingConf'] = 'prec0-0125deg'
        elif 0.0125 < objects_detObjCommon_headingConf[i] <= 0.01:
            detected_object['detObjCommon']['headingConf'] = 'prec0-01deg'
        elif 0.01 < objects_detObjCommon_headingConf[i] <= 0.05:
            detected_object['detObjCommon']['headingConf'] = 'prec0-05deg'
        elif 0.05 < objects_detObjCommon_headingConf[i] <= 0.1:
            detected_object['detObjCommon']['headingConf'] = 'prec0-1deg'
        elif 0.1 < objects_detObjCommon_headingConf[i] <= 1:
            detected_object['detObjCommon']['headingConf'] = 'prec01deg'
        elif 1 < objects_detObjCommon_headingConf[i] <= 5:
            detected_object['detObjCommon']['headingConf'] = 'prec05deg'
        elif 5 < objects_detObjCommon_headingConf[i] <= 10:
            detected_object['detObjCommon']['headingConf'] = 'prec10deg'
        elif 10 < objects_detObjCommon_headingConf[i]:
            detected_object['detObjCommon']['headingConf'] = 'unavailable'

        accel4way = {}
        if len(objects_detObjCommon_accel4way_lat) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accel4way_lat but there are only', len(objects_detObjCommon_accel4way_lat), 'of it!')
        elif objects_detObjCommon_accel4way_lat[i] < -20 or objects_detObjCommon_accel4way_lat[i] > 20:
            print('Object', i, ': objects_detObjCommon_accel4way_lat should be in range [-20, 20] m/s^2! But', objects_detObjCommon_accel4way_lat[i], 'is provided. Set to 20.01 (unavailable).')
            accel4way['lat'] = 2001
        else:
            accel4way['lat'] = int(objects_detObjCommon_accel4way_lat[i] * 100)
        
        if len(objects_detObjCommon_accel4way_long) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accel4way_long but there are only', len(objects_detObjCommon_accel4way_long), 'of it!')
        elif objects_detObjCommon_accel4way_long[i] < -20 or objects_detObjCommon_accel4way_long[i] > 20:
            print('Object', i, ': objects_detObjCommon_accel4way_long should be in range [-20, 20] m/s^2! But', objects_detObjCommon_accel4way_long[i], 'is provided. Set to 20.01 (unavailable).')
            accel4way['long'] = 2001
        else:
            accel4way['long'] = int(objects_detObjCommon_accel4way_long[i] * 100)
        
        if len(objects_detObjCommon_accel4way_vert) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accel4way_vert but there are only', len(objects_detObjCommon_accel4way_vert), 'of it!')
        elif objects_detObjCommon_accel4way_vert[i] < -2.52 * 9.80665:
            accel4way['vert'] = -126
        elif objects_detObjCommon_accel4way_vert[i] > 2.54 * 9.80665:
            accel4way['vert'] = 127
        else:
            accel4way['vert'] = int(objects_detObjCommon_accel4way_vert[i] / 9.80665 * 50)
        
        if len(objects_detObjCommon_accel4way_yaw) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accel4way_yaw but there are only', len(objects_detObjCommon_accel4way_yaw), 'of it!')
        elif objects_detObjCommon_accel4way_yaw[i] < -327.67:
            accel4way['yaw'] = -32767
        elif objects_detObjCommon_accel4way_yaw[i] > 327.67:
            accel4way['yaw'] = 32767
        else:
            accel4way['yaw'] = int(objects_detObjCommon_accel4way_yaw[i] * 100)
        
        if len(list(accel4way.keys())) == 4:
            detected_object['detObjCommon']['accel4way'] = accel4way
        
        if len(objects_detObjCommon_accCfdX) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accCfdX but there are only', len(objects_detObjCommon_accCfdX), 'of it!')
        elif objects_detObjCommon_accCfdX[i] <= 0:
            print('Object', i, ': objects_detObjCommon_accCfdX should be greater than 0 m/s^2! But', objects_detObjCommon_accCfdX[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['accCfdX'] = 'unavailable'
        elif 0 < objects_detObjCommon_accCfdX[i] <= 0.01:
            detected_object['detObjCommon']['accCfdX'] = 'accl-000-01'
        elif 0.01 < objects_detObjCommon_accCfdX[i] <= 0.05:
            detected_object['detObjCommon']['accCfdX'] = 'accl-000-05'
        elif 0.05 < objects_detObjCommon_accCfdX[i] <= 0.1:
            detected_object['detObjCommon']['accCfdX'] = 'accl-000-10'
        elif 0.1 < objects_detObjCommon_accCfdX[i] <= 1:
            detected_object['detObjCommon']['accCfdX'] = 'accl-001-00'
        elif 1 < objects_detObjCommon_accCfdX[i] <= 5:
            detected_object['detObjCommon']['accCfdX'] = 'accl-005-00'
        elif 5 < objects_detObjCommon_accCfdX[i] <= 10:
            detected_object['detObjCommon']['accCfdX'] = 'accl-010-00'
        elif 10 < objects_detObjCommon_accCfdX[i] <= 100:
            detected_object['detObjCommon']['accCfdX'] = 'accl-100-00'
        elif 100 < objects_detObjCommon_accCfdX[i]:
            detected_object['detObjCommon']['accCfdX'] = 'unavailable'
        
        if len(objects_detObjCommon_accCfdY) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accCfdY but there are only', len(objects_detObjCommon_accCfdY), 'of it!')
        elif objects_detObjCommon_accCfdY[i] <= 0:
            print('Object', i, ': objects_detObjCommon_accCfdY should be greater than 0 m/s^2! But', objects_detObjCommon_accCfdY[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['accCfdY'] = 'unavailable'
        elif 0 < objects_detObjCommon_accCfdY[i] <= 0.01:
            detected_object['detObjCommon']['accCfdY'] = 'accl-000-01'
        elif 0.01 < objects_detObjCommon_accCfdY[i] <= 0.05:
            detected_object['detObjCommon']['accCfdY'] = 'accl-000-05'
        elif 0.05 < objects_detObjCommon_accCfdY[i] <= 0.1:
            detected_object['detObjCommon']['accCfdY'] = 'accl-000-10'
        elif 0.1 < objects_detObjCommon_accCfdY[i] <= 1:
            detected_object['detObjCommon']['accCfdY'] = 'accl-001-00'
        elif 1 < objects_detObjCommon_accCfdY[i] <= 5:
            detected_object['detObjCommon']['accCfdY'] = 'accl-005-00'
        elif 5 < objects_detObjCommon_accCfdY[i] <= 10:
            detected_object['detObjCommon']['accCfdY'] = 'accl-010-00'
        elif 10 < objects_detObjCommon_accCfdY[i] <= 100:
            detected_object['detObjCommon']['accCfdY'] = 'accl-100-00'
        elif 100 < objects_detObjCommon_accCfdY[i]:
            detected_object['detObjCommon']['accCfdY'] = 'unavailable'
        
        if len(objects_detObjCommon_accCfdZ) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accCfdZ but there are only', len(objects_detObjCommon_accCfdZ), 'of it!')
        elif objects_detObjCommon_accCfdZ[i] <= 0:
            print('Object', i, ': objects_detObjCommon_accCfdZ should be greater than 0 m/s^2! But', objects_detObjCommon_accCfdZ[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['accCfdZ'] = 'unavailable'
        elif 0 < objects_detObjCommon_accCfdZ[i] <= 0.01:
            detected_object['detObjCommon']['accCfdZ'] = 'accl-000-01'
        elif 0.01 < objects_detObjCommon_accCfdZ[i] <= 0.05:
            detected_object['detObjCommon']['accCfdZ'] = 'accl-000-05'
        elif 0.05 < objects_detObjCommon_accCfdZ[i] <= 0.1:
            detected_object['detObjCommon']['accCfdZ'] = 'accl-000-10'
        elif 0.1 < objects_detObjCommon_accCfdZ[i] <= 1:
            detected_object['detObjCommon']['accCfdZ'] = 'accl-001-00'
        elif 1 < objects_detObjCommon_accCfdZ[i] <= 5:
            detected_object['detObjCommon']['accCfdZ'] = 'accl-005-00'
        elif 5 < objects_detObjCommon_accCfdZ[i] <= 10:
            detected_object['detObjCommon']['accCfdZ'] = 'accl-010-00'
        elif 10 < objects_detObjCommon_accCfdZ[i] <= 100:
            detected_object['detObjCommon']['accCfdZ'] = 'accl-100-00'
        elif 100 < objects_detObjCommon_accCfdZ[i]:
            detected_object['detObjCommon']['accCfdZ'] = 'unavailable'
        
        if len(objects_detObjCommon_accCfdYaw) <= i:
            print('Expect', objects_N, 'objects_detObjCommon_accCfdYaw but there are only', len(objects_detObjCommon_accCfdYaw), 'of it!')
        elif objects_detObjCommon_accCfdYaw[i] <= 0:
            print('Object', i, ': objects_detObjCommon_accCfdYaw should be greater than 0 deg/sec! But', objects_detObjCommon_accCfdYaw[i], 'is provided. Set to unavailable.')
            detected_object['detObjCommon']['accCfdYaw'] = 'unavailable'
        elif 0 < objects_detObjCommon_accCfdYaw[i] <= 0.01:
            detected_object['detObjCommon']['accCfdYaw'] = 'degSec-000-01'
        elif 0.01 < objects_detObjCommon_accCfdYaw[i] <= 0.05:
            detected_object['detObjCommon']['accCfdYaw'] = 'degSec-000-05'
        elif 0.05 < objects_detObjCommon_accCfdYaw[i] <= 0.1:
            detected_object['detObjCommon']['accCfdYaw'] = 'degSec-000-10'
        elif 0.1 < objects_detObjCommon_accCfdYaw[i] <= 1:
            detected_object['detObjCommon']['accCfdYaw'] = 'degSec-001-00'
        elif 1 < objects_detObjCommon_accCfdYaw[i] <= 5:
            detected_object['detObjCommon']['accCfdYaw'] = 'degSec-005-00'
        elif 5 < objects_detObjCommon_accCfdYaw[i] <= 10:
            detected_object['detObjCommon']['accCfdYaw'] = 'degSec-010-00'
        elif 10 < objects_detObjCommon_accCfdYaw[i] <= 100:
            detected_object['detObjCommon']['accCfdYaw'] = 'degSec-100-00'
        elif 100 < objects_detObjCommon_accCfdYaw[i]:
            detected_object['detObjCommon']['accCfdYaw'] = 'unavailable'
        
        if len(objects_detObjOptData_type) > i:
            if objects_detObjOptData_type[i] not in ['Veh', 'VRU', 'Obst']:
                print('Object', i, ': objects_detObjOptData_type should be one of Veh, VRU, or Obst! But', objects_detObjOptData_type[i], 'is provided. Remove detObjOptData.')
            else:
                detObjOptData = ()
                if objects_detObjOptData_type[i] == 'Veh':
                    detData = {}
                    if len(objects_detObjOptData_detVeh_lights) > i:
                        if objects_detObjOptData_detVeh_lights[i] not in [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8']:
                            print('Object', i, ': objects_detObjOptData_detVeh_lights should be one of 0 (lowBeamHeadlightsOn), 1 (highBeamHeadlightsOn), 2 (leftTurnSignalOn), 3 (rightTurnSignalOn), 4 (hazardSignalOn), 5 (automaticLightControlOn), 6 (daytimeRunningLightsOn), 7 (fogLightOn), or 8 (parkingLightsOn)! But', objects_detObjOptData_detVeh_lights[i], 'is provided. Remove it.')
                        else:
                            detData['lights'] = (int.from_bytes(objects_detObjOptData_detVeh_lights[i], byteorder='little'), 6)
                    
                    if len(objects_detObjOptData_detVeh_vehAttitude_pitch) > i and len(objects_detObjOptData_detVeh_vehAttitude_roll) > i and len(objects_detObjOptData_detVeh_vehAttitude_yaw) > i:
                        detData['vehAttitude'] = {}

                        if objects_detObjOptData_detVeh_vehAttitude_pitch[i] < -90 or objects_detObjOptData_detVeh_vehAttitude_pitch[i] > 90:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAttitude_pitch should be in range [-90, 90] deg! But', objects_detObjOptData_detVeh_vehAttitude_pitch[i], 'is provided. Set to 90 (unavailable).')
                            detData['vehAttitude']['pitch'] = 7200
                        else:
                            detData['vehAttitude']['pitch'] = int(objects_detObjOptData_detVeh_vehAttitude_pitch[i] / 0.0125)

                        if objects_detObjOptData_detVeh_vehAttitude_roll[i] < -180 or objects_detObjOptData_detVeh_vehAttitude_roll[i] > 180:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAttitude_roll should be in range [-180, 180] deg! But', objects_detObjOptData_detVeh_vehAttitude_roll[i], 'is provided. Set to 180 (unavailable).')
                            detData['vehAttitude']['roll'] = 14400
                        else:
                            detData['vehAttitude']['roll'] = int(objects_detObjOptData_detVeh_vehAttitude_roll[i] / 0.0125)
                        
                        if objects_detObjOptData_detVeh_vehAttitude_yaw[i] < -180 or objects_detObjOptData_detVeh_vehAttitude_yaw[i] > 180:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAttitude_yaw should be in range [-180, 180] deg! But', objects_detObjOptData_detVeh_vehAttitude_yaw[i], 'is provided. Set to 180 (unavailable).')
                            detData['vehAttitude']['yaw'] = 14400
                        else:
                            detData['vehAttitude']['yaw'] = int(objects_detObjOptData_detVeh_vehAttitude_yaw[i] / 0.0125)
                    else:
                        if len(objects_detObjOptData_detVeh_vehAttitude_pitch) <= i:
                            print('Expect', objects_N, 'objects_detObjOptData_detVeh_vehAttitude_pitch but there are only', len(objects_detObjOptData_detVeh_vehAttitude_pitch), 'of it!')
                        if len(objects_detObjOptData_detVeh_vehAttitude_roll) <= i:
                            print('Expect', objects_N, 'objects_detObjOptData_detVeh_vehAttitude_roll but there are only', len(objects_detObjOptData_detVeh_vehAttitude_roll), 'of it!')
                        if len(objects_detObjOptData_detVeh_vehAttitude_yaw) <= i:
                            print('Expect', objects_N, 'objects_detObjOptData_detVeh_vehAttitude_yaw but there are only', len(objects_detObjOptData_detVeh_vehAttitude_yaw), 'of it!')
                    
                    if len(objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence) > i and len(objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence) > i and len(objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence) > i:
                        detData['vehAttitudeConfidence'] = {}

                        if objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence should be greater than 0 deg! But', objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i], 'is provided. Set to unavailable.')
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 0.0125:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'prec0-0125deg'
                        elif 0.0125 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 0.01:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'prec0-01deg'
                        elif 0.01 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 0.05:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'prec0-05deg'
                        elif 0.05 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 0.1:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'prec0-1deg'
                        elif 0.1 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 1:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'prec01deg'
                        elif 1 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 5:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'prec05deg'
                        elif 5 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i] <= 10:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'prec10deg'
                        elif 10 < objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence[i]:
                            detData['vehAttitudeConfidence']['pitchConfidence'] = 'unavailable'
                        
                        if objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence should be greater than 0 deg! But', objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i], 'is provided. Set to unavailable.')
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 0.0125:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'prec0-0125deg'
                        elif 0.0125 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 0.01:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'prec0-01deg'
                        elif 0.01 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 0.05:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'prec0-05deg'
                        elif 0.05 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 0.1:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'prec0-1deg'
                        elif 0.1 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 1:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'prec01deg'
                        elif 1 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 5:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'prec05deg'
                        elif 5 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i] <= 10:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'prec10deg'
                        elif 10 < objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence[i]:
                            detData['vehAttitudeConfidence']['rollConfidence'] = 'unavailable'
                        
                        if objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence should be greater than 0 deg! But', objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i], 'is provided. Set to unavailable.')
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 0.0125:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'prec0-0125deg'
                        elif 0.0125 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 0.01:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'prec0-01deg'
                        elif 0.01 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 0.05:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'prec0-05deg'
                        elif 0.05 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 0.1:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'prec0-1deg'
                        elif 0.1 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 1:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'prec01deg'
                        elif 1 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 5:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'prec05deg'
                        elif 5 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i] <= 10:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'prec10deg'
                        elif 10 < objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence[i]:
                            detData['vehAttitudeConfidence']['yawConfidence'] = 'unavailable'

                    if len(objects_detObjOptData_detVeh_vehAngleVel_pitchRate) > i and len(objects_detObjOptData_detVeh_vehAngleVel_rollRate) > i:
                        detData['vehAngVel'] = {}

                        if objects_detObjOptData_detVeh_vehAngleVel_pitchRate[i] < -327.67 or objects_detObjOptData_detVeh_vehAngleVel_pitchRate[i] > 327.67:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAngleVel_pitchRate should be in range [-327.67, 327.67] deg! But', objects_detObjOptData_detVeh_vehAngleVel_pitchRate[i], 'is provided. Set to 327.67 (unavailable).')
                            detData['vehAngVel']['pitchRate'] = 32767
                        else:
                            detData['vehAngVel']['pitchRate'] = int(objects_detObjOptData_detVeh_vehAngleVel_pitchRate[i] * 100)
                        
                        if objects_detObjOptData_detVeh_vehAngleVel_rollRate[i] < -327.67 or objects_detObjOptData_detVeh_vehAngleVel_rollRate[i] > 327.67:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAngleVel_rollRate should be in range [-327.67, 327.67] deg! But', objects_detObjOptData_detVeh_vehAngleVel_rollRate[i], 'is provided. Set to 327.67 (unavailable).')
                            detData['vehAngVel']['rollRate'] = 32767
                        else:
                            detData['vehAngVel']['rollRate'] = int(objects_detObjOptData_detVeh_vehAngleVel_rollRate[i] * 100)

                    vehAngVelConfidence = {}
                    if len(objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence) > i:
                        if objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence should be greater than 0 deg/s! But', objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i], 'is provided. Set to unavailable.')
                            vehAngVelConfidence['pitchRateConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 0.01:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-000-01'
                        elif 0.01 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 0.05:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-000-05'
                        elif 0.05 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 0.1:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-000-10'
                        elif 0.1 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 1:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-001-00'
                        elif 1 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 5:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-005-00'
                        elif 5 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 10:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-010-00'
                        elif 10 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i] <= 100:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-100-00'
                        elif 100 < objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence[i]:
                            vehAngVelConfidence['pitchRateConfidence'] = 'unavailable'
                    if len(objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence) > i:
                        if objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence should be greater than 0 deg/s! But', objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i], 'is provided. Set to unavailable.')
                            vehAngVelConfidence['pitchRateConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 0.01:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-000-01'
                        elif 0.01 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 0.05:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-000-05'
                        elif 0.05 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 0.1:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-000-10'
                        elif 0.1 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 1:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-001-00'
                        elif 1 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 5:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-005-00'
                        elif 5 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 10:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-010-00'
                        elif 10 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i] <= 100:
                            vehAngVelConfidence['pitchRateConfidence'] = 'degSec-100-00'
                        elif 100 < objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence[i]:
                            vehAngVelConfidence['pitchRateConfidence'] = 'unavailable'
                    if len(list(vehAngVelConfidence.keys())) > 0:
                        detData['vehAngVelConfidence'] = vehAngVelConfidence

                    veh_size = {}
                    if len(objects_detObjOptData_detVeh_size_width) > i and len(objects_detObjOptData_detVeh_size_length) > i:
                        if objects_detObjOptData_detVeh_size_width[i] <= 0 or objects_detObjOptData_detVeh_size_width[i] > 10.23:
                            print('Object', i, ': objects_detObjOptData_detVeh_size_width should be in range (0, 10.23] m! But', objects_detObjOptData_detVeh_size_width[i], 'is provided. Set to 0 (unavailable).')
                            veh_size['width'] = 0
                        else:
                            veh_size['width'] = int(objects_detObjOptData_detVeh_size_width[i] * 100)
                        if objects_detObjOptData_detVeh_size_length[i] <= 0 or objects_detObjOptData_detVeh_size_length[i] > 40.95:
                            print('Object', i, ': objects_detObjOptData_detVeh_size_length should be in range (0, 40.95] m! But', objects_detObjOptData_detVeh_size_length[i], 'is provided. Set to 0 (unavailable).')
                            veh_size['length'] = 0
                        else:
                            veh_size['length'] = int(objects_detObjOptData_detVeh_size_length[i] * 100)
                    else:
                        if len(objects_detObjOptData_detVeh_size_width) <= i:
                            print('Expect', objects_N, 'objects_detObjOptData_detVeh_size_width but there are only', len(objects_detObjOptData_detVeh_size_width), 'of it!')
                        if len(objects_detObjOptData_detVeh_size_length) <= i:
                            print('Expect', objects_N, 'objects_detObjOptData_detVeh_size_length but there are only', len(objects_detObjOptData_detVeh_size_length), 'of it!')
                    if len(list(veh_size.keys())) > 0:
                        detData['size'] = veh_size
                    
                    if len(objects_detObjOptData_detVeh_height) > i:
                        if objects_detObjOptData_detVeh_height[i] <= 0 or objects_detObjOptData_detVeh_height[i] > 6.35:
                            print('Object', i, ': objects_detObjOptData_detVeh_height should be in range (0, 6.35] m! But', objects_detObjOptData_detVeh_height[i], 'is provided. Set to 0 (unavailable).')
                            detData['height'] = 0
                        else:
                            detData['height'] = int(objects_detObjOptData_detVeh_height[i] * 20)
                    
                    vehicleSizeConfidence = {}
                    if len(objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence) > i and len(objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence) > i and len(objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence) > i:
                        if objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence should be greater than 0 m! But', objects_detObjOptData_detVeh_size_width[i], 'is provided. Set to unavailable.')
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 0.01:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-000-01'
                        elif 0.01 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 0.02:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-000-02'
                        elif 0.02 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 0.05:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-000-05'
                        elif 0.05 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 0.1:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-000-10'
                        elif 0.1 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 0.2:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-000-20'
                        elif 0.2 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 0.5:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-000-50'
                        elif 0.5 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 1:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-001-00'
                        elif 1 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 2:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-002-00'
                        elif 2 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 5:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-005-00'
                        elif 5 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 10:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-010-00'
                        elif 10 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 20:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-020-00'
                        elif 20 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 50:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-050-00'
                        elif 50 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i] <= 100:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'size-100-00'
                        elif 100 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence[i]:
                            vehicleSizeConfidence['vehicleWidthConfidence'] = 'unavailable'
                        
                        if objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence should be greater than 0 m! But', objects_detObjOptData_detVeh_size_width[i], 'is provided. Set to unavailable.')
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 0.01:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-000-01'
                        elif 0.01 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 0.02:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-000-02'
                        elif 0.02 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 0.05:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-000-05'
                        elif 0.05 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 0.1:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-000-10'
                        elif 0.1 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 0.2:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-000-20'
                        elif 0.2 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 0.5:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-000-50'
                        elif 0.5 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 1:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-001-00'
                        elif 1 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 2:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-002-00'
                        elif 2 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 5:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-005-00'
                        elif 5 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 10:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-010-00'
                        elif 10 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 20:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-020-00'
                        elif 20 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 50:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-050-00'
                        elif 50 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i] <= 100:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'size-100-00'
                        elif 100 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence[i]:
                            vehicleSizeConfidence['vehicleLengthConfidence'] = 'unavailable'
                        
                        if objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence should be greater than 0 m! But', objects_detObjOptData_detVeh_size_width[i], 'is provided. Set to unavailable.')
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 0.01:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-000-01'
                        elif 0.01 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 0.02:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-000-02'
                        elif 0.02 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 0.05:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-000-05'
                        elif 0.05 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 0.1:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-000-10'
                        elif 0.1 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 0.2:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-000-20'
                        elif 0.2 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 0.5:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-000-50'
                        elif 0.5 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 1:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-001-00'
                        elif 1 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 2:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-002-00'
                        elif 2 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 5:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-005-00'
                        elif 5 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 10:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-010-00'
                        elif 10 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 20:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-020-00'
                        elif 20 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 50:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-050-00'
                        elif 50 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i] <= 100:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'size-100-00'
                        elif 100 < objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence[i]:
                            vehicleSizeConfidence['vehicleHeightConfidence'] = 'unavailable'

                    if len(list(vehicleSizeConfidence.keys())) > 0:
                        detData['vehicleSizeConfidence'] = vehicleSizeConfidence
                    
                    if len(objects_detObjOptData_detVeh_vehicleClass) > i:
                        if not isinstance(objects_detObjOptData_detVeh_vehicleClass[i], int):
                            print('Object', i, ': objects_detObjOptData_detVeh_vehicleClass should be an integer! But', objects_detObjOptData_detVeh_vehicleClass[i], 'is provided. Set to 0 (unknownVehicleClass).')
                            detData['vehicleClass'] = 0
                        elif objects_detObjOptData_detVeh_vehicleClass[i] < 0 or objects_detObjOptData_detVeh_vehicleClass[i] > 255:
                            print('Object', i, ': objects_detObjOptData_detVeh_vehicleClass should be in range [0, 255]! But', objects_detObjOptData_detVeh_vehicleClass[i], 'is provided. Set to 0 (unknownVehicleClass).')
                            detData['vehicleClass'] = 0
                        else:
                            detData['vehicleClass'] = objects_detObjOptData_detVeh_vehicleClass[i]

                    if len(objects_detObjOptData_detVeh_classConf) > i:
                        if not isinstance(objects_detObjOptData_detVeh_classConf[i], int):
                            print('Object', i, ': objects_detObjOptData_detVeh_classConf should be an integer! But', objects_detObjOptData_detVeh_classConf[i], 'is provided. Set to 101 (unavailable).')
                            detData['classConf'] = 101
                        elif objects_detObjOptData_detVeh_classConf[i] < 0 or objects_detObjOptData_detVeh_classConf[i] > 101:
                            print('Object', i, ': objects_detObjOptData_detVeh_classConf should be in range [0, 101]! But', objects_detObjOptData_detVeh_classConf[i], 'is provided. Set to 101 (unavailable).')
                            detData['classConf'] = 101
                        else:
                            detData['classConf'] = objects_detObjOptData_detVeh_classConf[i]

                    if len(list(detData.keys())) > 0:
                        detObjOptData = ('detVeh', detData)
                elif objects_detObjOptData_type[i] == 'VRU':
                    detData = {}

                    if len(objects_detObjOptData_detVRU_basicType) > i:
                        if objects_detObjOptData_detVRU_basicType[i] not in ['unavailable', 'aPEDESTRIAN', 'aPEDALCYCLIST', 'aPUBLICSAFETYWORKER', 'anANIMAL']:
                            print('Object', i, ': objects_detObjOptData_detVRU_basicType should be one of unavailable, aPEDESTRIAN, aPEDALCYCLIST, aPUBLICSAFETYWORKER, or anANIMAL! But', objects_detObjOptData_detVRU_basicType[i], 'is provided. Remove it.')
                        else:
                            detData['basicType'] = objects_detObjOptData_detVRU_basicType[i]
                    
                    propulsion = ()
                    if len(objects_detObjOptData_detVRU_propulsion) > i:
                        if objects_detObjOptData_detVRU_propulsion[i] not in ['human', 'animal', 'motor']:
                            print('Object', i, ': objects_detObjOptData_detVRU_propulsion should be one of human, animal, motor! But', objects_detObjOptData_detVRU_propulsion[i], 'is provided. Remove it.')
                        elif objects_detObjOptData_detVRU_propulsion[i] == 'human':
                            if len(objects_detObjOptData_detVRU_propulsion_human) > i:
                                if objects_detObjOptData_detVRU_propulsion_human[i] not in ['unavailable', 'otherTypes', 'onFoot', 'skateboard', 'pushOrKickScooter', 'wheelchair']:
                                    print('Object', i, ': objects_detObjOptData_detVRU_propulsion_human should be one of unavailable, otherTypes, onFoot, skateboard, pushOrKickScooter, or wheelchair! But', objects_detObjOptData_detVRU_propulsion_human[i], 'is provided. Remove it.')
                                else:
                                    propulsion = ('human', objects_detObjOptData_detVRU_propulsion_human[i])
                        elif objects_detObjOptData_detVRU_propulsion[i] == 'animal':
                            if len(objects_detObjOptData_detVRU_propulsion_animal) > i:
                                if objects_detObjOptData_detVRU_propulsion_animal[i] not in ['unavailable', 'otherTypes', 'animalMounted', 'animalDrawnCarriage']:
                                    print('Object', i, ': objects_detObjOptData_detVRU_propulsion_animal should be one of unavailable, otherTypes, animalMounted, or animalDrawnCarriage! But', objects_detObjOptData_detVRU_propulsion_animal[i], 'is provided. Remove it.')
                                else:
                                    propulsion = ('animal', objects_detObjOptData_detVRU_propulsion_animal[i])
                        elif objects_detObjOptData_detVRU_propulsion[i] == 'motor':
                            if len(objects_detObjOptData_detVRU_propulsion_motor) > i:
                                if objects_detObjOptData_detVRU_propulsion_motor[i] not in ['unavailable', 'otherTypes', 'wheelChair', 'bicycle', 'scooter', 'selfBalancingDevice']:
                                    print('Object', i, ': objects_detObjOptData_detVRU_propulsion_motor should be one of unavailable, otherTypes, wheelChair, bicycle, scooter, or selfBalancingDevice! But', objects_detObjOptData_detVRU_propulsion_motor[i], 'is provided. Remove it.')
                                else:
                                    propulsion = ('motor', objects_detObjOptData_detVRU_propulsion_motor[i])
                    
                    if len(propulsion) > 0:
                        detData['propulsion'] = propulsion

                    if len(objects_detObjOptData_detVRU_attachment) > i:
                        if objects_detObjOptData_detVRU_attachment[i] not in ['unavailable', 'stroller', 'bicycleTrailer', 'cart', 'wheelchair', 'otherWalkAssistAttachments', 'pet']:
                            print('Object', i, ': objects_detObjOptData_detVRU_attachment should be one of unavailable, stroller, bicycleTrailer, cart, wheelchair, otherWalkAssistAttachments, or pet! But', objects_detObjOptData_detVRU_attachment[i], 'is provided. Remove it.')
                        else:
                            detData['attachment'] = objects_detObjOptData_detVRU_attachment[i]
                    
                    if len(objects_detObjOptData_detVRU_radius) > i:
                        if not isinstance(objects_detObjOptData_detVRU_radius[i], int):
                            print('Object', i, ': objects_detObjOptData_detVRU_radius should be an integer! But', objects_detObjOptData_detVRU_radius[i], 'is provided. Set to 0.')
                            detData['radius'] = 0
                        elif objects_detObjOptData_detVRU_radius[i] < 0 or objects_detObjOptData_detVRU_radius[i] > 200:
                            print('Object', i, ': objects_detObjOptData_detVRU_radius should be in range [0, 200]! But', objects_detObjOptData_detVRU_radius[i], 'is provided. Set to 0.')
                            detData['radius'] = 0
                        else:
                            detData['radius'] = objects_detObjOptData_detVRU_radius[i]

                    if len(list(detData.keys())) > 0:
                        detObjOptData = ('detVRU', detData)
                elif objects_detObjOptData_type[i] == 'Obst':
                    detData = {}

                    obstSize = {}
                    if len(objects_detObjOptData_detObst_obstSize_width) > i and len(objects_detObjOptData_detObst_obstSize_length) > i:
                        if objects_detObjOptData_detObst_obstSize_width[i] < 0 or objects_detObjOptData_detObst_obstSize_width[i] > 10.23:
                            print('Object', i, ': objects_detObjOptData_detObst_obstSize_width should be in range [0, 10.23]! But', objects_detObjOptData_detObst_obstSize_width[i], 'is provided. Set to 0.')
                            obstSize['width'] = 0
                        else:
                            obstSize['width'] = int(objects_detObjOptData_detObst_obstSize_width[i] * 100)

                        if objects_detObjOptData_detObst_obstSize_length[i] < 0 or objects_detObjOptData_detObst_obstSize_length[i] > 10.23:
                            print('Object', i, ': objects_detObjOptData_detObst_obstSize_length should be in range [0, 10.23]! But', objects_detObjOptData_detObst_obstSize_length[i], 'is provided. Set to 0.')
                            obstSize['length'] = 0
                        else:
                            obstSize['length'] = int(objects_detObjOptData_detObst_obstSize_length[i] * 100)

                    if len(objects_detObjOptData_detObst_obstSize_height) > i:
                        if objects_detObjOptData_detObst_obstSize_height[i] < 0 or objects_detObjOptData_detObst_obstSize_height[i] > 10.23:
                            print('Object', i, ': objects_detObjOptData_detObst_obstSize_height should be in range [0, 10.23]! But', objects_detObjOptData_detObst_obstSize_height[i], 'is provided. Set to 0.')
                            obstSize['height'] = 0
                        else:
                            obstSize['height'] = int(objects_detObjOptData_detObst_obstSize_height[i] * 100)
                    
                    if len(list(obstSize.keys())) > 0:
                        detData['obstSize'] = obstSize
                    
                    obstSizeConfidence = {}
                    if len(objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence) > i and len(objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence) > i:
                        if objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence should be greater than 0 m! But', objects_detObjOptData_detVeh_size_width[i], 'is provided. Set to unavailable.')
                            obstSizeConfidence['widthConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 0.01:
                            obstSizeConfidence['widthConfidence'] = 'size-000-01'
                        elif 0.01 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 0.02:
                            obstSizeConfidence['widthConfidence'] = 'size-000-02'
                        elif 0.02 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 0.05:
                            obstSizeConfidence['widthConfidence'] = 'size-000-05'
                        elif 0.05 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 0.1:
                            obstSizeConfidence['widthConfidence'] = 'size-000-10'
                        elif 0.1 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 0.2:
                            obstSizeConfidence['widthConfidence'] = 'size-000-20'
                        elif 0.2 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 0.5:
                            obstSizeConfidence['widthConfidence'] = 'size-000-50'
                        elif 0.5 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 1:
                            obstSizeConfidence['widthConfidence'] = 'size-001-00'
                        elif 1 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 2:
                            obstSizeConfidence['widthConfidence'] = 'size-002-00'
                        elif 2 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 5:
                            obstSizeConfidence['widthConfidence'] = 'size-005-00'
                        elif 5 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 10:
                            obstSizeConfidence['widthConfidence'] = 'size-010-00'
                        elif 10 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 20:
                            obstSizeConfidence['widthConfidence'] = 'size-020-00'
                        elif 20 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 50:
                            obstSizeConfidence['widthConfidence'] = 'size-050-00'
                        elif 50 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i] <= 100:
                            obstSizeConfidence['widthConfidence'] = 'size-100-00'
                        elif 100 < objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence[i]:
                            obstSizeConfidence['widthConfidence'] = 'unavailable'
                        
                        if objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence should be greater than 0 m! But', objects_detObjOptData_detVeh_size_width[i], 'is provided. Set to unavailable.')
                            obstSizeConfidence['lengthConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 0.01:
                            obstSizeConfidence['lengthConfidence'] = 'size-000-01'
                        elif 0.01 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 0.02:
                            obstSizeConfidence['lengthConfidence'] = 'size-000-02'
                        elif 0.02 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 0.05:
                            obstSizeConfidence['lengthConfidence'] = 'size-000-05'
                        elif 0.05 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 0.1:
                            obstSizeConfidence['lengthConfidence'] = 'size-000-10'
                        elif 0.1 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 0.2:
                            obstSizeConfidence['lengthConfidence'] = 'size-000-20'
                        elif 0.2 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 0.5:
                            obstSizeConfidence['lengthConfidence'] = 'size-000-50'
                        elif 0.5 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 1:
                            obstSizeConfidence['lengthConfidence'] = 'size-001-00'
                        elif 1 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 2:
                            obstSizeConfidence['lengthConfidence'] = 'size-002-00'
                        elif 2 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 5:
                            obstSizeConfidence['lengthConfidence'] = 'size-005-00'
                        elif 5 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 10:
                            obstSizeConfidence['lengthConfidence'] = 'size-010-00'
                        elif 10 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 20:
                            obstSizeConfidence['lengthConfidence'] = 'size-020-00'
                        elif 20 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 50:
                            obstSizeConfidence['lengthConfidence'] = 'size-050-00'
                        elif 50 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i] <= 100:
                            obstSizeConfidence['lengthConfidence'] = 'size-100-00'
                        elif 100 < objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence[i]:
                            obstSizeConfidence['lengthConfidence'] = 'unavailable'

                    if len(objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence) > i:
                        if objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 0:
                            print('Object', i, ': objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence should be greater than 0 m! But', objects_detObjOptData_detVeh_size_width[i], 'is provided. Set to unavailable.')
                            obstSizeConfidence['heightConfidence'] = 'unavailable'
                        elif 0 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 0.01:
                            obstSizeConfidence['heightConfidence'] = 'size-000-01'
                        elif 0.01 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 0.02:
                            obstSizeConfidence['heightConfidence'] = 'size-000-02'
                        elif 0.02 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 0.05:
                            obstSizeConfidence['heightConfidence'] = 'size-000-05'
                        elif 0.05 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 0.1:
                            obstSizeConfidence['heightConfidence'] = 'size-000-10'
                        elif 0.1 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 0.2:
                            obstSizeConfidence['heightConfidence'] = 'size-000-20'
                        elif 0.2 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 0.5:
                            obstSizeConfidence['heightConfidence'] = 'size-000-50'
                        elif 0.5 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 1:
                            obstSizeConfidence['heightConfidence'] = 'size-001-00'
                        elif 1 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 2:
                            obstSizeConfidence['heightConfidence'] = 'size-002-00'
                        elif 2 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 5:
                            obstSizeConfidence['heightConfidence'] = 'size-005-00'
                        elif 5 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 10:
                            obstSizeConfidence['heightConfidence'] = 'size-010-00'
                        elif 10 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 20:
                            obstSizeConfidence['heightConfidence'] = 'size-020-00'
                        elif 20 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 50:
                            obstSizeConfidence['heightConfidence'] = 'size-050-00'
                        elif 50 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i] <= 100:
                            obstSizeConfidence['heightConfidence'] = 'size-100-00'
                        elif 100 < objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence[i]:
                            obstSizeConfidence['heightConfidence'] = 'unavailable'

                    if len(list(obstSizeConfidence.keys())) > 0:
                        detData['obstSizeConfidence'] = obstSizeConfidence

                    if len(list(detData.keys())) > 0:
                        detObjOptData = ('detObst', detData)

                if len(list(detObjOptData)) > 0:
                    detected_object['detObjOptData'] = detObjOptData

        sdsm['objects'].append(detected_object)

    # add header to SDSM
    header_sdsm = {
        'messageId': 41,
        'value': ('SensorDataSharingMessage', sdsm)
    }

    # encode SDSM to hex
    header_sdsm_msg = SDSM.MessageFrame.MessageFrame
    header_sdsm_msg.set_val(header_sdsm)
    hex_sdsm = hexlify(header_sdsm_msg.to_uper())

    header_sdsm_msg.from_uper_ws(unhexlify(hex_sdsm))

    return hex_sdsm.decode('utf-8')
