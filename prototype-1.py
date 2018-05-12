# conversions yet to be done properly for sin() , cos() - radian vs degree-minute-seconds
# h = N + H not implemented yet
from math import *

# input
# co-ordinates in local geodetic datums
lat_local = 0  # value not available yet
lon_local = 0  # value not available yet
h_local = 0  # value not available yet

# delta x, y, z - shifts between local geodetic datum and wgs84 ellipsoid center
delta_x = 0  # value not available yet
delta_y = 0  # value not available yet
delta_z = 0  # value not available yet

# a - semi-major axis of local geodetic datum ellipsoid
# b - semi-minor axis of local geodetic datum ellipsoid
# f - flattening of local geodetic datum ellipsoid
# e - first eccentricity
a = 1  # value not available yet
b = 1  # value not available yet
f = 1 - (float(b) / a)
e = sqrt(2 * f - f ** 2)

# f_wgs , a_wgs - flattening and semi-major axis of wgs84 ellipsoid
f_wgs = 1  # value not available yet
a_wgs = 1  # value not available yet

# delta a, f - difference between the semi-major and flattening of local geodetic datum ellipsoid and wgs84 ellipsoid
#  (wgs84 - local)
delta_f = f_wgs - f
delta_a = a_wgs - a

# Rn - radius of curvature in prime vertical
# Rm - radius of curvature in meridian
# Rn = a / sqrt(1 - pow(e*sin(radians(lat_local)),2))
Rn = a / (1 - (e * sin(lat_local / 3600)) ** 2) ** (1 / 2)
Rm = a * (1 - e ** 2) / (1 - (e * sin(lat_local)) ** 2) ** (3 / 2)

# lattitude correction
delta_lat = (-delta_x * sin(radians(lat_local / 3600)) * cos(radians(lon_local / 3600)) - delta_y * sin(
    radians(lat_local / 3600)) * sin(
    radians(lon_local / 3600)) + delta_z * cos(radians(
    lat_local / 3600)) + delta_a * (Rn * e ** 2 * sin(radians(lat_local / 3600)) * cos(
    radians(lat_local / 3600))) / a + delta_f * (
                     Rm * (a / b) + Rn * (b / a)) * sin(radians(lat_local / 3600)) * cos(radians(lat_local / 3600))) / (
                    (Rm + h_local) * sin(radians(1 / 3600)))

# longitude correction
delta_lon = (-delta_x * sin(radians(lon_local / 3600)) + delta_y * cos(radians(lon_local / 3600))) / (
        (Rn + h_local) * cos(radians(lat_local / 3600)) * sin(radians(1 / 3600)))

# height correction
delta_h = delta_x * cos(radians(lat_local / 3600)) * cos(radians(lon_local / 3600)) + delta_y * cos(
    radians(lat_local / 3600)) * sin(
    radians(lon_local / 3600)) + delta_z * sin(radians(
    lat_local / 3600)) - delta_a * (a / Rn) + delta_f * (b / a) * Rn * (sin(radians(lat_local / 3600)) ** 2)

# final step of conversion
lat_wgs = lat_local + delta_lat
lon_wgs = lon_local + delta_lon
h_wgs = h_local + delta_h
