import cv2
import matplotlib.pyplot as plt
import os

fgfolder_path = "C:/Users/siebe/OneDrive/Documenten/AAIndustrieel ingenieur/Masterjaar/Sem2/Masterproef/Experimentjes/dataset/small/"

def SMD_bb_drawer(dataset_folder,bb_images_folder):
    for filename in os.listdir(dataset_folder):
        if filename.endswith(".jpg"):
            print(filename)
            image_path = os.path.join(dataset_folder,filename)
            BGR_img = cv2.imread(image_path)
            dh, dw, _ = BGR_img.shape
            print("wxh: ",dw,"x",dh)
            img = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2RGB)
            txt = filename[:-4]+"_preds"+".txt"
            print(txt)
            txtpath = os.path.join(dataset_folder,txt)
            fl = open(txtpath)
            data = fl.readlines()
            fl.close()

            for dt in data:

                # Split string to float
                _, x, y, w, h = map(float, dt.split(' '))

                # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
                # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
                l = int((x))
                r = int((x+w))
                t = int((y))
                b = int((y+h) )

                if l < 0:
                    l = 0
                if r > dw - 1:
                    r = dw - 1
                if t < 0:
                    t = 0
                if b > dh - 1:
                    b = dh - 1
                cv2.rectangle(img, (l, t), (r, b), (255, 0, 0), 1)
                classes = ["Boat"]
                bb_class = "Boat"
                cv2.putText(
                    img,
                    bb_class,
                    (int(l), int(t) - 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.6,
                    color=(255, 0, 0),
                    thickness=2
                )
            # plt.imshow(img)
            # plt.show()
            bb_filename = "bb_"+filename
            bb_path = os.path.join(bb_images_folder,bb_filename)

            cv2.imwrite(f"{bb_path}", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

SMD_bb_drawer(r"D:\Master\Sem2\Masterproef\draw_bb\test_2_resizer\predictions",r"D:\Master\Sem2\Masterproef\draw_bb\bb")
