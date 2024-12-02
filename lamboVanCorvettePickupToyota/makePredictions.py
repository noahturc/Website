print('hi makePredictions')
import torch
from mainP2 import carModelDetectorLinearModel, classNames  # Import the correct model class



# Instantiate the same model used when saving
model = carModelDetectorLinearModel(inputShape=224*224*3, hiddenUnits=32, outputShape=len(classNames))
model.load_state_dict(torch.load('linearModel_fold3.pt'))

#print(model.state_dict)

def makePrediction(image):
    prediction = model.predict(image)
    print('hi makePred fn')
    return prediction


#x = makePrediction(testingImage)
#print(x)

#image_data = mpimg.imread(testingImage)
#plt.imshow(image_data)
#plt.title("Original Image")
#plt.show()