import torch
import torch.nn as nn


class SPDConv(nn.Module):
    """
    Space-to-Depth Conv used as stride-2 replacement
    Compatible with Ultralytics parser.
    """

    def __init__(self, c1, c2, k=3, s=1, p=1, scale=2):
        super().__init__()
        self.scale = scale

        # after space-to-depth channels increase
        self.conv = nn.Conv2d(c1 * (scale ** 2), c2, k, s, p, bias=False)
        self.bn = nn.BatchNorm2d(c2)
        self.act = nn.SiLU()

    def forward(self, x):
        b, c, h, w = x.shape

        # space-to-depth
        x = x.view(b, c, h // 2, 2, w // 2, 2)
        x = x.permute(0, 1, 3, 5, 2, 4).contiguous()
        x = x.view(b, c * 4, h // 2, w // 2)

        return self.act(self.bn(self.conv(x)))