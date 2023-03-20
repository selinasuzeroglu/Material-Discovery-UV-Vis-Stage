from Camera import Camera

# Replace the below path with the absolute or relative path to your CameraControlCmd executable.

# sample_list = [item for item in input("Enter the list items : ").split()]  this list will pop up in the beginning
# of each run, so user can put sample names. Plots and Photos will be saved under those names.
sample_list = range(10000)  # for test measurement runs, we chose to try 10000 subsequent runs.
image_index = 0


def snapshot():

    # Camera Settings:
    camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'
    save_folder = 'C:\\Users\\ssuz0008\\PycharmProjects\\UVVis_3.0\\Photos\\'
    # change folder direction
    image_type = 'raw'
    collection_name = sample_list[image_index]

    def camera():

        global image_index
        camera = Camera(control_cmd_location=camera_control_cmd_path,
                        image_type=image_type,
                        collection_name=f'{collection_name}',
                        save_folder=save_folder)

        camera.capture_single_image(autofocus=False)
        image_index += 1

    return camera()


