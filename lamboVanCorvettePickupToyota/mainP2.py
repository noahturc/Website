print('hi main P2')
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
print('line 4')
from PIL import Image
import torchvision.transforms.functional as TF
#import matplotlib.pyplot as plt
from torch import nn
import torch
print('import torch ran')
#from sklearn.model_selection import KFold as kfold
from sklearn.model_selection import KFold
from torch.utils.data import SubsetRandomSampler, DataLoader
import torch.nn.functional as F
#from helper_functions import accuracy_fn
import os
print('all imports ran')

try:
    car_photos_path = os.path.join(os.path.dirname(__file__), "carPhotos")
    folder_path = car_photos_path  # Path to the folder with car models (classes)
except:
    folder_path = r'carPhotos'
    
# Walk through the folder and all subfolders
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith('.jfif'):  # Check for JFIF files
            file_path = os.path.join(root, file)
            img = Image.open(file_path)
            img = img.convert('RGB')  # Convert to RGB format
            new_file_path = file_path.replace('.jfif', '.jpg')
            img.save(new_file_path, 'JPEG')  # Save as JPEG

#import deleteDuplicatePhotos
breakpoint = 0


# Make all images 224 by 224 and filled with padding if necessary
def pad_to_square(image):
    width, height = image.size
    padding = (0, 0, 0, 0)
    if width != height:
        diff = abs(width - height)
        if width > height:
            padding = (0, diff // 2, 0, diff - diff // 2)
        else:
            padding = (diff // 2, 0, diff - diff // 2, 0)

    return TF.pad(image, padding, fill=0, padding_mode='constant')

transform = transforms.Compose([
        transforms.Resize(224),
        transforms.Lambda(pad_to_square),  # Pad dynamically to make the image square
        transforms.Resize((224, 224)),      # Resize to the final size
        transforms.ToTensor()
    ])


# Load the dataset from the folder
trainData = datasets.ImageFolder(root=folder_path, transform=transform, allow_empty=True)
# DataLoader for batching and shuffling
#trainDataloader = DataLoader(dataset=trainData, batch_size=8, shuffle=True)

classNames = trainData.classes



class carModelDetectorLinearModel(nn.Module):
    def __init__(self, inputShape : int, hiddenUnits: int, outputShape: int):
        super().__init__()
        self.layerStack = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=inputShape, out_features=hiddenUnits),
            nn.Linear(in_features=hiddenUnits, out_features=outputShape)
        )

    def forward(self, x):
        #print(self.layerStack(x))
        return self.layerStack(x)
    
    def predict(self, imagePath):
        # Set model to evaluation mode
        self.eval()
        
        # Load the image from the path
        image = Image.open(imagePath).convert('RGB')  # Convert to RGB in case it's grayscale
        
        # Apply the same transformations used during training
        transformed_image = transform(image)  # 'transform' should be the same one you used in ImageFolder
        
        # Add batch dimension (batch_size=1)
        transformed_image = transformed_image.unsqueeze(0)
        
        # Pass the image through the model
        with torch.no_grad():
            output = self.forward(transformed_image)

            confidenceLevels = F.softmax(output, dim=1)
            
            # Get the predicted class
            prediction = torch.argmax(output, dim=1)
            labelPrediction = classNames[prediction.item()]
            
            confidenceList = []
            for idx, confidence in enumerate(confidenceLevels[0]):
                label, probability = classNames[idx], confidence.item()
                probability = probability * 100
                probability = "{:.2f}".format(probability)
                d = {label: probability+'%'} 
                confidenceList.append(d)

            confidenceList = sorted(confidenceList, key=lambda x: float(list(x.values())[0].replace('%', '')), reverse=True)

        print(f'Linear prediction: {labelPrediction}\nConfidence: {confidenceList}')
        #x = [labelPrediction, confidenceList]
        return labelPrediction, confidenceList


print('end of mainP2')

if __name__ == '__main__':

#    linearModel = carModelDetectorLinearModel(inputShape=224*224*3, hiddenUnits=32, outputShape=len(classNames))
    #print('\n', linearModel.state_dict())


#    lossFn = nn.CrossEntropyLoss()                                              # measures how wrong the model is
#    linearOptimizer = torch.optim.SGD(params=linearModel.parameters())          # updates the model's parameters to reduce the loss

    def accuracy_fn(y_true, y_pred):
        if y_pred.ndim == 1:  # if y_pred is already 1D
            correct = (y_pred == y_true).sum().item()
        else:
            correct = (y_pred.argmax(dim=1) == y_true).sum().item()
        accuracy = correct / len(y_true)
        return accuracy

    def trainStep(model, optimizer, trainDataloader, lossFn):
        trainLoss, trainAcc = 0, 0
        model.train()
        for batch, (X, y) in enumerate(trainDataloader):
            y_pred = model(X)
            loss = lossFn(y_pred, y)
            trainLoss += loss.item()
            trainAcc += accuracy_fn(y_true=y, y_pred=y_pred.argmax(dim=1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        trainLoss /= len(trainDataloader)
        trainAcc /= len(trainDataloader)
        print(f'Train loss: {trainLoss:.5f} | Train accuracy: {trainAcc}')


    def testStep(model, valDataloader, lossFn):
        valLoss, valAcc = 0, 0
        model.eval()
        with torch.no_grad():
            for X, y in valDataloader:
                y_pred = model(X)
                loss = lossFn(y_pred, y)
                valLoss += loss.item()
                valAcc += accuracy_fn(y_true=y, y_pred=y_pred.argmax(dim=1))
        valLoss /= len(valDataloader)
        valAcc /= len(valDataloader)
        print(f'Validation loss: {valLoss:.5f} | Validation accuracy: {valAcc}')
        return valLoss, valAcc








    epochs = 20
    k_folds = 3
    #torch.manual_seed(42)  # For reproducibility

    # Prepare the k-fold cross-validation
    kfold = KFold(n_splits=k_folds, shuffle=True)

    # Start print
    print('--------------------------------')

    # K-fold Cross Validation model evaluation
    for fold, (train_ids, val_ids) in enumerate(kfold.split(trainData)):
        print(f'FOLD {fold + 1}')
        print('--------------------------------')

        # Sample elements randomly from a given list of ids
        train_subsampler = SubsetRandomSampler(train_ids)
        val_subsampler = SubsetRandomSampler(val_ids)

        # Define data loaders for training and validation
        trainDataloader = DataLoader(
            trainData,
            batch_size=8,
            sampler=train_subsampler
        )
        valDataloader = DataLoader(
            trainData,
            batch_size=8,
            sampler=val_subsampler
        )

        # Initialize the model and optimizer for each fold
        model = carModelDetectorLinearModel(inputShape=224*224*3, hiddenUnits=32, outputShape=len(classNames))
        optimizer = torch.optim.SGD(params=model.parameters())

        # Initialize the loss function
        lossFn = nn.CrossEntropyLoss()

        # Training loop
        for epoch in range(epochs):
            print(f'Epoch: {epoch + 1}/{epochs}')
            trainStep(model=model, optimizer=optimizer, trainDataloader=trainDataloader, lossFn=lossFn)
            testStep(model=model, valDataloader=valDataloader, lossFn=lossFn)

        # Optionally, save the model for each fold
#        torch.save(model.state_dict(), f'linearModel_fold{fold + 1}.pt')
        print('--------------------------------')