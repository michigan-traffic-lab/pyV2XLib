from binascii import hexlify, unhexlify
from .utils import load_v2xlib
v2xlib = load_v2xlib()

def rsa_encoder(msgCnt=None,
                timeStamp=None,  # optional
                typeEvent=None,
                description=[],  # optional
                priority=None,  # optional
                heading=None,  # optional
                extent=None,  # optional
                position_exists=False,
                # if position_exists is True, position_long and position_lat are mandatory
                position_utcTime_year=None,  # optional
                position_utcTime_month=None,  # optional
                position_utcTime_day=None,  # optional
                position_utcTime_hour=None,  # optional
                position_utcTime_minute=None,  # optional
                position_utcTime_second=None,  # optional
                position_utcTime_offset=None,  # optional
                position_long=None,
                position_lat=None,
                position_elevation=None,  # optional
                position_heading=None,  # optional
                position_speed_transmission=None,  # optional
                position_speed_velocity=None,  # optional
                position_posAccuracy_semiMajor=None,  # optional
                position_posAccuracy_semiMinor=None,  # optional
                position_posAccuracy_orientation=None,  # optional
                position_timeConfidence=None,  # optional
                position_posConfidence_pos=None,  # optional
                position_posConfidence_elevation=None,  # optional
                position_speedConfidence_heading=None,  # optional
                position_speedConfidence_speed=None,  # optional
                position_speedConfidence_throttle=None,  # optional

                furtherInfoID=None,  # optional
                ):
    '''
    This function encodes RSA message.

    Args:
        msgCnt (int): Message counter. Range: [0, 127]. Mandatory.
        timeStamp (int): Minute of the year this alert was generated. Range: [0, 527040]. Optional.
        typeEvent (int): The primary ITIS code describing the hazard/event (e.g. accident, wrong-way driver, obstruction). See itis_codes.py for a lookup table of names to codes. Range: [0, 65535]. Mandatory.
        description (list): Up to 8 additional ITIS codes providing further detail or advice on top of typeEvent (e.g. location context, "reduce your speed"). Each entry range: [0, 65535]. List size: [1, 8]. Optional.
        priority (int): Relative urgency of this alert compared to other RSA messages of the same type. 0 = routine (e.g. roadside signage), 7 = highest/most important. Encoded into the top 3 bits of a single byte. Range: [0, 7]. Optional.
        heading (int): 16-bit HeadingSlice bitmask. Each bit represents whether one 22.5-degree compass slice (starting at North, moving clockwise) is included as a direction this alert applies to. Multiple bits may be set to cover several direction ranges at once (e.g. 0x8181 = both due east and due west, each with a +/-22.5deg cone). This is NOT a single heading angle in degrees. Range: [0, 65535]. Optional.
        extent (str): How far (in distance traveled past the hazard) this alert should remain relevant, chosen from a fixed set of tiers. One of useInstantlyOnly, useFor3meters, useFor10meters, useFor50meters, useFor100meters, useFor500meters, useFor1000meters, useFor5000meters, useFor10000meters, useFor50000meters, useFor100000meters, useFor500000meters, useFor1000000meters, useFor5000000meters, useFor10000000meters, or forever. Optional.

        position_exists (bool): True if the FullPositionVector describing the hazard's location is included. Mandatory.
        position_utcTime_year (int): Year of the position timestamp. Range: [0, 4095]. Optional.
        position_utcTime_month (int): Month of the position timestamp. Range: [0, 12]. Optional.
        position_utcTime_day (int): Day of the position timestamp. Range: [0, 31]. Optional.
        position_utcTime_hour (int): Hour of the position timestamp. Range: [0, 31]. Unit: hour. Optional.
        position_utcTime_minute (int): Minute of the position timestamp. Range: [0, 60]. Unit: minute. Optional.
        position_utcTime_second (float): Second of the position timestamp. Range: [0, 65.535]. Unit: second. Optional.
        position_utcTime_offset (int): UTC offset of the position timestamp. Range: [-840, 840]. Unit: minute. Optional.
        position_long (float): Longitude of the hazard/alert location. Range: [-179.9999999, 180]. Unit: deg. Mandatory if position_exists.
        position_lat (float): Latitude of the hazard/alert location. Range: [-90, 90]. Unit: deg. Mandatory if position_exists.
        position_elevation (float): Elevation of the hazard/alert location. Range: [-409.5, 6143.9]. Unit: meter. Optional.
        position_heading (float): Heading at the position (a single angle, distinct from the top-level HeadingSlice bitmask field). Range: [0, 359.9875]. Unit: deg. Optional.
        position_speed_transmission (str): Transmission/gear state associated with the position (e.g. if reported from a moving source). One of neutral, park, forwardGears, reverseGears, unavailable. Optional.
        position_speed_velocity (float): Speed associated with the position. Range: [0, 163.8]. 163.8 is the practical max to avoid colliding with the 8191 (encoded) "unavailable" sentinel value. Unit: m/s. Optional.
        position_posAccuracy_semiMajor (float): Radius of the semi-major axis of the GPS uncertainty ellipse. Range: [0, 12.7]. 12.75 (encoded) = unavailable. Unit: meter. Optional.
        position_posAccuracy_semiMinor (float): Radius of the semi-minor axis of the GPS uncertainty ellipse. Range: [0, 12.7]. 12.75 (encoded) = unavailable. Unit: meter. Optional.
        position_posAccuracy_orientation (float): Orientation angle of the semi-major axis relative to true north. Range: [0, 359.9945078786]. 360 (encoded) = unavailable. Unit: deg. Optional.
        position_timeConfidence (float): 95% confidence interval for the position timestamp. Mapped to the nearest enumerated tier (e.g. time-010-000). Range: (0, 100+]. Unit: second. Optional.
        position_posConfidence_pos (float): 95% confidence interval for the horizontal position. Mapped to the nearest enumerated tier (e.g. a5m). Range: (0, 500+]. Unit: meter. Optional.
        position_posConfidence_elevation (float): 95% confidence interval for the elevation. Mapped to the nearest enumerated tier (e.g. elev-002-00). Range: (0, 500+]. Unit: meter. Optional.
        position_speedConfidence_heading (float): 95% confidence interval for heading at the position. Mapped to the nearest enumerated tier (e.g. prec01deg). Range: (0, 10+]. Unit: deg. Optional.
        position_speedConfidence_speed (float): 95% confidence interval for speed at the position. Mapped to the nearest enumerated tier (e.g. prec1ms). Range: (0, 100+]. Unit: m/s. Optional.
        position_speedConfidence_throttle (float): 95% confidence interval for throttle at the position. Mapped to the nearest enumerated tier (e.g. prec1percent). Range: (0, 0.1+]. Unit: percent as fraction. Optional.

        furtherInfoID (int): A 2-byte link/reference number to other messages related to the same event (e.g. a fuller ATIS incident description elsewhere). Use 0 when unknown or not present. Range: [0, 65535]. Optional.

    Returns:
        hex_rsa (str): RSA message encoded as a hex string.
    '''
    rsa = {}

    if msgCnt is None:
        print('msgCnt is mandatory! Please provide msgCnt. Set to 0.')
        rsa['msgCnt'] = 0
    elif not isinstance(msgCnt, int):
        print('msgCnt should be an integer! But', msgCnt, 'is provided. Set to 0.')
        rsa['msgCnt'] = 0
    elif msgCnt < 0 or msgCnt > 127:
        print('msgCnt should be in range [0, 127]! But', msgCnt, 'is provided. Set to 0.')
        rsa['msgCnt'] = 0
    else:
        rsa['msgCnt'] = msgCnt

    if timeStamp is not None:
        if not isinstance(timeStamp, int):
            print('timeStamp should be an integer! But', timeStamp, 'is provided. Remove it.')
        elif timeStamp < 0 or timeStamp > 527040:
            print('timeStamp should be in range [0, 527040]! But', timeStamp, 'is provided. Remove it.')
        else:
            rsa['timeStamp'] = timeStamp

    if typeEvent is None:
        print('typeEvent is mandatory! Please provide typeEvent. Set to 0.')
        rsa['typeEvent'] = 0
    elif not isinstance(typeEvent, int):
        print('typeEvent should be an integer ITIS code! But', typeEvent, 'is provided. Set to 0.')
        rsa['typeEvent'] = 0
    elif typeEvent < 0 or typeEvent > 65535:
        print('typeEvent should be in range [0, 65535]! But', typeEvent, 'is provided. Set to 0.')
        rsa['typeEvent'] = 0
    else:
        rsa['typeEvent'] = typeEvent

    if description is not None:
        if not isinstance(description, list):
            print('description should be a list of ITIS codes! But', description, 'is provided. Remove it.')
        elif len(description) < 1 or len(description) > 8:
            print('description should have 1 to 8 ITIS codes! But', len(description), 'codes provided. Remove it.')
        else:
            rsa['description'] = []
            for i, code in enumerate(description):
                if not isinstance(code, int):
                    print('description[', i, '] should be an integer ITIS code! But', code, 'is provided. Skip it.')
                elif code < 0 or code > 65535:
                    print('description[', i, '] should be in range [0, 65535]! But', code, 'is provided. Skip it.')
                else:
                    rsa['description'].append(code)
            if len(rsa['description']) == 0:
                print('No valid ITIS codes in description. Remove it.')
                del rsa['description']

    if priority is not None:
        if not isinstance(priority, int):
            print('priority should be an integer! But', priority, 'is provided. Set to 0 (routine).')
            rsa['priority'] = bytes([0])
        elif priority < 0 or priority > 7:
            print('priority should be in range [0, 7]! But', priority, 'is provided. Set to 0 (routine).')
            rsa['priority'] = bytes([0])
        else:
            rsa['priority'] = bytes([priority << 5])

    if heading is not None:
        if not isinstance(heading, int):
            print('heading should be an integer! But', heading, 'is provided. Set to 0.')
            rsa['heading'] = (0, 16)
        elif heading < 0 or heading > 65535:
            print('heading should be in a range [0, 65535] but', heading, 'is provided. Set to 0.')
            rsa['heading'] = (0, 16)
        else:
            rsa['heading'] = (heading, 16)

    if extent is not None:
        if extent in ['useInstantlyOnly', 'useFor3meters', 'useFor10meters', 'useFor50meters', 'useFor100meters', 'useFor500meters', 'useFor1000meters', 'useFor5000meters', 'useFor10000meters', 'useFor50000meters', 'useFor100000meters', 'useFor500000meters', 'useFor1000000meters', 'useFor5000000meters', 'useFor10000000meters', 'forever']:
            rsa['extent'] = extent
        else:
            print('extent should be one of useInstantlyOnly, useFor3meters, useFor10meters, useFor50meters, useFor100meters, useFor500meters, useFor1000meters, useFor5000meters, useFor10000meters, useFor50000meters, useFor100000meters, useFor500000meters, useFor1000000meters, useFor5000000meters, useFor10000000meters, forever. But', extent, 'is provided. Set to forever.')
            rsa['extent'] = 'forever'

    if position_exists:
        rsa['position'] = {}
        utcTime = {}
 
        if position_utcTime_year is not None:
            if not isinstance(position_utcTime_year, int):
                print('position_utcTime_year should be an integer! But', position_utcTime_year, 'is provided. Remove it.')
            elif position_utcTime_year < 0 or position_utcTime_year > 4095:
                print('position_utcTime_year should be in range [0, 4095]! But', position_utcTime_year, 'is provided. Remove it.')
            else:
                utcTime['year'] = position_utcTime_year
 
        if position_utcTime_month is not None:
            if not isinstance(position_utcTime_month, int):
                print('position_utcTime_month should be an integer! But', position_utcTime_month, 'is provided. Remove it.')
            elif position_utcTime_month < 0 or position_utcTime_month > 12:
                print('position_utcTime_month should be in range [0, 12]! But', position_utcTime_month, 'is provided. Remove it.')
            else:
                utcTime['month'] = position_utcTime_month
 
        if position_utcTime_day is not None:
            if not isinstance(position_utcTime_day, int):
                print('position_utcTime_day should be an integer! But', position_utcTime_day, 'is provided. Remove it.')
            elif position_utcTime_day < 0 or position_utcTime_day > 31:
                print('position_utcTime_day should be in range [0, 31]! But', position_utcTime_day, 'is provided. Remove it.')
            else:
                utcTime['day'] = position_utcTime_day
 
        if position_utcTime_hour is not None:
            if not isinstance(position_utcTime_hour, int):
                print('position_utcTime_hour should be an integer! But', position_utcTime_hour, 'is provided. Remove it.')
            elif position_utcTime_hour < 0 or position_utcTime_hour > 31:
                print('position_utcTime_hour should be in range [0, 31] h! But', position_utcTime_hour, 'is provided. Remove it.')
            else:
                utcTime['hour'] = position_utcTime_hour
 
        if position_utcTime_minute is not None:
            if not isinstance(position_utcTime_minute, int):
                print('position_utcTime_minute should be an integer! But', position_utcTime_minute, 'is provided. Remove it.')
            elif position_utcTime_minute < 0 or position_utcTime_minute > 60:
                print('position_utcTime_minute should be in range [0, 60] min! But', position_utcTime_minute, 'is provided. Remove it.')
            else:
                utcTime['minute'] = position_utcTime_minute
 
        if position_utcTime_second is not None:
            if position_utcTime_second < 0 or position_utcTime_second > 65.535:
                print('position_utcTime_second should be in range [0, 65.535] s! But', position_utcTime_second, 'is provided. Remove it.')
            else:
                utcTime['second'] = int(position_utcTime_second * 10 ** 3)
 
        if position_utcTime_offset is not None:
            if not isinstance(position_utcTime_offset, int):
                print('position_utcTime_offset should be an integer! But', position_utcTime_offset, 'is provided. Remove it.')
            elif position_utcTime_offset < -840 or position_utcTime_offset > 840:
                print('position_utcTime_offset should be in range [-840, 840] min! But', position_utcTime_offset, 'is provided. Remove it.')
            else:
                utcTime['offset'] = position_utcTime_offset
 
        if utcTime:
            rsa['position']['utcTime'] = utcTime
 
        if position_long is None:
            print('position_long is mandatory if position is included! Set to 180.0000001.')
            rsa['position']['long'] = 1800000001
        elif position_long < -179.9999999 or position_long > 180:
            print('position_long should be in range [-179.9999999, 180] deg! But', position_long, 'is provided. Set to 180.0000001.')
            rsa['position']['long'] = 1800000001
        else:
            rsa['position']['long'] = int(position_long * 10 ** 7)
 
        if position_lat is None:
            print('position_lat is mandatory if position is included! Set to 90.0000001.')
            rsa['position']['lat'] = 900000001
        elif position_lat < -90 or position_lat > 90:
            print('position_lat should be in range [-90, 90] deg! But', position_lat, 'is provided. Set to 90.0000001.')
            rsa['position']['lat'] = 900000001
        else:
            rsa['position']['lat'] = int(position_lat * 10 ** 7)
 
        if position_elevation is not None:
            if position_elevation < -409.5 or position_elevation > 6143.9:
                print('position_elevation should be in range [-409.5, 6143.9] m! But', position_elevation, 'is provided. Remove it.')
                rsa['position']['elevation'] = -4096
            else:
                rsa['position']['elevation'] = int(position_elevation * 10)
 
        if position_heading is not None:
            if position_heading < 0 or position_heading > 359.9875:
                print('position_heading should be in range [0, 359.9875] deg! But', position_heading, 'is provided. Remove it.')
            else:
                rsa['position']['heading'] = int(position_heading / 0.0125)
 
        if position_speed_transmission is not None or position_speed_velocity is not None:
            rsa['position']['speed'] = {}
            if position_speed_transmission is None:
                print('position_speed_transmission is mandatory! Please provide. Set to unavailable.')
                rsa['position']['speed']['transmisson'] = 'unavailable'
            elif position_speed_transmission in ['neutral', 'park', 'forwardGears', 'reverseGears', 'unavailable']:
                rsa['position']['speed']['transmisson'] = position_speed_transmission
            else:
                print('position_speed_transmission should be one of neutral, park, forwardGears, reverseGears, or unavailable! But', position_speed_transmission, 'is provided. Set to unavailable.')
                rsa['position']['speed']['transmisson'] = 'unavailable'
 
            if position_speed_velocity is None:
                print('position_speed_velocity is mandatory! Please provide the speed. Set to unavailable.')
                rsa['position']['speed']['speed'] = 8191
            elif not isinstance(position_speed_velocity, (int, float)):
                print('position_speed_velocity should be a number! But', position_speed_velocity, 'is provided. Set to unavailable.')
                rsa['position']['speed']['speed'] = 8191
            elif position_speed_velocity < 0 or position_speed_velocity > 163.8:
                print('position_speed_velocity should be in range [0, 163.8] m/s! But', position_speed_velocity, 'is provided. Set to unavailable.')
                rsa['position']['speed']['speed'] = 8191
            else:
                rsa['position']['speed']['speed'] = int(position_speed_velocity * 50)
 
        if position_posAccuracy_semiMinor is not None or position_posAccuracy_semiMajor is not None or position_posAccuracy_orientation is not None:
            rsa['position']['posAccuracy'] = {}
            if position_posAccuracy_semiMajor is None:
                print('position_posAccuracy_semiMajor is mandatory! Please provide the radius of the semi-major axis of an ellipsoid. Set to 12.75.')
                rsa['position']['posAccuracy']['semiMajor'] = 255
            elif position_posAccuracy_semiMajor < 0:
                print('position_posAccuracy_semiMajor should be in range [0, 12.7] m! But', position_posAccuracy_semiMajor, 'is provided. Set to 12.75.')
                rsa['position']['posAccuracy']['semiMajor'] = 255
            elif position_posAccuracy_semiMajor > 12.7:
                print('position_posAccuracy_semiMajor should be in range [0, 12.7] m! But', position_posAccuracy_semiMajor, 'is provided. Set to 12.7.')
                rsa['position']['posAccuracy']['semiMajor'] = 254
            else:
                rsa['position']['posAccuracy']['semiMajor'] = int(position_posAccuracy_semiMajor * 20)
 
            if position_posAccuracy_semiMinor is None:
                print('position_posAccuracy_semiMinor is mandatory! Please provide the radius of the semi-minor axis of an ellipsoid. Set to 12.75.')
                rsa['position']['posAccuracy']['semiMinor'] = 255
            elif position_posAccuracy_semiMinor < 0:
                print('position_posAccuracy_semiMinor should be in range [0, 12.7] m! But', position_posAccuracy_semiMinor, 'is provided. Set to 12.75.')
                rsa['position']['posAccuracy']['semiMinor'] = 255
            elif position_posAccuracy_semiMinor > 12.7:
                print('position_posAccuracy_semiMinor should be in range [0, 12.7] m! But', position_posAccuracy_semiMinor, 'is provided. Set to 12.7.')
                rsa['position']['posAccuracy']['semiMinor'] = 254
            else:
                rsa['position']['posAccuracy']['semiMinor'] = int(position_posAccuracy_semiMinor * 20)
 
            if position_posAccuracy_orientation is None:
                print('position_posAccuracy_orientation is mandatory! Please provide the orientation of the angle of the semi-major axis of an ellipsoid. Set to 360.')
                rsa['position']['posAccuracy']['orientation'] = 65535
            elif position_posAccuracy_orientation < 0 or position_posAccuracy_orientation > 359.9945078786:
                print('position_posAccuracy_orientation should be in range [0, 359.9945078786] deg! But', position_posAccuracy_orientation, 'is provided. Set to 360.')
                rsa['position']['posAccuracy']['orientation'] = 65535
            else:
                rsa['position']['posAccuracy']['orientation'] = int(position_posAccuracy_orientation / 360 * 65535)
 
        if position_timeConfidence is not None:
            if position_timeConfidence <= 0:
                print('position_timeConfidence should be greater than 0 s! But', position_timeConfidence, 'is provided. Set to unavailable.')
                rsa['position']['timeConfidence'] = 'unavailable'
            elif 0 < position_timeConfidence <= 1e-11:
                rsa['position']['timeConfidence'] = 'time-000-000-000-000-01'
            elif 1e-11 < position_timeConfidence <= 2e-11:
                rsa['position']['timeConfidence'] = 'time-000-000-000-000-02'
            elif 2e-11 < position_timeConfidence <= 5e-11:
                rsa['position']['timeConfidence'] = 'time-000-000-000-000-05'
            elif 5e-11 < position_timeConfidence <= 1e-10:
                rsa['position']['timeConfidence'] = 'time-000-000-000-000-1'
            elif 1e-10 < position_timeConfidence <= 2e-10:
                rsa['position']['timeConfidence'] = 'time-000-000-000-000-2'
            elif 2e-10 < position_timeConfidence <= 5e-10:
                rsa['position']['timeConfidence'] = 'time-000-000-000-000-5'
            elif 5e-10 < position_timeConfidence <= 1e-9:
                rsa['position']['timeConfidence'] = 'time-000-000-000-001'
            elif 1e-9 < position_timeConfidence <= 2e-9:
                rsa['position']['timeConfidence'] = 'time-000-000-000-002'
            elif 2e-9 < position_timeConfidence <= 5e-9:
                rsa['position']['timeConfidence'] = 'time-000-000-000-005'
            elif 5e-9 < position_timeConfidence <= 1e-8:
                rsa['position']['timeConfidence'] = 'time-000-000-000-01'
            elif 1e-8 < position_timeConfidence <= 2e-8:
                rsa['position']['timeConfidence'] = 'time-000-000-000-02'
            elif 2e-8 < position_timeConfidence <= 5e-8:
                rsa['position']['timeConfidence'] = 'time-000-000-000-05'
            elif 5e-8 < position_timeConfidence <= 1e-7:
                rsa['position']['timeConfidence'] = 'time-000-000-000-1'
            elif 1e-7 < position_timeConfidence <= 2e-7:
                rsa['position']['timeConfidence'] = 'time-000-000-000-2'
            elif 2e-7 < position_timeConfidence <= 5e-7:
                rsa['position']['timeConfidence'] = 'time-000-000-000-5'
            elif 5e-7 < position_timeConfidence <= 1e-6:
                rsa['position']['timeConfidence'] = 'time-000-000-001'
            elif 1e-6 < position_timeConfidence <= 2e-6:
                rsa['position']['timeConfidence'] = 'time-000-000-002'
            elif 2e-6 < position_timeConfidence <= 5e-6:
                rsa['position']['timeConfidence'] = 'time-000-000-005'
            elif 5e-6 < position_timeConfidence <= 1e-5:
                rsa['position']['timeConfidence'] = 'time-000-000-01'
            elif 1e-5 < position_timeConfidence <= 2e-5:
                rsa['position']['timeConfidence'] = 'time-000-000-02'
            elif 2e-5 < position_timeConfidence <= 5e-5:
                rsa['position']['timeConfidence'] = 'time-000-000-05'
            elif 5e-5 < position_timeConfidence <= 1e-4:
                rsa['position']['timeConfidence'] = 'time-000-000-1'
            elif 1e-4 < position_timeConfidence <= 2e-4:
                rsa['position']['timeConfidence'] = 'time-000-000-2'
            elif 2e-4 < position_timeConfidence <= 5e-4:
                rsa['position']['timeConfidence'] = 'time-000-000-5'
            elif 5e-4 < position_timeConfidence <= 1e-3:
                rsa['position']['timeConfidence'] = 'time-000-001'
            elif 1e-3 < position_timeConfidence <= 2e-3:
                rsa['position']['timeConfidence'] = 'time-000-002'
            elif 2e-3 < position_timeConfidence <= 5e-3:
                rsa['position']['timeConfidence'] = 'time-000-005'
            elif 5e-3 < position_timeConfidence <= 1e-2:
                rsa['position']['timeConfidence'] = 'time-000-010'
            elif 1e-2 < position_timeConfidence <= 2e-2:
                rsa['position']['timeConfidence'] = 'time-000-020'
            elif 2e-2 < position_timeConfidence <= 5e-2:
                rsa['position']['timeConfidence'] = 'time-000-050'
            elif 5e-2 < position_timeConfidence <= 1e-1:
                rsa['position']['timeConfidence'] = 'time-000-100'
            elif 1e-1 < position_timeConfidence <= 2e-1:
                rsa['position']['timeConfidence'] = 'time-000-200'
            elif 2e-1 < position_timeConfidence <= 5e-1:
                rsa['position']['timeConfidence'] = 'time-000-500'
            elif 5e-1 < position_timeConfidence <= 1:
                rsa['position']['timeConfidence'] = 'time-001-000'
            elif 1 < position_timeConfidence <= 2:
                rsa['position']['timeConfidence'] = 'time-002-000'
            elif 2 < position_timeConfidence <= 10:
                rsa['position']['timeConfidence'] = 'time-010-000'
            elif 10 < position_timeConfidence <= 20:
                rsa['position']['timeConfidence'] = 'time-020-000'
            elif 20 < position_timeConfidence <= 50:
                rsa['position']['timeConfidence'] = 'time-050-000'
            elif 50 < position_timeConfidence <= 100:
                rsa['position']['timeConfidence'] = 'time-100-000'
            elif 100 < position_timeConfidence:
                rsa['position']['timeConfidence'] = 'unavailable'
 
        if position_posConfidence_pos is not None or position_posConfidence_elevation is not None:
            rsa['position']['posConfidence'] = {}
            if position_posConfidence_pos is None:
                print('position_posConfidence_pos is mandatory! Please provide. Set to unavailable')
                rsa['position']['posConfidence']['pos'] = 'unavailable'
            elif position_posConfidence_pos <= 0:
                print('position_posConfidence_pos should be greater than 0 m! But', position_posConfidence_pos, 'is provided. Set to unavailable.')
                rsa['position']['posConfidence']['pos'] = 'unavailable'
            elif 0 < position_posConfidence_pos <= 0.01:
                rsa['position']['posConfidence']['pos'] = 'a1cm'
            elif 0.01 < position_posConfidence_pos <= 0.02:
                rsa['position']['posConfidence']['pos'] = 'a2cm'
            elif 0.02 < position_posConfidence_pos <= 0.05:
                rsa['position']['posConfidence']['pos'] = 'a5cm'
            elif 0.05 < position_posConfidence_pos <= 0.1:
                rsa['position']['posConfidence']['pos'] = 'a10cm'
            elif 0.1 < position_posConfidence_pos <= 0.2:
                rsa['position']['posConfidence']['pos'] = 'a20cm'
            elif 0.2 < position_posConfidence_pos <= 0.5:
                rsa['position']['posConfidence']['pos'] = 'a50cm'
            elif 0.5 < position_posConfidence_pos <= 1:
                rsa['position']['posConfidence']['pos'] = 'a1m'
            elif 1 < position_posConfidence_pos <= 2:
                rsa['position']['posConfidence']['pos'] = 'a2m'
            elif 2 < position_posConfidence_pos <= 5:
                rsa['position']['posConfidence']['pos'] = 'a5m'
            elif 5 < position_posConfidence_pos <= 10:
                rsa['position']['posConfidence']['pos'] = 'a10m'
            elif 10 < position_posConfidence_pos <= 20:
                rsa['position']['posConfidence']['pos'] = 'a20m'
            elif 20 < position_posConfidence_pos <= 50:
                rsa['position']['posConfidence']['pos'] = 'a50m'
            elif 50 < position_posConfidence_pos <= 100:
                rsa['position']['posConfidence']['pos'] = 'a100m'
            elif 100 < position_posConfidence_pos <= 200:
                rsa['position']['posConfidence']['pos'] = 'a200m'
            elif 200 < position_posConfidence_pos <= 500:
                rsa['position']['posConfidence']['pos'] = 'a500m'
            else:
                rsa['position']['posConfidence']['pos'] = 'unavailable'
 
            if position_posConfidence_elevation is None:
                print('position_posConfidence_elevation is mandatory! Please provide. Set to unavailable.')
                rsa['position']['posConfidence']['elevation'] = 'unavailable'
            elif position_posConfidence_elevation <= 0:
                print('position_posConfidence_elevation should be greater than 0 m! But', position_posConfidence_elevation, 'is provided. Set to unavailable.')
                rsa['position']['posConfidence']['elevation'] = 'unavailable'
            elif position_posConfidence_elevation <= 0.01:
                rsa['position']['posConfidence']['elevation'] = 'elev-000-01'
            elif position_posConfidence_elevation <= 0.02:
                rsa['position']['posConfidence']['elevation'] = 'elev-000-02'
            elif position_posConfidence_elevation <= 0.05:
                rsa['position']['posConfidence']['elevation'] = 'elev-000-05'
            elif position_posConfidence_elevation <= 0.10:
                rsa['position']['posConfidence']['elevation'] = 'elev-000-10'
            elif position_posConfidence_elevation <= 0.20:
                rsa['position']['posConfidence']['elevation'] = 'elev-000-20'
            elif position_posConfidence_elevation <= 0.50:
                rsa['position']['posConfidence']['elevation'] = 'elev-000-50'
            elif position_posConfidence_elevation <= 1.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-001-00'
            elif position_posConfidence_elevation <= 2.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-002-00'
            elif position_posConfidence_elevation <= 5.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-005-00'
            elif position_posConfidence_elevation <= 10.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-010-00'
            elif position_posConfidence_elevation <= 20.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-020-00'
            elif position_posConfidence_elevation <= 50.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-050-00'
            elif position_posConfidence_elevation <= 100.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-100-00'
            elif position_posConfidence_elevation <= 200.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-200-00'
            elif position_posConfidence_elevation <= 500.00:
                rsa['position']['posConfidence']['elevation'] = 'elev-500-00'
            else:
                rsa['position']['posConfidence']['elevation'] = 'unavailable'
 
        if position_speedConfidence_heading is not None or position_speedConfidence_speed is not None or position_speedConfidence_throttle is not None:
            rsa['position']['speedConfidence'] = {}
            if position_speedConfidence_heading is None:
                print('position_speedConfidence_heading is mandatory! Please provide. Set to unavailable')
                rsa['position']['speedConfidence']['heading'] = 'unavailable'
            elif position_speedConfidence_heading <= 0:
                print('position_speedConfidence_heading should be greater than 0 deg! But', position_speedConfidence_heading, 'is provided. Set to unavailable.')
                rsa['position']['speedConfidence']['heading'] = 'unavailable'
            elif 0 < position_speedConfidence_heading <= 0.01:
                rsa['position']['speedConfidence']['heading'] = 'prec0-01deg'
            elif 0.01 < position_speedConfidence_heading <= 0.0125:
                rsa['position']['speedConfidence']['heading'] = 'prec0-0125deg'
            elif 0.0125 < position_speedConfidence_heading <= 0.05:
                rsa['position']['speedConfidence']['heading'] = 'prec0-05deg'
            elif 0.05 < position_speedConfidence_heading <= 0.1:
                rsa['position']['speedConfidence']['heading'] = 'prec0-1deg'
            elif 0.1 < position_speedConfidence_heading <= 1:
                rsa['position']['speedConfidence']['heading'] = 'prec01deg'
            elif 1 < position_speedConfidence_heading <= 5:
                rsa['position']['speedConfidence']['heading'] = 'prec05deg'
            elif 5 < position_speedConfidence_heading <= 10:
                rsa['position']['speedConfidence']['heading'] = 'prec10deg'
            else:
                rsa['position']['speedConfidence']['heading'] = 'unavailable'
 
            if position_speedConfidence_speed is None:
                print('position_speedConfidence_speed is mandatory! Please provide. Set to unavailable')
                rsa['position']['speedConfidence']['speed'] = 'unavailable'
            elif position_speedConfidence_speed <= 0:
                print('position_speedConfidence_speed should be greater than 0 m/s! But', position_speedConfidence_speed, 'is provided. Set to unavailable.')
                rsa['position']['speedConfidence']['speed'] = 'unavailable'
            elif 0 < position_speedConfidence_speed <= 0.01:
                rsa['position']['speedConfidence']['speed'] = 'prec0-01ms'
            elif 0.01 < position_speedConfidence_speed <= 0.05:
                rsa['position']['speedConfidence']['speed'] = 'prec0-05ms'
            elif 0.05 < position_speedConfidence_speed <= 0.1:
                rsa['position']['speedConfidence']['speed'] = 'prec0-1ms'
            elif 0.1 < position_speedConfidence_speed <= 1:
                rsa['position']['speedConfidence']['speed'] = 'prec1ms'
            elif 1 < position_speedConfidence_speed <= 5:
                rsa['position']['speedConfidence']['speed'] = 'prec5ms'
            elif 5 < position_speedConfidence_speed <= 10:
                rsa['position']['speedConfidence']['speed'] = 'prec10ms'
            elif 10 < position_speedConfidence_speed <= 100:
                rsa['position']['speedConfidence']['speed'] = 'prec100ms'
            else:
                rsa['position']['speedConfidence']['speed'] = 'unavailable'
 
            if position_speedConfidence_throttle is None:
                print('position_speedConfidence_throttle is mandatory! Please provide. Set to unavailable')
                rsa['position']['speedConfidence']['throttle'] = 'unavailable'
            elif position_speedConfidence_throttle <= 0:
                print('position_speedConfidence_throttle should be greater than 0! But', position_speedConfidence_throttle, 'is provided. Set to unavailable.')
                rsa['position']['speedConfidence']['throttle'] = 'unavailable'
            elif 0 < position_speedConfidence_throttle <= 0.005:
                rsa['position']['speedConfidence']['throttle'] = 'prec0-5percent'
            elif 0.005 < position_speedConfidence_throttle <= 0.01:
                rsa['position']['speedConfidence']['throttle'] = 'prec1percent'
            elif 0.01 < position_speedConfidence_throttle <= 0.1:
                rsa['position']['speedConfidence']['throttle'] = 'prec10percent'
            else:
                rsa['position']['speedConfidence']['throttle'] = 'unavailable'

    if furtherInfoID is not None:
        if not isinstance(furtherInfoID, int):
            print('furtherInfoID should be an integer! But', furtherInfoID, 'is provided. Set to 0.')
            rsa['furtherInfoID'] = bytes([0, 0])
        elif furtherInfoID < 0 or furtherInfoID > 65535:
            print('furtherInfoID should be in range [0, 65535]! But', furtherInfoID, 'is provided. Set to 0.')
            rsa['furtherInfoID'] = bytes([0, 0])
        else:
            rsa['furtherInfoID'] = furtherInfoID.to_bytes(2, byteorder='big')

    header_rsa = {
        'messageId': 27,
        'value': ('RoadSideAlert', rsa)
    }

    header_rsa_msg = v2xlib.MessageFrame.MessageFrame
    header_rsa_msg.set_val(header_rsa)
    hex_rsa = hexlify(header_rsa_msg.to_uper())
    return hex_rsa.decode('utf-8')