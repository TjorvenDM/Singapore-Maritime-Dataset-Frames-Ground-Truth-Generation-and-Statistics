import csv
import os
import shutil
import random

#This version is able to make train, test, validation folders for each class. IMO numbers of train will not be used in test and validation, etc.
def make_balanced_dataset(classname, wanted_classes_csv, IMO_info_csv_path, image_info_csv_path, all_IMO_info_freq_path, images_folder_path, destination_folder_path, images_of_each_class_train, images_of_each_ship_train,images_of_each_class_test, images_of_each_ship_test,images_of_each_class_validation, images_of_each_ship_validation):
    total_images_class = images_of_each_class_test + images_of_each_class_validation + images_of_each_class_train
    print("Total amount of images 1 class: ",(total_images_class),"\nTrain percentage: ",(images_of_each_class_train/total_images_class),"\nTest percentage: ",(images_of_each_class_test/total_images_class),"\nValidation percentage: ",(images_of_each_class_validation/total_images_class),"\n")
    if images_of_each_class_train%images_of_each_ship_train != 0 or images_of_each_class_test%images_of_each_ship_test != 0 or images_of_each_class_validation%images_of_each_ship_validation != 0:
        print("Error: images_of_each_clas % images_of_each_ship != 0")
        return 0
    # Read the wanted classes from the CSV file
    with open(wanted_classes_csv, 'r') as f:
        wanted_classes = [line.strip() for line in f.readlines()]
    print("Wanted classes: ",wanted_classes)

    # Translate classname to what column that classname is specified
    if classname == "shiptypegroup":
        classname_column = 2
    elif classname == "shiptypelevel2":
        classname_column = 3
    elif classname == "shiptypelevel3":
        classname_column = 4
    elif classname == "shiptypelevel4":
        classname_column = 5
    elif classname == "shiptypelevel5":
        classname_column = 6
    elif classname == "shiptypelevel5hulltype":
        classname_column = 7
    elif classname == "shiptypelevel5subgroup":
        classname_column = 8
    elif classname == "shiptypelevel5subtype":
        classname_column = 9

    # Load all IMO info from CSV. Store this in a dictionary called all_IMO_info
    all_IMO_info = {}
    with open(IMO_info_csv_path, newline='') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            all_IMO_numbers = int(row[0])
            classname_value = row[classname_column]
            all_IMO_info[all_IMO_numbers] = classname_value
    #print(all_IMO_info)

    all_IMO_info_freq = {}
    with open(all_IMO_info_freq_path,newline='') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            all_IMO_freq_numbers = int(row[0])
            frequency = int(row[1])
            all_IMO_info_freq[all_IMO_freq_numbers] = frequency
    #print(all_IMO_info_freq)

    # Read the image information from the CSV file
    with open(image_info_csv_path, newline='') as f:
        reader = csv.reader(f, delimiter=';')
        image_info = {row[0]: row[1] for row in reader}
    #print(image_info)

    # Create a dictionary to count the number of images for each class
    images_per_class = {c: 0 for c in wanted_classes}


    # Loop over the wanted classes
    for c in wanted_classes:
        # Create a list of IMO numbers for the current class
        IMO_list = [IMO for IMO, cls in all_IMO_info.items() if cls == c]
        random.shuffle(IMO_list)

        # First quick check
        print(f"Amount of ships of class {c}: {len(IMO_list)}")
        needed_ships = (images_of_each_class_validation/images_of_each_ship_validation) + (images_of_each_class_train / images_of_each_ship_train) + (images_of_each_class_test/images_of_each_ship_test)
        if needed_ships > len(IMO_list):
            print(f'ERROR: Not possible to get {needed_ships} ships for class {c}. Not enough ships')
            return 0

        needed_ship_counter_train = images_of_each_class_train / images_of_each_ship_train
        needed_ship_counter_test = images_of_each_class_test / images_of_each_ship_test
        needed_ship_counter_validation = images_of_each_class_validation / images_of_each_ship_validation
        ship_counter = 0
        ship_counter_train=0
        ship_counter_test = 0
        ship_counter_validation = 0
        list_of_valid_boats_train = []
        list_of_valid_boats_test = []
        list_of_valid_boats_validation = []
        for IMO_num in IMO_list:
            if ship_counter < total_images_class:
                if IMO_num in all_IMO_info_freq:
                    if ship_counter_train < needed_ship_counter_train and all_IMO_info_freq[IMO_num] >= images_of_each_ship_train:
                        ship_counter_train += 1
                        ship_counter += 1
                        list_of_valid_boats_train.append(IMO_num)
                    elif ship_counter_test < needed_ship_counter_test and all_IMO_info_freq[IMO_num] >= images_of_each_ship_test:
                        ship_counter_test +=1
                        ship_counter += 1
                        list_of_valid_boats_test.append(IMO_num)
                    elif ship_counter_validation < needed_ship_counter_validation and all_IMO_info_freq[IMO_num] >= images_of_each_ship_validation:
                        ship_counter_validation +=1
                        ship_counter += 1
                        list_of_valid_boats_validation.append(IMO_num)
                    else:
                        ship_counter += 0
            else:
                break
        print(f"Selected training IMOS for class {c}: {list_of_valid_boats_train}")
        print(f"Selected testing IMOS for class {c}: {list_of_valid_boats_test}")
        print(f"Selected validation IMOS for class {c}: {list_of_valid_boats_validation}")
        if ship_counter < needed_ships:
            print(f"ERROR: Not possible to get {total_images_class} images for class {c}. Not enough images per ship")
            return 0
        else:
            dict_of_valid_ships_train = {}
            all_images_class_train = []
            for IMOS_tr in list_of_valid_boats_train:
                list_of_images_per_ship_train = []
                for image,IMO in image_info.items():
                    if IMO == str(IMOS_tr):
                        list_of_images_per_ship_train.append(image)
                random_images_out_of_list_train = random.sample(list_of_images_per_ship_train, images_of_each_ship_train)
                all_images_class_train += random_images_out_of_list_train
                dict_of_valid_ships_train[IMOS_tr] = random_images_out_of_list_train

            dict_of_valid_ships_test = {}
            all_images_class_test = []
            for IMOS_te in list_of_valid_boats_test:
                list_of_images_per_ship_test = []
                for image,IMO in image_info.items():
                    if IMO == str(IMOS_te):
                        list_of_images_per_ship_test.append(image)
                random_images_out_of_list_test = random.sample(list_of_images_per_ship_test, images_of_each_ship_test)
                all_images_class_test += random_images_out_of_list_test
                dict_of_valid_ships_test[IMOS_te] = random_images_out_of_list_test

            dict_of_valid_ships_validation = {}
            all_images_class_validation = []
            for IMOS_v in list_of_valid_boats_validation:
                list_of_images_per_ship_validation = []
                for image,IMO in image_info.items():
                    if IMO == str(IMOS_v):
                        list_of_images_per_ship_validation.append(image)
                random_images_out_of_list_validation = random.sample(list_of_images_per_ship_validation, images_of_each_ship_validation)
                all_images_class_validation += random_images_out_of_list_validation
                dict_of_valid_ships_validation[IMOS_v] = random_images_out_of_list_validation
            #print(all_images_class)
            #print(dict_of_valid_ships)

        if "/" in c:
            c = c.replace("/","_")

        new_folder_path = os.path.join(destination_folder_path, c)
        os.makedirs(new_folder_path, exist_ok=True)
        new_folder_path_train = os.path.join(new_folder_path, "train")
        os.makedirs(new_folder_path_train, exist_ok=True)
        new_folder_path_test = os.path.join(new_folder_path, "test")
        os.makedirs(new_folder_path_test, exist_ok=True)
        new_folder_path_validation = os.path.join(new_folder_path, "validation")
        os.makedirs(new_folder_path_validation, exist_ok=True)

        for image_names in all_images_class_train:
            wanted_image_name_train = str(image_names) + '_2' + '.jpg'
            if int(image_names) < 1000000:
                images_dataset_folder_prefix_train = wanted_image_name_train[:4]
            else:
                images_dataset_folder_prefix_train = wanted_image_name_train[:5]
            image_folder_path_specific_train = images_folder_path + images_dataset_folder_prefix_train + "/" + wanted_image_name_train
            new_folder_path_complete_train = os.path.join(new_folder_path_train, wanted_image_name_train)
            print("Train: ",wanted_image_name_train)
            if os.path.exists(image_folder_path_specific_train):
                shutil.copyfile(image_folder_path_specific_train, new_folder_path_complete_train)
            else:
                print("Image folder path: ", image_folder_path_specific_train, " does not exist")
        for image_names in all_images_class_test:
            wanted_image_name_test = str(image_names) + '_2' + '.jpg'
            if int(image_names) < 1000000:
                images_dataset_folder_prefix_test = wanted_image_name_test[:4]
            else:
                images_dataset_folder_prefix_test = wanted_image_name_test[:5]
            image_folder_path_specific_test = images_folder_path + images_dataset_folder_prefix_test + "/" + wanted_image_name_test
            new_folder_path_complete_test = os.path.join(new_folder_path_test, wanted_image_name_test)
            print("Test: ",wanted_image_name_test)
            if os.path.exists(image_folder_path_specific_test):
                shutil.copyfile(image_folder_path_specific_test, new_folder_path_complete_test)
            else:
                print("Image folder path: ", image_folder_path_specific_test, " does not exist")

        for image_names in all_images_class_validation:
            wanted_image_name_validation = str(image_names) + '_2' + '.jpg'
            if int(image_names) < 1000000:
                images_dataset_folder_prefix_validation = wanted_image_name_validation[:4]
            else:
                images_dataset_folder_prefix_validation = wanted_image_name_validation[:5]
            image_folder_path_specific_validation = images_folder_path + images_dataset_folder_prefix_validation + "/" + wanted_image_name_validation
            new_folder_path_complete_validation = os.path.join(new_folder_path_validation, wanted_image_name_validation)
            print("Validation: ",wanted_image_name_validation)
            if os.path.exists(image_folder_path_specific_validation):
                shutil.copyfile(image_folder_path_specific_validation, new_folder_path_complete_validation)
            else:
                print("Image folder path: ", image_folder_path_specific_validation, " does not exist")


