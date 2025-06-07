import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import heapq
from dataclasses import dataclass
from typing import List, Dict, Optional
import random

@dataclass
class Customer:
    """顾客类"""
    id: int
    arrival_time: float
    service_start_time: Optional[float] = None
    departure_time: Optional[float] = None
    current_station: int = 0
    
    @property
    def waiting_time(self) -> float:
        if self.service_start_time is None:
            return 0
        return self.service_start_time - self.arrival_time
    
    @property
    def service_time(self) -> float:
        if self.service_start_time is None or self.departure_time is None:
            return 0
        return self.departure_time - self.service_start_time
    
    @property
    def total_time(self) -> float:
        if self.departure_time is None:
            return 0
        return self.departure_time - self.arrival_time

class ServiceStation:
    """服务台类"""
    def __init__(self, station_id: int, num_servers: int, service_rate: float):
        self.station_id = station_id
        self.num_servers = num_servers
        self.service_rate = service_rate  # 服务率（每小时服务的顾客数）
        self.queue = deque()  # 等待队列
        self.servers = [None] * num_servers  # 服务器状态
        self.total_customers_served = 0
        self.total_waiting_time = 0
        self.total_service_time = 0
    
    def is_server_available(self) -> bool:
        """检查是否有空闲服务器"""
        return None in self.servers
    
    def get_available_server(self) -> Optional[int]:
        """获取空闲服务器编号"""
        for i, server in enumerate(self.servers):
            if server is None:
                return i
        return None
    
    def add_customer(self, customer: Customer):
        """添加顾客到队列"""
        self.queue.append(customer)
    
    def start_service(self, customer: Customer, current_time: float) -> float:
        """开始服务，返回服务完成时间"""
        server_id = self.get_available_server()
        if server_id is not None:
            self.servers[server_id] = customer
            customer.service_start_time = current_time
            # 服务时间服从指数分布
            service_duration = np.random.exponential(1.0 / self.service_rate)
            completion_time = current_time + service_duration
            return completion_time
        return float('inf')
    
    def complete_service(self, customer: Customer, completion_time: float):
        """完成服务"""
        customer.departure_time = completion_time
        # 释放服务器
        for i, server_customer in enumerate(self.servers):
            if server_customer == customer:
                self.servers[i] = None
                break
        
        # 更新统计数据
        self.total_customers_served += 1
        self.total_waiting_time += customer.waiting_time
        self.total_service_time += customer.service_time
    
    @property
    def queue_length(self) -> int:
        return len(self.queue)
    
    @property
    def utilization(self) -> float:
        """服务台利用率"""
        busy_servers = sum(1 for server in self.servers if server is not None)
        return busy_servers / self.num_servers
    
    @property
    def average_waiting_time(self) -> float:
        if self.total_customers_served == 0:
            return 0
        return self.total_waiting_time / self.total_customers_served

