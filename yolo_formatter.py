import os


def yolo_formatter(dataset_path, objects_onshore_path, objects_onboard_path, objects_nir_path):
    """
    :param dataset_path: directory to images (frames)
    :param objects_onshore_path: directory to objects_onshore.txt
    :param objects_onboard_path: directory to objects_onboard.txt
    :param objects_nir_path: directory to objects_nir.txt
    :return: separate txt files per image annotated in yolo format
    """
    # put all objects on shore in objects_onshore
    objects_onshore = []
    with open(objects_onshore_path) as f:
        for line in f:
            line = line.strip()
            objects_onshore.append(line)

    # put all objects on board in objects_onboard
    objects_onboard = []
    with open(objects_onboard_path) as f:
        for line in f:
            line = line.strip()
            objects_onboard.append(line)

    # put all objects on board in objects_onboard
    objects_nir = []
    with open(objects_nir_path) as f:
        for line in f:
            line = line.strip()
            objects_nir.append(line)

    # iterate through folder
    for filename in os.listdir(dataset_path):
        if os.path.isfile(os.path.join(dataset_path, filename)):
            # print filenames
            print(filename)
            # relevant obj
            if "OB" in filename:
                relevant_objects = [i for i in objects_onboard if i.startswith(filename)]
            elif "NIR" in filename:
                relevant_objects = [i for i in objects_nir if i.startswith(filename)]
            else:
                relevant_objects = [i for i in objects_onshore if i.startswith(filename)]
            # print(relevant_objects)

            # yolo list
            yolo_list = []
            for element in relevant_objects:
                parts = element.split(',')

                # Convert bbox x1 y1 w h to yolo format (each image is 1080x1920)

                #    ----------------------------
                #    |                          |
                #    |                          |
                #    |                          |
                # (x1,y1)------------------------

                x1 = float(parts[1])
                y1 = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])

                #    ----------------------------
                #    |             |            |
                #    |----------(x1,y1)---------|
                #    |             |            |
                #    ----------------------------

                x_yolo = (x1 + (width / 2)) / 1920
                y_yolo = (y1 + (height / 2)) / 1080
                width = width / 1920.
                height = height / 1080.

                #change classes:
                if parts[-3] in (1,3,4,5,6,7):
                    parts[-3] = 1

                    object = str(int(parts[-3]) - 1)
                    new_element = object, str(x_yolo), str(y_yolo), str(width), str(height)
                    # new_element = [parts[-3], parts[1], parts[2], parts[3], parts[4]] #object_type x y w h
                    yolo_list.append(' '.join(new_element))

                else:
                    print("object with class "+parts[-3]+" not added")



            # print(yolo_list)

            # make txt
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_filepath = os.path.join(dataset_path, txt_filename)
            with open(txt_filepath, 'w') as f:
                for element in yolo_list:
                    f.write(element + '\n')


print("yolo_formatter")
yolo_formatter("C:/Users/tjorv/OneDrive/Bureaublad/dataset/test",
               "C:/Users/tjorv/OneDrive/Documenten/KU Leuven/FASE 4/SEM II/Masterproef/repos/Singapore-Maritime-Dataset-Frames-Ground-Truth-Generation-and-Statistics/objects_onshore.txt",
               "C:/Users/tjorv/OneDrive/Documenten/KU Leuven/FASE 4/SEM II/Masterproef/repos/Singapore-Maritime-Dataset-Frames-Ground-Truth-Generation-and-Statistics/objects_onboard.txt",
               "C:/Users/tjorv/OneDrive/Documenten/KU Leuven/FASE 4/SEM II/Masterproef/repos/Singapore-Maritime-Dataset-Frames-Ground-Truth-Generation-and-Statistics/objects_nir.txt")
