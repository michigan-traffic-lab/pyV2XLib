from pyv2xlib.RSAEncoder import rsa_encoder
import random


if __name__ == '__main__':
    hex_rsa = rsa_encoder(
        msgCnt=random.randint(0, 127),
        timeStamp=random.randint(0, 527039),  # optional

        # integer represents the ITIS code of the corresponding event
        typeEvent=1793,  # 'vehicle-traveling-wrong-way'
        description=[8032] + [random.choice([   # 8032 = 'intersection' 
            7438,  # 'allow-emergency-vehicles-to-pass' 
            7440,  # 'pull-over-to-the-edge-of-the-roadway' 
            7443,  # 'reduce-your-speed' 
            7444,  # 'observe-speed-limits' 
        ]) for _ in range(2)],  # optional
        
        priority=random.randint(0, 7),  # optional
        heading=random.randint(0, 65535),  # optional 
        extent=random.choice(['useInstantlyOnly', 'useFor3meters', 'useFor10meters', 'useFor50meters',
                               'useFor100meters', 'useFor500meters', 'useFor1000meters', 'useFor5000meters',
                               'useFor10000meters', 'useFor50000meters', 'useFor100000meters',
                               'useFor500000meters', 'useFor1000000meters', 'useFor5000000meters',
                               'useFor10000000meters', 'forever']),  # optional

        position_exists=True,
        position_utcTime_year=2026,  # optional
        position_utcTime_month=random.randint(0, 12),  # optional
        position_utcTime_day=random.randint(0, 31),  # optional
        position_utcTime_hour=random.randint(0, 31),  # optional
        position_utcTime_minute=random.randint(0, 60),  # optional
        position_utcTime_second=random.uniform(0, 65.535),  # optional
        position_utcTime_offset=random.randint(-840, 840),  # optional
        position_long=random.uniform(-179.9999999, 180),
        position_lat=random.uniform(-90, 90),
        position_elevation=random.uniform(-409.5, 6143.9),  # optional
        position_heading=random.uniform(0, 359.9875),  # optional
        position_speed_transmission=random.choice(['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']),  # optional
        position_speed_velocity=163.8,  # optional
        position_posAccuracy_semiMajor=random.uniform(0, 12.7),  # optional
        position_posAccuracy_semiMinor=random.uniform(0, 12.7),  # optional
        position_posAccuracy_orientation=random.uniform(0, 359.9945078786),  # optional
        position_timeConfidence=random.uniform(0, 100),  # optional
        position_posConfidence_pos=random.uniform(0, 500),  # optional
        position_posConfidence_elevation=random.uniform(0, 500),  # optional
        position_speedConfidence_heading=random.uniform(0, 10),  # optional
        position_speedConfidence_speed=random.uniform(0, 100),  # optional
        position_speedConfidence_throttle=random.uniform(0, 0.1),  # optional

        furtherInfoID=random.randint(0, 65535),  # optional
    )
    print('Encoder result:')
    print(hex_rsa)