from pyv2xlib.TIMEncoder import tim_encoder
import random


if __name__ == '__main__':
    hex_tim = tim_encoder(
        msgCnt=random.randint(0, 127),
        timeStamp=random.randint(0, 527039),  # optional
        packetID=random.randint(0, 2 ** 72 - 1),  # optional
        urlB='http://mdot.gov/tim/a',  # optional

        dataFrames_N=1,
        dataFrames_frameType=['advisory'],
        dataFrames_msgId=['furtherInfoID'],
        dataFrames_furtherInfoID=[random.randint(0, 65535)],

        dataFrames_startYear=[2026],  # optional
        dataFrames_startTime=[random.randint(0, 527039)],
        dataFrames_durationTime=[random.randint(0, 32000)],
        dataFrames_priority=[random.randint(0, 7)],

        dataFrames_regions_N=[1],
        dataFrames_region_name=[['Main St Construction']],  # optional
        dataFrames_region_lat=[[random.uniform(-90, 90)]],  # optional
        dataFrames_region_long=[[random.uniform(-179.9999999, 180)]],  # optional
        dataFrames_region_elevation=[[random.uniform(-409.5, 6143.9)]],  # optional
        dataFrames_region_laneWidth=[[random.uniform(0, 327.67)]],  # optional
        dataFrames_region_directionality=[[random.choice(['unavailable', 'forward', 'reverse', 'both'])]],  # optional
        dataFrames_region_closedPath=[[random.choice([True, False])]],  # optional
        dataFrames_region_direction=[[random.randint(0, 65535)]],  # optional

        # description: 'geometry' branch (a circle)
        dataFrames_region_description='geometry',
        dataFrames_region_geometry_direction=[[random.randint(0, 65535)]],
        dataFrames_region_geometry_extent=[[random.choice(['useInstantlyOnly', 'useFor3meters', 'useFor10meters',
                                                             'useFor50meters', 'useFor100meters', 'useFor500meters',
                                                             'useFor1000meters', 'useFor5000meters', 'useFor10000meters',
                                                             'useFor50000meters', 'useFor100000meters', 'useFor500000meters',
                                                             'useFor1000000meters', 'useFor5000000meters',
                                                             'useFor10000000meters', 'forever'])]],  # optional
        dataFrames_region_geometry_laneWidth=[[random.uniform(0, 327.67)]],  # optional
        dataFrames_region_geometry_circle_lat=[[random.uniform(-90, 90)]],
        dataFrames_region_geometry_circle_long=[[random.uniform(-179.9999999, 180)]],
        dataFrames_region_geometry_circle_elevation=[[random.uniform(-409.5, 6143.9)]],  # optional
        dataFrames_region_geometry_circle_radius=[[random.randint(0, 4095)]],
        dataFrames_region_geometry_circle_units=[[random.choice(['centimeter', 'cm2-5', 'decimeter', 'meter',
                                                                   'kilometer', 'foot', 'yard', 'mile'])]],

        # content: 'advisory' branch
        # integer represents the ITIS code of the corresponding event
        dataFrames_content_type=['advisory'],
        dataFrames_content_items=[[
            {'type': 'itis', 'value': 1025},  # 'road-construction' (ITIS Roadwork category)
            {'type': 'itis', 'value': 7443},  # 'reduce-your-speed' (ITIS AdviceInstructionsMandatory)
        ]],
        dataFrames_url=['a123'],  # optional
    )
    print('Encoder result:')
    print(hex_tim)