from Camera import Camera


# Replace the below path with the absolute or relative path to your CameraControlCmd executable.

def snapshot():
    camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'
    camera = Camera(control_cmd_location=camera_control_cmd_path)
    camera.capture_single_image(autofocus=True)
