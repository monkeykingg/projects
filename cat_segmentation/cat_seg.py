import glob
from torchvision import datasets, transforms
import cv2
from PIL import Image
import torch
import torch.backends.cudnn as cudnn
from tqdm import tqdm
import random
import numpy as np
from torch import nn

train_input_path = glob.glob("./cat_data/Train/input/*.jpg")
train_input_path.sort()
train_mask_path = glob.glob("./cat_data/Train/mask/*.jpg")
train_mask_path.sort()

test_input_path = glob.glob("./cat_data/Test/input/*.jpg")
test_input_path.sort()
test_mask_path = glob.glob("./cat_data/Test/mask/*.jpg")
test_mask_path.sort()


transfer_train_input_path = glob.glob("./images/*.jpg")
transfer_train_input_path.sort()
transfer_train_mask_path = glob.glob("./annotations/trimaps/*.png")
transfer_train_mask_path.sort()

transform = transforms.Compose([transforms.ToPILImage(),
                                transforms.Resize((128, 128)),
                                transforms.ToTensor()])

def load_transform_dataset(input_path, mask_path, transform):
    images = []
    masks = []
    size = 0
    corrupted_index = []
    print("original number of images = ", len(input_path), ", original number of masks = ", len(mask_path))

    for imagepath in input_path:
        size = size + 1
        color_img = cv2.imread(str(imagepath))
        if color_img is None:
            index = input_path.index(imagepath)
            corrupted_index.append(index)
            continue
        color_img = transform(color_img)
        images.append(color_img)

    for maskpath in mask_path:
        img = cv2.imread(str(maskpath))
        mask_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask_img = transform(mask_img)
        masks.append(mask_img)

    for index in sorted(corrupted_index, reverse=True):
        del masks[index]

    size = size - len(corrupted_index)

    print("number of images = ", len(images), ", number of masks = ", len(masks), ", size = ",  size)
    return images, masks, size

def load_dataset(input_path, mask_path):
    images = []
    masks = []
    size = 0

    for imagepath in input_path:
        size = size + 1
        color_img = cv2.imread(str(imagepath))
        images.append(color_img)

    for imagepath in mask_path:
        img = cv2.imread(str(imagepath))
        mask_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        masks.append(mask_img)

    return images, masks, size

def load_transfer_dataset(input_path, mask_path, transform):
    images = []
    masks = []
    size = 0
    corrupted_index = []
    print("original number of images = ", len(input_path), ", original number of masks = ", len(mask_path))

    for imagepath in input_path:
        size = size + 1
        color_img = cv2.imread(str(imagepath))
        if color_img is None:
            index = input_path.index(imagepath)
            corrupted_index.append(index)
            continue
        color_img = transform(color_img)
        images.append(color_img)

    for imagepath in mask_path:
        mask = Image.open(imagepath).convert("L")
        mask = np.array(mask)
        mask = (mask == 1)
        mask = (mask * 255).astype("uint8")
        mask_img = transform(mask)
        masks.append(mask_img)

    for index in sorted(corrupted_index, reverse=True):
        del masks[index]

    size = size - len(corrupted_index)

    print("number of images = ", len(images), ", number of masks = ", len(masks), ", size = ",  size)

    return images, masks, size


class MyDataset:

    def __init__(self, inputs, masks, size):
        self.inputs = inputs
        self.masks = masks
        self.len = size

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        return self.inputs[idx], self.masks[idx].float()


class MyAugmentDataset:

    def __init__(self, inputs, masks, size, transform):
        self.inputs = inputs
        self.masks = masks
        self.len = size
        self.transform = transform

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        image = self.inputs[idx]
        mask = self.masks[idx]
        seed = np.random.randint(0, 2147483640)
        random.seed(seed)
        image = self.transform(image)
        random.seed(seed)
        mask = self.transform(mask)
        return image, mask.float()


class DoubleConv(nn.Module):

    def __init__(self, in_ch, out_ch):
        super(DoubleConv, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),

            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.conv(x)


class UNet(nn.Module):

    def __init__(self, in_ch=3, out_ch=1):
        super(UNet, self).__init__()

        self.conv1 = DoubleConv(in_ch, 64)
        self.pool1 = nn.MaxPool2d(2)

        self.conv2 = DoubleConv(64, 128)
        self.pool2 = nn.MaxPool2d(2)

        self.conv3 = DoubleConv(128, 256)
        self.pool3 = nn.MaxPool2d(2)

        self.conv4 = DoubleConv(256, 512)
        self.pool4 = nn.MaxPool2d(2)

        self.conv5 = DoubleConv(512, 1024)

        self.up6 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.conv6 = DoubleConv(1024, 512)

        self.up7 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.conv7 = DoubleConv(512, 256)

        self.up8 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.conv8 = DoubleConv(256, 128)

        self.up9 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.conv9 = DoubleConv(128, 64)

        self.conv10 = nn.Conv2d(64, out_ch, 1)

    def forward(self, x):
        c1 = self.conv1(x)
        p1 = self.pool1(c1)

        c2 = self.conv2(p1)
        p2 = self.pool2(c2)

        c3 = self.conv3(p2)
        p3 = self.pool3(c3)

        c4 = self.conv4(p3)
        p4 = self.pool4(c4)

        c5 = self.conv5(p4)

        up_6 = self.up6(c5)
        merge6 = torch.cat([up_6, c4], dim=1)
        c6 = self.conv6(merge6)

        up_7 = self.up7(c6)
        merge7 = torch.cat([up_7, c3], dim=1)
        c7 = self.conv7(merge7)

        up_8 = self.up8(c7)
        merge8 = torch.cat([up_8, c2], dim=1)
        c8 = self.conv8(merge8)

        up_9 = self.up9(c8)
        merge9 = torch.cat([up_9, c1], dim=1)
        c9 = self.conv9(merge9)

        c10 = self.conv10(c9)

        out = nn.Sigmoid()(c10)

        return out


