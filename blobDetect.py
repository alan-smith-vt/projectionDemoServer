import cv2
import numpy as np

def detect_blobs(img_bgr):
    # Load the image
    image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 50  # Min area of the blob. Adjust according to your needs.
    
    # Filter by Color (black or white)
    params.filterByColor = True
    params.blobColor = 0  # To detect black blobs (255 for white blobs)
    
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.25
    
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.25
    
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.25
    
    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    
    # Detect blobs.
    keypoints = detector.detect(image)
    
    # Extract the x,y coordinates of the keypoints (centroids of the blobs)
    centroids = np.array([[kp.pt[0], kp.pt[1]] for kp in keypoints])
    centroids = np.insert(centroids, 0, [0, 0], axis=0)

    imgOverlay = np.copy(img_bgr)
    for cg in centroids:
        cv2.circle(imgOverlay, (int(cg[0]), int(cg[1])), 10, [0,0,255], -1)
    cv2.imwrite("blobImage_overlay.jpg", imgOverlay)
    
    return centroids
'''
# Example usage
image_path = 'PXL_20240328_182819987.jpg'
centroids = detect_blobs_with_simple_blob_detector(image_path)
print("Centroids:", centroids)

img = cv2.imread(image_path)

for cg in centroids:
    cv2.circle(img, (int(cg[0]), int(cg[1])), 10, [0,0,255], 2)

cv2.imwrite("test.jpg",img)
'''
