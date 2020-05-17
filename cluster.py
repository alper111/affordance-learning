import argparse
import os
import torch
import numpy as np
import utils

parser = argparse.ArgumentParser("Cluster effects.")
parser.add_argument("-ckpt", help="save path", type=str, required=True)
args = parser.parse_args()

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")

sorted_idx = torch.load("data/sorted_effidx.pt")
effects = torch.load("data/effects_2.pt").to(device)
effects = effects.abs()
eff_mu = effects.mean(dim=0)
eff_std = effects.std(dim=0)
effects = (effects - eff_mu) / (eff_std + 1e-6)

K = 6
centroids, assigns, mse, _ = utils.kmeans(effects, k=K)
centroids = centroids * (eff_std + 1e-6) + eff_mu
effect_names = []
for i, c_i in enumerate(centroids):
    print("Centroid %d: %.2f, %.2f, %.2f, %.2f, %.2f, %.2f" %
          (i, c_i[0], c_i[1], c_i[2], c_i[3], c_i[4], c_i[5]))

for i, c_i in enumerate(centroids):
    print("Centroid %d: %.2f, %.2f, %.2f, %.2f, %.2f, %.2f" %
          (i, c_i[0], c_i[1], c_i[2], c_i[3], c_i[4], c_i[5]))
    print("What is this effect?")
    print(">>>", end="")
    effect_names.append(input())
effect_names = np.array(effect_names)
print("Effect names are:")
print(effect_names)
torch.save(os.path.join(args.ckpt, "labels.pt"), assigns[sorted_idx].cpu())
