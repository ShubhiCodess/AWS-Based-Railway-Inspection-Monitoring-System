import torch
import torch.nn as nn


class EMA(nn.Module):
    """
    Lightweight attention block.
    Does NOT change tensor size.
    """

    def __init__(self, c1, c2=None):
        super().__init__()
        c = c1

        self.conv1 = nn.Conv2d(c, c, 1, bias=False)
        self.conv3 = nn.Conv2d(c, c, 3, padding=1, bias=False)
        self.bn = nn.BatchNorm2d(c)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        w = self.sigmoid(self.bn(self.conv1(x) + self.conv3(x)))
        return x * w