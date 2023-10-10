from pycrate_sdsm.SDSMEncoder import sdsm_encoder
import random


if __name__ == '__main__':
    N = 1
    hex_sdsm = sdsm_encoder(
        msgCnt=random.randint(0, 127),
        sourceID='test',
        equipmentType=random.choice(['unknown', 'rsu', 'obu', 'vru']),
        sDSMTimeStamp_year=2023,  # optional
        sDSMTimeStamp_month=random.randint(0, 12),  # optional
        sDSMTimeStamp_day=random.randint(0, 31),  # optional
        sDSMTimeStamp_hour=random.randint(0, 31),  # optional
        sDSMTimeStamp_minute=random.randint(0, 60),  # optional
        sDSMTimeStamp_second=random.uniform(0, 65.535),  # optional
        sDSMTimeStamp_offset=random.randint(-840, 840),  # optional
        refPos_lat=random.uniform(-90, 90),
        refPos_long=random.uniform(-180, 180),
        refPos_elevation=random.uniform(-409.6, 6143.9),  # optional
        refPosXYConf_semiMajor=random.uniform(0, 13),
        refPosXYConf_semiMinor=random.uniform(0, 13),
        refPosXYConf_orientation=random.uniform(0, 360),
        refPosElConf=random.uniform(0, 550),  # optional
        objects_N=N,  # objects_N > 0
        objects_detObjCommon_objType=['vehicle'] + [random.choice(['unknown', 'vehicle', 'vru', 'animal']) for _ in range(N-1)],
        objects_detObjCommon_objTypeCfd=[101] + [random.randint(0, 101) for _ in range(N-1)],
        objects_detObjCommon_objectID=[0] + [random.randint(0, 65535) for _ in range(N-1)],
        objects_detObjCommon_measurementTime=[0] + [random.uniform(-1.5, 1.5) for _ in range(N-1)],
        objects_detObjCommon_timeConfidence=[0] + [random.uniform(0, 110) for _ in range(N-1)],
        objects_detObjCommon_pos_offsetX=[0] + [random.uniform(-3276.7, 3276.7) for _ in range(N-1)],
        objects_detObjCommon_pos_offsetY=[0] + [random.uniform(-3276.7, 3276.7) for _ in range(N-1)],
        objects_detObjCommon_pos_offsetZ=[0] + [random.uniform(-3276.7, 3276.7) for _ in range(N-1)],  # optional
        objects_detObjCommon_posConfidence_pos=[0] + [random.uniform(0, 550) for _ in range(N-1)],
        objects_detObjCommon_posConfidence_elevation=[0] + [random.uniform(0, 550) for _ in range(N-1)],
        objects_detObjCommon_speed=[163.82] + [random.uniform(0, 163.8) for _ in range(N-1)],
        objects_detObjCommon_speedConfidence=[0] + [random.uniform(0, 110) for _ in range(N-1)],
        objects_detObjCommon_speedZ=[163.82] + [random.uniform(0, 163.82) for _ in range(N-1)],  # optional
        objects_detObjCommon_speedConfidenceZ=[0] + [random.uniform(0, 110) for _ in range(N-1)],  # optional
        objects_detObjCommon_heading=[359.999999] + [random.uniform(0, 360) for _ in range(N-1)],
        objects_detObjCommon_headingConf=[0] + [random.uniform(0, 12) for _ in range(N-1)],
        objects_detObjCommon_accel4way_lat=[20.01] + [random.uniform(-20, 20.01) for _ in range(N-1)],  # optional
        objects_detObjCommon_accel4way_long=[20.01] + [random.uniform(-20, 20.01) for _ in range(N-1)],  # optional
        objects_detObjCommon_accel4way_vert=[-24.9174] + [random.uniform(-24.9174, 24.9174) for _ in range(N-1)],  # optional
        objects_detObjCommon_accel4way_yaw=[0] + [random.uniform(-327.67, 327.67) for _ in range(N-1)],  # optional
        objects_detObjCommon_accCfdX=[0] + [random.uniform(0, 110) for _ in range(N-1)],  # optional
        objects_detObjCommon_accCfdY=[0] + [random.uniform(0, 110) for _ in range(N-1)],  # optional
        objects_detObjCommon_accCfdZ=[0] + [random.uniform(0, 110) for _ in range(N-1)],  # optional
        objects_detObjCommon_accCfdYaw=[0] + [random.uniform(0, 110) for _ in range(N-1)],  # optional

        objects_detObjOptData_type=['Veh'] + [random.choice(['Veh', 'VRU', 'Obst']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_lights=[b'0'] + [random.choice([b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAttitude_pitch=[91] + [random.uniform(-90, 90) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAttitude_roll=[-181] + [random.uniform(-180, 180) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAttitude_yaw=[181] + [random.uniform(-180, 180) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAttitudeConfidence_pitchConffidence=[0] + [random.uniform(0, 12) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAttitudeConfidence_rollConffidence=[0] + [random.uniform(0, 12) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAttitudeConfidence_yawConffidence=[0] + [random.uniform(0, 12) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAngleVel_pitchRate=[360] + [random.uniform(-327.67, 327.67) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAngleVel_rollRate=[360] + [random.uniform(-327.67, 327.67) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAngleVelConfidence_pitchRateConfidence=[0] + [random.uniform(0, 120) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehAngleVelConfidence_rollRateConfidence=[0] + [random.uniform(0, 120) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_size_width=[11] + [random.uniform(0, 10.23) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_size_length=[100] + [random.uniform(0, 40.95) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_height=[10] + [random.uniform(0, 6.35) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleWidthConfidence=[15] + [random.uniform(0, 120) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleLengthConfidence=[15] + [random.randint(0, 120) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehicleSizeConfidence_vehicleHeightConfidence=[15] + [random.randint(0, 120) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_vehicleClass=[256] + [random.randint(0, 255) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVeh_classConf=[101] + [random.randint(0, 100) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVRU_basicType=['aPEDESTRIAN'] + [random.choice(['unavailable', 'aPEDESTRIAN', 'aPEDALCYCLIST', 'aPUBLICSAFETYWORKER', 'anANIMAL']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVRU_propulsion=['human'] + [random.choice(['human', 'animal', 'motor']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVRU_propulsion_human=['onFoot'] + [random.choice(['unavailable', 'otherTypes', 'onFoot', 'skateboard', 'pushOrKickScooter', 'wheelchair']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVRU_propulsion_animal=['animalMounted'] + [random.choice(['unavailable', 'otherTypes', 'animalMounted', 'animalDrawnCarriage']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVRU_propulsion_motor=['wheelChair'] + [random.choice(['unavailable', 'otherTypes', 'wheelChair', 'bicycle', 'scooter', 'selfBalancingDevice']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVRU_attachment=['stroller'] + [random.choice(['unavailable', 'stroller', 'bicycleTrailer', 'cart', 'wheelchair', 'otherWalkAssistAttachments', 'pet']) for _ in range(N-1)],  # optional
        objects_detObjOptData_detVRU_radius=[21] + [random.randint(0, 200) for _ in range(N-1)],  # optional
        objects_detObjOptData_detObst_obstSize_width=[2] + [random.uniform(0, 10.23) for _ in range(N-1)],  # optional
        objects_detObjOptData_detObst_obstSize_length=[4.1] + [random.uniform(0, 10.23) for _ in range(N-1)],  # optional
        objects_detObjOptData_detObst_obstSize_height=[3.1] + [random.uniform(0, 10.23) for _ in range(N-1)],  # optional
        objects_detObjOptData_detObst_obstSizeConfidence_widthConfidence=[15] + [random.uniform(0, 120) for _ in range(N-1)],  # optional
        objects_detObjOptData_detObst_obstSizeConfidence_lengthConfidence=[15] + [random.uniform(0, 120) for _ in range(N-1)],  # optional
        objects_detObjOptData_detObst_obstSizeConfidence_heightConfidence=[15] + [random.uniform(0, 120) for _ in range(N-1)],  # optional
    )
    print('Encoder result:')
    print(hex_sdsm)
