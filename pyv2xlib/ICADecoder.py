from .utils import load_v2xlib
from binascii import hexlify, unhexlify
v2xlib = load_v2xlib()

def ica_decoder(hex_ica):
    '''
    Decode ICA message from hex string to dictionary

    Args:
        hex_ica (str): hex string of ICA message

    Returns:
        dict: ICA message in dictionary format
    '''
    # decode ICA message
    header_ica_msg = v2xlib.MessageFrame.MessageFrame
    header_ica_msg.from_uper_ws(unhexlify(hex_ica))
    header_ica = header_ica_msg()

    ica = header_ica['value'][1]
    ica['id'] = ica['id'].decode('utf-8')

    # partOne (BSMcoreData)
    if 'partOne' in ica:
        ica['partOne']['id'] = ica['partOne']['id'].decode('utf-8')
        if ica['partOne']['lat'] == 900000001:
            ica['partOne']['lat'] = 'unavailable'
        else:
            ica['partOne']['lat'] /= 10 ** 7
        if ica['partOne']['long'] == 1800000001:
            ica['partOne']['long'] = 'unavailable'
        else:
            ica['partOne']['long'] /= 10 ** 7
        if ica['partOne']['elev'] == -4096:
            ica['partOne']['elev'] = 'unavailable'
        else:
            ica['partOne']['elev'] /= 10
        if ica['partOne']['accuracy']['semiMajor'] == 255:
            ica['partOne']['accuracy']['semiMajor'] = 'unavailable'
        else:
            ica['partOne']['accuracy']['semiMajor'] /= 20
        if ica['partOne']['accuracy']['semiMinor'] == 255:
            ica['partOne']['accuracy']['semiMinor'] = 'unavailable'
        else:
            ica['partOne']['accuracy']['semiMinor'] /= 20
        if ica['partOne']['accuracy']['orientation'] == 65535:
            ica['partOne']['accuracy']['orientation'] = 'unavailable'
        else:
            ica['partOne']['accuracy']['orientation'] *= 360 / 65535
        if ica['partOne']['speed'] == 8191:
            ica['partOne']['speed'] = 'unavailable'
        else:
            ica['partOne']['speed'] /= 50
        if ica['partOne']['heading'] == 28800:
            ica['partOne']['heading'] = 'unavailable'
        else:
            ica['partOne']['heading'] *= 0.0125
        if ica['partOne']['angle'] == 127:
            ica['partOne']['angle'] = 'unavailable'
        else:
            ica['partOne']['angle'] *= 1.5
        if ica['partOne']['accelSet']['long'] == 2001:
            ica['partOne']['accelSet']['long'] = 'unavailable'
        else:
            ica['partOne']['accelSet']['long'] /= 100
        if ica['partOne']['accelSet']['lat'] == 2001:
            ica['partOne']['accelSet']['lat'] = 'unavailable'
        else:
            ica['partOne']['accelSet']['lat'] /= 100
        if ica['partOne']['accelSet']['vert'] == -127:
            ica['partOne']['accelSet']['vert'] = 'unavailable'
        else:
            ica['partOne']['accelSet']['vert'] = ica['partOne']['accelSet']['vert'] / 50 * 9.80665
        ica['partOne']['accelSet']['yaw'] /= 100

    # path
    if 'path' in ica:
        if 'initialPosition' in ica['path']:
            ip = ica['path']['initialPosition']
            if ip['lat'] == 900000001:
                ip['lat'] = 'unavailable'
            else:
                ip['lat'] /= 10 ** 7
            if ip['long'] == 1800000001:
                ip['long'] = 'unavailable'
            else:
                ip['long'] /= 10 ** 7
            if 'elevation' in ip:
                if ip['elevation'] == -4096:
                    ip['elevation'] = 'unavailable'
                else:
                    ip['elevation'] /= 10
            if 'heading' in ip:
                if ip['heading'] == 28800:
                    ip['heading'] = 'unavailable'
                else:
                    ip['heading'] *= 0.0125
            if 'speed' in ip:
                if ip['speed']['speed'] == 8191:
                    ip['speed']['speed'] = 'unavailable'
                else:
                    ip['speed']['speed'] /= 50
            if 'posAccuracy' in ip:
                if ip['posAccuracy']['semiMajor'] == 255:
                    ip['posAccuracy']['semiMajor'] = 'unavailable'
                else:
                    ip['posAccuracy']['semiMajor'] /= 20
                if ip['posAccuracy']['semiMinor'] == 255:
                    ip['posAccuracy']['semiMinor'] = 'unavailable'
                else:
                    ip['posAccuracy']['semiMinor'] /= 20
                if ip['posAccuracy']['orientation'] == 65535:
                    ip['posAccuracy']['orientation'] = 'unavailable'
                else:
                    ip['posAccuracy']['orientation'] *= 360 / 65535
            if 'utcTime' in ip and 'second' in ip['utcTime']:
                ip['utcTime']['second'] /= 1000

        for crumb in ica['path'].get('crumbData', []):
            if crumb['latOffset'] == -131072:
                crumb['latOffset'] = 'unavailable'
            else:
                crumb['latOffset'] /= 10 ** 7
            if crumb['lonOffset'] == -131072:
                crumb['lonOffset'] = 'unavailable'
            else:
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
                if crumb['posAccuracy']['semiMajor'] == 255:
                    crumb['posAccuracy']['semiMajor'] = 'unavailable'
                else:
                    crumb['posAccuracy']['semiMajor'] /= 20
                if crumb['posAccuracy']['semiMinor'] == 255:
                    crumb['posAccuracy']['semiMinor'] = 'unavailable'
                else:
                    crumb['posAccuracy']['semiMinor'] /= 20
                if crumb['posAccuracy']['orientation'] == 65535:
                    crumb['posAccuracy']['orientation'] = 'unavailable'
                else:
                    crumb['posAccuracy']['orientation'] *= 360 / 65535
            if 'heading' in crumb:
                if crumb['heading'] == 240:
                    crumb['heading'] = 'unavailable'
                else:
                    crumb['heading'] *= 1.5

    # pathPrediction
    if 'pathPrediction' in ica:
        if ica['pathPrediction']['radiusOfCurve'] == 32767:
            ica['pathPrediction']['radiusOfCurve'] = 'unavailable'
        else:
            ica['pathPrediction']['radiusOfCurve'] /= 10
        ica['pathPrediction']['confidence'] /= 2

    return ica