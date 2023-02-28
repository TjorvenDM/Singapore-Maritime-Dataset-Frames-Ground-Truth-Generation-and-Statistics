import os
def yolo_formatter(dataset_path, objects_onshore_path, objects_onboard_path, objects_nir_path):
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

    #iterate through folder
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
                parts = element.split(' ')

                # Convert bbox x1 y1 w h to yolo format (each image is 1080x1920)
                #    ----------------------------
                #    |                          |
                #    |                          |
                # (x1,y1)------------------------

                x1 = parts[1]
                y1 = parts[2]
                width = parts[3]
                heights = parts[4]

                x_yolo = x1 + (1920./2)
                y_yolo = Y1 + (1080./2)
                width =  width/1920.
                height = height/1080.

                new_element = parts[-3], x_yolo, y_yolo, width, height
                # new_element = [parts[-3], parts[1], parts[2], parts[3], parts[4]] #object_type x y w h
                yolo_list.append(' '.join(new_element))

            #print(yolo_list)

            #make txt
            txt_filename =  os.path.splitext(filename)[0] + '.txt'
            txt_filepath = os.path.join(dataset_path, txt_filename)
            with open(txt_filepath, 'w') as f:
                for element in yolo_list:
                    f.write(element + '\n')

yolo_formatter("D:/Masterproef/train_dataset","D:/Masterproef/Singapore-Maritime-Dataset-Frames-Ground-Truth-Generation-and-Statistics-master/objects_onshore.txt","D:/Masterproef/Singapore-Maritime-Dataset-Frames-Ground-Truth-Generation-and-Statistics-master/objects_onboard.txt","D:/Masterproef/Singapore-Maritime-Dataset-Frames-Ground-Truth-Generation-and-Statistics-master/objects_nir.txt")
