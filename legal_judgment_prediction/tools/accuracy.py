import logging
import torch

logger = logging.Logger(__name__)


def get_prf(resource):
    # According to https://github.com/dice-group/gerbil/wiki/Precision,-Recall-and-F1-measure

    if resource['TP'] == 0:
        if resource['FP'] == 0 and resource['FN'] == 0:
            precision = 1.0
            recall = 1.0
            f1 = 1.0
        else:
            precision = 0.0
            recall = 0.0
            f1 = 0.0
    else:
        precision = 1.0 * resource['TP'] / (resource['TP'] + resource['FP'])
        recall = 1.0 * resource['TP'] / (resource['TP'] + resource['FN'])
        f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1


def get_micro_macro_prf(resources):
    precision = []
    recall = []
    f1 = []

    total = {'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0}

    for resource in range(0, len(resources)):
        total['TP'] += resources[resource]['TP']
        total['FP'] += resources[resource]['FP']
        total['FN'] += resources[resource]['FN']
        total['TN'] += resources[resource]['TN']

        p, r, f = get_prf(resources[resource])

        precision.append(p)
        recall.append(r)
        f1.append(f)

    micro_precision, micro_recall, micro_f1 = get_prf(total)

    macro_precision = 0
    macro_recall = 0
    macro_f1 = 0

    for index in range(0, len(f1)):
        macro_precision += precision[index]
        macro_recall += recall[index]
        macro_f1 += f1[index]

    macro_precision /= len(f1)
    macro_recall /= len(f1)
    macro_f1 /= len(f1)

    return {
        'mip': round(micro_precision, 3),
        'mir': round(micro_recall, 3),
        'mif': round(micro_f1, 3),
        'map': round(macro_precision, 3),
        'mar': round(macro_recall, 3),
        'maf': round(macro_f1, 3)
    }


# def null_accuracy_function(outputs, label, config, result=None):
#     return None


# def log_distance_accuracy_function(outputs, label, config, result=None):
#     if result is None:
#         result = [0, 0]

#     result[0] += outputs.size()[0]
#     result[1] += float(torch.sum(torch.log(torch.abs(torch.clamp(outputs, 0, 450) - torch.clamp(label, 0, 450)) + 1)))

#     return result


# def single_label_top1_accuracy(outputs, label, config, result=None):
#     if result is None:
#         result = []

#     id1 = torch.max(outputs, dim=1)[1]
#     id2 = label

#     nr_classes = outputs.size(1)

#     while len(result) < nr_classes:
#         result.append({'TP': 0, 'FN': 0, 'FP': 0, 'TN': 0})

#     for a in range(0, len(id1)):
#         it_is = int(id1[a])
#         should_be = int(id2[a])

#         if it_is == should_be:
#             result[it_is]['TP'] += 1
#         else:
#             result[it_is]['FP'] += 1
#             result[should_be]['FN'] += 1

#     return result


def multi_label_accuracy(outputs, label, config, result=None):
    if len(label[0]) != len(outputs[0]):
        raise ValueError('Input dimensions of labels and outputs must match.')

    if len(outputs.size()) > 2:
        outputs = outputs.view(outputs.size()[0], -1, 2)
        outputs = torch.nn.Softmax(dim=2)(outputs)
        outputs = outputs[:, :, 1]

    outputs = outputs.data
    labels = label.data

    if result is None:
        result = []

    total = 0
    nr_classes = outputs.size(1)

    while len(result) < nr_classes:
        result.append({'TP': 0, 'FN': 0, 'FP': 0, 'TN': 0})

    for i in range(nr_classes):
        outputs1 = (outputs[:, i] >= 0.5).long()
        labels1 = (labels[:, i].float() >= 0.5).long()
        total += int((labels1 * outputs1).sum())
        total += int(((1 - labels1) * (1 - outputs1)).sum())

        if result is None:
            continue

        result[i]['TP'] += int((labels1 * outputs1).sum())
        result[i]['FN'] += int((labels1 * (1 - outputs1)).sum())
        result[i]['FP'] += int(((1 - labels1) * outputs1).sum())
        result[i]['TN'] += int(((1 - labels1) * (1 - outputs1)).sum())

    return result
