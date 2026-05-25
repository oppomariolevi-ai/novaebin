"""
Rete neurale Wide & Deep Novae su MNIST.
Dimostra il Capitolo 7 del Principia Novae Mathematicae v1.3.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import numpy as np
import matplotlib.pyplot as plt

# --- Layer Unipolare Novae Continuo ---
class LinearNovaeContinuo(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.5)
        self.bias = nn.Parameter(torch.randn(out_features) * 0.5)
        self.valori = torch.tensor([-10.0,-9,-8,-7,-6,-5,-4,-3,-2,-1,
                                     0.0,1,2,3,4,5,6,7,8,9,10.0])
    def forward(self, x):
        return nn.functional.linear(x, self.weight, self.bias)
    def reg_loss(self):
        w_flat = self.weight.view(-1)
        dist = torch.abs(w_flat.unsqueeze(1) - self.valori.to(w_flat.device))
        return dist.min(dim=1)[0].mean()

# --- Neurone Multipolare Icosaedrico ---
class IcosaNeuron(nn.Module):
    def __init__(self):
        super().__init__()
        self.vertex_weights = nn.Parameter(torch.randn(12) * 0.5)
        phi = (1 + np.sqrt(5)) / 2
        coords = np.array([
            [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
            [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
            [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
        ])
        coords = coords / np.linalg.norm(coords[0])
        edge_len = 1.05146
        self.adj = torch.zeros(12, 12)
        for i in range(12):
            for j in range(i+1, 12):
                if np.abs(np.linalg.norm(coords[i] - coords[j]) - edge_len) < 0.01:
                    self.adj[i, j] = 1.0; self.adj[j, i] = 1.0
        degree = self.adj.sum(dim=1, keepdim=True)
        degree[degree == 0] = 1.0
        self.register_buffer('adj_norm', self.adj / degree)
        in_mask = torch.zeros(12); out_mask = torch.zeros(12)
        in_mask[[0,1,4,5,9,11]] = 1.0
        out_mask[[3,2,6,7,8,10]] = 1.0
        self.register_buffer('in_mask', in_mask.bool())
        self.register_buffer('out_mask', out_mask.bool())
    def forward(self, x):
        batch = x.shape[0]
        state = torch.zeros(batch, 12, device=x.device)
        state[:, self.in_mask] = x
        for _ in range(3):
            state = torch.tanh(state @ self.adj_norm * self.vertex_weights.unsqueeze(0))
        return state[:, self.out_mask]

# --- Wide & Deep Novae ---
class WideDeepNovae(nn.Module):
    def __init__(self):
        super().__init__()
        self.wide_fc1 = LinearNovaeContinuo(784, 64)
        self.wide_fc2 = LinearNovaeContinuo(64, 10)
        self.deep_proj = nn.Linear(784, 6)
        self.deep_ico = IcosaNeuron()
        self.deep_fc = nn.Linear(6, 10)
        self.alpha = nn.Parameter(torch.tensor(0.5))
    def forward(self, x):
        x = x.view(x.size(0), -1)
        wide = torch.relu(self.wide_fc1(x))
        wide = self.wide_fc2(wide)
        deep = torch.tanh(self.deep_proj(x))
        deep = self.deep_ico(deep)
        deep = self.deep_fc(deep)
        return self.alpha * wide + (1 - self.alpha) * deep

# --- Rete Classica ---
class ClassicNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 64)
        self.fc2 = nn.Linear(64, 10)
    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x.view(x.size(0), -1))))

# --- Caricamento dati ---
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_data = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=1000)

# --- Addestramento ---
def allena_e_valuta(modello, epochs=5, use_reg=False):
    optimizer = optim.Adam(modello.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()
    storia = []
    for ep in range(epochs):
        modello.train()
        for Xb, yb in train_loader:
            optimizer.zero_grad()
            out = modello(Xb)
            loss = loss_fn(out, yb)
            if use_reg:
                loss += 0.0005 * (modello.wide_fc1.reg_loss() + modello.wide_fc2.reg_loss())
            loss.backward()
            optimizer.step()
        modello.eval()
        corr, tot = 0, 0
        with torch.no_grad():
            for Xb, yb in test_loader:
                pred = modello(Xb).argmax(dim=1)
                corr += (pred == yb).sum().item()
                tot += yb.size(0)
        storia.append(corr / tot)
        print(f"Epoca {ep+1}: {storia[-1]:.4f}")
    return storia

print("Allenamento ClassicNet...")
storia_c = allena_e_valuta(ClassicNet())
print("Allenamento Wide+Deep Novae...")
storia_n = allena_e_valuta(WideDeepNovae(), use_reg=True)

# Grafico
plt.plot(storia_c, label='ClassicNet', color='red', marker='o')
plt.plot(storia_n, label='Wide+Deep Novae', color='green', marker='s')
plt.xlabel('Epoca'); plt.ylabel('Accuratezza'); plt.legend()
plt.title('MNIST: ClassicNet vs Wide+Deep Novae')
plt.grid(True); plt.show()
print(f"ClassicNet finale: {storia_c[-1]:.4f}")
print(f"Wide+Deep Novae finale: {storia_n[-1]:.4f}")
