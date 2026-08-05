from binascii import hexlify, unhexlify
from .utils import load_v2xlib
v2xlib = load_v2xlib()

def tim_encoder(msgCnt=None,
                timeStamp=None,  # optional
                packetID=None,  # optional
                urlB=None,  # optional

                dataFrames_N=0,
                dataFrames_frameType=[],
                dataFrames_msgId=[],
                dataFrames_furtherInfoID=[],  # optional
                dataFrames_roadSignID_position_lat=[],
                dataFrames_roadSignID_position_long=[],
                dataFrames_roadSignID_position_elevation=[],  # optional
                dataFrames_roadSignID_viewAngle=[],
                dataFrames_roadSignID_mutcdCode=[],  # optional
                dataFrames_roadSignID_crc=[],  # optional
                dataFrames_startYear=[],  # optional
                dataFrames_startTime=[],
                dataFrames_durationTime=[],
                dataFrames_priority=[],

                dataFrames_regions_N=[],
                dataFrames_region_name=[],  # optional
                dataFrames_region_id_region=[],  # optional
                dataFrames_region_id_segment=[],  # optional
                dataFrames_region_lat=[],  # optional
                dataFrames_region_long=[],  # optional
                dataFrames_region_elevation=[],  # optional
                dataFrames_region_laneWidth=[],  # optional
                dataFrames_region_directionality=[],  # optional
                dataFrames_region_closedPath=[],  # optional
                dataFrames_region_direction=[],  # optional
                dataFrames_region_description=None,  # optional

                dataFrames_region_geometry_direction=[],
                dataFrames_region_geometry_extent=[],  # optional
                dataFrames_region_geometry_laneWidth=[],  # optional
                dataFrames_region_geometry_circle_lat=[],
                dataFrames_region_geometry_circle_long=[],
                dataFrames_region_geometry_circle_elevation=[],  # optional
                dataFrames_region_geometry_circle_radius=[],
                dataFrames_region_geometry_circle_units=[],

                dataFrames_region_path_scale=[],  # optional
                dataFrames_region_path_offset_type=[],
                dataFrames_region_path_nodelistxy_type=[],
                dataFrames_region_path_nodes=[],
                dataFrames_region_path_computed=[],

                dataFrames_region_oldRegion_direction=[],
                dataFrames_region_oldRegion_extent=[],  # optional
                dataFrames_region_oldRegion_area_type=[],
                dataFrames_region_oldRegion_shapePointSet_anchor_lat=[],  # optional
                dataFrames_region_oldRegion_shapePointSet_anchor_long=[],  # optional
                dataFrames_region_oldRegion_shapePointSet_anchor_elevation=[],  # optional
                dataFrames_region_oldRegion_shapePointSet_laneWidth=[],  # optional
                dataFrames_region_oldRegion_shapePointSet_directionality=[],  # optional
                dataFrames_region_oldRegion_shapePointSet_nodelistxy_type=[],
                dataFrames_region_oldRegion_shapePointSet_nodes=[],
                dataFrames_region_oldRegion_shapePointSet_computed=[],
                dataFrames_region_oldRegion_circle_lat=[],
                dataFrames_region_oldRegion_circle_long=[],
                dataFrames_region_oldRegion_circle_elevation=[],  # optional
                dataFrames_region_oldRegion_circle_radius=[],
                dataFrames_region_oldRegion_circle_units=[],
                dataFrames_region_oldRegion_regionPointSet_anchor_lat=[],  # optional
                dataFrames_region_oldRegion_regionPointSet_anchor_long=[],  # optional
                dataFrames_region_oldRegion_regionPointSet_anchor_elevation=[],  # optional
                dataFrames_region_oldRegion_regionPointSet_scale=[],  # optional
                dataFrames_region_oldRegion_regionPointSet_nodeList=[],

                dataFrames_content_type=[],
                dataFrames_content_items=[],
                dataFrames_url=[],  # optional
                dataFrames_contentNew_type=[],  # optional, not implemented
                dataFrames_contentNew_frictionInfo=[],  # optional, not implemented
                ):
    '''
    This function encodes TIM message.

    Args:
        msgCnt (int): Message counter. Range: [0, 127]. Mandatory.
        timeStamp (int): Minute of the year this message was generated. Range: [0, 527040]. Optional.
        packetID (int): A relatively unique 9-byte linking value connecting this message to other supporting messages in other formats. Range: [0, 2**72 - 1]. Optional.
        urlB (str): Base URL for supplementary information about this message. The last character of the string is used as a matching tag with a corresponding URL-Short elsewhere. Length: [1, 45] characters. Optional.
        dataFrames_N (int): Number of data frames (TravelerDataFrame entries) in this message. Range: [1, 8]. Mandatory.

        -- Part I: Frame header (per frame, index i) --
        dataFrames_frameType (list): Frame type. One of unknown, advisory, roadSignage, commercialSignage. Mandatory.
        dataFrames_msgId (list): Which msgId CHOICE branch this frame uses. One of furtherInfoID, roadSignID. Mandatory.
        dataFrames_furtherInfoID (list): Used if dataFrames_msgId is furtherInfoID. A 2-byte link number to other messages related to the same event. Range: [0, 65535].
        dataFrames_roadSignID_position_lat (list): Used if dataFrames_msgId is roadSignID. Latitude of the sign's location. Range: [-90, 90]. Unit: deg. Mandatory in that case.
        dataFrames_roadSignID_position_long (list): Longitude of the sign's location. Range: [-179.9999999, 180]. Unit: deg. Mandatory in that case.
        dataFrames_roadSignID_position_elevation (list): Elevation of the sign's location. Range: [-409.5, 6143.9]. Unit: meter. Optional.
        dataFrames_roadSignID_viewAngle (list): 16-bit HeadingSlice bitmask - vehicle direction of travel while facing the active side of the sign. NOT a single angle in degrees. Range: [0, 65535]. Mandatory in that case.
        dataFrames_roadSignID_mutcdCode (list): Tag for the sign's MUTCD code, or generic. One of none, regulatory, warning, maintenance, motoristService, guide, rec. Optional.
        dataFrames_roadSignID_crc (list): 2-byte checksum value for the sign data (MsgCRC). Not actually computed as a real CRC-CCITT checksum here - accepted as a placeholder integer only. Range: [0, 65535]. Optional.
        dataFrames_startYear (list): Year the frame becomes active. Range: [0, 4095]. Optional.
        dataFrames_startTime (list): Minute of the year the frame becomes active. Range: [0, 527040]. Mandatory.
        dataFrames_durationTime (list): How many whole minutes the frame remains active. Range: [0, 32000]. 32000 (per spec) means "persists forever." Mandatory.
        dataFrames_priority (list): Relative display priority of this frame vs other signs. Range: [0, 7]. Mandatory.

        -- Part II: Applicable Regions of Use (per frame, per region) --
        dataFrames_regions_N (list): Number of regions (GeographicalPath entries) for this frame. Range: [1, 16]. Mandatory.
        dataFrames_region_name (list of lists): Descriptive name of the region. Length [1, 63] characters. Optional.
        dataFrames_region_id_region (list of lists): Regional authority ID for the region's road segment reference. Range: [0, 65535]. Optional.
        dataFrames_region_id_segment (list of lists): Road segment ID within the above region. Range: [0, 65535]. Mandatory if id is used at all.
        dataFrames_region_lat (list of lists): Latitude of the region's anchor position (Position3D). Range: [-90, 90]. Unit: deg. Optional overall - anchor only added if lat or long is given.
        dataFrames_region_long (list of lists): Longitude of the region's anchor position. Range: [-179.9999999, 180]. Unit: deg. Optional overall - anchor only added if lat or long is given.
        dataFrames_region_elevation (list of lists): Elevation of the region's anchor position. Range: [-409.5, 6143.9]. Unit: meter. Optional.
        dataFrames_region_laneWidth (list of lists): Lane width at this region. Range: [0, 327.67]. Unit: meter. Optional.
        dataFrames_region_directionality (list of lists): Direction of use. One of unavailable, forward, reverse, both. Optional.
        dataFrames_region_closedPath (list of lists): Whether the last point closes back to the first (True/False). Optional.
        dataFrames_region_direction (list of lists): 16-bit HeadingSlice bitmask - field of view over which this region applies. NOT a single angle. Range: [0, 65535]. Optional.
        dataFrames_region_description (str): Which description CHOICE branch this region's shape uses. One of path, geometry, oldRegion. Optional. 

        -- description: 'geometry' branch (GeometricProjection / a circle) --
        dataFrames_region_geometry_direction (list of lists): 16-bit HeadingSlice bitmask. Mandatory if geometry is used.
        dataFrames_region_geometry_extent (list of lists): How far this geometry projection stays relevant. Same enum as RSA's extent (useInstantlyOnly ... forever). Optional.
        dataFrames_region_geometry_laneWidth (list of lists): Lane width for the geometry projection. Range: [0, 327.67] m. Optional.
        dataFrames_region_geometry_circle_lat (list of lists): Latitude of the circle's center point. Mandatory if geometry used.
        dataFrames_region_geometry_circle_long (list of lists): Longitude of the circle's center point. Mandatory if geometry used.
        dataFrames_region_geometry_circle_elevation (list of lists): Elevation of the circle's center point. Optional.
        dataFrames_region_geometry_circle_radius (list of lists): Circle radius. Range: [0, 4095]. Mandatory if geometry used.
        dataFrames_region_geometry_circle_units (list of lists): Units for the radius. One of centimeter, cm2-5, decimeter, meter, kilometer, foot, yard, mile. Mandatory if geometry used.

        -- description: 'path' branch (OffsetSystem - node lists or a computed lane) --
        dataFrames_region_path_scale (list of lists): Zoom factor (2^N) applied to node offsets. Range: [0, 15]. Optional.
        dataFrames_region_path_offset_type (list of lists): Which offset CHOICE branch. One of xy, ll. Mandatory if path is used.
        dataFrames_region_path_nodelistxy_type (list of lists): Only used when offset_type is xy. Which NodeListXY CHOICE branch. One of nodes, computed.
        dataFrames_region_path_nodes (list of lists): List of node dicts (2-63 entries) used for both xy+'nodes' and ll (ll only has this branch). See node dict shape note below.
        dataFrames_region_path_computed (list of lists): Used when nodelistxy_type is computed. A single ComputedLane dict per region. See ComputedLane dict shape note below.

        -- description: 'oldRegion' branch (ValidRegion - legacy, per spec no longer recommended) --
        dataFrames_region_oldRegion_direction (list of lists): 16-bit HeadingSlice bitmask. Mandatory if oldRegion used.
        dataFrames_region_oldRegion_extent (list of lists): Same enum as RSA's extent. Optional.
        dataFrames_region_oldRegion_area_type (list of lists): Which area CHOICE branch. One of shapePointSet, circle, regionPointSet. Mandatory if oldRegion used.
        dataFrames_region_oldRegion_shapePointSet_anchor_lat (list of lists): Optional latitude of the anchor position for the shape.
        dataFrames_region_oldRegion_shapePointSet_anchor_long (list of lists): Optional longitude of the anchor position for the shape.
        dataFrames_region_oldRegion_shapePointSet_anchor_elevation (list of lists): Optional elevation of the anchor position for the shape.
        dataFrames_region_oldRegion_shapePointSet_laneWidth (list of lists): Optional lane width, in meters.
        dataFrames_region_oldRegion_shapePointSet_directionality (list of lists): Optional, same enum as dataFrames_region_directionality.
        dataFrames_region_oldRegion_shapePointSet_nodelistxy_type (list of lists): nodes or computed. Mandatory if shapePointSet used.
        dataFrames_region_oldRegion_shapePointSet_nodes (list of lists): Same shape as dataFrames_region_path_nodes above (ShapePointSet.nodeList is NodeListXY only - no ll variant here).
        dataFrames_region_oldRegion_shapePointSet_computed (list of lists): Same shape as dataFrames_region_path_computed above.
        dataFrames_region_oldRegion_circle_lat (list of lists): Latitude of the circle's center. Mandatory if oldRegion circle used.
        dataFrames_region_oldRegion_circle_long (list of lists): Longitude of the circle's center. Mandatory if oldRegion circle used.
        dataFrames_region_oldRegion_circle_elevation (list of lists): Elevation of the circle's center. Optional.
        dataFrames_region_oldRegion_circle_radius (list of lists): Circle radius. Mandatory if oldRegion circle used.
        dataFrames_region_oldRegion_circle_units (list of lists): Units for the radius. Mandatory if oldRegion circle used.
        dataFrames_region_oldRegion_regionPointSet_anchor_lat (list of lists): Optional latitude of the region point set's anchor.
        dataFrames_region_oldRegion_regionPointSet_anchor_long (list of lists): Optional longitude of the region point set's anchor.
        dataFrames_region_oldRegion_regionPointSet_anchor_elevation (list of lists): Optional elevation of the region point set's anchor.
        dataFrames_region_oldRegion_regionPointSet_scale (list of lists): Optional zoom factor. Range: [0, 15].
        dataFrames_region_oldRegion_regionPointSet_nodeList (list of lists): Mandatory if regionPointSet used. A list of 1-64 offset dicts in whole meters (NOT the 0.1-microdegree scaling used elsewhere for lat/long offsets, despite reusing the same underlying OffsetLL-B16 type). Range for each: [-32768, 32767]. See offset dict shape note below.

        -- Part III: Content --
        dataFrames_content_type (list): Which content CHOICE branch. One of advisory, workZone, genericSign, speedLimit, exitService. Mandatory.
        dataFrames_content_items (list of lists): List of content items for the above branch. advisory allows 1-100 entries with text up to 500 chars (ITIStext); workZone/genericSign/speedLimit/exitService allow 1-16 entries with text up to 16 chars (ITIStextPhrase). See content item dict shape note below.
        dataFrames_url (list): URL-Short - may link to an image or other content associated with this frame. Length [1, 15] characters. Optional.
        dataFrames_contentNew_type (list): Which contentNew CHOICE branch. Only frictionInfo is currently defined in the spec. NOT IMPLEMENTED - FrictionInformation's field structure has not been provided, so requesting this branch will be logged and omitted rather than encoded.
        dataFrames_contentNew_frictionInfo (list): Placeholder for frictionInfo data - unused until FrictionInformation's structure is available.

        Node dict shape (for dataFrames_region_path_nodes / dataFrames_region_oldRegion_shapePointSet_nodes): {'delta_tier': 'node-XY1'..'node-XY6'/'node-LatLon' (or 'node-LL1'..'node-LL6'/'node-LatLon' for ll), 'delta_x': <int>, 'delta_y': <int>, 'delta_lon': <float>, 'delta_lat': <float>, 'attr_localNode': [...], 'attr_disabled': [...], 'attr_enabled': [...], 'attr_data': [{'type': ..., 'value': ...}, ...], 'attr_dWidth': <int>, 'attr_dElevation': <int>}.

        ComputedLane dict shape (for dataFrames_region_path_computed / dataFrames_region_oldRegion_shapePointSet_computed): {'referenceLaneId': <int 0-255>, 'offsetX_size': 'small'/'large', 'offsetX_value': <int>, 'offsetY_size': 'small'/'large', 'offsetY_value': <int>, 'rotateXY': <float deg, optional>, 'scaleXaxis': <int, optional>, 'scaleYaxis': <int, optional>}.

        Offset dict shape (for dataFrames_region_oldRegion_regionPointSet_nodeList): {'xOffset': <int>, 'yOffset': <int>, 'zOffset': <int, optional>}.

        Content item dict shape (for dataFrames_content_items): {'type': 'itis', 'value': <int 0-65535>} or {'type': 'text', 'value': <str>}.

    Returns:
        tim (str): TIM message
    '''

    # convert input to correct format 
    tim = {}

    if msgCnt is None:
        print('msgCnt is mandatory! Please provide msgCnt. Set to 0.')
        tim['msgCnt'] = 0
    elif not isinstance(msgCnt, int):
        print('msgCnt should be an integer! But', msgCnt, 'is provided. Set to 0.')
        tim['msgCnt'] = 0
    elif msgCnt < 0 or msgCnt > 127:
        print('msgCnt should be in range [0, 127]! But', msgCnt, 'is provided. Set to 0.')
        tim['msgCnt'] = 0
    else:
        tim['msgCnt'] = msgCnt

    if timeStamp is not None:
        if not isinstance(timeStamp, int):
            print('timeStamp should be an integer! But', timeStamp, 'is provided. Remove it.')
        elif timeStamp < 0 or timeStamp > 527040:
            print('timeStamp should be in range [0, 527040]! But', timeStamp, 'is provided. Remove it.')
        else:
            tim['timeStamp'] = timeStamp

    if packetID is not None:
        if not isinstance(packetID, int):
            print('packetID should be an integer! But', packetID, 'is provided. Set to 0.')
            tim['packetID'] = bytes(9)
        elif packetID < 0 or packetID > 2 ** 72 - 1:
            print('packetID should be in range [0, 2**72 - 1]! But', packetID, 'is provided. Set to 0.')
            tim['packetID'] = bytes(9)
        else:
            tim['packetID'] = packetID.to_bytes(9, byteorder='big')

    if urlB is not None:
        if not isinstance(urlB, str):
            print('urlB should be a string! But', urlB, 'is provided. Remove it.')
        elif len(urlB) < 1 or len(urlB) > 45:
            print('urlB should be 1 to 45 characters! But', urlB, '(', len(urlB), 'chars) is provided. Remove it.')
        else:
            tim['urlB'] = urlB

    tim['dataFrames'] = []
    if not isinstance(dataFrames_N, int):
        print('dataFrames_N should be an integer! But', dataFrames_N, 'is provided. Set dataframes_N to an integer.')
    elif dataFrames_N < 1 or dataFrames_N > 8:
        print('dataFrames_N should be in range [1, 8]! But', dataFrames_N, 'is provided. dataFrames cannot be encoded without at least 1 frame.')
    else:
        for i in range(dataFrames_N):
            df = {}
            df['doNotUse1'] = 0

            if dataFrames_frameType is None or len(dataFrames_frameType) <= i:
                print('Frame', i, ': dataFrames_frameType is mandatory! Set to unknown.')
                df['frameType'] = 'unknown'
            elif dataFrames_frameType[i] in ['unknown', 'advisory', 'roadSignage', 'commercialSignage']:
                df['frameType'] = dataFrames_frameType[i]
            else:
                print('Frame', i, ': dataFrames_frameType should be one of unknown, advisory, roadSignage, commercialSignage! But', dataFrames_frameType[i], 'is provided. Set to unknown.')
                df['frameType'] = 'unknown'

            frame_msgId = dataFrames_msgId[i] if dataFrames_msgId and len(dataFrames_msgId) > i else None
            if frame_msgId == 'furtherInfoID':
                if dataFrames_furtherInfoID is None or len(dataFrames_furtherInfoID) <= i or dataFrames_furtherInfoID[i] is None:
                    print('Frame', i, ': dataFrames_furtherInfoID is mandatory (msgId CHOICE)! Set to 0.')
                    df['msgId'] = ('furtherInfoID', bytes(2))
                elif not isinstance(dataFrames_furtherInfoID[i], int) or dataFrames_furtherInfoID[i] < 0 or dataFrames_furtherInfoID[i] > 65535:
                    print('Frame', i, ': dataFrames_furtherInfoID should be an integer in range [0, 65535]! But', dataFrames_furtherInfoID[i], 'is provided. Set to 0.')
                    df['msgId'] = ('furtherInfoID', bytes(2))
                else:
                    df['msgId'] = ('furtherInfoID', dataFrames_furtherInfoID[i].to_bytes(2, byteorder='big'))

            elif frame_msgId == 'roadSignID':
                roadSign = {}
                roadSign['position'] = {}
                frame_lat = dataFrames_roadSignID_position_lat[i] if dataFrames_roadSignID_position_lat and len(dataFrames_roadSignID_position_lat) > i else None
                if frame_lat is None or frame_lat < -90 or frame_lat > 90:
                    print('Frame', i, ': dataFrames_roadSignID_position_lat is mandatory and should be in range [-90, 90]! But', frame_lat, 'is provided. Set to 90.0000001.')
                    roadSign['position']['lat'] = 900000001
                else:
                    roadSign['position']['lat'] = int(frame_lat * 10 ** 7)

                frame_long = dataFrames_roadSignID_position_long[i] if dataFrames_roadSignID_position_long and len(dataFrames_roadSignID_position_long) > i else None
                if frame_long is None or frame_long < -179.9999999 or frame_long > 180:
                    print('Frame', i, ': dataFrames_roadSignID_position_long is mandatory and should be in range [-179.9999999, 180]! But', frame_long, 'is provided. Set to 180.0000001.')
                    roadSign['position']['long'] = 1800000001
                else:
                    roadSign['position']['long'] = int(frame_long * 10 ** 7)

                frame_elev = dataFrames_roadSignID_position_elevation[i] if dataFrames_roadSignID_position_elevation and len(dataFrames_roadSignID_position_elevation) > i else None
                if frame_elev is not None:
                    if frame_elev < -409.5 or frame_elev > 6143.9:
                        print('Frame', i, ': dataFrames_roadSignID_position_elevation should be in range [-409.5, 6143.9] m! But', frame_elev, 'is provided. Omit it.')
                    else:
                        roadSign['position']['elevation'] = int(frame_elev * 10)
            
                frame_viewAngle = dataFrames_roadSignID_viewAngle[i] if dataFrames_roadSignID_viewAngle and len(dataFrames_roadSignID_viewAngle) > i else None
                if frame_viewAngle is None or not isinstance(frame_viewAngle, int) or frame_viewAngle < 0 or frame_viewAngle > 65535:
                    print('Frame', i, ': dataFrames_roadSignID_viewAngle is mandatory and should be an integer in range [0, 65535]! But', frame_viewAngle, 'is provided. Set to 0.')
                    roadSign['viewAngle'] = (0, 16)
                else:
                    roadSign['viewAngle'] = (frame_viewAngle, 16)

                frame_mutcdcode = dataFrames_roadSignID_mutcdCode[i] if dataFrames_roadSignID_mutcdCode and len(dataFrames_roadSignID_mutcdCode) > i else None
                if frame_mutcdcode is not None:
                    if frame_mutcdcode not in ['none', 'regulatory', 'warning', 'maintenance', 'motoristService', 'guide', 'rec']:
                        print('Frame', i, ': dataFrames_roadSignID_mutcdCode should be one of none, regulatory, warning, maintenance, motoristService, guide, rec! But', frame_mutcdcode, 'is provided. Omit it.')
                    else:
                        roadSign['mutcdCode'] = frame_mutcdcode

                frame_crc = dataFrames_roadSignID_crc[i] if dataFrames_roadSignID_crc and len(dataFrames_roadSignID_crc) > i else None
                if frame_crc is not None:
                    if not isinstance(frame_crc, int) or frame_crc < 0 or frame_crc > 65535:
                        print('Frame', i, ': dataFrames_roadSignID_crc should be an integer in range [0, 65535]! But', frame_crc, 'is provided. Omit it.')
                    else:
                        roadSign['crc'] = frame_crc.to_bytes(2, byteorder = 'big')
                
                df['msgId'] = ('roadSignID', roadSign)
            else:
                print('Frame', i, ': dataFrames_msgId is mandatory, one of furtherInfoID or roadSignID! But', frame_msgId, 'is provided. Set to furtherInfoID 0.')
                df['msgId'] = ('furtherInfoID', bytes(2))


            if dataFrames_startYear is not None and len(dataFrames_startYear) > i and dataFrames_startYear[i] is not None:
                year = dataFrames_startYear[i]
                if not isinstance(year, int) or year < 0 or year > 4095:
                    print('Frame', i, ': dataFrames_startYear should be an integer in range [0, 4095]! But', year, 'is provided. Remove it.')
                else:
                    df['startYear'] = year

            if dataFrames_startTime is None or len(dataFrames_startTime) <= i or dataFrames_startTime[i] is None:
                print('Frame', i, ': dataFrames_startTime is mandatory! Set to 52740.')
                df['startTime'] = 52740
            elif not isinstance(dataFrames_startTime[i], int) or dataFrames_startTime[i] < 0 or dataFrames_startTime[i] > 527040:
                print('Frame', i, ': dataFrames_startTime should be an integer in range [0, 527040]! But', dataFrames_startTime[i], 'is provided. Set to 527040.')
                df['startTime'] = 527040
            else:
                df['startTime'] = dataFrames_startTime[i]

    
            if dataFrames_durationTime is None or len(dataFrames_durationTime) <= i or dataFrames_durationTime[i] is None:
                print('Frame', i, ': dataFrames_durationTime is mandatory! Set to 0.')
                df['durationTime'] = 0
            elif not isinstance(dataFrames_durationTime[i], int) or dataFrames_durationTime[i] < 0 or dataFrames_durationTime[i] > 32000:
                print('Frame', i, ': dataFrames_durationTime should be an integer in range [0, 32000]! But', dataFrames_durationTime[i], 'is provided. Set to 0.')
                df['durationTime'] = 0
            else:
                df['durationTime'] = dataFrames_durationTime[i]
 
            if dataFrames_priority is None or len(dataFrames_priority) <= i or dataFrames_priority[i] is None:
                print('Frame', i, ': dataFrames_priority is mandatory! Set to 0.')
                df['priority'] = 0
            elif not isinstance(dataFrames_priority[i], int) or dataFrames_priority[i] < 0 or dataFrames_priority[i] > 7:
                print('Frame', i, ': dataFrames_priority should be an integer in range [0, 7]! But', dataFrames_priority[i], 'is provided. Set to 0.')
                df['priority'] = 0
            else:
                df['priority'] = dataFrames_priority[i]

            df['doNotUse2'] = 0

            df['regions'] = []
            frame_regions_N = dataFrames_regions_N[i] if dataFrames_regions_N and len(dataFrames_regions_N) > i else None
            if frame_regions_N is None or not isinstance(frame_regions_N, int):
                print('Frame', i, ': dataFrames_regions_N is mandatory! Please provide the number of regions for this frame. Regions cannot be encoded.')
            elif frame_regions_N < 1 or frame_regions_N > 16:
                print('Frame', i, ': dataFrames_regions_N should be in range [1, 16]! But', frame_regions_N, 'is provided. Regions cannot be encoded.')
            else:
                for idx in range(frame_regions_N):
                    region = {}
                    # name 
                    name = dataFrames_region_name[i][idx] if dataFrames_region_name and len(dataFrames_region_name) > i and len(dataFrames_region_name[i]) > idx else None
                    if name is not None:
                        if not isinstance(name, str) or len(name) < 1 or len(name) > 63:
                            print('Frame', i, ', region', idx, ': name should be a string 1-63 characters! But', name, 'is provided. Omit it.')
                        else:
                            region['name'] = name
            
                    # id
                    seg_id = dataFrames_region_id_segment[i][idx] if dataFrames_region_id_segment and len(dataFrames_region_id_segment) > i and len(dataFrames_region_id_segment[i]) > idx else None
                    if seg_id is not None:
                        if not isinstance(seg_id, int) or seg_id < 0 or seg_id > 65535:
                            print('Frame', i, ', region', idx, ': id_segment should be an integer in range [0, 65535]! But', seg_id, 'is provided. Omit id.')
                        else:
                            region['id'] = {'id': seg_id}
                            reg_val = dataFrames_region_id_region[i][idx] if dataFrames_region_id_region and len(dataFrames_region_id_region) > i and len(dataFrames_region_id_region[i]) > idx else None
                            if reg_val is not None:
                                if not isinstance(reg_val, int) or reg_val < 0 or reg_val > 65535:
                                    print('Frame', i, ', region', idx, ': id_region should be an integer in range [0, 65535]! But', reg_val, 'is provided. Omit region sub-field.')
                                else:
                                    region['id']['region'] = reg_val

                    # anchor 
                    lat = dataFrames_region_lat[i][idx] if dataFrames_region_lat and len(dataFrames_region_lat) > i and len(dataFrames_region_lat[i]) > idx else None
                    long = dataFrames_region_long[i][idx] if dataFrames_region_long and len(dataFrames_region_long) > i and len(dataFrames_region_long[i]) > idx else None
                    elev = dataFrames_region_elevation[i][idx] if dataFrames_region_elevation and len(dataFrames_region_elevation) > i and len(dataFrames_region_elevation[i]) > idx else None
            
                    if lat is not None or long is not None:
                        anchor = {}
                        if lat is None or lat < -90 or lat > 90:
                            print('Frame', i, ', region', idx, ': anchor lat should be in range [-90, 90] if anchor is used! But', lat, 'is provided. Set to 90.0000001.')
                            anchor['lat'] = 900000001
                        else:
                            anchor['lat'] = int(lat * 10 ** 7)
            
                        if long is None or long < -179.9999999 or long > 180:
                            print('Frame', i, ', region', idx, ': anchor long should be in range [-179.9999999, 180] if anchor is used! But', long, 'is provided. Set to 180.0000001.')
                            anchor['long'] = 1800000001
                        else:
                            anchor['long'] = int(long * 10 ** 7)
            
                        if elev is not None:
                            if elev < -409.5 or elev > 6143.9:
                                print('Frame', i, ', region', idx, ': anchor elevation should be in range [-409.5, 6143.9] m! But', elev, 'is provided. Omit it.')
                            else:
                                anchor['elevation'] = int(elev * 10)
            
                        region['anchor'] = anchor
            
                    # laneWidth
                    width = dataFrames_region_laneWidth[i][idx] if dataFrames_region_laneWidth and len(dataFrames_region_laneWidth) > i and len(dataFrames_region_laneWidth[i]) > idx else None
                    if width is not None:
                        if width < 0 or width > 327.67:
                            print('Frame', i, ', region', idx, ': laneWidth should be in range [0, 327.67] m! But', width, 'is provided. Omit it.')
                        else:
                            region['laneWidth'] = int(width * 100)
            
                    # directionality
                    directionality = dataFrames_region_directionality[i][idx] if dataFrames_region_directionality and len(dataFrames_region_directionality) > i and len(dataFrames_region_directionality[i]) > idx else None
                    if directionality is not None:
                        if directionality in ['unavailable', 'forward', 'reverse', 'both']:
                            region['directionality'] = directionality
                        else:
                            print('Frame', i, ', region', idx, ': directionality should be one of unavailable, forward, reverse, both! But', directionality, 'is provided. Omit it.')
            
                    # closedPath
                    cp = dataFrames_region_closedPath[i][idx] if dataFrames_region_closedPath and len(dataFrames_region_closedPath) > i and len(dataFrames_region_closedPath[i]) > idx else None
                    if cp is not None:
                        if isinstance(cp, bool):
                            region['closedPath'] = cp
                        else:
                            print('Frame', i, ', region', idx, ': closedPath should be a boolean! But', cp, 'is provided. Omit it.')
            
                    # direction
                    direction = dataFrames_region_direction[i][idx] if dataFrames_region_direction and len(dataFrames_region_direction) > i and len(dataFrames_region_direction[i]) > idx else None
                    if direction is not None:
                        if not isinstance(direction, int) or direction < 0 or direction > 65535:
                            print('Frame', i, ', region', idx, ': direction should be an integer in range [0, 65535]! But', direction, 'is provided. Omit it.')
                        else:
                            region['direction'] = (direction, 16)

                    if dataFrames_region_description == 'path':
                        path = {}
                        scale = dataFrames_region_path_scale[i][idx] if dataFrames_region_path_scale and len(dataFrames_region_path_scale) > i and len(dataFrames_region_path_scale[i]) > idx else None
                        if scale is not None:
                            if not isinstance(scale, int) or scale < 0 or scale > 15:
                                print('Frame', i, ', region', idx, ': scale should be an integer in range [0, 15]! But', scale, 'is provided. Omit it.')
                            else:
                                path['scale'] = scale

                        offset_type = dataFrames_region_path_offset_type[i][idx] if dataFrames_region_path_offset_type and len(dataFrames_region_path_offset_type) > i and len(dataFrames_region_path_offset_type[i]) > idx else None
                        if offset_type == 'xy':
                            nodelistxy_type = dataFrames_region_path_nodelistxy_type[i][idx] if dataFrames_region_path_nodelistxy_type and len(dataFrames_region_path_nodelistxy_type) > i and len(dataFrames_region_path_nodelistxy_type[i]) > idx else None

                            if nodelistxy_type == 'nodes':
                                raw_nodes = dataFrames_region_path_nodes[i][idx] if dataFrames_region_path_nodes and len(dataFrames_region_path_nodes) > i and len(dataFrames_region_path_nodes[i]) > idx else None

                                if raw_nodes is None or len(raw_nodes) < 2 or len(raw_nodes) > 63:
                                    print('Frame', i, ', region', idx, ': path nodes (xy) should contain 2 to 63 entries! Omit offset.')
                                else:
                                    node_list = []
                                    for node_idx, node in enumerate(raw_nodes):
                                        node_out = {}
                                        tier = node.get('delta_tier')

                                        # delta
                                        if tier == 'node-LatLon':
                                            lon = node.get('delta_lon')
                                            lat = node.get('delta_lat')
                                            if lon is None or lon < -179.9999999 or lon > 180:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-LatLon lon invalid! Set to 0.')
                                                lon = 1800000001
                                            else:
                                                lon = int(lon * 10 ** 7)
                                            if lat is None or lat < -90 or lat > 90:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-LatLon lat invalid! Set to 0.')
                                                lat = 900000001
                                            else:
                                                lat = int(lat * 10 ** 7)
                                            node_out['delta'] = ('node-LatLon', {'lon': lon, 'lat': lat})

                                        elif tier == 'node-XY1':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -512 or x > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY1 x should be in range [-512, 511]! Set to 0.')
                                                x = -512
                                            if not isinstance(y, int) or y < -512 or y > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY1 y should be in range [-512, 511]! Set to 0.')
                                                y = -512
                                            node_out['delta'] = ('node-XY1', {'x': x, 'y': y})

                                        elif tier == 'node-XY2':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -1024 or x > 1023:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY2 x should be in range [-1024, 1023]! Set to 0.')
                                                x = -1024
                                            if not isinstance(y, int) or y < -1024 or y > 1023:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY2 y should be in range [-1024, 1023]! Set to 0.')
                                                y = -1024
                                            node_out['delta'] = ('node-XY2', {'x': x, 'y': y})

                                        elif tier == 'node-XY3':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -2048 or x > 2047:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY3 x should be in range [-2048, 2047]! Set to 0.')
                                                x = -2048
                                            if not isinstance(y, int) or y < -2048 or y > 2047:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY3 y should be in range [-2048, 2047]! Set to 0.')
                                                y = -2048
                                            node_out['delta'] = ('node-XY3', {'x': x, 'y': y})

                                        elif tier == 'node-XY4':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -4096 or x > 4095:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY4 x should be in range [-4096, 4095]! Set to 0.')
                                                x = -4096
                                            if not isinstance(y, int) or y < -4096 or y > 4095:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY4 y should be in range [-4096, 4095]! Set to 0.')
                                                y = -4096
                                            node_out['delta'] = ('node-XY4', {'x': x, 'y': y})

                                        elif tier == 'node-XY5':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -8192 or x > 8191:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY5 x should be in range [-8192, 8191]! Set to 0.')
                                                x = -8192
                                            if not isinstance(y, int) or y < -8192 or y > 8191:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY5 y should be in range [-8192, 8191]! Set to 0.')
                                                y = -8192
                                            node_out['delta'] = ('node-XY5', {'x': x, 'y': y})

                                        elif tier == 'node-XY6':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -32768 or x > 32767:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY6 x should be in range [-32768, 32767]! Set to 0.')
                                                x = -32768
                                            if not isinstance(y, int) or y < -32768 or y > 32767:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY6 y should be in range [-32768, 32767]! Set to 0.')
                                                y = -32768
                                            node_out['delta'] = ('node-XY6', {'x': x, 'y': y})

                                        else:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': delta_tier invalid! Defaulting to node-XY1 (0,0).')
                                            node_out['delta'] = ('node-XY1', {'x': 0, 'y': 0})

                                        # attributes
                                        attrs = {}

                                        localNode = node.get('attr_localNode')
                                        if localNode is not None:
                                            if len(localNode) < 1 or len(localNode) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_localNode should have 1-8 entries! Omit it.')
                                            else:
                                                valid_list = [a for a in localNode if a in ['reserved', 'stopLine', 'roundedCapStyleA', 'roundedCapStyleB', 'mergePoint', 'divergePoint', 'downstreamStopLine', 'downstreamStartNode', 'closedToTraffic', 'safeIsland', 'curbPresentAtStepOff', 'hydrantPresent']]
                                                if valid_list:
                                                    attrs['localNode'] = valid_list

                                        disabled = node.get('attr_disabled')
                                        if disabled is not None:
                                            if len(disabled) < 1 or len(disabled) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_disabled should have 1-8 entries! Omit it.')
                                            else:
                                                valid_list = [a for a in disabled if a in ['reserved', 'doNotBlock', 'whiteLine', 'mergingLaneLeft', 'mergingLaneRight', 'curbOnLeft', 'curbOnRight', 'loadingzoneOnLeft', 'loadingzoneOnRight', 'turnOutPointOnLeft', 'turnOutPointOnRight', 'adjacentParkingOnLeft', 'adjacentParkingOnRight', 'adjacentBikeLaneOnLeft', 'adjacentBikeLaneOnRight', 'sharedBikeLane', 'bikeBoxInFront', 'transitStopOnLeft', 'transitStopOnRight', 'transitStopInLane', 'sharedWithTrackedVehicle', 'safeIsland', 'lowCurbsPresent', 'rumbleStripPresent', 'audibleSignalingPresent', 'adaptiveTimingPresent', 'rfSignalRequestPresent', 'partialCurbIntrusion', 'taperToLeft', 'taperToRight', 'taperToCenterLine', 'parallelParking', 'headInParking', 'freeParking', 'timeRestrictionsOnParking', 'costToPark', 'midBlockCurbPresent', 'unEvenPavementPresent']]
                                                if valid_list:
                                                    attrs['disabled'] = valid_list

                                        enabled = node.get('attr_enabled')
                                        if enabled is not None:
                                            if len(enabled) < 1 or len(enabled) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_enabled should have 1-8 entries! Omit it.')
                                            else:
                                                valid_list = [a for a in enabled if a in ['reserved', 'doNotBlock', 'whiteLine', 'mergingLaneLeft', 'mergingLaneRight', 'curbOnLeft', 'curbOnRight', 'loadingzoneOnLeft', 'loadingzoneOnRight', 'turnOutPointOnLeft', 'turnOutPointOnRight', 'adjacentParkingOnLeft', 'adjacentParkingOnRight', 'adjacentBikeLaneOnLeft', 'adjacentBikeLaneOnRight', 'sharedBikeLane', 'bikeBoxInFront', 'transitStopOnLeft', 'transitStopOnRight', 'transitStopInLane', 'sharedWithTrackedVehicle', 'safeIsland', 'lowCurbsPresent', 'rumbleStripPresent', 'audibleSignalingPresent', 'adaptiveTimingPresent', 'rfSignalRequestPresent', 'partialCurbIntrusion', 'taperToLeft', 'taperToRight', 'taperToCenterLine', 'parallelParking', 'headInParking', 'freeParking', 'timeRestrictionsOnParking', 'costToPark', 'midBlockCurbPresent', 'unEvenPavementPresent']]
                                                if valid_list:
                                                    attrs['enabled'] = valid_list

                                        attr_data = node.get('attr_data')
                                        if attr_data is not None:
                                            if len(attr_data) < 1 or len(attr_data) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_data should have 1-8 entries! Omit it.')
                                            else:
                                                data_list = []
                                                for entry in attr_data:
                                                    t = entry.get('type')
                                                    v = entry.get('value')
                                                    if t == 'pathEndPointAngle':
                                                        if not isinstance(v, int) or v < -150 or v > 150:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': pathEndPointAngle should be in range [-150, 150]! Skip entry.')
                                                            continue
                                                        data_list.append(('pathEndPointAngle', v))
                                                    elif t == 'laneCrownPointCenter':
                                                        if not isinstance(v, int) or v < -128 or v > 127:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointCenter should be in range [-128, 127]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneCrownPointCenter', v))
                                                    elif t == 'laneCrownPointLeft':
                                                        if not isinstance(v, int) or v < -128 or v > 127:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointLeft should be in range [-128, 127]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneCrownPointLeft', v))
                                                    elif t == 'laneCrownPointRight':
                                                        if not isinstance(v, int) or v < -128 or v > 127:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointRight should be in range [-128, 127]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneCrownPointRight', v))
                                                    elif t == 'laneAngle':
                                                        if not isinstance(v, int) or v < -180 or v > 180:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneAngle should be in range [-180, 180]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneAngle', v))
                                                    elif t == 'speedLimits':
                                                        if not isinstance(v, list) or len(v) < 1 or len(v) > 9:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': speedLimits should be a list of 1-9 entries! Skip entry.')
                                                            continue
                                                        limits = []
                                                        for lim in v:
                                                            lim_type = lim.get('type')
                                                            lim_speed = lim.get('speed')
                                                            if lim_type not in ['unknown', 'maxSpeedInSchoolZone', 'maxSpeedInSchoolZoneWhenChildrenArePresent', 'maxSpeedInConstructionZone', 'vehicleMinSpeed', 'vehicleMaxSpeed', 'vehicleNightMaxSpeed', 'truckMinSpeed', 'truckMaxSpeed', 'truckNightMaxSpeed', 'vehiclesWithTrailersMinSpeed', 'vehiclesWithTrailersMaxSpeed', 'vehiclesWithTrailersNightMaxSpeed']:
                                                                print('Frame', i, ', region', idx, ', node', node_idx, ': speed limit type invalid! Skip this limit.')
                                                                continue
                                                            if not isinstance(lim_speed, (int, float)) or lim_speed < 0 or lim_speed > 163.82:
                                                                print('Frame', i, ', region', idx, ', node', node_idx, ': speed limit speed should be in range [0, 163.82] m/s! Skip this limit.')
                                                                continue
                                                            limits.append({'type': lim_type, 'speed': int(lim_speed / 0.02)})
                                                        if limits:
                                                            data_list.append(('speedLimits', limits))
                                                    else:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': attr_data type', t, 'not recognized! Skip entry.')
                                                if data_list:
                                                    attrs['data'] = data_list

                                        dWidth = node.get('attr_dWidth')
                                        if dWidth is not None:
                                            if not isinstance(dWidth, int) or dWidth == 0 or dWidth < -512 or dWidth > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_dWidth should be a nonzero integer in range [-512, 511]! Omit it.')
                                            else:
                                                attrs['dWidth'] = dWidth

                                        dElevation = node.get('attr_dElevation')
                                        if dElevation is not None:
                                            if not isinstance(dElevation, int) or dElevation == 0 or dElevation < -512 or dElevation > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_dElevation should be a nonzero integer in range [-512, 511]! Omit it.')
                                            else:
                                                attrs['dElevation'] = dElevation

                                        if attrs:
                                            node_out['attributes'] = attrs

                                        node_list.append(node_out)

                                    path['offset'] = ('xy', ('nodes', node_list))

                            elif nodelistxy_type == 'computed':
                                raw_computed = dataFrames_region_path_computed[i][idx] if dataFrames_region_path_computed and len(dataFrames_region_path_computed) > i and len(dataFrames_region_path_computed[i]) > idx else None

                                if raw_computed is None:
                                    print('Frame', i, ', region', idx, ': path computed lane data missing! Omit offset.')
                                else:
                                    computed_lane = {}
                                    ref_id = raw_computed.get('referenceLaneId')
                                    if not isinstance(ref_id, int) or ref_id < 0 or ref_id > 255:
                                        print('Frame', i, ', region', idx, ': referenceLaneId should be an integer in range [0, 255]! Set to 0.')
                                        computed_lane['referenceLaneId'] = 0
                                    else:
                                        computed_lane['referenceLaneId'] = ref_id

                                    offsetX_size = raw_computed.get('offsetX_size')
                                    offsetX_value = raw_computed.get('offsetX_value')
                                    if offsetX_size == 'small':
                                        if not isinstance(offsetX_value, int) or offsetX_value < -2047 or offsetX_value > 2047:
                                            print('Frame', i, ', region', idx, ': offsetXaxis small should be in range [-2047, 2047]! Set to 0.')
                                            offsetX_value = 0
                                        computed_lane['offsetXaxis'] = ('small', offsetX_value)
                                    elif offsetX_size == 'large':
                                        if not isinstance(offsetX_value, int) or offsetX_value < -32767 or offsetX_value > 32767:
                                            print('Frame', i, ', region', idx, ': offsetXaxis large should be in range [-32767, 32767]! Set to 0.')
                                            offsetX_value = 0
                                        computed_lane['offsetXaxis'] = ('large', offsetX_value)
                                    else:
                                        print('Frame', i, ', region', idx, ': offsetXaxis is mandatory (small/large)! Set to small 0.')
                                        computed_lane['offsetXaxis'] = ('small', 0)

                                    offsetY_size = raw_computed.get('offsetY_size')
                                    offsetY_value = raw_computed.get('offsetY_value')
                                    if offsetY_size == 'small':
                                        if not isinstance(offsetY_value, int) or offsetY_value < -2047 or offsetY_value > 2047:
                                            print('Frame', i, ', region', idx, ': offsetYaxis small should be in range [-2047, 2047]! Set to 0.')
                                            offsetY_value = 0
                                        computed_lane['offsetYaxis'] = ('small', offsetY_value)
                                    elif offsetY_size == 'large':
                                        if not isinstance(offsetY_value, int) or offsetY_value < -32767 or offsetY_value > 32767:
                                            print('Frame', i, ', region', idx, ': offsetYaxis large should be in range [-32767, 32767]! Set to 0.')
                                            offsetY_value = 0
                                        computed_lane['offsetYaxis'] = ('large', offsetY_value)
                                    else:
                                        print('Frame', i, ', region', idx, ': offsetYaxis is mandatory (small/large)! Set to small 0.')
                                        computed_lane['offsetYaxis'] = ('small', 0)

                                    rotate = raw_computed.get('rotateXY')
                                    if rotate is not None:
                                        if rotate < 0 or rotate > 359.9875:
                                            print('Frame', i, ', region', idx, ': rotateXY should be in range [0, 359.9875] deg! Omit it.')
                                        else:
                                            computed_lane['rotateXY'] = int(rotate / 0.0125)

                                    scaleX = raw_computed.get('scaleXaxis')
                                    if scaleX is not None:
                                        if not isinstance(scaleX, int) or scaleX < -1999 or scaleX > 2047:
                                            print('Frame', i, ', region', idx, ': scaleXaxis should be an integer in range [-1999, 2047]! Omit it.')
                                        else:
                                            computed_lane['scaleXaxis'] = scaleX

                                    scaleY = raw_computed.get('scaleYaxis')
                                    if scaleY is not None:
                                        if not isinstance(scaleY, int) or scaleY < -1999 or scaleY > 2047:
                                            print('Frame', i, ', region', idx, ': scaleYaxis should be an integer in range [-1999, 2047]! Omit it.')
                                        else:
                                            computed_lane['scaleYaxis'] = scaleY

                                    path['offset'] = ('xy', ('computed', computed_lane))
                            else:
                                print('Frame', i, ', region', idx, ': path offset xy requires nodelistxy_type to be nodes or computed! Omit offset.')

                        elif offset_type == 'll':
                            raw_nodes = dataFrames_region_path_nodes[i][idx] if dataFrames_region_path_nodes and len(dataFrames_region_path_nodes) > i and len(dataFrames_region_path_nodes[i]) > idx else None

                            if raw_nodes is None or len(raw_nodes) < 2 or len(raw_nodes) > 63:
                                print('Frame', i, ', region', idx, ': path nodes (ll) should contain 2 to 63 entries! Omit offset.')
                            else:
                                node_list = []
                                for node_idx, node in enumerate(raw_nodes):
                                    node_out = {}
                                    tier = node.get('delta_tier')

                                    if tier == 'node-LatLon':
                                        lon = node.get('delta_lon')
                                        lat = node.get('delta_lat')
                                        if lon is None or lon < -179.9999999 or lon > 180:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LatLon lon invalid! Set to 0.')
                                            lon = 1800000001
                                        else:
                                            lon = int(lon * 10 ** 7)
                                        if lat is None or lat < -90 or lat > 90:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LatLon lat invalid! Set to 0.')
                                            lat = 900000001
                                        else:
                                            lat = int(lat * 10 ** 7)
                                        node_out['delta'] = ('node-LatLon', {'lon': lon, 'lat': lat})

                                    elif tier == 'node-LL1':
                                        lon = node.get('delta_lon')
                                        lat = node.get('delta_lat')
                                        if not isinstance(lon, (int, float)) or lon < -0.0002048 or lon > 0.0002047:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL1 lon should be in range [-0.0002048, 0.0002047] deg! Set to -0.0002048 (unknown).')
                                            lon = -0.0002048
                                        if not isinstance(lat, (int, float)) or lat < -0.0002048 or lat > 0.0002047:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL1 lat should be in range [-0.0002048, 0.0002047] deg! Set to -0.0002048 (unknown).')
                                            lat = -0.0002048
                                        node_out['delta'] = ('node-LL1', {'lon': int(lon * 10 ** 7), 'lat': int(lat * 10 ** 7)})

                                    elif tier == 'node-LL2':
                                        lon = node.get('delta_lon')
                                        lat = node.get('delta_lat')
                                        if not isinstance(lon, (int, float)) or lon < -0.0008192 or lon > 0.0008191:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL2 lon should be in range [-0.0008192, 0.0008191] deg! Set to -0.0008192 (unknown).')
                                            lon = -0.0008192
                                        if not isinstance(lat, (int, float)) or lat < -0.0008192 or lat > 0.0008191:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL2 lat should be in range [-0.0008192, 0.0008191] deg! Set to -0.0008192 (unknown).')
                                            lat = -0.0008192
                                        node_out['delta'] = ('node-LL2', {'lon': int(lon * 10 ** 7), 'lat': int(lat * 10 ** 7)})

                                    elif tier == 'node-LL3':
                                        lon = node.get('delta_lon')
                                        lat = node.get('delta_lat')
                                        if not isinstance(lon, (int, float)) or lon < -0.0032768 or lon > 0.0032767:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL3 lon should be in range [-0.0032768, 0.0032767] deg! Set to -0.0032768 (unknown).')
                                            lon = -0.0032768
                                        if not isinstance(lat, (int, float)) or lat < -0.0032768 or lat > 0.0032767:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL3 lat should be in range [-0.0032768, 0.0032767] deg! Set to -0.0032768 (unknown).')
                                            lat = -0.0032768
                                        node_out['delta'] = ('node-LL3', {'lon': int(lon * 10 ** 7), 'lat': int(lat * 10 ** 7)})

                                    elif tier == 'node-LL4':
                                        # OffsetLL-B18 has explicit sentinel/clamp values per spec:
                                        # +131071 = clamp-high, -131071 = clamp-low, -131072 = unknown
                                        lon = node.get('delta_lon')
                                        lat = node.get('delta_lat')
                                        if lon is None:
                                            lon_enc = -131072
                                        elif lon >= 0.0131071:
                                            lon_enc = 131071
                                        elif lon <= -0.0131071:
                                            lon_enc = -131071
                                        else:
                                            lon_enc = int(lon * 10 ** 7)
                                        if lat is None:
                                            lat_enc = -131072
                                        elif lat >= 0.0131071:
                                            lat_enc = 131071
                                        elif lat <= -0.0131071:
                                            lat_enc = -131071
                                        else:
                                            lat_enc = int(lat * 10 ** 7)
                                        node_out['delta'] = ('node-LL4', {'lon': lon_enc, 'lat': lat_enc})

                                    elif tier == 'node-LL5':
                                        lon = node.get('delta_lon')
                                        lat = node.get('delta_lat')
                                        if not isinstance(lon, (int, float)) or lon < -0.2097152 or lon > 0.2097151:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL5 lon should be in range [-0.2097152, 0.2097151] deg! Set to -0.2097152 (unknown).')
                                            lon = -0.2097152
                                        if not isinstance(lat, (int, float)) or lat < -0.2097152 or lat > 0.2097151:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL5 lat should be in range [-0.2097152, 0.2097151] deg! Set to -0.2097152 (unknown).')
                                            lat = -0.2097152
                                        node_out['delta'] = ('node-LL5', {'lon': int(lon * 10 ** 7), 'lat': int(lat * 10 ** 7)})

                                    elif tier == 'node-LL6':
                                        lon = node.get('delta_lon')
                                        lat = node.get('delta_lat')
                                        if not isinstance(lon, (int, float)) or lon < -0.8388608 or lon > 0.8388607:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL6 lon should be in range [-0.8388608, 0.8388607] deg! Set to -0.8388608 (unknown).')
                                            lon = -0.8388608
                                        if not isinstance(lat, (int, float)) or lat < -0.8388608 or lat > 0.8388607:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': node-LL6 lat should be in range [-0.8388608, 0.8388607] deg! Set to -0.8388608 (unknown).')
                                            lat = -0.8388608
                                        node_out['delta'] = ('node-LL6', {'lon': int(lon * 10 ** 7), 'lat': int(lat * 10 ** 7)})

                                    else:
                                        print('Frame', i, ', region', idx, ', node', node_idx, ': delta_tier invalid! Defaulting to node-LL1 (0,0).')
                                        node_out['delta'] = ('node-LL1', {'lon': 0, 'lat': 0})

                                    # attributes: NodeAttributeSetLL, OPTIONAL (identical shape to XY)
                                    attrs = {}

                                    localNode = node.get('attr_localNode')
                                    if localNode is not None:
                                        if len(localNode) < 1 or len(localNode) > 8:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': attr_localNode should have 1-8 entries! Omit it.')
                                        else:
                                            valid_list = [a for a in localNode if a in ['reserved', 'stopLine', 'roundedCapStyleA', 'roundedCapStyleB', 'mergePoint', 'divergePoint', 'downstreamStopLine', 'downstreamStartNode', 'closedToTraffic', 'safeIsland', 'curbPresentAtStepOff', 'hydrantPresent']]
                                            if valid_list:
                                                attrs['localNode'] = valid_list

                                    disabled = node.get('attr_disabled')
                                    if disabled is not None:
                                        if len(disabled) < 1 or len(disabled) > 8:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': attr_disabled should have 1-8 entries! Omit it.')
                                        else:
                                            valid_list = [a for a in disabled if a in ['reserved', 'doNotBlock', 'whiteLine', 'mergingLaneLeft', 'mergingLaneRight', 'curbOnLeft', 'curbOnRight', 'loadingzoneOnLeft', 'loadingzoneOnRight', 'turnOutPointOnLeft', 'turnOutPointOnRight', 'adjacentParkingOnLeft', 'adjacentParkingOnRight', 'adjacentBikeLaneOnLeft', 'adjacentBikeLaneOnRight', 'sharedBikeLane', 'bikeBoxInFront', 'transitStopOnLeft', 'transitStopOnRight', 'transitStopInLane', 'sharedWithTrackedVehicle', 'safeIsland', 'lowCurbsPresent', 'rumbleStripPresent', 'audibleSignalingPresent', 'adaptiveTimingPresent', 'rfSignalRequestPresent', 'partialCurbIntrusion', 'taperToLeft', 'taperToRight', 'taperToCenterLine', 'parallelParking', 'headInParking', 'freeParking', 'timeRestrictionsOnParking', 'costToPark', 'midBlockCurbPresent', 'unEvenPavementPresent']]
                                            if valid_list:
                                                attrs['disabled'] = valid_list

                                    enabled = node.get('attr_enabled')
                                    if enabled is not None:
                                        if len(enabled) < 1 or len(enabled) > 8:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': attr_enabled should have 1-8 entries! Omit it.')
                                        else:
                                            valid_list = [a for a in enabled if a in ['reserved', 'doNotBlock', 'whiteLine', 'mergingLaneLeft', 'mergingLaneRight', 'curbOnLeft', 'curbOnRight', 'loadingzoneOnLeft', 'loadingzoneOnRight', 'turnOutPointOnLeft', 'turnOutPointOnRight', 'adjacentParkingOnLeft', 'adjacentParkingOnRight', 'adjacentBikeLaneOnLeft', 'adjacentBikeLaneOnRight', 'sharedBikeLane', 'bikeBoxInFront', 'transitStopOnLeft', 'transitStopOnRight', 'transitStopInLane', 'sharedWithTrackedVehicle', 'safeIsland', 'lowCurbsPresent', 'rumbleStripPresent', 'audibleSignalingPresent', 'adaptiveTimingPresent', 'rfSignalRequestPresent', 'partialCurbIntrusion', 'taperToLeft', 'taperToRight', 'taperToCenterLine', 'parallelParking', 'headInParking', 'freeParking', 'timeRestrictionsOnParking', 'costToPark', 'midBlockCurbPresent', 'unEvenPavementPresent']]
                                            if valid_list:
                                                attrs['enabled'] = valid_list

                                    attr_data = node.get('attr_data')
                                    if attr_data is not None:
                                        if len(attr_data) < 1 or len(attr_data) > 8:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': attr_data should have 1-8 entries! Omit it.')
                                        else:
                                            data_list = []
                                            for entry in attr_data:
                                                t = entry.get('type')
                                                v = entry.get('value')
                                                if t == 'pathEndPointAngle':
                                                    if not isinstance(v, int) or v < -150 or v > 150:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': pathEndPointAngle should be in range [-150, 150]! Skip entry.')
                                                        continue
                                                    data_list.append(('pathEndPointAngle', v))
                                                elif t == 'laneCrownPointCenter':
                                                    if not isinstance(v, int) or v < -128 or v > 127:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointCenter should be in range [-128, 127]! Skip entry.')
                                                        continue
                                                    data_list.append(('laneCrownPointCenter', v))
                                                elif t == 'laneCrownPointLeft':
                                                    if not isinstance(v, int) or v < -128 or v > 127:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointLeft should be in range [-128, 127]! Skip entry.')
                                                        continue
                                                    data_list.append(('laneCrownPointLeft', v))
                                                elif t == 'laneCrownPointRight':
                                                    if not isinstance(v, int) or v < -128 or v > 127:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointRight should be in range [-128, 127]! Skip entry.')
                                                        continue
                                                    data_list.append(('laneCrownPointRight', v))
                                                elif t == 'laneAngle':
                                                    if not isinstance(v, int) or v < -180 or v > 180:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': laneAngle should be in range [-180, 180]! Skip entry.')
                                                        continue
                                                    data_list.append(('laneAngle', v))
                                                elif t == 'speedLimits':
                                                    if not isinstance(v, list) or len(v) < 1 or len(v) > 9:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': speedLimits should be a list of 1-9 entries! Skip entry.')
                                                        continue
                                                    limits = []
                                                    for lim in v:
                                                        lim_type = lim.get('type')
                                                        lim_speed = lim.get('speed')
                                                        if lim_type not in ['unknown', 'maxSpeedInSchoolZone', 'maxSpeedInSchoolZoneWhenChildrenArePresent', 'maxSpeedInConstructionZone', 'vehicleMinSpeed', 'vehicleMaxSpeed', 'vehicleNightMaxSpeed', 'truckMinSpeed', 'truckMaxSpeed', 'truckNightMaxSpeed', 'vehiclesWithTrailersMinSpeed', 'vehiclesWithTrailersMaxSpeed', 'vehiclesWithTrailersNightMaxSpeed']:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': speed limit type invalid! Skip this limit.')
                                                            continue
                                                        if not isinstance(lim_speed, (int, float)) or lim_speed < 0 or lim_speed > 163.82:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': speed limit speed should be in range [0, 163.82] m/s! Skip this limit.')
                                                            continue
                                                        limits.append({'type': lim_type, 'speed': int(lim_speed / 0.02)})
                                                    if limits:
                                                        data_list.append(('speedLimits', limits))
                                                else:
                                                    print('Frame', i, ', region', idx, ', node', node_idx, ': attr_data type', t, 'not recognized! Skip entry.')
                                            if data_list:
                                                attrs['data'] = data_list

                                    dWidth = node.get('attr_dWidth')
                                    if dWidth is not None:
                                        if not isinstance(dWidth, int) or dWidth == 0 or dWidth < -512 or dWidth > 511:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': attr_dWidth should be a nonzero integer in range [-512, 511]! Omit it.')
                                        else:
                                            attrs['dWidth'] = dWidth

                                    dElevation = node.get('attr_dElevation')
                                    if dElevation is not None:
                                        if not isinstance(dElevation, int) or dElevation == 0 or dElevation < -512 or dElevation > 511:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': attr_dElevation should be a nonzero integer in range [-512, 511]! Omit it.')
                                        else:
                                            attrs['dElevation'] = dElevation

                                    if attrs:
                                        node_out['attributes'] = attrs

                                    node_list.append(node_out)

                                path['offset'] = ('ll', ('nodes', node_list))

                        else:
                            print('Frame', i, ', region', idx, ': path offset_type should be xy or ll! Omit offset.')

                        if path:
                            region['description'] = ('path', path)

                    elif dataFrames_region_description == 'geometry':
                        geometry = {}
                        # direction
                        geom_dir = dataFrames_region_geometry_direction[i][idx] if dataFrames_region_geometry_direction and len(dataFrames_region_geometry_direction) > i and len(dataFrames_region_geometry_direction[i]) > idx else None
                        if geom_dir is None or not isinstance(geom_dir, int) or geom_dir < 0 or geom_dir > 65535:
                            print('Frame', i, ', region', idx, ': geometry direction is mandatory if geometry is used! Set to 0.')
                            geometry['direction'] = (0, 16)
                        else:
                            geometry['direction'] = (geom_dir, 16)
            
                        # extent
                        geom_extent = dataFrames_region_geometry_extent[i][idx] if dataFrames_region_geometry_extent and len(dataFrames_region_geometry_extent) > i and len(dataFrames_region_geometry_extent[i]) > idx else None
                        if geom_extent is not None:
                            if geom_extent in ['useInstantlyOnly', 'useFor3meters', 'useFor10meters', 'useFor50meters', 'useFor100meters', 'useFor500meters', 'useFor1000meters', 'useFor5000meters', 'useFor10000meters', 'useFor50000meters', 'useFor100000meters', 'useFor500000meters', 'useFor1000000meters', 'useFor5000000meters', 'useFor10000000meters', 'forever']:
                                geometry['extent'] = geom_extent
                            else:
                                print('Frame', i, ', region', idx, ': geometry extent invalid! Omit it.')
            
                        # laneWidth
                        geom_width = dataFrames_region_geometry_laneWidth[i][idx] if dataFrames_region_geometry_laneWidth and len(dataFrames_region_geometry_laneWidth) > i and len(dataFrames_region_geometry_laneWidth[i]) > idx else None
                        if geom_width is not None:
                            if geom_width < 0 or geom_width > 327.67:
                                print('Frame', i, ', region', idx, ': geometry laneWidth should be in range [0, 327.67] m! Omit it.')
                            else:
                                geometry['laneWidth'] = int(geom_width * 100)
            
                        # circle
                        circle = {}
                        circ_lat = dataFrames_region_geometry_circle_lat[i][idx] if dataFrames_region_geometry_circle_lat and len(dataFrames_region_geometry_circle_lat) > i and len(dataFrames_region_geometry_circle_lat[i]) > idx else None
                        circle['center'] = {}
                        if circ_lat < -90 or circ_lat > 90:
                            print('Frame', i, ', region', idx, ': geometry circle lat should be in range [-90, 90]! Set to 90.0000001.')
                            circle['center']['lat'] = 900000001
                        else:
                            circle['center']['lat'] = int(circ_lat * 10 ** 7)

                        circ_long = dataFrames_region_geometry_circle_long[i][idx] if dataFrames_region_geometry_circle_long and len(dataFrames_region_geometry_circle_long) > i and len(dataFrames_region_geometry_circle_long[i]) > idx else None
                        if circ_long < -179.9999999 or circ_long > 180:
                            print('Frame', i, ', region', idx, ': geometry circle long should be in range [-179.9999999, 180]! Set to 180.0000001.')
                            circle['center']['long'] = 1800000001
                        else:
                            circle['center']['long'] = int(circ_long * 10 ** 7)
            
                        circ_elev = dataFrames_region_geometry_circle_elevation[i][idx] if dataFrames_region_geometry_circle_elevation and len(dataFrames_region_geometry_circle_elevation) > i and len(dataFrames_region_geometry_circle_elevation[i]) > idx else None
                        if circ_elev is not None:
                            if circ_elev < -409.5 or circ_elev > 6143.9:
                                print('Frame', i, ', region', idx, ': geometry circle elevation out of range! Omit it.')
                            else:
                                circle['center']['elevation'] = int(circ_elev * 10)
            
                        # raidus
                        circ_radius = dataFrames_region_geometry_circle_radius[i][idx] if dataFrames_region_geometry_circle_radius and len(dataFrames_region_geometry_circle_radius) > i and len(dataFrames_region_geometry_circle_radius[i]) > idx else None
                        if not isinstance(circ_radius, int) or circ_radius < 0 or circ_radius > 4095:
                            print('Frame', i, ', region', idx, ': geometry circle radius should be an integer in range [0, 4095]! Set to 0.')
                            circle['radius'] = 0
                        else:
                            circle['radius'] = circ_radius
            
                        # units
                        circ_units = dataFrames_region_geometry_circle_units[i][idx] if dataFrames_region_geometry_circle_units and len(dataFrames_region_geometry_circle_units) > i and len(dataFrames_region_geometry_circle_units[i]) > idx else None
                        if circ_units is None or circ_units not in ['centimeter', 'cm2-5', 'decimeter', 'meter', 'kilometer', 'foot', 'yard', 'mile']:
                            print('Frame', i, ', region', idx, ': geometry circle units is mandatory, one of centimeter, cm2-5, decimeter, meter, kilometer, foot, yard, mile! Set to meter.')
                            circle['units'] = 'meter'
                        else:
                            circle['units'] = circ_units
            
                        geometry['circle'] = circle
                        region['description'] = ('geometry', geometry)

                    elif dataFrames_region_description == 'oldRegion':
                        oldRegion = {}
                        # direction
                        direction = dataFrames_region_oldRegion_direction[i][idx] if dataFrames_region_oldRegion_direction and len(dataFrames_region_oldRegion_direction) > i and len(dataFrames_region_oldRegion_direction[i]) > idx else None
                        if direction is None or not isinstance(direction, int) or direction < 0 or direction > 65535:
                            print('Frame', i, ', region', idx, ': oldRegion direction is mandatory and should be an integer in range [0, 65535]! Set to 0.')
                            oldRegion['direction'] = (0, 16)
                        else:
                            oldRegion['direction'] = (direction, 16)
                    
                        # extent
                        extent = dataFrames_region_oldRegion_extent[i][idx] if dataFrames_region_oldRegion_extent and len(dataFrames_region_oldRegion_extent) > i and len(dataFrames_region_oldRegion_extent[i]) > idx else None
                        if extent is not None:
                            if extent in ['useInstantlyOnly', 'useFor3meters', 'useFor10meters', 'useFor50meters', 'useFor100meters', 'useFor500meters', 'useFor1000meters', 'useFor5000meters', 'useFor10000meters', 'useFor50000meters', 'useFor100000meters', 'useFor500000meters', 'useFor1000000meters', 'useFor5000000meters', 'useFor10000000meters', 'forever']:
                                oldRegion['extent'] = extent
                            else:
                                print('Frame', i, ', region', idx, ': oldRegion extent invalid! Omit it.')
                    
                        # area
                        area_type = dataFrames_region_oldRegion_area_type[i][idx] if dataFrames_region_oldRegion_area_type and len(dataFrames_region_oldRegion_area_type) > i and len(dataFrames_region_oldRegion_area_type[i]) > idx else None
                        if area_type == 'shapePointSet':
                            shapePointSet = {}
                            # anchor
                            sp_lat = dataFrames_region_oldRegion_shapePointSet_anchor_lat[i][idx] if dataFrames_region_oldRegion_shapePointSet_anchor_lat and len(dataFrames_region_oldRegion_shapePointSet_anchor_lat) > i and len(dataFrames_region_oldRegion_shapePointSet_anchor_lat[i]) > idx else None
                            sp_long = dataFrames_region_oldRegion_shapePointSet_anchor_long[i][idx] if dataFrames_region_oldRegion_shapePointSet_anchor_long and len(dataFrames_region_oldRegion_shapePointSet_anchor_long) > i and len(dataFrames_region_oldRegion_shapePointSet_anchor_long[i]) > idx else None
                            sp_elev = dataFrames_region_oldRegion_shapePointSet_anchor_elevation[i][idx] if dataFrames_region_oldRegion_shapePointSet_anchor_elevation and len(dataFrames_region_oldRegion_shapePointSet_anchor_elevation) > i and len(dataFrames_region_oldRegion_shapePointSet_anchor_elevation[i]) > idx else None
                    
                            if sp_lat is not None or sp_long is not None:
                                anchor = {}
                                if sp_lat is None or sp_lat < -90 or sp_lat > 90:
                                    print('Frame', i, ', region', idx, ': shapePointSet anchor lat invalid! Set to 90.0000001.')
                                    anchor['lat'] = 900000001
                                else:
                                    anchor['lat'] = int(sp_lat * 10 ** 7)
                                if sp_long is None or sp_long < -179.9999999 or sp_long > 180:
                                    print('Frame', i, ', region', idx, ': shapePointSet anchor long invalid! Set to 180.0000001.')
                                    anchor['long'] = 1800000001
                                else:
                                    anchor['long'] = int(sp_long * 10 ** 7)
                                if sp_elev is not None:
                                    if sp_elev < -409.5 or sp_elev > 6143.9:
                                        print('Frame', i, ', region', idx, ': shapePointSet anchor elevation out of range! Omit it.')
                                    else:
                                        anchor['elevation'] = int(sp_elev * 10)
                                shapePointSet['anchor'] = anchor
                    
                            # laneWidth
                            sp_width = dataFrames_region_oldRegion_shapePointSet_laneWidth[i][idx] if dataFrames_region_oldRegion_shapePointSet_laneWidth and len(dataFrames_region_oldRegion_shapePointSet_laneWidth) > i and len(dataFrames_region_oldRegion_shapePointSet_laneWidth[i]) > idx else None
                            if sp_width is not None:
                                if sp_width < 0 or sp_width > 327.67:
                                    print('Frame', i, ', region', idx, ': shapePointSet laneWidth should be in range [0, 327.67] m! Omit it.')
                                else:
                                    shapePointSet['laneWidth'] = int(sp_width * 100)
                    
                            # directionality
                            sp_dir = dataFrames_region_oldRegion_shapePointSet_directionality[i][idx] if dataFrames_region_oldRegion_shapePointSet_directionality and len(dataFrames_region_oldRegion_shapePointSet_directionality) > i and len(dataFrames_region_oldRegion_shapePointSet_directionality[i]) > idx else None
                            if sp_dir is not None:
                                if sp_dir in ['unavailable', 'forward', 'reverse', 'both']:
                                    shapePointSet['directionality'] = sp_dir
                                else:
                                    print('Frame', i, ', region', idx, ': shapePointSet directionality invalid! Omit it.')
                    
                            # nodeList
                            sp_nodelistxy_type = dataFrames_region_oldRegion_shapePointSet_nodelistxy_type[i][idx] if dataFrames_region_oldRegion_shapePointSet_nodelistxy_type and len(dataFrames_region_oldRegion_shapePointSet_nodelistxy_type) > i and len(dataFrames_region_oldRegion_shapePointSet_nodelistxy_type[i]) > idx else None
                    
                            if sp_nodelistxy_type == 'nodes':
                                sp_raw_nodes = dataFrames_region_oldRegion_shapePointSet_nodes[i][idx] if dataFrames_region_oldRegion_shapePointSet_nodes and len(dataFrames_region_oldRegion_shapePointSet_nodes) > i and len(dataFrames_region_oldRegion_shapePointSet_nodes[i]) > idx else None
                    
                                if sp_raw_nodes is None or len(sp_raw_nodes) < 2 or len(sp_raw_nodes) > 63:
                                    print('Frame', i, ', region', idx, ': shapePointSet nodes should contain 2 to 63 entries! nodeList cannot be encoded.')
                                else:
                                    sp_node_list = []
                                    for node_idx, node in enumerate(sp_raw_nodes):
                                        node_out = {}
                                        tier = node.get('delta_tier')
                    
                                        if tier == 'node-LatLon':
                                            lon = node.get('delta_lon')
                                            lat = node.get('delta_lat')
                                            if lon is None or lon < -179.9999999 or lon > 180:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-LatLon lon invalid! Set to 0.')
                                                lon = 1800000001
                                            else:
                                                lon = int(lon * 10 ** 7)
                                            if lat is None or lat < -90 or lat > 90:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-LatLon lat invalid! Set to 0.')
                                                lat = 900000001
                                            else:
                                                lat = int(lat * 10 ** 7)
                                            node_out['delta'] = ('node-LatLon', {'lon': lon, 'lat': lat})
                                        elif tier == 'node-XY1':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -512 or x > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY1 x should be in range [-512, 511]! Set to 0.')
                                                x = -512
                                            if not isinstance(y, int) or y < -512 or y > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY1 y should be in range [-512, 511]! Set to 0.')
                                                y = -512
                                            node_out['delta'] = ('node-XY1', {'x': x, 'y': y})
                                        elif tier == 'node-XY2':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -1024 or x > 1023:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY2 x should be in range [-1024, 1023]! Set to 0.')
                                                x = -1024
                                            if not isinstance(y, int) or y < -1024 or y > 1023:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY2 y should be in range [-1024, 1023]! Set to 0.')
                                                y = -1024
                                            node_out['delta'] = ('node-XY2', {'x': x, 'y': y})
                                        elif tier == 'node-XY3':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -2048 or x > 2047:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY3 x should be in range [-2048, 2047]! Set to 0.')
                                                x = -2048
                                            if not isinstance(y, int) or y < -2048 or y > 2047:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY3 y should be in range [-2048, 2047]! Set to 0.')
                                                y = -2048
                                            node_out['delta'] = ('node-XY3', {'x': x, 'y': y})
                                        elif tier == 'node-XY4':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -4096 or x > 4095:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY4 x should be in range [-4096, 4095]! Set to 0.')
                                                x = -4096
                                            if not isinstance(y, int) or y < -4096 or y > 4095:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY4 y should be in range [-4096, 4095]! Set to 0.')
                                                y = -4096
                                            node_out['delta'] = ('node-XY4', {'x': x, 'y': y})
                                        elif tier == 'node-XY5':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -8192 or x > 8191:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY5 x should be in range [-8192, 8191]! Set to 0.')
                                                x = -8192
                                            if not isinstance(y, int) or y < -8192 or y > 8191:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY5 y should be in range [-8192, 8191]! Set to 0.')
                                                y = -8192
                                            node_out['delta'] = ('node-XY5', {'x': x, 'y': y})
                                        elif tier == 'node-XY6':
                                            x = node.get('delta_x')
                                            y = node.get('delta_y')
                                            if not isinstance(x, int) or x < -32768 or x > 32767:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY6 x should be in range [-32768, 32767]! Set to 0.')
                                                x = -32768
                                            if not isinstance(y, int) or y < -32768 or y > 32767:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': node-XY6 y should be in range [-32768, 32767]! Set to 0.')
                                                y = -32768
                                            node_out['delta'] = ('node-XY6', {'x': x, 'y': y})
                                        else:
                                            print('Frame', i, ', region', idx, ', node', node_idx, ': delta_tier invalid! Defaulting to node-XY1 (0,0).')
                                            node_out['delta'] = ('node-XY1', {'x': 0, 'y': 0})
                    
                                        # attributes
                                        attrs = {}
                                        localNode = node.get('attr_localNode')
                                        if localNode is not None:
                                            if len(localNode) < 1 or len(localNode) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_localNode should have 1-8 entries! Omit it.')
                                            else:
                                                valid_list = [a for a in localNode if a in ['reserved', 'stopLine', 'roundedCapStyleA', 'roundedCapStyleB', 'mergePoint', 'divergePoint', 'downstreamStopLine', 'downstreamStartNode', 'closedToTraffic', 'safeIsland', 'curbPresentAtStepOff', 'hydrantPresent']]
                                                if valid_list:
                                                    attrs['localNode'] = valid_list
                                        disabled = node.get('attr_disabled')
                                        if disabled is not None:
                                            if len(disabled) < 1 or len(disabled) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_disabled should have 1-8 entries! Omit it.')
                                            else:
                                                valid_list = [a for a in disabled if a in ['reserved', 'doNotBlock', 'whiteLine', 'mergingLaneLeft', 'mergingLaneRight', 'curbOnLeft', 'curbOnRight', 'loadingzoneOnLeft', 'loadingzoneOnRight', 'turnOutPointOnLeft', 'turnOutPointOnRight', 'adjacentParkingOnLeft', 'adjacentParkingOnRight', 'adjacentBikeLaneOnLeft', 'adjacentBikeLaneOnRight', 'sharedBikeLane', 'bikeBoxInFront', 'transitStopOnLeft', 'transitStopOnRight', 'transitStopInLane', 'sharedWithTrackedVehicle', 'safeIsland', 'lowCurbsPresent', 'rumbleStripPresent', 'audibleSignalingPresent', 'adaptiveTimingPresent', 'rfSignalRequestPresent', 'partialCurbIntrusion', 'taperToLeft', 'taperToRight', 'taperToCenterLine', 'parallelParking', 'headInParking', 'freeParking', 'timeRestrictionsOnParking', 'costToPark', 'midBlockCurbPresent', 'unEvenPavementPresent']]
                                                if valid_list:
                                                    attrs['disabled'] = valid_list
                                        enabled = node.get('attr_enabled')
                                        if enabled is not None:
                                            if len(enabled) < 1 or len(enabled) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_enabled should have 1-8 entries! Omit it.')
                                            else:
                                                valid_list = [a for a in enabled if a in ['reserved', 'doNotBlock', 'whiteLine', 'mergingLaneLeft', 'mergingLaneRight', 'curbOnLeft', 'curbOnRight', 'loadingzoneOnLeft', 'loadingzoneOnRight', 'turnOutPointOnLeft', 'turnOutPointOnRight', 'adjacentParkingOnLeft', 'adjacentParkingOnRight', 'adjacentBikeLaneOnLeft', 'adjacentBikeLaneOnRight', 'sharedBikeLane', 'bikeBoxInFront', 'transitStopOnLeft', 'transitStopOnRight', 'transitStopInLane', 'sharedWithTrackedVehicle', 'safeIsland', 'lowCurbsPresent', 'rumbleStripPresent', 'audibleSignalingPresent', 'adaptiveTimingPresent', 'rfSignalRequestPresent', 'partialCurbIntrusion', 'taperToLeft', 'taperToRight', 'taperToCenterLine', 'parallelParking', 'headInParking', 'freeParking', 'timeRestrictionsOnParking', 'costToPark', 'midBlockCurbPresent', 'unEvenPavementPresent']]
                                                if valid_list:
                                                    attrs['enabled'] = valid_list
                                        attr_data = node.get('attr_data')
                                        if attr_data is not None:
                                            if len(attr_data) < 1 or len(attr_data) > 8:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_data should have 1-8 entries! Omit it.')
                                            else:
                                                data_list = []
                                                for entry in attr_data:
                                                    t = entry.get('type')
                                                    v = entry.get('value')
                                                    if t == 'pathEndPointAngle':
                                                        if not isinstance(v, int) or v < -150 or v > 150:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': pathEndPointAngle should be in range [-150, 150]! Skip entry.')
                                                            continue
                                                        data_list.append(('pathEndPointAngle', v))
                                                    elif t == 'laneCrownPointCenter':
                                                        if not isinstance(v, int) or v < -128 or v > 127:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointCenter should be in range [-128, 127]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneCrownPointCenter', v))
                                                    elif t == 'laneCrownPointLeft':
                                                        if not isinstance(v, int) or v < -128 or v > 127:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointLeft should be in range [-128, 127]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneCrownPointLeft', v))
                                                    elif t == 'laneCrownPointRight':
                                                        if not isinstance(v, int) or v < -128 or v > 127:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneCrownPointRight should be in range [-128, 127]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneCrownPointRight', v))
                                                    elif t == 'laneAngle':
                                                        if not isinstance(v, int) or v < -180 or v > 180:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': laneAngle should be in range [-180, 180]! Skip entry.')
                                                            continue
                                                        data_list.append(('laneAngle', v))
                                                    elif t == 'speedLimits':
                                                        if not isinstance(v, list) or len(v) < 1 or len(v) > 9:
                                                            print('Frame', i, ', region', idx, ', node', node_idx, ': speedLimits should be a list of 1-9 entries! Skip entry.')
                                                            continue
                                                        limits = []
                                                        for lim in v:
                                                            lim_type = lim.get('type')
                                                            lim_speed = lim.get('speed')
                                                            if lim_type not in ['unknown', 'maxSpeedInSchoolZone', 'maxSpeedInSchoolZoneWhenChildrenArePresent', 'maxSpeedInConstructionZone', 'vehicleMinSpeed', 'vehicleMaxSpeed', 'vehicleNightMaxSpeed', 'truckMinSpeed', 'truckMaxSpeed', 'truckNightMaxSpeed', 'vehiclesWithTrailersMinSpeed', 'vehiclesWithTrailersMaxSpeed', 'vehiclesWithTrailersNightMaxSpeed']:
                                                                print('Frame', i, ', region', idx, ', node', node_idx, ': speed limit type invalid! Skip this limit.')
                                                                continue
                                                            if not isinstance(lim_speed, (int, float)) or lim_speed < 0 or lim_speed > 163.82:
                                                                print('Frame', i, ', region', idx, ', node', node_idx, ': speed limit speed should be in range [0, 163.82] m/s! Skip this limit.')
                                                                continue
                                                            limits.append({'type': lim_type, 'speed': int(lim_speed / 0.02)})
                                                        if limits:
                                                            data_list.append(('speedLimits', limits))
                                                    else:
                                                        print('Frame', i, ', region', idx, ', node', node_idx, ': attr_data type', t, 'not recognized! Skip entry.')
                                                if data_list:
                                                    node_out['data'] = data_list
                                        dWidth = node.get('attr_dWidth')
                                        if dWidth is not None:
                                            if not isinstance(dWidth, int) or dWidth == 0 or dWidth < -512 or dWidth > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_dWidth should be a nonzero integer in range [-512, 511]! Omit it.')
                                            else:
                                                attrs['dWidth'] = dWidth
                                        dElevation = node.get('attr_dElevation')
                                        if dElevation is not None:
                                            if not isinstance(dElevation, int) or dElevation == 0 or dElevation < -512 or dElevation > 511:
                                                print('Frame', i, ', region', idx, ', node', node_idx, ': attr_dElevation should be a nonzero integer in range [-512, 511]! Omit it.')
                                            else:
                                                attrs['dElevation'] = dElevation
                                        if attrs:
                                            node_out['attributes'] = attrs
                    
                                        sp_node_list.append(node_out)
                    
                                    shapePointSet['nodeList'] = ('nodes', sp_node_list)
                    
                            elif sp_nodelistxy_type == 'computed':
                                sp_raw_computed = dataFrames_region_oldRegion_shapePointSet_computed[i][idx] if dataFrames_region_oldRegion_shapePointSet_computed and len(dataFrames_region_oldRegion_shapePointSet_computed) > i and len(dataFrames_region_oldRegion_shapePointSet_computed[i]) > idx else None
                    
                                if sp_raw_computed is None:
                                    print('Frame', i, ', region', idx, ': shapePointSet computed lane data missing! nodeList cannot be encoded.')
                                else:
                                    computed_lane = {}
                                    ref_id = sp_raw_computed.get('referenceLaneId')
                                    if not isinstance(ref_id, int) or ref_id < 0 or ref_id > 255:
                                        print('Frame', i, ', region', idx, ': referenceLaneId should be an integer in range [0, 255]! Set to 0.')
                                        computed_lane['referenceLaneId'] = 0
                                    else:
                                        computed_lane['referenceLaneId'] = ref_id
                    
                                    offsetX_size = sp_raw_computed.get('offsetX_size')
                                    offsetX_value = sp_raw_computed.get('offsetX_value')
                                    if offsetX_size == 'small':
                                        if not isinstance(offsetX_value, int) or offsetX_value < -2047 or offsetX_value > 2047:
                                            print('Frame', i, ', region', idx, ': offsetXaxis small should be in range [-2047, 2047]! Set to 0.')
                                            offsetX_value = 0
                                        computed_lane['offsetXaxis'] = ('small', offsetX_value)
                                    elif offsetX_size == 'large':
                                        if not isinstance(offsetX_value, int) or offsetX_value < -32767 or offsetX_value > 32767:
                                            print('Frame', i, ', region', idx, ': offsetXaxis large should be in range [-32767, 32767]! Set to 0.')
                                            offsetX_value = 0
                                        computed_lane['offsetXaxis'] = ('large', offsetX_value)
                                    else:
                                        print('Frame', i, ', region', idx, ': offsetXaxis is mandatory (small/large)! Set to small 0.')
                                        computed_lane['offsetXaxis'] = ('small', 0)
                    
                                    offsetY_size = sp_raw_computed.get('offsetY_size')
                                    offsetY_value = sp_raw_computed.get('offsetY_value')
                                    if offsetY_size == 'small':
                                        if not isinstance(offsetY_value, int) or offsetY_value < -2047 or offsetY_value > 2047:
                                            print('Frame', i, ', region', idx, ': offsetYaxis small should be in range [-2047, 2047]! Set to 0.')
                                            offsetY_value = 0
                                        computed_lane['offsetYaxis'] = ('small', offsetY_value)
                                    elif offsetY_size == 'large':
                                        if not isinstance(offsetY_value, int) or offsetY_value < -32767 or offsetY_value > 32767:
                                            print('Frame', i, ', region', idx, ': offsetYaxis large should be in range [-32767, 32767]! Set to 0.')
                                            offsetY_value = 0
                                        computed_lane['offsetYaxis'] = ('large', offsetY_value)
                                    else:
                                        print('Frame', i, ', region', idx, ': offsetYaxis is mandatory (small/large)! Set to small 0.')
                                        computed_lane['offsetYaxis'] = ('small', 0)
                    
                                    rotate = sp_raw_computed.get('rotateXY')
                                    if rotate is not None:
                                        if rotate < 0 or rotate > 359.9875:
                                            print('Frame', i, ', region', idx, ': rotateXY should be in range [0, 359.9875] deg! Omit it.')
                                        else:
                                            computed_lane['rotateXY'] = int(rotate / 0.0125)
                    
                                    scaleX = sp_raw_computed.get('scaleXaxis')
                                    if scaleX is not None:
                                        if not isinstance(scaleX, int) or scaleX < -1999 or scaleX > 2047:
                                            print('Frame', i, ', region', idx, ': scaleXaxis should be an integer in range [-1999, 2047]! Omit it.')
                                        else:
                                            computed_lane['scaleXaxis'] = scaleX
                    
                                    scaleY = sp_raw_computed.get('scaleYaxis')
                                    if scaleY is not None:
                                        if not isinstance(scaleY, int) or scaleY < -1999 or scaleY > 2047:
                                            print('Frame', i, ', region', idx, ': scaleYaxis should be an integer in range [-1999, 2047]! Omit it.')
                                        else:
                                            computed_lane['scaleYaxis'] = scaleY
                    
                                    shapePointSet['nodeList'] = ('computed', computed_lane)
                            else:
                                print('Frame', i, ', region', idx, ': shapePointSet nodeList requires nodelistxy_type to be nodes or computed! nodeList cannot be encoded.')
                    
                            oldRegion['area'] = ('shapePointSet', shapePointSet)
                    
                        elif area_type == 'circle':
                            circle = {}
                            circle['center'] = {}
                    
                            c_lat = dataFrames_region_oldRegion_circle_lat[i][idx] if dataFrames_region_oldRegion_circle_lat and len(dataFrames_region_oldRegion_circle_lat) > i and len(dataFrames_region_oldRegion_circle_lat[i]) > idx else None
                            if c_lat is None or c_lat < -90 or c_lat > 90:
                                print('Frame', i, ', region', idx, ': circle center lat is mandatory and should be in range [-90, 90]! Set to 90.0000001.')
                                circle['center']['lat'] = 900000001
                            else:
                                circle['center']['lat'] = int(c_lat * 10 ** 7)
                            
                            c_long = dataFrames_region_oldRegion_circle_long[i][idx] if dataFrames_region_oldRegion_circle_long and len(dataFrames_region_oldRegion_circle_long) > i and len(dataFrames_region_oldRegion_circle_long[i]) > idx else None
                            if c_long is None or c_long < -179.9999999 or c_long > 180:
                                print('Frame', i, ', region', idx, ': circle center long is mandatory and should be in range [-179.9999999, 180]! Set to 180.0000001.')
                                circle['center']['long'] = 1800000001
                            else:
                                circle['center']['long'] = int(c_long * 10 ** 7)

                            c_elev = dataFrames_region_oldRegion_circle_elevation[i][idx] if dataFrames_region_oldRegion_circle_elevation and len(dataFrames_region_oldRegion_circle_elevation) > i and len(dataFrames_region_oldRegion_circle_elevation[i]) > idx else None
                            if c_elev is not None:
                                if c_elev < -409.5 or c_elev > 6143.9:
                                    print('Frame', i, ', region', idx, ': circle center elevation out of range! Omit it.')
                                else:
                                    circle['center']['elevation'] = int(c_elev * 10)

                            c_radius = dataFrames_region_oldRegion_circle_radius[i][idx] if dataFrames_region_oldRegion_circle_radius and len(dataFrames_region_oldRegion_circle_radius) > i and len(dataFrames_region_oldRegion_circle_radius[i]) > idx else None
                            if c_radius is None or not isinstance(c_radius, int) or c_radius < 0 or c_radius > 4095:
                                print('Frame', i, ', region', idx, ': circle radius is mandatory and should be an integer in range [0, 4095]! Set to 0.')
                                circle['radius'] = 0
                            else:
                                circle['radius'] = c_radius

                            c_units = dataFrames_region_oldRegion_circle_units[i][idx] if dataFrames_region_oldRegion_circle_units and len(dataFrames_region_oldRegion_circle_units) > i and len(dataFrames_region_oldRegion_circle_units[i]) > idx else None
                            if c_units is None or c_units not in ['centimeter', 'cm2-5', 'decimeter', 'meter', 'kilometer', 'foot', 'yard', 'mile']:
                                print('Frame', i, ', region', idx, ': circle units is mandatory, one of centimeter, cm2-5, decimeter, meter, kilometer, foot, yard, mile! Set to meter.')
                                circle['units'] = 'meter'
                            else:
                                circle['units'] = c_units
                    
                            oldRegion['area'] = ('circle', circle)
                    
                        elif area_type == 'regionPointSet':
                            regionPointSet = {}
                    
                            rp_lat = dataFrames_region_oldRegion_regionPointSet_anchor_lat[i][idx] if dataFrames_region_oldRegion_regionPointSet_anchor_lat and len(dataFrames_region_oldRegion_regionPointSet_anchor_lat) > i and len(dataFrames_region_oldRegion_regionPointSet_anchor_lat[i]) > idx else None
                            rp_long = dataFrames_region_oldRegion_regionPointSet_anchor_long[i][idx] if dataFrames_region_oldRegion_regionPointSet_anchor_long and len(dataFrames_region_oldRegion_regionPointSet_anchor_long) > i and len(dataFrames_region_oldRegion_regionPointSet_anchor_long[i]) > idx else None
                            rp_elev = dataFrames_region_oldRegion_regionPointSet_anchor_elevation[i][idx] if dataFrames_region_oldRegion_regionPointSet_anchor_elevation and len(dataFrames_region_oldRegion_regionPointSet_anchor_elevation) > i and len(dataFrames_region_oldRegion_regionPointSet_anchor_elevation[i]) > idx else None
                            if rp_lat is not None or rp_long is not None:
                                anchor = {}
                                if rp_lat is None or rp_lat < -90 or rp_lat > 90:
                                    print('Frame', i, ', region', idx, ': regionPointSet anchor lat invalid! Set to 90.0000001.')
                                    anchor['lat'] = 900000001
                                else:
                                    anchor['lat'] = int(rp_lat * 10 ** 7)
                                if rp_long is None or rp_long < -179.9999999 or rp_long > 180:
                                    print('Frame', i, ', region', idx, ': regionPointSet anchor long invalid! Set to 180.0000001.')
                                    anchor['long'] = 1800000001
                                else:
                                    anchor['long'] = int(rp_long * 10 ** 7)
                                if rp_elev is not None:
                                    if rp_elev < -409.5 or rp_elev > 6143.9:
                                        print('Frame', i, ', region', idx, ': regionPointSet anchor elevation out of range! Omit it.')
                                    else:
                                        anchor['elevation'] = int(rp_elev * 10)
                                regionPointSet['anchor'] = anchor
                    
                            rp_scale = dataFrames_region_oldRegion_regionPointSet_scale[i][idx] if dataFrames_region_oldRegion_regionPointSet_scale and len(dataFrames_region_oldRegion_regionPointSet_scale) > i and len(dataFrames_region_oldRegion_regionPointSet_scale[i]) > idx else None
                            if rp_scale is not None:
                                if not isinstance(rp_scale, int) or rp_scale < 0 or rp_scale > 15:
                                    print('Frame', i, ', region', idx, ': regionPointSet scale should be an integer in range [0, 15]! Omit it.')
                                else:
                                    regionPointSet['scale'] = rp_scale
                    
                            rp_nodeList = dataFrames_region_oldRegion_regionPointSet_nodeList[i][idx] if dataFrames_region_oldRegion_regionPointSet_nodeList and len(dataFrames_region_oldRegion_regionPointSet_nodeList) > i and len(dataFrames_region_oldRegion_regionPointSet_nodeList[i]) > idx else None
                            if rp_nodeList is None or len(rp_nodeList) < 1 or len(rp_nodeList) > 64:
                                print('Frame', i, ', region', idx, ': regionPointSet nodeList is mandatory and should contain 1 to 64 entries! nodeList cannot be encoded.')
                            else:
                                offsets_list = []
                                for off_idx, off in enumerate(rp_nodeList):
                                    offset_out = {}
                                    xOffset = off.get('xOffset')
                                    yOffset = off.get('yOffset')
                                    zOffset = off.get('zOffset')
                    
                                    if not isinstance(xOffset, int) or xOffset < -32768 or xOffset > 32767:
                                        print('Frame', i, ', region', idx, ', offset', off_idx, ': xOffset is mandatory and should be an integer in range [-32768, 32767]! Set to -32768.')
                                        offset_out['xOffset'] = -32768
                                    else:
                                        offset_out['xOffset'] = xOffset
                    
                                    if not isinstance(yOffset, int) or yOffset < -32768 or yOffset > 32767:
                                        print('Frame', i, ', region', idx, ', offset', off_idx, ': yOffset is mandatory and should be an integer in range [-32768, 32767]! Set to -32768.')
                                        offset_out['yOffset'] = -32768
                                    else:
                                        offset_out['yOffset'] = yOffset
                    
                                    if zOffset is not None:
                                        if not isinstance(zOffset, int) or zOffset < -32768 or zOffset > 32767:
                                            print('Frame', i, ', region', idx, ', offset', off_idx, ': zOffset should be an integer in range [-32768, 32767]! Omit it.')
                                        else:
                                            offset_out['zOffset'] = zOffset
                    
                                    offsets_list.append(offset_out)
                    
                                regionPointSet['nodeList'] = offsets_list
                    
                            oldRegion['area'] = ('regionPointSet', regionPointSet)
                        else:
                            print('Frame', i, ', region', idx, ': oldRegion area is mandatory, one of shapePointSet, circle, regionPointSet! oldRegion cannot be fully encoded.')
                        if oldRegion:
                            region['description'] = ('oldRegion', oldRegion)
                    else:
                        print('dataFrames_region_description should be one of path, geometry, or oldRegion! But', dataFrames_region_description, 'is provided. Omit it')
                    df['regions'].append(region)

            df['doNotUse3'] = 0
            df['doNotUse4'] = 0
            
            # content 
            content_type = dataFrames_content_type[i] if dataFrames_content_type and len(dataFrames_content_type) > i else None
            content_items = dataFrames_content_items[i] if dataFrames_content_items and len(dataFrames_content_items) > i else None
            
            if content_type == 'advisory':
                if content_items is None or len(content_items) < 1 or len(content_items) > 100:
                    print('Frame', i, ': content advisory items should contain 1 to 100 entries! Set to a single itis 0.')
                    df['content'] = ('advisory', [{'item' :('itis', 0)}])
                else:
                    item_list = []
                    for item_idx, entry in enumerate(content_items):
                        t = entry.get('type')
                        v = entry.get('value')
                        if t == 'itis':
                            if not isinstance(v, int) or v < 0 or v > 65535:
                                print('Frame', i, ', item', item_idx, ': advisory itis should be an integer in range [0, 65535]! Skip entry.')
                                continue
                            item_list.append({'item' : ('itis', v)})
                        elif t == 'text':
                            if not isinstance(v, str) or len(v) < 1 or len(v) > 500:
                                print('Frame', i, ', item', item_idx, ': advisory text should be a string 1-500 characters! Skip entry.')
                                continue
                            item_list.append({'item' : ('text', v)})
                        else:
                            print('Frame', i, ', item', item_idx, ': advisory item type should be itis or text! Skip entry.')
                    if not item_list:
                        print('Frame', i, ': no valid advisory items! Set to a single itis 0.')
                        item_list = [('itis', 0)]
                    df['content'] = ('advisory', item_list)
            
            elif content_type in ('workZone', 'genericSign', 'speedLimit', 'exitService'):
                if content_items is None or len(content_items) < 1 or len(content_items) > 16:
                    print('Frame', i, ':', content_type, 'items should contain 1 to 16 entries! Set to a single itis 0.')
                    df['content'] = (content_type, [{'item' : ('itis', 0)}])
                else:
                    item_list = []
                    for item_idx, entry in enumerate(content_items):
                        t = entry.get('type')
                        v = entry.get('value')
                        if t == 'itis':
                            if not isinstance(v, int) or v < 0 or v > 65535:
                                print('Frame', i, ', item', item_idx, ':', content_type, 'itis should be an integer in range [0, 65535]! Skip entry.')
                                continue
                            item_list.append({'item' : ('itis', v)})
                        elif t == 'text':
                            if not isinstance(v, str) or len(v) < 1 or len(v) > 16:
                                print('Frame', i, ', item', item_idx, ':', content_type, 'text should be a string 1-16 characters (ITIStextPhrase)! Skip entry.')
                                continue
                            item_list.append({'item' : ('text', v)})
                        else:
                            print('Frame', i, ', item', item_idx, ':', content_type, 'item type should be itis or text! Skip entry.')
                    if not item_list:
                        print('Frame', i, ': no valid', content_type, 'items! Set to a single itis 0.')
                        item_list = [('itis', 0)]
                    df['content'] = (content_type, item_list)
            
            else:
                print('Frame', i, ': content_type is mandatory, one of advisory, workZone, genericSign, speedLimit, exitService! But', content_type, 'is provided. Set to advisory [itis 0].')
                df['content'] = ('advisory', [{'item' : ('itis', 0)}])
            
            url = dataFrames_url[i] if dataFrames_url and len(dataFrames_url) > i else None
            if url is not None:
                if not isinstance(url, str) or len(url) < 1 or len(url) > 15:
                    print('Frame', i, ': url should be a string 1-15 characters! But', url, 'is provided. Omit it.')
                else:
                    df['url'] = url

            # FrictionInformation content is not provided - skip for now 
            contentNew_type = dataFrames_contentNew_type[i] if dataFrames_contentNew_type and len(dataFrames_contentNew_type) > i else None
            if contentNew_type == 'frictionInfo':
                friction_raw = dataFrames_contentNew_frictionInfo[i] if dataFrames_contentNew_frictionInfo and len(dataFrames_contentNew_frictionInfo) > i else None
                print('Frame', i, ': contentNew frictionInfo requested, but FrictionInformation structure is not yet implemented (definition not provided). Omit contentNew.')
            elif contentNew_type is not None:
                print('Frame', i, ': contentNew_type', contentNew_type, 'not recognized (only frictionInfo currently defined)! Omit contentNew.')

            tim['dataFrames'].append(df)

    # add header to TIM
    header_tim = {
        'messageId': 31,
        'value': ('TravelerInformation', tim)
    }

    # enode TIM to hex
    header_tim_msg = v2xlib.MessageFrame.MessageFrame
    header_tim_msg.set_val(header_tim)
    hex_tim = hexlify(header_tim_msg.to_uper())
    return hex_tim.decode('utf-8')