class QueueingNetwork:
    """排队网络模型"""
    def __init__(self):
        self.stations: Dict[int, ServiceStation] = {}
        self.routing_matrix: Dict[int, Dict[int, float]] = {}  # 路由概率矩阵
        self.customers: List[Customer] = []
        self.event_queue = []  # 事件队列 (时间, 事件类型, 顾客, 服务台)
        self.current_time = 0.0
        self.customer_counter = 0
        
        # 统计数据
        self.arrival_times = []
        self.departure_times = []
        self.system_stats = {
            'total_arrivals': 0,
            'total_departures': 0,
            'total_system_time': 0
        }
    
    def add_station(self, station_id: int, num_servers: int, service_rate: float):
        """添加服务台"""
        self.stations[station_id] = ServiceStation(station_id, num_servers, service_rate)
        self.routing_matrix[station_id] = {}
    
    def set_routing_probability(self, from_station: int, to_station: int, probability: float):
        """设置路由概率"""
        self.routing_matrix[from_station][to_station] = probability
    
    def set_external_arrival_rate(self, station_id: int, arrival_rate: float):
        """设置外部到达率"""
        self.external_arrival_rate = {station_id: arrival_rate}
    
    def generate_arrivals(self, simulation_time: float):
        """生成外部到达事件"""
        for station_id, rate in self.external_arrival_rate.items():
            current_time = 0
            while current_time < simulation_time:
                # 泊松到达过程，时间间隔服从指数分布
                inter_arrival_time = np.random.exponential(1.0 / rate)
                current_time += inter_arrival_time
                if current_time < simulation_time:
                    heapq.heappush(self.event_queue, 
                                 (current_time, 'arrival', None, station_id))
    
    def schedule_event(self, time: float, event_type: str, customer: Customer, station_id: int):
        """调度事件"""
        heapq.heappush(self.event_queue, (time, event_type, customer, station_id))
    
    def process_arrival(self, station_id: int):
        """处理到达事件"""
        self.customer_counter += 1
        customer = Customer(id=self.customer_counter, 
                          arrival_time=self.current_time,
                          current_station=station_id)
        self.customers.append(customer)
        self.system_stats['total_arrivals'] += 1
        self.arrival_times.append(self.current_time)
        
        station = self.stations[station_id]
        
        if station.is_server_available():
            # 直接开始服务
            completion_time = station.start_service(customer, self.current_time)
            self.schedule_event(completion_time, 'departure', customer, station_id)
        else:
            # 加入等待队列
            station.add_customer(customer)
    
    def process_departure(self, customer: Customer, station_id: int):
        """处理离开事件"""
        station = self.stations[station_id]
        station.complete_service(customer, self.current_time)
        
        # 检查是否有等待的顾客
        if station.queue:
            next_customer = station.queue.popleft()
            completion_time = station.start_service(next_customer, self.current_time)
            self.schedule_event(completion_time, 'departure', next_customer, station_id)
        
        # 根据路由概率决定下一个服务台
        next_station = self.get_next_station(station_id)
        
        if next_station is not None:
            # 转移到下一个服务台
            customer.current_station = next_station
            self.schedule_event(self.current_time, 'arrival_internal', customer, next_station)
        else:
            # 离开系统
            self.system_stats['total_departures'] += 1
            self.system_stats['total_system_time'] += customer.total_time
            self.departure_times.append(self.current_time)
    
    def process_internal_arrival(self, customer: Customer, station_id: int):
        """处理内部到达事件"""
        station = self.stations[station_id]
        
        if station.is_server_available():
            completion_time = station.start_service(customer, self.current_time)
            self.schedule_event(completion_time, 'departure', customer, station_id)
        else:
            station.add_customer(customer)
    
    def get_next_station(self, current_station: int) -> Optional[int]:
        """根据路由概率获取下一个服务台"""
        probabilities = self.routing_matrix[current_station]
        if not probabilities:
            return None
        
        rand = random.random()
        cumulative_prob = 0
        
        for next_station, prob in probabilities.items():
            cumulative_prob += prob
            if rand <= cumulative_prob:
                return next_station
        
        return None
    
    def run_simulation(self, simulation_time: float):
        """运行仿真"""
        print(f"开始仿真，仿真时间: {simulation_time}")
        
        # 生成外部到达事件
        self.generate_arrivals(simulation_time)
        
        # 处理事件
        while self.event_queue and self.event_queue[0][0] <= simulation_time:
            event_time, event_type, customer, station_id = heapq.heappop(self.event_queue)
            self.current_time = event_time
            
            if event_type == 'arrival':
                self.process_arrival(station_id)
            elif event_type == 'departure':
                self.process_departure(customer, station_id)
            elif event_type == 'arrival_internal':
                self.process_internal_arrival(customer, station_id)
        
        self.print_results()
        self.plot_results()
    
    def print_results(self):
        """输出仿真结果"""
        print("\n=== 仿真结果 ===")
        print(f"总到达顾客数: {self.system_stats['total_arrivals']}")
        print(f"总离开顾客数: {self.system_stats['total_departures']}")
        
        if self.system_stats['total_departures'] > 0:
            avg_system_time = self.system_stats['total_system_time'] / self.system_stats['total_departures']
            print(f"平均系统时间: {avg_system_time:.2f}")
        
        print("\n各服务台统计:")
        for station_id, station in self.stations.items():
            print(f"服务台 {station_id}:")
            print(f"  服务顾客总数: {station.total_customers_served}")
            print(f"  平均等待时间: {station.average_waiting_time:.2f}")
            print(f"  当前队列长度: {station.queue_length}")
            print(f"  服务台利用率: {station.utilization:.2%}")
    
    def plot_results(self):
        """绘制结果图表"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        # 到达和离开时间分布
        ax1.hist(self.arrival_times, bins=50, alpha=0.7, label='到达时间', color='blue')
        ax1.hist(self.departure_times, bins=50, alpha=0.7, label='离开时间', color='red')
        ax1.set_xlabel('时间')
        ax1.set_ylabel('频次')
        ax1.set_title('到达和离开时间分布')
        ax1.legend()
        
        # 各服务台队列长度
        station_ids = list(self.stations.keys())
        queue_lengths = [self.stations[sid].queue_length for sid in station_ids]
        ax2.bar(station_ids, queue_lengths, color='green')
        ax2.set_xlabel('服务台ID')
        ax2.set_ylabel('队列长度')
        ax2.set_title('各服务台当前队列长度')
        
        # 各服务台利用率
        utilizations = [self.stations[sid].utilization for sid in station_ids]
        ax3.bar(station_ids, utilizations, color='orange')
        ax3.set_xlabel('服务台ID')
        ax3.set_ylabel('利用率')
        ax3.set_title('各服务台利用率')
        ax3.set_ylim(0, 1)
        
        # 顾客系统时间分布
        completed_customers = [c for c in self.customers if c.departure_time is not None]
        system_times = [c.total_time for c in completed_customers]
        if system_times:
            ax4.hist(system_times, bins=30, color='purple', alpha=0.7)
            ax4.set_xlabel('系统时间')
            ax4.set_ylabel('频次')
            ax4.set_title('顾客系统时间分布')
        
        plt.tight_layout()
        plt.show()

def main():
    """主函数 - 示例使用"""
    # 创建排队网络
    network = QueueingNetwork()
    
    # 添加服务台
    network.add_station(1, num_servers=2, service_rate=3.0)  # 服务台1：2个服务器，服务率3/小时
    network.add_station(2, num_servers=1, service_rate=2.0)  # 服务台2：1个服务器，服务率2/小时
    network.add_station(3, num_servers=1, service_rate=4.0)  # 服务台3：1个服务器，服务率4/小时
    
    # 设置路由概率
    network.set_routing_probability(1, 2, 0.6)  # 从服务台1到服务台2的概率为0.6
    network.set_routing_probability(1, 3, 0.4)  # 从服务台1到服务台3的概率为0.4
    # 服务台2和3完成服务后直接离开系统（不设置路由）
    
    # 设置外部到达率
    network.set_external_arrival_rate(1, 2.5)  # 到服务台1的到达率为2.5/小时
    
    # 运行仿真
    network.run_simulation(simulation_time=100.0)

if __name__ == "__main__":
    main()