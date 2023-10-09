from pycrate_sdsm import SDSM
from binascii import hexlify, unhexlify


def sdsm_decoder(hex_sdsm):
    header_sdsm_msg = SDSM.MessageFrame.MessageFrame
    
    header_sdsm_msg.from_uper_ws(unhexlify(hex_sdsm))
    header_sdsm = header_sdsm_msg()

    sdsm = header_sdsm['value'][1]

    if 'second' in list(sdsm['sDSMTimeStamp'].keys()):
        sdsm['sDSMTimeStamp']['second'] /= 1000
    sdsm['refPos']['lat'] /= 10 ** 7
    sdsm['refPos']['long'] /= 10 ** 7
    if 'elevation' in list(sdsm['refPos'].keys()):
        sdsm['refPos']['elevation'] /= 10
    sdsm['refPosXYConf']['semiMajor'] /= 20
    sdsm['refPosXYConf']['semiMinor'] /= 20
    sdsm['refPosXYConf']['orientation'] /= 65535 / 360

    for i in range(len(sdsm['objects'])):
        sdsm['objects'][i]['detObjCommon']['measurementTime'] /= 1000
        sdsm['objects'][i]['detObjCommon']['pos']['offsetX'] /= 10
        sdsm['objects'][i]['detObjCommon']['pos']['offsetY'] /= 10
        if 'offsetZ' in list(sdsm['objects'][i]['detObjCommon']['pos'].keys()):
            sdsm['objects'][i]['detObjCommon']['pos']['offsetZ'] /= 10
        sdsm['objects'][i]['detObjCommon']['speed'] /= 50
        if 'speedZ' in list(sdsm['objects'][i]['detObjCommon'].keys()):
            sdsm['objects'][i]['detObjCommon']['speedZ'] /= 50
        sdsm['objects'][i]['detObjCommon']['heading'] *= 0.0125
        if 'accel4way' in list(sdsm['objects'][i]['detObjCommon'].keys()):
            if 'lat' in list(sdsm['objects'][i]['detObjCommon']['accel4way'].keys()):
                sdsm['objects'][i]['detObjCommon']['accel4way']['lat'] /= 100
            if 'long' in list(sdsm['objects'][i]['detObjCommon']['accel4way'].keys()):
                sdsm['objects'][i]['detObjCommon']['accel4way']['long'] /= 100
            if 'vert' in list(sdsm['objects'][i]['detObjCommon']['accel4way'].keys()):
                sdsm['objects'][i]['detObjCommon']['accel4way']['vert'] /= 50 / 9.80665
            if 'yaw' in list(sdsm['objects'][i]['detObjCommon']['accel4way'].keys()):
                sdsm['objects'][i]['detObjCommon']['accel4way']['yaw'] /= 100
        
        if 'detObjOptData' in list(sdsm['objects'][i].keys()):
            if sdsm['objects'][i]['detObjOptData'][0] == 'detVeh':
                if 'lights' in list(sdsm['objects'][i]['detObjOptData'][1].keys()):
                    if sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 48:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'lowBeamHeadlightsOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 49:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'highBeamHeadlightsOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 50:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'leftTurnSignalOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 51:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'rightTurnSignalOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 52:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'hazardSignalOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 53:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'automaticLightControlOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 54:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'daytimeRunningLightsOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 55:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'fogLightOn'
                    elif sdsm['objects'][i]['detObjOptData'][1]['lights'][0] == 56:
                        sdsm['objects'][i]['detObjOptData'][1]['lights'] = 'parkingLightsOn'
                if 'vehAttitude' in list(sdsm['objects'][i]['detObjOptData'][1].keys()):
                    sdsm['objects'][i]['detObjOptData'][1]['vehAttitude']['pitch'] *= 0.0125
                    sdsm['objects'][i]['detObjOptData'][1]['vehAttitude']['roll'] *= 0.0125
                    sdsm['objects'][i]['detObjOptData'][1]['vehAttitude']['yaw'] *= 0.0125
                if 'vehAngleVel' in list(sdsm['objects'][i]['detObjOptData'][1].keys()):
                    sdsm['objects'][i]['detObjOptData'][1]['vehAngleVel']['pitchRate'] /= 100
                    sdsm['objects'][i]['detObjOptData'][1]['vehAngleVel']['rollRate'] /= 100
                if 'size' in list(sdsm['objects'][i]['detObjOptData'][1].keys()):
                    sdsm['objects'][i]['detObjOptData'][1]['size']['width'] /= 100
                    sdsm['objects'][i]['detObjOptData'][1]['size']['length'] /= 100
                if 'height' in list(sdsm['objects'][i]['detObjOptData'][1].keys()):
                    sdsm['objects'][i]['detObjOptData'][1]['height'] /= 20
            elif sdsm['objects'][i]['detObjOptData'][0] == 'detVRU':
                pass
            elif sdsm['objects'][i]['detObjOptData'][0] == 'detObst':
                if 'obstSize' in list(sdsm['objects'][i]['detObjOptData'][1].keys()):
                    sdsm['objects'][i]['detObjOptData'][1]['obstSize']['length'] /= 100
                    sdsm['objects'][i]['detObjOptData'][1]['obstSize']['width'] /= 100
                    if 'height' in list(sdsm['objects'][i]['detObjOptData'][1]['obstSize'].keys()):
                        sdsm['objects'][i]['detObjOptData'][1]['obstSize']['height'] /= 100

    return sdsm
