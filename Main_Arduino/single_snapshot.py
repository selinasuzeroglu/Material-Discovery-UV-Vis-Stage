from Camera import Camera
import os

# Replace the below path with the absolute or relative path to your CameraControlCmd executable.

# User Input for Image Name
sample_list = []
sample_list = [item for item in input("Enter the list items : ").split()]

image_index = 0
#index = 0


def snapshot():

    # Camera Settings:
    camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'
    save_folder = 'C:\\Users\\ssuz0008\\PycharmProjects\\UVVis_3.0\\Main_Arduino\\Photos\\'

    image_type = 'raw'
    collection_name = sample_list[image_index]
    image_name = collection_name + image_type

    def camera():

        global image_index
        #global index

        # path = f'{save_folder}{image_name}'
        # while os.path.exists(path):
        #     index += 1

        camera = Camera(control_cmd_location=camera_control_cmd_path,
                        image_type=image_type,
                        collection_name=collection_name,
                        save_folder=save_folder)

        camera.capture_single_image(autofocus=True)
        image_index += 1

    return camera()





