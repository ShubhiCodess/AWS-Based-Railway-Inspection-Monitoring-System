import torch.nn as nn
from ultralytics.nn.modules.block import C2f
from ultralytics.nn.modules.ema import EMA


class C2fEMA(nn.Module):
    """
    C2f block followed by EMA attention.
    Keeps SAME output shape → YOLO neck safe.
    """

    def __init__(self, c1, c2, n=1, shortcut=True):
        super().__init__()
        self.block = C2f(c1, c2, n, shortcut)
        self.attn = EMA(c2, c2)

    def forward(self, x):
        x = self.block(x)
        return self.attn(x)