import os
import shutil

base_dir = os.path.expanduser("~/projects/warehouse_ws/src/warehouse_gazebo")
generated_dir = os.path.join(base_dir, "markers", "generated")
models_dir = os.path.join(base_dir, "models")

markers = {
    0: ("aruco_marker_0", "charging_dock.png", "Charging Dock"),
    1: ("aruco_marker_1", "loading_zone.png", "Loading Zone"),
    2: ("aruco_marker_2", "inventory_station_a.png", "Inventory Station A"),
    3: ("aruco_marker_3", "inventory_station_b.png", "Inventory Station B"),
}

for marker_id, (model_name, image_name, description) in markers.items():
    model_path = os.path.join(models_dir, model_name)
    texture_path = os.path.join(model_path, "materials", "textures")
    script_path = os.path.join(model_path, "materials", "scripts")

    os.makedirs(texture_path, exist_ok=True)
    os.makedirs(script_path, exist_ok=True)

    shutil.copy(
        os.path.join(generated_dir, image_name),
        os.path.join(texture_path, image_name)
    )

    with open(os.path.join(model_path, "model.config"), "w") as f:
        f.write(f"""<?xml version="1.0"?>
<model>
  <name>{model_name}</name>
  <version>1.0</version>
  <sdf version="1.6">model.sdf</sdf>
  <author>
    <name>Sara Esmaeili</name>
  </author>
  <description>{description} ArUco marker</description>
</model>
""")

    with open(os.path.join(script_path, "aruco_marker.material"), "w") as f:
        f.write(f"""material Aruco/{model_name}
{{
  technique
  {{
    pass
    {{
      texture_unit
      {{
        texture {image_name}
      }}
    }}
  }}
}}
""")

    with open(os.path.join(model_path, "model.sdf"), "w") as f:
        f.write(f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="{model_name}">
    <static>true</static>

    <link name="marker_link">
      <visual name="marker_visual">
        <geometry>
          <plane>
            <normal>1 0 0</normal>
            <size>0.8 0.8</size>
          </plane>
        </geometry>

        <material>
          <script>
            <uri>model://{model_name}/materials/scripts</uri>
            <uri>model://{model_name}/materials/textures</uri>
            <name>Aruco/{model_name}</name>
          </script>
        </material>
      </visual>
    </link>
  </model>
</sdf>
""")

    print(f"Created {model_name}: ID {marker_id} - {description}")

print("All marker models created.")
