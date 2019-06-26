# -*- coding: utf-8 -*-


########## imports ########
import os
import folium

# print(folium.__version__)
import branca.colormap as cm
import os
import math

# env = %env
# pd.set_option('display.max_rows', 2000)

center2 = [54.840471, -110.269399]
zoom2 = 6


linear2 = cm.LinearColormap(
    ["#edf8b1", "#7fcdbb", "#2c7fb8", "#273891"], vmin=-100, vmax=75
)

print(linear2)


def depth_color(depth):
    if math.isnan(depth):
        print(" math.isnan(depth) => ", depth)
        return "blue"
    else:
        depth = float(depth)
        if depth >= 50:
            color = "#3182bd"
        elif depth > 10 and depth < 50:
            color = "#9ecae1"
        elif depth > -10 and depth < 10:
            color = "green"
        elif depth > -50 and depth < -10:
            color = "#ffeda0"
        elif depth > -150 and depth < -50:
            color = "#feb24c"
        elif depth > -300 and depth < -150:
            color = "#f03b20"
        else:
            color = "blue"
    return color


def depth_color3(depth, colorMap):
    if math.isnan(depth):
        print("!!!!!!!!!!!!!!!!!!!!  ' '  or nan is in depth => ", depth)
        color = "#000000"
    else:
        depth = float(depth)
        print("depth in colormap 3", depth)
        color = colorMap(depth)

    print("color = ", color)
    return color


def makeMap_1(no_zeros_df):
    m5 = folium.Map(center2, tiles="Stamen Toner", zoom_start=zoom2)
    list_df_for_map = no_zeros_df.values.tolist()

    for row in list_df_for_map[0:]:
        print(
            "location = ",
            row[1:3],
            " and depth is",
            row[12:13][0],
            " and UWI is ",
            row[3:4][0],
        )
        folium.CircleMarker(
            location=row[1:3],
            radius=2,
            color=depth_color(row[13:14][0]),
            fill=True,
            #     popup=folium.Popup(str(row[9:10][0])+ " & depth Top McMurray=", parse_html=True)
            #     popup=folium.Popup(str(row[9:10][0]+ ", depth Top McMurray="+str(row[15:16][0])), parse_html=True)
        ).add_to(m5)
    return m5


def saveFoliumMap(map_m5):
    map_m5.save(os.path.join(".", "MM_Top_Depth_Real_v_predBy_NN1thick_v2.html"))