make_balanced_dataset("shiptypelevel2", r"C:\Users\siebe\OneDrive\Documenten\AAIndustrieel ingenieur\Masterjaar\Sem2\Masterproef\IMO_dataset\wanted_classes.txt",r"C:\Users\siebe\OneDrive\Documenten\AAIndustrieel ingenieur\Masterjaar\Sem2\Masterproef\IMO_dataset\alle_imos.csv",r"C:\Users\siebe\OneDrive\Documenten\AAIndustrieel ingenieur\Masterjaar\Sem2\Masterproef\IMO_dataset\ShipScapeIndex.txt", r"C:\Users\siebe\OneDrive\Documenten\AAIndustrieel ingenieur\Masterjaar\Sem2\Masterproef\IMO_dataset\lrno_vs_freq.csv","D:/Photostore/", r"C:\Users\siebe\OneDrive\Documenten\AAIndustrieel ingenieur\Masterjaar\Sem2\Masterproef\IMO_dataset\werktfunctie", 20,1,1,1,1,1)
#IMO_dataset_maker(r"D:\Master\Sem2\Masterproef\IMO_dataset\IMO_nums.txt","shiptypegroup",r"D:\Master\Sem2\Masterproef\IMO_dataset\alle_imos.csv",r"D:\Master\Sem2\Masterproef\IMO_dataset\ShipScapeIndex.txt","F:/",r"D:\Master\Sem2\Masterproef\IMO_dataset\Werktdit")
