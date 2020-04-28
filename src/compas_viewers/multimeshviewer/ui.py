from compas_traits import *

UI = {
    'menubar': [
        {
            'type': 'menu',
            'text': 'View',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Mesh',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Tools',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'OpenGL',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Window',
            'items': []
        },
        {
            'type': 'menu',
            'text': 'Help',
            'items': []
        }
    ],
    'toolbar': [
        # {'text': 'Zoom Extents', 'action': 'zoom_extents', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-to-extents-50.png')},
        # {'text': 'Zoom In', 'action': 'zoom_in', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-in-50.png')},
        # {'text': 'Zoom Out', 'action': 'zoom_out', 'image': os.path.join(here, '../icons/zoom/icons8-zoom-out-50.png')},
        {'text': 'View:Perspective', 'action': 'set_view', 'args': [1], 'image': None},
        {'text': 'View:Front', 'action': 'set_view', 'args': [2], 'image': None},
        {'text': 'View:Left', 'action': 'set_view', 'args': [3], 'image': None},
        {'text': 'View:Top', 'action': 'set_view', 'args': [4], 'image': None},
        {'text': 'View:Capture', 'action': 'capture_image', 'args': [], 'image': None},
    ],

    'sidebar': [
        Group([
            String(
                'Search Command...',
                Attributes={'edit': 'select_command'}
            )
        ]),

        Group([
            Bool(True, Name='vertices', Attributes={'action': 'toggle_vertices'}),
            Bool(True, Name='edges', Attributes={'action': 'toggle_edges'}),
            Bool(True, Name='faces', Attributes={'action': 'toggle_faces'})
        ]),

        # # Traits.group([

        # #     Traits.color(
        # #         '#222222',
        # #         Attributes={
        # #             'text': 'color vertices',
        # #             'action': 'change_vertices_color',
        # #             'size': (16, 16)
        # #         }
        # #     ),

        # #     Traits.color(
        # #         '#666666',
        # #         Attributes={
        # #             'text': 'color edges',
        # #             'action': 'change_edges_color',
        # #             'size': (16, 16)
        # #         }
        # #     )

        # # ]),


        Group([

            Float(
                1,
                Name='size_vertices',
                Min=1,
                Max=100,
                Step=1,
                Attributes={
                    'scale' : 0.1,
                    'text': 'size vertices',
                    'slide': 'slide_size_vertices',
                    'edit': 'edit_size_vertices'
                }
            ),

            Float(
                1,
                Name='width_edges',
                Min=1,
                Max=100,
                Step=1,
                Attributes={
                    'scale' : 0.1,
                    'text': 'width edges',
                    'slide': 'slide_width_edges',
                    'edit': 'edit_width_edges'
                }
            ),
        ]),


        Group([
            Int(
                35,
                Name='azimuth',
                Min=-180,
                Max=180,
                Attributes={
                    'slide': 'slide_azimuth',
                    'edit': 'edit_azimuth'
                }
            ),

            Int(
                -65,
                Name='elevation',
                Min=-180,
                Max=180,
                Attributes={
                    'slide': 'slide_elevation',
                    'edit': 'edit_elevation'
                }
            ),

            Int(
                25,
                Name='distance',
                Min=0,
                Max=100,
                Attributes={
                    'slide': 'slide_distance',
                    'edit': 'edit_distance'
                }
            ),

            Int(
                35,
                Name='fov',
                Min=10,
                Max=170,
                Attributes={
                    'slide': 'slide_fov',
                    'edit': 'edit_fov'
                }
            )
        ]),

        Empty()
    ]
}
