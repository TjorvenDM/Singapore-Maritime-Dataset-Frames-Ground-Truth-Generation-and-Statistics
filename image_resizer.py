import os
import cv2

def image_resizer_overview(image_folder, destination_folder_txt,scale_factor,iterations):
    if scale_factor < 0 or iterations < 0 or scale_factor>1:
        print("incorrect input")
    else:
        # Create a text file to log the rescaling
        scale_factor_string = str(scale_factor)
        log_file = open(os.path.join(destination_folder_txt,f"resizer_log_sf{scale_factor_string[2:]}_it{iterations}.txt"), "w")

        # Loop through all the files in the input folder
        k=0
        for filename in os.listdir(image_folder):
            # Check if the file is an image
            if filename.endswith(('.png', '.jpg')):
                print(filename)
                txt = filename[:-4] + ".txt"
                fl = open(image_folder+ "/" + txt)
                data = fl.readlines()
                k+=1

                # Load the image
                img = cv2.imread(os.path.join(image_folder, filename))

                log_file.write(f"image{k}: {filename}, number of boats: {len(data)}\n")
                for i in range(iterations):
                    log_file.write(f"    size{i+1}: {int(img.shape[1]*(scale_factor**(i)))} x {int(img.shape[0]*(scale_factor**(i)))}, total: {int((img.shape[1]*(scale_factor**(i)))*(img.shape[0]*(scale_factor**(i))))}\n")
                    j = 1
                    for line in data:
                        values = line.split()
                        log_file.write(f"       boat{j}: x:{float(values[1])*int(img.shape[1]*(scale_factor**(i)))}, y:{float(values[2])*int(img.shape[0]*(scale_factor**(i)))}, width:{float(values[3])*(img.shape[1]*int(scale_factor**(i)))}, height:{float(values[4])*int(img.shape[0]*(scale_factor**(i)))}, area:{(float(values[3])*int(img.shape[1]*(scale_factor**(i)))) * (float(values[4])*int(img.shape[0]*(scale_factor**(i))))}\n")
                        j+=1
                fl.close()
        # Close the log file
        log_file.close()


def image_resizer(image_folder,destination_folder,scale_factor,iterations):
    if scale_factor < 0 or iterations < 0 or scale_factor > 1:
        print("incorrect input")
    else:
        # Loop through all the files in the input folder
        for filename in os.listdir(image_folder):
            # Check if the file is an image
            if filename.endswith(('.png', '.jpg')):
                print(filename)
                # Load the image
                img = cv2.imread(os.path.join(image_folder, filename))
                for i in range(iterations):
                    # Calculate the new width and height
                    new_width = int(img.shape[1] * (scale_factor ** (i)))
                    new_height = int(img.shape[0] * (scale_factor ** (i)))
                    # Resize the image
                    resized_img = cv2.resize(img, (new_width, new_height))
                    scale_factor_string = str(scale_factor)
                    output_name = f"resizer_log_sf{scale_factor_string[2:]}_it{iterations}_"
                    output_folder = destination_folder+"/"+output_name + str(i + 1)
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    cv2.imwrite(os.path.join(output_folder, filename), resized_img)

                    txt = filename[:-4] + ".txt"
                    log_file = open(os.path.join(destination_folder,output_folder,
                                                 f"{txt}"), "w")
                    fl = open(image_folder + "/" + txt)
                    data = fl.readlines()
                    for line in data:
                        values = line.split()
                        log_file.write(f"{values[0]} {float(values[1])} {float(values[2])} {float(values[3])} {float(values[4])}\n")
                    # Close the log file
                    log_file.close()



image_resizer("D:/Master/Sem2/dataset/klein","D:/Master/Sem2/dataset",0.83,5)
image_resizer_overview("D:/Master/Sem2/dataset/klein","D:/Master/Sem2/dataset",0.83,5)
