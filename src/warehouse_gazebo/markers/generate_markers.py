import cv2
import os

# Create output directory
output_dir = os.path.expanduser(
    "~/projects/warehouse_ws/src/warehouse_gazebo/markers/generated"
)

os.makedirs(output_dir, exist_ok=True)

# ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

# Marker IDs
markers = {
    0: "charging_dock",
    1: "loading_zone",
    2: "inventory_station_a",
    3: "inventory_station_b"
}

# Generate markers
for marker_id, name in markers.items():

    marker_image = cv2.aruco.generateImageMarker(
        aruco_dict,
        marker_id,
        400
    )

    filename = os.path.join(
        output_dir,
        f"{name}.png"
    )

    cv2.imwrite(filename, marker_image)

    print(f"Generated: {filename}")

print("All markers generated successfully.")
