
import torch
import torch.nn as nn
import torch.optim as optim

# 定义一个简单的前馈神经网络
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# 示例参数
input_size = 10
hidden_size = 20
output_size = 2

# 实例化网络
model = SimpleNet(input_size, hidden_size, output_size)

# 损失函数和优化器
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 随机生成输入和目标数据
inputs = torch.randn(5, input_size)
targets = torch.randn(5, output_size)

# 前向传播
outputs = model(inputs)
loss = criterion(outputs, targets)

# 反向传播和优化
optimizer.zero_grad()
loss.backward()
optimizer.step()
print("Loss:", loss.item())