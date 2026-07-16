from .utils import load_v2xlib
from binascii import hexlify, unhexlify
v2xlib = load_v2xlib()

def psm_decoder(hex_psm):
    '''
    Decode PSM message from hex string to dictionary

    Args:
        hex_psm (str): hex string of PSM message

    Returns:
        dict: PSM message in dictionary format
    '''
    # decode PSM message
    header_psm_msg = v2xlib.MessageFrame.MessageFrame
    header_psm_msg.from_uper_ws(unhexlify(hex_psm))
    header_psm = header_psm_msg()

    psm = header_psm['value'][1]

    # id
    psm['id'] = psm['id'].decode('utf-8')

    # position
    psm['position']['lat'] /= 10 ** 7
    psm['position']['long'] /= 10 ** 7
    if 'elevation' in psm['position']:
        psm['position']['elevation'] /= 10

    # accuracy
    psm['accuracy']['semiMajor'] /= 20
    psm['accuracy']['semiMinor'] /= 20
    psm['accuracy']['orientation'] *= 360 / 65535

    # speed
    if psm['speed'] == 8191:
        psm['speed'] = 'unavailable'
    else:
        psm['speed'] /= 50

    # heading
    if psm['heading'] == 28800:
        psm['heading'] = 'unavailable'
    else:
        psm['heading'] *= 0.0125

    # accelSet (optional)
    if 'accelSet' in psm:
        if psm['accelSet']['long'] == 2001:
            psm['accelSet']['long'] = 'unavailable'
        else:
            psm['accelSet']['long'] /= 100

        if psm['accelSet']['lat'] == 2001:
            psm['accelSet']['lat'] = 'unavailable'
        else:
            psm['accelSet']['lat'] /= 100

        if psm['accelSet']['vert'] == -127:
            psm['accelSet']['vert'] = 'unavailable'
        else:
            psm['accelSet']['vert'] = psm['accelSet']['vert'] / 50 * 9.80665

        psm['accelSet']['yaw'] /= 100

    # pathHistory (optional)
    if 'pathHistory' in psm:
        if 'initialPosition' in psm['pathHistory']:
            ip = psm['pathHistory']['initialPosition']
            ip['lat'] /= 10 ** 7
            ip['long'] /= 10 ** 7
            if 'elevation' in ip:
                ip['elevation'] /= 10
            if 'heading' in ip:
                ip['heading'] *= 0.0125
            if 'speed' in ip:
                if ip['speed']['speed'] == 8191:
                    ip['speed']['speed'] = 'unavailable'
                else:
                    ip['speed']['speed'] /= 50
            if 'posAccuracy' in ip:
                ip['posAccuracy']['semiMajor'] /= 20
                ip['posAccuracy']['semiMinor'] /= 20
                ip['posAccuracy']['orientation'] *= 360 / 65535
            if 'utcTime' in ip and 'second' in ip['utcTime']:
                ip['utcTime']['second'] /= 1000

        for crumb in psm['pathHistory'].get('crumbData', []):
            crumb['latOffset'] /= 10 ** 7
            crumb['lonOffset'] /= 10 ** 7
            if crumb['elevationOffset'] == -2048:
                crumb['elevationOffset'] = 'unavailable'
            else:
                crumb['elevationOffset'] /= 10
            if crumb['timeOffset'] == 65535:
                crumb['timeOffset'] = 'unavailable'
            else:
                crumb['timeOffset'] /= 100
            if 'speed' in crumb:
                if crumb['speed'] == 8191:
                    crumb['speed'] = 'unavailable'
                else:
                    crumb['speed'] /= 50
            if 'posAccuracy' in crumb:
                crumb['posAccuracy']['semiMajor'] /= 20
                crumb['posAccuracy']['semiMinor'] /= 20
                crumb['posAccuracy']['orientation'] *= 360 / 65535
            if 'heading' in crumb:
                if crumb['heading'] == 240:
                    crumb['heading'] = 'unavailable'
                else:
                    crumb['heading'] *= 1.5

    # pathPrediction (optional)
    if 'pathPrediction' in psm:
        psm['pathPrediction']['radiusOfCurve'] /= 10
        psm['pathPrediction']['confidence'] /= 2

    if 'useState' in psm:
        psm['useState'] = psm['useState'][0]
    
    for bitmask_field in ['activityType', 'activitySubType', 'assistType', 'sizing']:
        if bitmask_field in psm:
            psm[bitmask_field] = psm[bitmask_field][0]  # extract integer value

    return psm