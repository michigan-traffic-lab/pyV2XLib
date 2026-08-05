from .utils import load_v2xlib
from binascii import hexlify, unhexlify
v2xlib = load_v2xlib()


def rsa_decoder(hex_rsa):
    '''
    Decode RSA message from hex string to dictionary

    Args:
        hex_rsa (str): hex string of RSA message

    Returns:
        dict: RSA message in dictionary format
    '''
    # decode RSA message
    header_rsa_msg = v2xlib.MessageFrame.MessageFrame
    header_rsa_msg.from_uper_ws(unhexlify(hex_rsa))
    header_rsa = header_rsa_msg()

    rsa = header_rsa['value'][1]

    if 'priority' in rsa:
        raw_byte = rsa['priority'][0]
        rsa['priority'] = raw_byte >> 5

    if 'heading' in rsa:
        if isinstance(rsa['heading'], tuple):
            rsa['heading'] = rsa['heading'][0]

    if 'position' in rsa:
        pos = rsa['position']

        if pos.get('long') == 1800000001:
            pos['long'] = 'unavailable'
        else:
            pos['long'] /= 10 ** 7

        if pos.get('lat') == 900000001:
            pos['lat'] = 'unavailable'
        else:
            pos['lat'] /= 10 ** 7

        if 'elevation' in pos:
            if pos['elevation'] == -4096:
                pos['elevation'] = 'unavailable'
            else:
                pos['elevation'] /= 10

        if 'heading' in pos:
            if pos['heading'] == 28800:
                pos['heading'] = 'unavailable'
            else:
                pos['heading'] *= 0.0125

        if 'speed' in pos:
            if pos['speed'].get('speed') == 8191:
                pos['speed']['speed'] = 'unavailable'
            else:
                pos['speed']['speed'] /= 50

        if 'posAccuracy' in pos:
            if pos['posAccuracy']['semiMajor'] == 255:
                pos['posAccuracy']['semiMajor'] = 'unavailable'
            else:
                pos['posAccuracy']['semiMajor'] /= 20
            if pos['posAccuracy']['semiMinor'] == 255:
                pos['posAccuracy']['semiMinor'] = 'unavailable'
            else:
                pos['posAccuracy']['semiMinor'] /= 20
            if pos['posAccuracy']['orientation'] == 65535:
                pos['posAccuracy']['orientation'] = 'unavailable'
            else:
                pos['posAccuracy']['orientation'] *= 360 / 65535

        if 'utcTime' in pos and 'second' in pos['utcTime']:
            pos['utcTime']['second'] /= 1000

    if 'furtherInfoID' in rsa:
        raw = rsa['furtherInfoID']
        value = int.from_bytes(raw, byteorder='big')
        rsa['furtherInfoID'] = value

    return rsa