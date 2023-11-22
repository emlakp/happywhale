from torchvision import models
import torch
import torchvision
from utils import *
from torchvision.models._api import WeightsEnum
from torch.hub import load_state_dict_from_url


def get_state_dict(self, *args, **kwargs):
    kwargs.pop("check_hash")
    return load_state_dict_from_url(self.url, *args, **kwargs)


def weights_init_normal(model):
    classnames = model.__class__.__name__
    if classnames.find('Linear'):
        y = model.in_features
        model.weight.data.normal(0.0, 1 / np.sqrt(y))
        model.bias.data.fill_(0)


WeightsEnum.get_state_dict = get_state_dict


def effnet(
        model_str='efficientnet_b3',
        pretrained=True,
        frozen=True,
        device='cpu'):

    model = torchvision.models.get_model(model_str, pretrained=pretrained)
    model.classifier[1] = torch.nn.Linear(1536, 28)
    model.classifier[1].apply(weights_init_normal)

    if frozen:
        for layer in model.parameters():
            layer.requires_grad = False

        model.classifier[1].weight.requires_grad = True
        model.classifier[1].bias.requires_grad = True

    return model.to(device)