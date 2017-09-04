# ------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
# Copyright (C) 2017 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------


def linear(colors):
    top = float(len(colors) - 1)
    return [
        (float(i) / top, color)
        for i, color in enumerate(colors)
    ]


BASE_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
    "brown": (165, 42, 42)
}

# some color scales require a specific offsite color to not interfere with the
# colors and accidentially produce transparent pixels
OFFSITE_COLORS = {
    "blackwhite": (255, 0, 0),
    "diverging_2": (255, 0, 0),
    "hot": (0, 0, 255),
    "bone": (255, 0, 0),
    "copper": (255, 0, 0),
    "greys": (255, 0, 0),
    "blackbody": (255, 0, 0),
    "electric": (255, 0, 0),
}

COLOR_SCALES = {
    "blackwhite": linear([
        (0, 0, 0),
        (255, 255, 255),
    ]),

    "coolwarm": linear([
        (255, 0, 0),
        (255, 255, 255),
        (0, 0, 255),
    ]),

    "rainbow": linear([
        (150, 0, 90),
        (0, 0, 200),
        (0, 25, 255),
        (0, 152, 255),
        (44, 255, 150),
        (151, 255, 0),
        (255, 234, 0),
        (255, 111, 0),
        (255, 0, 0),
    ]),

    "jet": linear([
        (0, 0, 144),
        (0, 15, 255),
        (0, 144, 255),
        (15, 255, 238),
        (144, 255, 112),
        (255, 238, 0),
        (255, 112, 0),
        (238, 0, 0),
        (127, 0, 0),
    ]),

    "diverging_2": [
        (0.0, (0, 0, 0)),
        (0.000000000001, (3, 10, 255)),
        (0.1, (32, 74, 255)),
        (0.2, (60, 138, 255)),
        (0.3333, (119, 196, 255)),
        (0.4666, (240, 255, 255)),
        (0.5333, (240, 255, 255)),
        (0.6666, (242, 255, 127)),
        (0.8, (255, 255, 0)),
        (0.9, (255, 131, 30)),
        (0.999999999999, (255, 8, 61)),
        (1.0, (255, 0, 255)),
    ],

    "diverging_1": linear([
        (64, 0, 64),
        (59, 0, 77),
        (54, 0, 91),
        (50, 0, 104),
        (45, 0, 118),
        (41, 0, 132),
        (36, 0, 145),
        (32, 0, 159),
        (27, 0, 173),
        (22, 0, 186),
        (18, 0, 200),
        (13, 0, 214),
        (9, 0, 227),
        (4, 0, 241),
        (0, 0, 255),
        (2, 23, 255),
        (4, 46, 255),
        (6, 69, 255),
        (9, 92, 255),
        (11, 115, 255),
        (13, 139, 255),
        (16, 162, 255),
        (18, 185, 255),
        (20, 208, 255),
        (23, 231, 255),
        (25, 255, 255),
        (63, 255, 255),
        (102, 255, 255),
        (140, 255, 255),
        (178, 255, 255),
        (216, 255, 255),
        (255, 255, 255),
        (255, 255, 212),
        (255, 255, 170),
        (255, 255, 127),
        (255, 255, 84),
        (255, 255, 42),
        (255, 255, 0),
        (255, 237, 0),
        (255, 221, 0),
        (255, 204, 0),
        (255, 186, 0),
        (255, 170, 0),
        (255, 153, 0),
        (255, 135, 0),
        (255, 119, 0),
        (255, 102, 0),
        (255, 84, 0),
        (255, 68, 0),
        (255, 51, 0),
        (255, 33, 0),
        (255, 17, 0),
        (255, 0, 0),
        (255, 0, 23),
        (255, 0, 46),
        (255, 0, 69),
        (255, 0, 92),
        (255, 0, 115),
        (255, 0, 139),
        (255, 0, 162),
        (255, 0, 185),
        (255, 0, 208),
        (255, 0, 231),
        (255, 0, 255),
    ]),

    "viridis": linear([
        (68, 1, 84),
        (68, 2, 86),
        (69, 4, 87),
        (69, 5, 89),
        (70, 7, 90),
        (70, 8, 92),
        (70, 10, 93),
        (70, 11, 94),
        (71, 13, 96),
        (71, 14, 97),
        (71, 16, 99),
        (71, 17, 100),
        (71, 19, 101),
        (72, 20, 103),
        (72, 22, 104),
        (72, 23, 105),
        (72, 24, 106),
        (72, 26, 108),
        (72, 27, 109),
        (72, 28, 110),
        (72, 29, 111),
        (72, 31, 112),
        (72, 32, 113),
        (72, 33, 115),
        (72, 35, 116),
        (72, 36, 117),
        (72, 37, 118),
        (72, 38, 119),
        (72, 40, 120),
        (72, 41, 121),
        (71, 42, 122),
        (71, 44, 122),
        (71, 45, 123),
        (71, 46, 124),
        (71, 47, 125),
        (70, 48, 126),
        (70, 50, 126),
        (70, 51, 127),
        (70, 52, 128),
        (69, 53, 129),
        (69, 55, 129),
        (69, 56, 130),
        (68, 57, 131),
        (68, 58, 131),
        (68, 59, 132),
        (67, 61, 132),
        (67, 62, 133),
        (66, 63, 133),
        (66, 64, 134),
        (66, 65, 134),
        (65, 66, 135),
        (65, 68, 135),
        (64, 69, 136),
        (64, 70, 136),
        (63, 71, 136),
        (63, 72, 137),
        (62, 73, 137),
        (62, 74, 137),
        (62, 76, 138),
        (61, 77, 138),
        (61, 78, 138),
        (60, 79, 138),
        (60, 80, 139),
        (59, 81, 139),
        (59, 82, 139),
        (58, 83, 139),
        (58, 84, 140),
        (57, 85, 140),
        (57, 86, 140),
        (56, 88, 140),
        (56, 89, 140),
        (55, 90, 140),
        (55, 91, 141),
        (54, 92, 141),
        (54, 93, 141),
        (53, 94, 141),
        (53, 95, 141),
        (52, 96, 141),
        (52, 97, 141),
        (51, 98, 141),
        (51, 99, 141),
        (50, 100, 142),
        (50, 101, 142),
        (49, 102, 142),
        (49, 103, 142),
        (49, 104, 142),
        (48, 105, 142),
        (48, 106, 142),
        (47, 107, 142),
        (47, 108, 142),
        (46, 109, 142),
        (46, 110, 142),
        (46, 111, 142),
        (45, 112, 142),
        (45, 113, 142),
        (44, 113, 142),
        (44, 114, 142),
        (44, 115, 142),
        (43, 116, 142),
        (43, 117, 142),
        (42, 118, 142),
        (42, 119, 142),
        (42, 120, 142),
        (41, 121, 142),
        (41, 122, 142),
        (41, 123, 142),
        (40, 124, 142),
        (40, 125, 142),
        (39, 126, 142),
        (39, 127, 142),
        (39, 128, 142),
        (38, 129, 142),
        (38, 130, 142),
        (38, 130, 142),
        (37, 131, 142),
        (37, 132, 142),
        (37, 133, 142),
        (36, 134, 142),
        (36, 135, 142),
        (35, 136, 142),
        (35, 137, 142),
        (35, 138, 141),
        (34, 139, 141),
        (34, 140, 141),
        (34, 141, 141),
        (33, 142, 141),
        (33, 143, 141),
        (33, 144, 141),
        (33, 145, 140),
        (32, 146, 140),
        (32, 146, 140),
        (32, 147, 140),
        (31, 148, 140),
        (31, 149, 139),
        (31, 150, 139),
        (31, 151, 139),
        (31, 152, 139),
        (31, 153, 138),
        (31, 154, 138),
        (30, 155, 138),
        (30, 156, 137),
        (30, 157, 137),
        (31, 158, 137),
        (31, 159, 136),
        (31, 160, 136),
        (31, 161, 136),
        (31, 161, 135),
        (31, 162, 135),
        (32, 163, 134),
        (32, 164, 134),
        (33, 165, 133),
        (33, 166, 133),
        (34, 167, 133),
        (34, 168, 132),
        (35, 169, 131),
        (36, 170, 131),
        (37, 171, 130),
        (37, 172, 130),
        (38, 173, 129),
        (39, 173, 129),
        (40, 174, 128),
        (41, 175, 127),
        (42, 176, 127),
        (44, 177, 126),
        (45, 178, 125),
        (46, 179, 124),
        (47, 180, 124),
        (49, 181, 123),
        (50, 182, 122),
        (52, 182, 121),
        (53, 183, 121),
        (55, 184, 120),
        (56, 185, 119),
        (58, 186, 118),
        (59, 187, 117),
        (61, 188, 116),
        (63, 188, 115),
        (64, 189, 114),
        (66, 190, 113),
        (68, 191, 112),
        (70, 192, 111),
        (72, 193, 110),
        (74, 193, 109),
        (76, 194, 108),
        (78, 195, 107),
        (80, 196, 106),
        (82, 197, 105),
        (84, 197, 104),
        (86, 198, 103),
        (88, 199, 101),
        (90, 200, 100),
        (92, 200, 99),
        (94, 201, 98),
        (96, 202, 96),
        (99, 203, 95),
        (101, 203, 94),
        (103, 204, 92),
        (105, 205, 91),
        (108, 205, 90),
        (110, 206, 88),
        (112, 207, 87),
        (115, 208, 86),
        (117, 208, 84),
        (119, 209, 83),
        (122, 209, 81),
        (124, 210, 80),
        (127, 211, 78),
        (129, 211, 77),
        (132, 212, 75),
        (134, 213, 73),
        (137, 213, 72),
        (139, 214, 70),
        (142, 214, 69),
        (144, 215, 67),
        (147, 215, 65),
        (149, 216, 64),
        (152, 216, 62),
        (155, 217, 60),
        (157, 217, 59),
        (160, 218, 57),
        (162, 218, 55),
        (165, 219, 54),
        (168, 219, 52),
        (170, 220, 50),
        (173, 220, 48),
        (176, 221, 47),
        (178, 221, 45),
        (181, 222, 43),
        (184, 222, 41),
        (186, 222, 40),
        (189, 223, 38),
        (192, 223, 37),
        (194, 223, 35),
        (197, 224, 33),
        (200, 224, 32),
        (202, 225, 31),
        (205, 225, 29),
        (208, 225, 28),
        (210, 226, 27),
        (213, 226, 26),
        (216, 226, 25),
        (218, 227, 25),
        (221, 227, 24),
        (223, 227, 24),
        (226, 228, 24),
        (229, 228, 25),
        (231, 228, 25),
        (234, 229, 26),
        (236, 229, 27),
        (239, 229, 28),
        (241, 229, 29),
        (244, 230, 30),
        (246, 230, 32),
        (248, 230, 33),
        (251, 231, 35),
        (253, 231, 37),
    ]),

    "inferno": linear([
        (0, 0, 4),
        (1, 0, 5),
        (1, 1, 6),
        (1, 1, 8),
        (2, 1, 10),
        (2, 2, 12),
        (2, 2, 14),
        (3, 2, 16),
        (4, 3, 18),
        (4, 3, 20),
        (5, 4, 23),
        (6, 4, 25),
        (7, 5, 27),
        (8, 5, 29),
        (9, 6, 31),
        (10, 7, 34),
        (11, 7, 36),
        (12, 8, 38),
        (13, 8, 41),
        (14, 9, 43),
        (16, 9, 45),
        (17, 10, 48),
        (18, 10, 50),
        (20, 11, 52),
        (21, 11, 55),
        (22, 11, 57),
        (24, 12, 60),
        (25, 12, 62),
        (27, 12, 65),
        (28, 12, 67),
        (30, 12, 69),
        (31, 12, 72),
        (33, 12, 74),
        (35, 12, 76),
        (36, 12, 79),
        (38, 12, 81),
        (40, 11, 83),
        (41, 11, 85),
        (43, 11, 87),
        (45, 11, 89),
        (47, 10, 91),
        (49, 10, 92),
        (50, 10, 94),
        (52, 10, 95),
        (54, 9, 97),
        (56, 9, 98),
        (57, 9, 99),
        (59, 9, 100),
        (61, 9, 101),
        (62, 9, 102),
        (64, 10, 103),
        (66, 10, 104),
        (68, 10, 104),
        (69, 10, 105),
        (71, 11, 106),
        (73, 11, 106),
        (74, 12, 107),
        (76, 12, 107),
        (77, 13, 108),
        (79, 13, 108),
        (81, 14, 108),
        (82, 14, 109),
        (84, 15, 109),
        (85, 15, 109),
        (87, 16, 110),
        (89, 16, 110),
        (90, 17, 110),
        (92, 18, 110),
        (93, 18, 110),
        (95, 19, 110),
        (97, 19, 110),
        (98, 20, 110),
        (100, 21, 110),
        (101, 21, 110),
        (103, 22, 110),
        (105, 22, 110),
        (106, 23, 110),
        (108, 24, 110),
        (109, 24, 110),
        (111, 25, 110),
        (113, 25, 110),
        (114, 26, 110),
        (116, 26, 110),
        (117, 27, 110),
        (119, 28, 109),
        (120, 28, 109),
        (122, 29, 109),
        (124, 29, 109),
        (125, 30, 109),
        (127, 30, 108),
        (128, 31, 108),
        (130, 32, 108),
        (132, 32, 107),
        (133, 33, 107),
        (135, 33, 107),
        (136, 34, 106),
        (138, 34, 106),
        (140, 35, 105),
        (141, 35, 105),
        (143, 36, 105),
        (144, 37, 104),
        (146, 37, 104),
        (147, 38, 103),
        (149, 38, 103),
        (151, 39, 102),
        (152, 39, 102),
        (154, 40, 101),
        (155, 41, 100),
        (157, 41, 100),
        (159, 42, 99),
        (160, 42, 99),
        (162, 43, 98),
        (163, 44, 97),
        (165, 44, 96),
        (166, 45, 96),
        (168, 46, 95),
        (169, 46, 94),
        (171, 47, 94),
        (173, 48, 93),
        (174, 48, 92),
        (176, 49, 91),
        (177, 50, 90),
        (179, 50, 90),
        (180, 51, 89),
        (182, 52, 88),
        (183, 53, 87),
        (185, 53, 86),
        (186, 54, 85),
        (188, 55, 84),
        (189, 56, 83),
        (191, 57, 82),
        (192, 58, 81),
        (193, 58, 80),
        (195, 59, 79),
        (196, 60, 78),
        (198, 61, 77),
        (199, 62, 76),
        (200, 63, 75),
        (202, 64, 74),
        (203, 65, 73),
        (204, 66, 72),
        (206, 67, 71),
        (207, 68, 70),
        (208, 69, 69),
        (210, 70, 68),
        (211, 71, 67),
        (212, 72, 66),
        (213, 74, 65),
        (215, 75, 63),
        (216, 76, 62),
        (217, 77, 61),
        (218, 78, 60),
        (219, 80, 59),
        (221, 81, 58),
        (222, 82, 56),
        (223, 83, 55),
        (224, 85, 54),
        (225, 86, 53),
        (226, 87, 52),
        (227, 89, 51),
        (228, 90, 49),
        (229, 92, 48),
        (230, 93, 47),
        (231, 94, 46),
        (232, 96, 45),
        (233, 97, 43),
        (234, 99, 42),
        (235, 100, 41),
        (235, 102, 40),
        (236, 103, 38),
        (237, 105, 37),
        (238, 106, 36),
        (239, 108, 35),
        (239, 110, 33),
        (240, 111, 32),
        (241, 113, 31),
        (241, 115, 29),
        (242, 116, 28),
        (243, 118, 27),
        (243, 120, 25),
        (244, 121, 24),
        (245, 123, 23),
        (245, 125, 21),
        (246, 126, 20),
        (246, 128, 19),
        (247, 130, 18),
        (247, 132, 16),
        (248, 133, 15),
        (248, 135, 14),
        (248, 137, 12),
        (249, 139, 11),
        (249, 140, 10),
        (249, 142, 9),
        (250, 144, 8),
        (250, 146, 7),
        (250, 148, 7),
        (251, 150, 6),
        (251, 151, 6),
        (251, 153, 6),
        (251, 155, 6),
        (251, 157, 7),
        (252, 159, 7),
        (252, 161, 8),
        (252, 163, 9),
        (252, 165, 10),
        (252, 166, 12),
        (252, 168, 13),
        (252, 170, 15),
        (252, 172, 17),
        (252, 174, 18),
        (252, 176, 20),
        (252, 178, 22),
        (252, 180, 24),
        (251, 182, 26),
        (251, 184, 29),
        (251, 186, 31),
        (251, 188, 33),
        (251, 190, 35),
        (250, 192, 38),
        (250, 194, 40),
        (250, 196, 42),
        (250, 198, 45),
        (249, 199, 47),
        (249, 201, 50),
        (249, 203, 53),
        (248, 205, 55),
        (248, 207, 58),
        (247, 209, 61),
        (247, 211, 64),
        (246, 213, 67),
        (246, 215, 70),
        (245, 217, 73),
        (245, 219, 76),
        (244, 221, 79),
        (244, 223, 83),
        (244, 225, 86),
        (243, 227, 90),
        (243, 229, 93),
        (242, 230, 97),
        (242, 232, 101),
        (242, 234, 105),
        (241, 236, 109),
        (241, 237, 113),
        (241, 239, 117),
        (241, 241, 121),
        (242, 242, 125),
        (242, 244, 130),
        (243, 245, 134),
        (243, 246, 138),
        (244, 248, 142),
        (245, 249, 146),
        (246, 250, 150),
        (248, 251, 154),
        (249, 252, 157),
        (250, 253, 161),
        (252, 255, 164),
    ]),

    "hsv": [
        (0.0, (255, 0, 0)),
        (0.169, (253, 255, 2)),
        (0.173, (247, 255, 2)),
        (0.337, (0, 252, 4)),
        (0.341, (0, 252, 10)),
        (0.506, (1, 249, 255)),
        (0.671, (2, 0, 253)),
        (0.675, (8, 0, 253)),
        (0.839, (255, 0, 251)),
        (0.843, (255, 0, 245)),
        (1.0, (255, 0, 6)),
    ],

    "hot": [
        (0.0, (0, 0, 0)),
        (0.3, (230, 0, 0)),
        (0.6, (255, 210, 0)),
        (1.0, (255, 255, 255)),
    ],

    "cool": [
        (0.0, (0, 255, 255)),
        (1.0, (255, 0, 255)),
    ],

    "spring": [
        (0.0, (255, 0, 255)),
        (1.0, (255, 255, 0)),
    ],

    "summer": [
        (0.0, (0, 128, 102)),
        (1.0, (255, 255, 102)),
    ],

    "autumn": [
        (0.0, (255, 0, 0)),
        (1.0, (255, 255, 0)),
    ],

    "winter": [
        (0.0, (0, 0, 255)),
        (1.0, (0, 255, 128)),
    ],

    "bone": [
        (0.0, (0, 0, 0)),
        (0.376, (84, 84, 116)),
        (0.753, (169, 200, 200)),
        (1.0, (255, 255, 255)),
    ],

    "copper": [
        (0.0, (0, 0, 0)),
        (0.804, (255, 160, 102)),
        (1.0, (255, 199, 127)),
    ],

    "greys": [
        (0.0, (0, 0, 0)),
        (1.0, (255, 255, 255)),
    ],


    "yignbu": [
        (0.0, (8, 29, 88)),
        (0.125, (37, 52, 148)),
        (0.25, (34, 94, 168)),
        (0.375, (29, 145, 192)),
        (0.5, (65, 182, 196)),
        (0.625, (127, 205, 187)),
        (0.75, (199, 233, 180)),
        (0.875, (237, 248, 217)),
        (1.0, (255, 255, 217)),
    ],

    "greens": [
        (0.0, (0, 68, 27)),
        (0.125, (0, 109, 44)),
        (0.25, (35, 139, 69)),
        (0.375, (65, 171, 93)),
        (0.5, (116, 196, 118)),
        (0.625, (161, 217, 155)),
        (0.75, (199, 233, 192)),
        (0.875, (229, 245, 224)),
        (1.0, (247, 252, 245)),
    ],

    "yiorrd": [
        (0.0, (128, 0, 38)),
        (0.125, (189, 0, 38)),
        (0.25, (227, 26, 28)),
        (0.375, (252, 78, 42)),
        (0.5, (253, 141, 60)),
        (0.625, (254, 178, 76)),
        (0.75, (254, 217, 118)),
        (0.875, (255, 237, 160)),
        (1.0, (255, 255, 204)),
    ],

    "bluered": [
        (0.0, (0, 0, 255)),
        (1.0, (255, 0, 0)),
    ],

    "rdbu": [
        (0.0, (5, 10, 172)),
        (0.35, (106, 137, 247)),
        (0.5, (190, 190, 190)),
        (0.6, (220, 170, 132)),
        (0.7, (230, 145, 90)),
        (1.0, (178, 10, 28)),
    ],

    "picnic": [
        (0.0, (0, 0, 255)),
        (0.1, (51, 153, 255)),
        (0.2, (102, 204, 255)),
        (0.3, (153, 204, 255)),
        (0.4, (204, 204, 255)),
        (0.5, (255, 255, 255)),
        (0.6, (255, 204, 255)),
        (0.7, (255, 153, 255)),
        (0.8, (255, 102, 204)),
        (0.9, (255, 102, 102)),
        (1.0, (255, 0, 0)),
    ],

    "portland": [
        (0.0, (12, 51, 131)),
        (0.25, (10, 136, 186)),
        (0.5, (242, 211, 56)),
        (0.75, (242, 143, 56)),
        (1.0, (217, 30, 30)),
    ],

    "blackbody": [
        (0.0, (0, 0, 0)),
        (0.2, (230, 0, 0)),
        (0.4, (230, 210, 0)),
        (0.7, (255, 255, 255)),
        (1.0, (160, 200, 255)),
    ],

    "earth": [
        (0.0, (0, 0, 130)),
        (0.1, (0, 180, 180)),
        (0.2, (40, 210, 40)),
        (0.4, (230, 230, 50)),
        (0.6, (120, 70, 20)),
        (1.0, (255, 255, 255)),
    ],

    "electric": [
        (0.0, (0, 0, 0)),
        (0.15, (30, 0, 100)),
        (0.4, (120, 0, 100)),
        (0.6, (160, 90, 0)),
        (0.8, (230, 200, 0)),
        (1.0, (255, 250, 220)),
    ],

    "magma": linear([
        (0, 0, 4),
        (1, 0, 5),
        (1, 1, 6),
        (1, 1, 8),
        (2, 1, 9),
        (2, 2, 11),
        (2, 2, 13),
        (3, 3, 15),
        (3, 3, 18),
        (4, 4, 20),
        (5, 4, 22),
        (6, 5, 24),
        (6, 5, 26),
        (7, 6, 28),
        (8, 7, 30),
        (9, 7, 32),
        (10, 8, 34),
        (11, 9, 36),
        (12, 9, 38),
        (13, 10, 41),
        (14, 11, 43),
        (16, 11, 45),
        (17, 12, 47),
        (18, 13, 49),
        (19, 13, 52),
        (20, 14, 54),
        (21, 14, 56),
        (22, 15, 59),
        (24, 15, 61),
        (25, 16, 63),
        (26, 16, 66),
        (28, 16, 68),
        (29, 17, 71),
        (30, 17, 73),
        (32, 17, 75),
        (33, 17, 78),
        (34, 17, 80),
        (36, 18, 83),
        (37, 18, 85),
        (39, 18, 88),
        (41, 17, 90),
        (42, 17, 92),
        (44, 17, 95),
        (45, 17, 97),
        (47, 17, 99),
        (49, 17, 101),
        (51, 16, 103),
        (52, 16, 105),
        (54, 16, 107),
        (56, 16, 108),
        (57, 15, 110),
        (59, 15, 112),
        (61, 15, 113),
        (63, 15, 114),
        (64, 15, 116),
        (66, 15, 117),
        (68, 15, 118),
        (69, 16, 119),
        (71, 16, 120),
        (73, 16, 120),
        (74, 16, 121),
        (76, 17, 122),
        (78, 17, 123),
        (79, 18, 123),
        (81, 18, 124),
        (82, 19, 124),
        (84, 19, 125),
        (86, 20, 125),
        (87, 21, 126),
        (89, 21, 126),
        (90, 22, 126),
        (92, 22, 127),
        (93, 23, 127),
        (95, 24, 127),
        (96, 24, 128),
        (98, 25, 128),
        (100, 26, 128),
        (101, 26, 128),
        (103, 27, 128),
        (104, 28, 129),
        (106, 28, 129),
        (107, 29, 129),
        (109, 29, 129),
        (110, 30, 129),
        (112, 31, 129),
        (114, 31, 129),
        (115, 32, 129),
        (117, 33, 129),
        (118, 33, 129),
        (120, 34, 129),
        (121, 34, 130),
        (123, 35, 130),
        (124, 35, 130),
        (126, 36, 130),
        (128, 37, 130),
        (129, 37, 129),
        (131, 38, 129),
        (132, 38, 129),
        (134, 39, 129),
        (136, 39, 129),
        (137, 40, 129),
        (139, 41, 129),
        (140, 41, 129),
        (142, 42, 129),
        (144, 42, 129),
        (145, 43, 129),
        (147, 43, 128),
        (148, 44, 128),
        (150, 44, 128),
        (152, 45, 128),
        (153, 45, 128),
        (155, 46, 127),
        (156, 46, 127),
        (158, 47, 127),
        (160, 47, 127),
        (161, 48, 126),
        (163, 48, 126),
        (165, 49, 126),
        (166, 49, 125),
        (168, 50, 125),
        (170, 51, 125),
        (171, 51, 124),
        (173, 52, 124),
        (174, 52, 123),
        (176, 53, 123),
        (178, 53, 123),
        (179, 54, 122),
        (181, 54, 122),
        (183, 55, 121),
        (184, 55, 121),
        (186, 56, 120),
        (188, 57, 120),
        (189, 57, 119),
        (191, 58, 119),
        (192, 58, 118),
        (194, 59, 117),
        (196, 60, 117),
        (197, 60, 116),
        (199, 61, 115),
        (200, 62, 115),
        (202, 62, 114),
        (204, 63, 113),
        (205, 64, 113),
        (207, 64, 112),
        (208, 65, 111),
        (210, 66, 111),
        (211, 67, 110),
        (213, 68, 109),
        (214, 69, 108),
        (216, 69, 108),
        (217, 70, 107),
        (219, 71, 106),
        (220, 72, 105),
        (222, 73, 104),
        (223, 74, 104),
        (224, 76, 103),
        (226, 77, 102),
        (227, 78, 101),
        (228, 79, 100),
        (229, 80, 100),
        (231, 82, 99),
        (232, 83, 98),
        (233, 84, 98),
        (234, 86, 97),
        (235, 87, 96),
        (236, 88, 96),
        (237, 90, 95),
        (238, 91, 94),
        (239, 93, 94),
        (240, 95, 94),
        (241, 96, 93),
        (242, 98, 93),
        (242, 100, 92),
        (243, 101, 92),
        (244, 103, 92),
        (244, 105, 92),
        (245, 107, 92),
        (246, 108, 92),
        (246, 110, 92),
        (247, 112, 92),
        (247, 114, 92),
        (248, 116, 92),
        (248, 118, 92),
        (249, 120, 93),
        (249, 121, 93),
        (249, 123, 93),
        (250, 125, 94),
        (250, 127, 94),
        (250, 129, 95),
        (251, 131, 95),
        (251, 133, 96),
        (251, 135, 97),
        (252, 137, 97),
        (252, 138, 98),
        (252, 140, 99),
        (252, 142, 100),
        (252, 144, 101),
        (253, 146, 102),
        (253, 148, 103),
        (253, 150, 104),
        (253, 152, 105),
        (253, 154, 106),
        (253, 155, 107),
        (254, 157, 108),
        (254, 159, 109),
        (254, 161, 110),
        (254, 163, 111),
        (254, 165, 113),
        (254, 167, 114),
        (254, 169, 115),
        (254, 170, 116),
        (254, 172, 118),
        (254, 174, 119),
        (254, 176, 120),
        (254, 178, 122),
        (254, 180, 123),
        (254, 182, 124),
        (254, 183, 126),
        (254, 185, 127),
        (254, 187, 129),
        (254, 189, 130),
        (254, 191, 132),
        (254, 193, 133),
        (254, 194, 135),
        (254, 196, 136),
        (254, 198, 138),
        (254, 200, 140),
        (254, 202, 141),
        (254, 204, 143),
        (254, 205, 144),
        (254, 207, 146),
        (254, 209, 148),
        (254, 211, 149),
        (254, 213, 151),
        (254, 215, 153),
        (254, 216, 154),
        (253, 218, 156),
        (253, 220, 158),
        (253, 222, 160),
        (253, 224, 161),
        (253, 226, 163),
        (253, 227, 165),
        (253, 229, 167),
        (253, 231, 169),
        (253, 233, 170),
        (253, 235, 172),
        (252, 236, 174),
        (252, 238, 176),
        (252, 240, 178),
        (252, 242, 180),
        (252, 244, 182),
        (252, 246, 184),
        (252, 247, 185),
        (252, 249, 187),
        (252, 251, 189),
        (252, 253, 191),
    ]),

    "plasma": linear([
        (13, 8, 135),
        (16, 7, 136),
        (19, 7, 137),
        (22, 7, 138),
        (25, 6, 140),
        (27, 6, 141),
        (29, 6, 142),
        (32, 6, 143),
        (34, 6, 144),
        (36, 6, 145),
        (38, 5, 145),
        (40, 5, 146),
        (42, 5, 147),
        (44, 5, 148),
        (46, 5, 149),
        (47, 5, 150),
        (49, 5, 151),
        (51, 5, 151),
        (53, 4, 152),
        (55, 4, 153),
        (56, 4, 154),
        (58, 4, 154),
        (60, 4, 155),
        (62, 4, 156),
        (63, 4, 156),
        (65, 4, 157),
        (67, 3, 158),
        (68, 3, 158),
        (70, 3, 159),
        (72, 3, 159),
        (73, 3, 160),
        (75, 3, 161),
        (76, 2, 161),
        (78, 2, 162),
        (80, 2, 162),
        (81, 2, 163),
        (83, 2, 163),
        (85, 2, 164),
        (86, 1, 164),
        (88, 1, 164),
        (89, 1, 165),
        (91, 1, 165),
        (92, 1, 166),
        (94, 1, 166),
        (96, 1, 166),
        (97, 0, 167),
        (99, 0, 167),
        (100, 0, 167),
        (102, 0, 167),
        (103, 0, 168),
        (105, 0, 168),
        (106, 0, 168),
        (108, 0, 168),
        (110, 0, 168),
        (111, 0, 168),
        (113, 0, 168),
        (114, 1, 168),
        (116, 1, 168),
        (117, 1, 168),
        (119, 1, 168),
        (120, 1, 168),
        (122, 2, 168),
        (123, 2, 168),
        (125, 3, 168),
        (126, 3, 168),
        (128, 4, 168),
        (129, 4, 167),
        (131, 5, 167),
        (132, 5, 167),
        (134, 6, 166),
        (135, 7, 166),
        (136, 8, 166),
        (138, 9, 165),
        (139, 10, 165),
        (141, 11, 165),
        (142, 12, 164),
        (143, 13, 164),
        (145, 14, 163),
        (146, 15, 163),
        (148, 16, 162),
        (149, 17, 161),
        (150, 19, 161),
        (152, 20, 160),
        (153, 21, 159),
        (154, 22, 159),
        (156, 23, 158),
        (157, 24, 157),
        (158, 25, 157),
        (160, 26, 156),
        (161, 27, 155),
        (162, 29, 154),
        (163, 30, 154),
        (165, 31, 153),
        (166, 32, 152),
        (167, 33, 151),
        (168, 34, 150),
        (170, 35, 149),
        (171, 36, 148),
        (172, 38, 148),
        (173, 39, 147),
        (174, 40, 146),
        (176, 41, 145),
        (177, 42, 144),
        (178, 43, 143),
        (179, 44, 142),
        (180, 46, 141),
        (181, 47, 140),
        (182, 48, 139),
        (183, 49, 138),
        (184, 50, 137),
        (186, 51, 136),
        (187, 52, 136),
        (188, 53, 135),
        (189, 55, 134),
        (190, 56, 133),
        (191, 57, 132),
        (192, 58, 131),
        (193, 59, 130),
        (194, 60, 129),
        (195, 61, 128),
        (196, 62, 127),
        (197, 64, 126),
        (198, 65, 125),
        (199, 66, 124),
        (200, 67, 123),
        (201, 68, 122),
        (202, 69, 122),
        (203, 70, 121),
        (204, 71, 120),
        (204, 73, 119),
        (205, 74, 118),
        (206, 75, 117),
        (207, 76, 116),
        (208, 77, 115),
        (209, 78, 114),
        (210, 79, 113),
        (211, 81, 113),
        (212, 82, 112),
        (213, 83, 111),
        (213, 84, 110),
        (214, 85, 109),
        (215, 86, 108),
        (216, 87, 107),
        (217, 88, 106),
        (218, 90, 106),
        (218, 91, 105),
        (219, 92, 104),
        (220, 93, 103),
        (221, 94, 102),
        (222, 95, 101),
        (222, 97, 100),
        (223, 98, 99),
        (224, 99, 99),
        (225, 100, 98),
        (226, 101, 97),
        (226, 102, 96),
        (227, 104, 95),
        (228, 105, 94),
        (229, 106, 93),
        (229, 107, 93),
        (230, 108, 92),
        (231, 110, 91),
        (231, 111, 90),
        (232, 112, 89),
        (233, 113, 88),
        (233, 114, 87),
        (234, 116, 87),
        (235, 117, 86),
        (235, 118, 85),
        (236, 119, 84),
        (237, 121, 83),
        (237, 122, 82),
        (238, 123, 81),
        (239, 124, 81),
        (239, 126, 80),
        (240, 127, 79),
        (240, 128, 78),
        (241, 129, 77),
        (241, 131, 76),
        (242, 132, 75),
        (243, 133, 75),
        (243, 135, 74),
        (244, 136, 73),
        (244, 137, 72),
        (245, 139, 71),
        (245, 140, 70),
        (246, 141, 69),
        (246, 143, 68),
        (247, 144, 68),
        (247, 145, 67),
        (247, 147, 66),
        (248, 148, 65),
        (248, 149, 64),
        (249, 151, 63),
        (249, 152, 62),
        (249, 154, 62),
        (250, 155, 61),
        (250, 156, 60),
        (250, 158, 59),
        (251, 159, 58),
        (251, 161, 57),
        (251, 162, 56),
        (252, 163, 56),
        (252, 165, 55),
        (252, 166, 54),
        (252, 168, 53),
        (252, 169, 52),
        (253, 171, 51),
        (253, 172, 51),
        (253, 174, 50),
        (253, 175, 49),
        (253, 177, 48),
        (253, 178, 47),
        (253, 180, 47),
        (253, 181, 46),
        (254, 183, 45),
        (254, 184, 44),
        (254, 186, 44),
        (254, 187, 43),
        (254, 189, 42),
        (254, 190, 42),
        (254, 192, 41),
        (253, 194, 41),
        (253, 195, 40),
        (253, 197, 39),
        (253, 198, 39),
        (253, 200, 39),
        (253, 202, 38),
        (253, 203, 38),
        (252, 205, 37),
        (252, 206, 37),
        (252, 208, 37),
        (252, 210, 37),
        (251, 211, 36),
        (251, 213, 36),
        (251, 215, 36),
        (250, 216, 36),
        (250, 218, 36),
        (249, 220, 36),
        (249, 221, 37),
        (248, 223, 37),
        (248, 225, 37),
        (247, 226, 37),
        (247, 228, 37),
        (246, 230, 38),
        (246, 232, 38),
        (245, 233, 38),
        (245, 235, 39),
        (244, 237, 39),
        (243, 238, 39),
        (243, 240, 39),
        (242, 242, 39),
        (241, 244, 38),
        (241, 245, 37),
        (240, 247, 36),
        (240, 249, 33),
    ])
}
