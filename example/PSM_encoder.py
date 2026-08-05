from pyv2xlib.PSMEncoder import psm_encoder
import random


if __name__ == '__main__':
    N = 5
    hex_psm = psm_encoder(
        basicType=random.choice(['unavailable', 'aPEDESTRIAN', 'aPEDALCYCLIST', 'aPUBLICSAFETYWORKER', 'anANIMAL']),
        secMark=random.randint(0, 65535),
        msgCnt=random.randint(0, 127),
        sourceID='ped1',
        position_lat=random.uniform(-90, 90),
        position_long=random.uniform(-179.9999999, 180),
        position_elevation=random.uniform(-409.5, 6143.9),  # optional
        accuracy_semiMajor=random.uniform(0, 12.7),
        accuracy_semiMinor=random.uniform(0, 12.7),
        accuracy_orientation=random.uniform(0, 359.9945078786),
        speed=random.uniform(0, 163.8),
        heading=random.uniform(0, 359.9875),

        accelSet_long=random.uniform(-20, 20),  # optional
        accelSet_lat=random.uniform(-20, 20),  # optional
        accelSet_vert=random.uniform(-24.72, 24.92),  # optional
        accelSet_yaw=random.uniform(-327.67, 327.67),  # optional

        # pathHistory
        pathHistory_exists=True,
        pathHistory_initialPosition_exists=True,
        pathHistory_initialPosition_utcTime_year=2026,  # optional
        pathHistory_initialPosition_utcTime_month=random.randint(0, 12),  # optional
        pathHistory_initialPosition_utcTime_day=random.randint(0, 31),  # optional
        pathHistory_initialPosition_utcTime_hour=random.randint(0, 31),  # optional
        pathHistory_initialPosition_utcTime_minute=random.randint(0, 60),  # optional
        pathHistory_initialPosition_utcTime_second=random.uniform(0, 65.535),  # optional
        pathHistory_initialPosition_utcTime_offset=random.randint(-840, 840),  # optional
        pathHistory_initialPosition_long=random.uniform(-179.9999999, 180),
        pathHistory_initialPosition_lat=random.uniform(-90, 90),
        pathHistory_initialPosition_elevation=random.uniform(-409.5, 6143.9),  # optional
        pathHistory_initialPosition_heading=random.uniform(0, 359.9875),  # optional
        pathHistory_initialPosition_speed_transmission=random.choice(['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']),  # optional
        pathHistory_initialPosition_speed_velocity=random.uniform(0, 163.8),  # optional
        pathHistory_initialPosition_posAccuracy_semiMajor=random.uniform(0, 12.7),  # optional
        pathHistory_initialPosition_posAccuracy_semiMinor=random.uniform(0, 12.7),  # optional
        pathHistory_initialPosition_posAccuracy_orientation=random.uniform(0, 359.9945078786),  # optional
        pathHistory_initialPosition_timeConfidence=random.uniform(0, 100),  # optional
        pathHistory_initialPosition_posConfidence_pos=random.uniform(0, 500),  # optional
        pathHistory_initialPosition_posConfidence_elevation=random.uniform(0, 500),  # optional
        pathHistory_initialPosition_speedConfidence_heading=random.uniform(0, 10),  # optional
        pathHistory_initialPosition_speedConfidence_speed=random.uniform(0, 100),  # optional
        pathHistory_initialPosition_speedConfidence_throttle=random.uniform(0, 0.1),  # optional
        pathHistory_currGNSSstatus=random.randint(0, 255),  # optional

        pathHistory_crumbData_N=N,
        # index 0 deliberately tests the "missing/unavailable" fallback path;
        # remaining N-1 entries are randomized within valid range
        pathHistory_crumbData_latOffset=[None] + [random.uniform(-0.0131071, 0.0131071) for _ in range(N - 1)],
        pathHistory_crumbData_lonOffset=[None] + [random.uniform(-0.0131071, 0.0131071) for _ in range(N - 1)],
        pathHistory_crumbData_elevationOffset=[None] + [random.uniform(-204.7, 204.7) for _ in range(N - 1)],
        pathHistory_crumbData_timeOffset=[None] + [random.uniform(0.01, 655.34) for _ in range(N - 1)],
        # index 0 deliberately tests the 163.80 boundary (avoids the 163.82/8191 sentinel collision)
        pathHistory_crumbData_speed=[163.80] + [random.uniform(0, 163.80) for _ in range(N - 1)],  # optional
        pathHistory_crumbData_posAccuracy_semiMajor=[0] + [random.uniform(0, 12.7) for _ in range(N - 1)],  # optional
        pathHistory_crumbData_posAccuracy_semiMinor=[0] + [random.uniform(0, 12.7) for _ in range(N - 1)],  # optional
        pathHistory_crumbData_posAccuracy_orientation=[0] + [random.uniform(0, 359.9945078786) for _ in range(N - 1)],  # optional
        # index 0 deliberately tests the top boundary of the heading range
        pathHistory_crumbData_heading=[358.5] + [random.uniform(0, 358.5) for _ in range(N - 1)],  # optional

        # pathPrediction
        pathPrediction_radiusOfCurve=random.uniform(-3276.7, 3276.7),  # optional
        pathPrediction_confidence=random.uniform(0, 100),  # optional

        # propulsion
        propulsion_type='human',  # optional
        propulsion_value='onFoot',  # optional

        useState=random.randint(0, 511),  # optional
        crossRequest=random.choice([True, False]),  # optional
        crossState=random.choice([True, False]),  # optional
        clusterSize=random.choice(['unavailable', 'small', 'medium', 'large']),  # optional
        clusterRadius=random.randint(0, 100),  # optional
        eventResponderType=random.choice(['unavailable', 'towOperator', 'fireAndEMSWorker', 'aDOTWorker', 'lawEnforcement', 'hazmatResponder', 'animalControlWorker', 'otherPersonnel']),  # optional
        activityType=random.randint(0, 63),  # optional
        activitySubType=random.randint(0, 127),  # optional
        assistType=random.randint(0, 63),  # optional
        sizing=random.randint(0, 31),  # optional
        attachment=random.choice(['unavailable', 'stroller', 'bicycleTrailer', 'cart', 'wheelchair', 'otherWalkAssistAttachments', 'pet']),  # optional
        attachmentRadius=random.randint(0, 200),  # optional
        animalType=random.choice(['unavailable', 'serviceUse', 'pet', 'farm']),  # optional
    )
    print('Encoder result:')
    print(hex_psm)