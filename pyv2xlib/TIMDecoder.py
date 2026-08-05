from .utils import load_v2xlib
from binascii import hexlify, unhexlify
v2xlib = load_v2xlib()


def tim_decoder(hex_tim, verbose = False):
    '''
    Decode TIM message from hex string to dictionary

    Args:
        hex_tim (str): hex string of TIM message

    Returns:
        dict: TIM message in dictionary format
    '''
    # decode TIM message
    header_tim_msg = v2xlib.MessageFrame.MessageFrame
    header_tim_msg.from_uper_ws(unhexlify(hex_tim))
    header_tim = header_tim_msg()

    tim = header_tim['value'][1]

    # convert values in the dictionary into correct range
    if 'packetID' in tim:
        tim['packetID'] = int.from_bytes(tim['packetID'], byteorder='big')
    for df in tim.get('dataFrames', []):

        if 'msgId' in df:
            choice, value = df['msgId']
            if choice == 'furtherInfoID':
                df['msgId'] = ('furtherInfoID', int.from_bytes(value, byteorder='big'))
            elif choice == 'roadSignID':
                roadSign = value
                if 'position' in roadSign:
                    pos = roadSign['position']
                    if pos.get('lat') == 900000001:
                        pos['lat'] = 'unavailable'
                    else:
                        pos['lat'] /= 10 ** 7
                    if pos.get('long') == 1800000001:
                        pos['long'] = 'unavailable'
                    else:
                        pos['long'] /= 10 ** 7
                    if 'elevation' in pos:
                        pos['elevation'] /= 10
                if 'viewAngle' in roadSign:
                    if isinstance(roadSign['viewAngle'], tuple):
                        roadSign['viewAngle'] = roadSign['viewAngle'][0]
                if 'crc' in roadSign:
                    roadSign['crc'] = int.from_bytes(roadSign['crc'], byteorder='big')
                df['msgId'] = ('roadSignID', roadSign)

        for region in df.get('regions', []):

            if 'anchor' in region:
                anchor = region['anchor']
                if anchor.get('lat') == 900000001:
                    anchor['lat'] = 'unavailable'
                else:
                    anchor['lat'] /= 10 ** 7
                if anchor.get('long') == 1800000001:
                    anchor['long'] = 'unavailable'
                else:
                    anchor['long'] /= 10 ** 7
                if 'elevation' in anchor:
                    anchor['elevation'] /= 10

            if 'laneWidth' in region:
                region['laneWidth'] /= 100

            if 'direction' in region:
                if isinstance(region['direction'], tuple):
                    region['direction'] = region['direction'][0]

            if 'description' in region:
                desc_choice, desc_value = region['description']

                if desc_choice == 'geometry':
                    geometry = desc_value
                    if 'direction' in geometry and isinstance(geometry['direction'], tuple):
                        geometry['direction'] = geometry['direction'][0]
                    if 'laneWidth' in geometry:
                        geometry['laneWidth'] /= 100
                    if 'circle' in geometry:
                        circle = geometry['circle']
                        center = circle['center']
                        if center.get('lat') == 900000001:
                            center['lat'] = 'unavailable'
                        else:
                            center['lat'] /= 10 ** 7
                        if center.get('long') == 1800000001:
                            center['long'] = 'unavailable'
                        else:
                            center['long'] /= 10 ** 7
                        if 'elevation' in center:
                            center['elevation'] /= 10
                    region['description'] = ('geometry', geometry)

                elif desc_choice == 'path':
                    path = desc_value

                    if 'offset' in path:
                        offset_choice, offset_value = path['offset']
                        inner_choice, inner_value = offset_value

                        if inner_choice == 'nodes':
                            for node in inner_value:
                                tier, delta = node['delta']

                                if tier == 'node-LatLon':
                                    delta['lon'] /= 10 ** 7
                                    delta['lat'] /= 10 ** 7

                                elif tier in ('node-XY1', 'node-XY2', 'node-XY3', 'node-XY4', 'node-XY5', 'node-XY6'):
                                    pass

                                elif tier == 'node-LL4':
                                    if delta['lon'] == -131072:
                                        delta['lon'] = 'unavailable'
                                    elif delta['lon'] == 131071:
                                        delta['lon'] = 'clamped-high'
                                    elif delta['lon'] == -131071:
                                        delta['lon'] = 'clamped-low'
                                    else:
                                        delta['lon'] /= 10 ** 7
                                    if delta['lat'] == -131072:
                                        delta['lat'] = 'unavailable'
                                    elif delta['lat'] == 131071:
                                        delta['lat'] = 'clamped-high'
                                    elif delta['lat'] == -131071:
                                        delta['lat'] = 'clamped-low'
                                    else:
                                        delta['lat'] /= 10 ** 7

                                elif tier in ('node-LL1', 'node-LL2', 'node-LL3', 'node-LL5', 'node-LL6'):
                                    delta['lon'] /= 10 ** 7
                                    delta['lat'] /= 10 ** 7

                                node['delta'] = (tier, delta)

                                if 'attributes' in node:
                                    attrs = node['attributes']
                                    if 'data' in attrs:
                                        decoded_data = []
                                        for entry_type, entry_value in attrs['data']:
                                            if entry_type == 'speedLimits':
                                                for lim in entry_value:
                                                    lim['speed'] *= 0.02
                                                decoded_data.append((entry_type, entry_value))
                                            else:
                                                decoded_data.append((entry_type, entry_value))
                                        attrs['data'] = decoded_data

                            path['offset'] = (offset_choice, (inner_choice, inner_value))

                        elif inner_choice == 'computed':
                            computed_lane = inner_value
                            if 'rotateXY' in computed_lane:
                                computed_lane['rotateXY'] *= 0.0125
                            path['offset'] = (offset_choice, (inner_choice, computed_lane))

                    region['description'] = ('path', path)

                elif desc_choice == 'oldRegion':
                    oldRegion = desc_value
                    if 'direction' in oldRegion and isinstance(oldRegion['direction'], tuple):
                        oldRegion['direction'] = oldRegion['direction'][0]

                    if 'area' in oldRegion:
                        area_choice, area_value = oldRegion['area']

                        if area_choice == 'shapePointSet':
                            shapePointSet = area_value
                            if 'anchor' in shapePointSet:
                                anchor = shapePointSet['anchor']
                                if anchor.get('lat') == 900000001:
                                    anchor['lat'] = 'unavailable'
                                else:
                                    anchor['lat'] /= 10 ** 7
                                if anchor.get('long') == 1800000001:
                                    anchor['long'] = 'unavailable'
                                else:
                                    anchor['long'] /= 10 ** 7
                                if 'elevation' in anchor:
                                    anchor['elevation'] /= 10
                            if 'laneWidth' in shapePointSet:
                                shapePointSet['laneWidth'] /= 100

                            if 'nodeList' in shapePointSet:
                                nl_choice, nl_value = shapePointSet['nodeList']
                                if nl_choice == 'nodes':
                                    for node in nl_value:
                                        tier, delta = node['delta']
                                        if tier == 'node-LatLon':
                                            delta['lon'] /= 10 ** 7
                                            delta['lat'] /= 10 ** 7
                                        node['delta'] = (tier, delta)
                                        if 'attributes' in node:
                                            attrs = node['attributes']
                                            if 'data' in attrs:
                                                decoded_data = []
                                                for entry_type, entry_value in attrs['data']:
                                                    if entry_type == 'speedLimits':
                                                        for lim in entry_value:
                                                            lim['speed'] *= 0.02
                                                    decoded_data.append((entry_type, entry_value))
                                                attrs['data'] = decoded_data
                                    shapePointSet['nodeList'] = (nl_choice, nl_value)
                                elif nl_choice == 'computed':
                                    computed_lane = nl_value
                                    if 'rotateXY' in computed_lane:
                                        computed_lane['rotateXY'] *= 0.0125
                                    shapePointSet['nodeList'] = (nl_choice, computed_lane)

                            oldRegion['area'] = ('shapePointSet', shapePointSet)

                        elif area_choice == 'circle':
                            circle = area_value
                            center = circle['center']
                            if center.get('lat') == 900000001:
                                center['lat'] = 'unavailable'
                            else:
                                center['lat'] /= 10 ** 7
                            if center.get('long') == 1800000001:
                                center['long'] = 'unavailable'
                            else:
                                center['long'] /= 10 ** 7
                            if 'elevation' in center:
                                center['elevation'] /= 10
                            oldRegion['area'] = ('circle', circle)

                        elif area_choice == 'regionPointSet':
                            regionPointSet = area_value
                            if 'anchor' in regionPointSet:
                                anchor = regionPointSet['anchor']
                                if anchor.get('lat') == 900000001:
                                    anchor['lat'] = 'unavailable'
                                else:
                                    anchor['lat'] /= 10 ** 7
                                if anchor.get('long') == 1800000001:
                                    anchor['long'] = 'unavailable'
                                else:
                                    anchor['long'] /= 10 ** 7
                                if 'elevation' in anchor:
                                    anchor['elevation'] /= 10
                            oldRegion['area'] = ('regionPointSet', regionPointSet)

                    region['description'] = ('oldRegion', oldRegion)

        if 'content' in df:
            content_choice, content_items = df['content']
            decoded_items = []
            for entry in content_items:
                item_choice, item_value = entry['item']
                decoded_items.append((item_choice, item_value))
            df['content'] = (content_choice, decoded_items)

        if 'contentNew' in df:
            if verbose:
                print('contentNew present but not implemented in decoder (FrictionInformation structure unknown).')

    return tim