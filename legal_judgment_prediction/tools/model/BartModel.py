import torch.nn as nn
from transformers import BartForConditionalGeneration


class BartModel(nn.Module):
    def __init__(self, config, *args, **kwargs):
        super(BartModel, self).__init__()

        self.bart = BartForConditionalGeneration.from_pretrained(config.get('model', 'bart_path'))


    # def forward(self, input):
    def forward(self, input, label, *args, **kwargs):
        # output = self.bart(input)
        loss = self.bart(input_ids=input, labels=label)['loss']
        tensors = self.bart.generate(input)

        return loss, tensors


    def generate(self, input, *args, **kwargs):
        output = self.bart.generate(input)

        return output