import random
import json

from pyv2xlib.ICAEncoder import ica_encoder
from pyv2xlib.ICADecoder import ica_decoder


if __name__ == '__main__':
    N = 5
    hex_ica = ica_encoder(
        msgCnt=random.randint(0, 127),
        sourceID='hihi',
        iCATimeStamp=random.randint(0, 527039),  # optional

        # partOne
        partOne_exists=True,
        partOne_msgCnt=random.randint(0, 127),
        partOne_sourceID='car1',
        partOne_secMark=random.randint(0, 65535),
        partOne_lat=random.uniform(-90, 90),
        partOne_long=random.uniform(-179.9999999, 180),
        partOne_elev=random.uniform(-409.5, 6143.9),
        partOnePosAcc_semiMajor=random.uniform(0, 12.7),
        partOnePosAcc_semiMinor=random.uniform(0, 12.7),
        partOnePosAcc_orientation=random.uniform(0, 359.9945078786),
        partOne_transmission=random.choice(['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']),
        partOne_speed=random.uniform(0, 163.8),
        partOne_heading=random.uniform(0, 359.9875),
        partOne_angle=random.uniform(-189, 189),
        partOne_accelSet_long=random.uniform(-20, 20),
        partOne_accelSet_lat=random.uniform(-20, 20),
        partOne_accelSet_vert=random.uniform(-2.52 * 9.80665, 2.54 * 9.80665),
        partOne_accelSet_yaw=random.uniform(-327.67, 327.67),
        partOne_brakes_wheelBrakes=random.randint(0, 31),
        partOne_brakes_traction=random.choice(['unavailable', 'off', 'on', 'engaged']),
        partOne_brakes_abs=random.choice(['unavailable', 'off', 'on', 'engaged']),
        partOne_brakes_scs=random.choice(['unavailable', 'off', 'on', 'engaged']),
        partOne_brakes_brakeBoost=random.choice(['unavailable', 'off', 'on']),
        partOne_brakes_auxBrakes=random.choice(['unavailable', 'off', 'on']),
        partOne_size_width=random.randint(0, 1023),
        partOne_size_length=random.randint(0, 4095),

        # path
        path_exists=True,
        path_initialPosition_exists=True,
        path_initialPosition_utcTime_year=2026,  # optional
        path_initialPosition_utcTime_month=random.randint(0, 12),  # optional
        path_initialPosition_utcTime_day=random.randint(0, 31),  # optional
        path_initialPosition_utcTime_hour=random.randint(0, 31),  # optional
        path_initialPosition_utcTime_minute=random.randint(0, 60),  # optional
        path_initialPosition_utcTime_second=random.uniform(0, 65.535),  # optional
        path_initialPosition_utcTime_offset=random.randint(-840, 840),  # optional
        path_initialPosition_long=random.uniform(-179.9999999, 180),
        path_initialPosition_lat=random.uniform(-90, 90),
        path_initialPosition_elevation=random.uniform(-409.5, 6143.9),  # optional
        path_initialPosition_heading=random.uniform(0, 359.9875),  # optional
        path_initialPosition_speed_transmission=random.choice(['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']),  # optional
        path_initialPosition_speed_velocity=random.uniform(0, 163.8),  # optional
        path_initialPosition_posAccuracy_semiMajor=random.uniform(0, 12.7),  # optional
        path_initialPosition_posAccuracy_semiMinor=random.uniform(0, 12.7),  # optional
        path_initialPosition_posAccuracy_orientation=random.uniform(0, 359.9945078786),  # optional
        path_initialPosition_timeConfidence=random.uniform(0, 100),  # optional
        path_initialPosition_posConfidence_pos=random.uniform(0, 500),  # optional
        path_initialPosition_posConfidence_elevation=random.uniform(0, 500),  # optional
        path_initialPosition_speedConfidence_heading=random.uniform(0, 10),  # optional
        path_initialPosition_speedConfidence_speed=random.uniform(0, 100),  # optional
        path_initialPosition_speedConfidence_throttle=random.uniform(0, 0.1),  # optional
        path_currGNSSstatus=random.randint(0, 255),  # optional

        path_crumbData_N=N,
        path_crumbData_latOffset=[None] + [random.uniform(-0.0131071, 0.0131071) for _ in range(N - 1)],
        path_crumbData_lonOffset=[None] + [random.uniform(-0.0131071, 0.0131071) for _ in range(N - 1)],
        path_crumbData_elevationOffset=[None] + [random.uniform(-204.7, 204.7) for _ in range(N - 1)],
        path_crumbData_timeOffset=[None] + [random.uniform(0.01, 655.34) for _ in range(N - 1)],
        path_crumbData_speed=[163.8] + [random.uniform(0, 163.8) for _ in range(N - 1)],  # optional
        path_crumbData_posAccuracy_semiMajor=[0] + [random.uniform(0, 12.7) for _ in range(N - 1)],  # optional
        path_crumbData_posAccuracy_semiMinor=[0] + [random.uniform(0, 12.7) for _ in range(N - 1)],  # optional
        path_crumbData_posAccuracy_orientation=[0] + [random.uniform(0, 359.9945078786) for _ in range(N - 1)],  # optional
        path_crumbData_heading=[358.5] + [random.uniform(0, 358.5) for _ in range(N - 1)],  # optional

        # pathPrediction
        pathPrediction_radiusOfCurve=random.uniform(-3276.7, 3276.7),
        pathPrediction_confidence=random.uniform(0, 100),

        # intersectionID
        intersectionID_id=random.randint(0, 65535),
        intersectionID_region=random.randint(0, 65535),  # optional

        # laneNumber
        laneNumber_type=random.choice(['approach', 'lane']),
        laneNumber_value=random.randint(0, 15),

        # eventFlag
        eventFlag_value=random.randint(1, 16383),
    )

    # here is an example of ICA
    # hex_ica = '0017717903434b434903e40563617231d8bf1f3aa35f498c12f93eda2abc47de3fffc203f4e6531113a8d986ca400ac08a000000000001fffdffff0572b9a5b561be863d02fd62b57e138f38a20fb329225d714c8fcdfda618bba42694b699b9fda20f99dc685f2e16798a494c03fda130e46d00'

    print('ICA:')
    print(hex_ica)

    output = ica_decoder(hex_ica)
    print('Decoder result:')
    print(json.dumps(output, indent=4, default=str))