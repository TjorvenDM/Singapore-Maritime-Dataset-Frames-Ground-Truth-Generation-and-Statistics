import os
import random
import tkinter as tk
from PIL import ImageTk, Image

##CITATION NEEDED
class IMO_dataset_plotter:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.subfolders = []
        self.image_paths = []
        self.image_widgets = []

        # Create the Tkinter window
        self.root = tk.Tk()
        self.root.title('Image Plotter')

        # Create a button to refresh the plot
        self.refresh_button = tk.Button(self.root, text='Refresh', command=self.refresh_plot)
        self.refresh_button.pack()

        # Create a frame to hold the image widgets
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Set up the plot
        self.setup_plot()

    def setup_plot(self):
        # Get subfolder names within the folder path
        self.subfolders = [os.path.join(self.folder_path, f.name, "train") for f in os.scandir(self.folder_path) if
                           f.is_dir()]

        # Determine number of rows and columns based on number of subfolders
        num_subfolders = len(self.subfolders)
        num_columns = 5  # set number of columns
        num_rows = (num_subfolders + num_columns - 1) // num_columns  # calculate number of rows

        # Create a grid of frames to hold the image and label widgets
        for row in range(num_rows):
            row_frame = tk.Frame(self.image_frame)
            row_frame.pack(side=tk.TOP, pady=10)
            for col in range(num_columns):
                if row * num_columns + col >= num_subfolders:
                    # Stop adding frames if there are no more subfolders
                    break
                subfolder = self.subfolders[row * num_columns + col]
                # Create a frame to hold the image and label widgets
                frame = tk.Frame(row_frame)
                frame.pack(side=tk.LEFT, padx=10)
                # Create an image widget for a random image from the subfolder
                image_path = random.choice(
                    [os.path.join(subfolder, f) for f in os.listdir(subfolder) if f.endswith('.jpg')])
                img = Image.open(image_path)
                img = img.resize((500, 500))
                img_tk = ImageTk.PhotoImage(img)
                self.image_widgets.append(tk.Label(frame, image=img_tk))
                self.image_widgets[-1].image = img_tk
                self.image_widgets[-1].pack()
                # Create an image widget for the subfolder name
                subfolder_name = os.path.basename(os.path.dirname(subfolder))
                label = tk.Label(frame, text=subfolder_name)
                label.pack(side=tk.BOTTOM)

    def refresh_plot(self):
        # Get image paths for each subfolder
        self.image_paths = []
        for subfolder in self.subfolders:
            image_paths = [os.path.join(subfolder, f) for f in os.listdir(subfolder) if f.endswith('.jpg')]
            self.image_paths.append(image_paths)

        # Update the image widgets with new images
        for i, image_widget in enumerate(self.image_widgets):
            # Select a random image from the corresponding subfolder
            image_path = random.choice(self.image_paths[i])

            # Open and resize the image
            img = Image.open(image_path)
            img = img.resize((500, 500))

            # Update the image widget with the new image
            img_tk = ImageTk.PhotoImage(img)
            image_widget.configure(image=img_tk)
            image_widget.image = img_tk

    def run(self):
        self.root.mainloop()


# Example usage
plotter = IMO_dataset_plotter(r"C:\Users\siebe\OneDrive\Documenten\AAIndustrieel ingenieur\Masterjaar\Sem2\Masterproef\IMO_dataset\werktfunctie")
plotter.run()
