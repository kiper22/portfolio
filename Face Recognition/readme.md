# Face Recognition with YOLOv8 and SVM
The project is an engineering diploma thesis. The topic of the work was to create system that is able to identifies people based on their face. There are several main themes in the project:
- preparing data - data annotation
- YOLO training
- prepare classifier
- testing prepared system

Programs that evaluated research results and other ancillary ones are not included

## Data annotation and YOLO training
The CFPW [http://www.cfpw.io/] dataset was used to train the yolo network. It was necessary to mark faces in the photos - the best solution was to write program. We need only to mark 1 class (face) as rectangle. Annotation file *.txt must have the same name as the photo. Txt file contains information about the faces position:

$<id_class> <x_center_boundingbox> <y_center_boundingbox> <width_boundingbox> <height_boundingbox>

The data marking program has the ability to manually select faces by dragging the left mouse button, scroll through images (left and right arrows) and save annotations (s). If the face occupied the entire photo, using a spacebar automatically saved the annotation '0 0.5 0.5 1 1' to the file using a spacebar. After saving the file (the target path must be set in the program), the list of untagged photos decreases.
![image](https://github.com/kiper22/portfolio/assets/125763668/f3db1d2d-cc80-4451-bdf4-504688416b1c)

To train yolo we must prepare *.yaml file. Nest sep is to train yolov8 for detection

## SVM classifier
The SVM classifier with linear kernel was prepared based on facial feature extraction (FaceNet). The classifier was supposed to be able to correctly distinguish 50 people. They were selected based on the number of photos (10 for training and 10+ for validation). Result of test:

| Confidence threshold [%] | TP   | FN   | FP   | PPV  | TPR  |
|--------------------|------|------|------|------|------|
| 5.0                | 1979 | 2    | 343  | 0.85 | 1.0  |
| 5.5                | 1979 | 2    | 246  | 0.89 | 1.0  |
| 6.0                | 1979 | 2    | 165  | 0.92 | 1.0  |
| 6.5                | 1976 | 5    | 108  | 0.95 | 1.0  |
| 7.0                | 1967 | 13   | 62   | 0.97 | 0.99 |
| 7.5                | 1957 | 24   | 42   | 0.98 | 0.99 |
| 8.0                | 1938 | 42   | 30   | 0.98 | 0.98 |
| 8.5                | 1916 | 64   | 21   | 0.99 | 0.97 |
| 9.0                | 1891 | 91   | 17   | 0.99 | 0.95 |
| 9.5                | 1856 | 125  | 15   | 0.99 | 0.94 |
| 10.0               | 1807 | 175  | 12   | 0.99 | 0.91 |
| 10.5               | 1739 | 242  | 11   | 0.99 | 0.88 |
| 11.0               | 1662 | 320  | 10   | 0.99 | 0.84 |
| 11.5               | 1586 | 396  | 7    | 1.0  | 0.8  |
| 12.0               | 1512 | 468  | 6    | 1.0  | 0.76 |
| 12.5               | 1399 | 580  | 5    | 1.0  | 0.71 |
- Confidence threshold: all detected faces are classified. The answer is the most likely outcome. In case of an unknown person, the output of the classifier will be low values
-    TP (True Positives): These are the cases where the model correctly identifies faces as faces
-    FN (False Negatives): These are the cases where the model incorrectly fails to identify faces that are actually present in the images (to low confidence threshold)
-    FP (False Positives): These are the cases where the model incorrectly identifies non-faces as faces
-    PPV (Positive Predictive Value): Precision
-    TPR (True Positive Rate): Recall

The best result was obtained for a confidence streshold of 7-9% - precision and recall > 0.95.
![image](https://github.com/kiper22/portfolio/assets/125763668/70830988-0856-4609-a2b1-eb3efe2c2731)
![image](https://github.com/kiper22/portfolio/assets/125763668/69af4a32-8378-4f21-adef-4cb37ea3cd1a)