class DiceLoss(nn.Module):
    def __init__(self):
        super(DiceLoss, self).__init__()

    def forward(self, input, target):
        smooth = 1.

        iflat = input.view(-1)
        tflat = target.view(-1)
        intersection = (iflat * tflat).sum()

        return 1 - ((2. * intersection + smooth) /
                    ((iflat * iflat).sum() + (tflat * tflat).sum() + smooth))


def loss_function(loss):
    if loss == 'ce':
        BCE_loss = nn.BCELoss()
        return BCE_loss
    elif loss == 'dice':
        dice_loss = DiceLoss()
        return dice_loss


def train(net, trainloader, epochs=15, loss_fun='dice'):

    if torch.cuda.is_available():
        net = net.cuda()

    criterion = loss_function(loss_fun)
    optimizer = torch.optim.Adam(net.parameters())

    net.train()

    for e in range(epochs):

        running_loss = 0

        for images, labels in tqdm(trainloader):
            if torch.cuda.is_available():
                images = images.cuda()
                labels = labels.cuda()

            log_ps = net(images)
            loss = criterion(log_ps, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += float(loss.cpu().detach().data)

        else:
            print(f"Training loss: {running_loss / len(trainloader)}")


def test(net, testloader, loss_fun='dice'):

    net.eval()
    if torch.cuda.is_available():
        net = net.cuda()

    accuracy = 0
    result = []

    criterion = loss_function(loss_fun)

    for images, labels in testloader:
        if torch.cuda.is_available():
            images = images.cuda()
            labels = labels.cuda()

        log_ps = net(images)
        loss = criterion(log_ps, labels)

        accuracy += 1 - loss

        result.append([log_ps, images, labels])

    print("Test Accuracy: {:.3f}".format(accuracy / len(testloader)))

    return result

if __name__=='__main__':

    torch.backends.cudnn.benchmark = True
    torch.cuda.empty_cache()
    # os.environ['CUDA_VISIBLE_DEVICES'] = '0, 1, 2'

    # train_inputs, train_masks, train_size = load_transform_dataset(train_input_path, train_mask_path, transform)
    # transfer_train_inputs, transfer_train_masks, transfer_train_size = load_transform_dataset(transfer_train_input_path, transfer_train_mask_path, transform)
    transfer_train_inputs, transfer_train_masks, transfer_train_size = load_transfer_dataset(transfer_train_input_path,
                                                                                             transfer_train_mask_path,
                                                                                             transform)
    test_inputs, test_masks, test_size = load_transform_dataset(test_input_path, test_mask_path, transform)

    # train_inputs, train_masks, train_size = load_dataset(train_input_path, train_mask_path)
    # train_data = MyAugmentDataset(train_inputs, train_masks, train_size, all_transform)

    # train_data = MyDataset(train_inputs, train_mask, train_size)
    train_data = MyDataset(transfer_train_inputs, transfer_train_masks, transfer_train_size)
    test_data = MyDataset(test_inputs, test_masks, test_size)

    trainloader = torch.utils.data.DataLoader(train_data, batch_size=64, shuffle=True, pin_memory=True)
    testloader = torch.utils.data.DataLoader(test_data, batch_size=1, shuffle=True)

#    dataiter = iter(trainloader)
#    images, labels = dataiter.next()
#    print(labels.shape)
#    cv2.imwrite("./img0.jpg", imshow(images[0]))
#    cv2.imwrite("./lab0.jpg", imshow(labels[0]))

    transfer_learning_net = UNet()
    if torch.cuda.is_available():
        transfer_learning_net = transfer_learning_net.cuda()
    # transfer_learning_net.load_state_dict(torch.load("./tf_model_post.pt"))

    # net = UNet()
    # if torch.cuda.is_available():
    #     net = net.cuda()

    # train(net, trainloader)
    # te_result = test(net, testloader)

    train(transfer_learning_net, trainloader)
    torch.save(transfer_learning_net.state_dict(), "./my_net.pt")
    te_result = test(transfer_learning_net, testloader)

    cv2.imwrite("./real_mask.jpg", te_result[0][2].cpu().squeeze().numpy()*255)
    cv2.imwrite("./prediction.jpg", te_result[0][0].cpu().squeeze().detach().numpy()*255)
    cv2.imwrite("./real_image.jpg", te_result[0][1].cpu().squeeze().permute(1, 2, 0).numpy() * 255)