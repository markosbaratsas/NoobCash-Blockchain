import matplotlib.pyplot as plt
import json


with open('results.json') as json_file:
    results = json.load(json_file)

capacity = [1, 5, 10]

block_time5n4d = []
block_time5n5d = []
block_time10n4d = []
block_time10n5d = []

throughput5n4d = []
throughput5n5d = []
throughput10n4d = []
throughput10n5d = []

for i in capacity:
    block_time5n4d.append(results[f"5_nodes_4_difficulty_{i}_capacity"]["block_time"])
    block_time5n5d.append(results[f"5_nodes_5_difficulty_{i}_capacity"]["block_time"])
    block_time10n4d.append(results[f"10_nodes_4_difficulty_{i}_capacity"]["block_time"])
    block_time10n5d.append(results[f"10_nodes_5_difficulty_{i}_capacity"]["block_time"])
    
    throughput5n4d.append(results[f"5_nodes_4_difficulty_{i}_capacity"]["throughput"])
    throughput5n5d.append(results[f"5_nodes_5_difficulty_{i}_capacity"]["throughput"])
    throughput10n4d.append(results[f"10_nodes_4_difficulty_{i}_capacity"]["throughput"])
    throughput10n5d.append(results[f"10_nodes_5_difficulty_{i}_capacity"]["throughput"])


plt.figure()
plt.title('Mean Block Time (5 nodes)')
plt.plot(block_time5n4d, marker="o", label='5 nodes, 4 difficulty', color="limegreen")
plt.plot(block_time5n5d, marker=".", label='5 nodes, 5 difficulty', color="royalblue")
plt.ylabel('Mean Block Time (sec)')
plt.xlabel('Capacity')
plt.xticks(range(len(capacity)), capacity)
plt.legend()
plt.savefig('plots/block_time5n.png', bbox_inches='tight')

plt.clf()


plt.figure()
plt.title('Mean Block Time (10 nodes)')
plt.plot(block_time10n4d, marker="v", label='10 nodes, 4 difficulty', color="tomato")
plt.plot(block_time10n5d, marker="^", label='10 nodes, 5 difficulty', color="orange")
plt.ylabel('Mean Block Time (sec)')
plt.xlabel('Capacity')
plt.xticks(range(len(capacity)), capacity)
plt.legend()
plt.savefig('plots/block_time10n.png', bbox_inches='tight')

plt.clf()


plt.figure()
plt.title('Throughput (5 nodes)')
plt.plot(throughput5n4d, marker="o", label='5 nodes, 4 difficulty', color="limegreen")
plt.plot(throughput5n5d, marker=".", label='5 nodes, 5 difficulty', color="royalblue")
plt.ylabel('Throughput')
plt.xlabel('Capacity')
plt.xticks(range(len(capacity)), capacity)
plt.legend()
plt.savefig('plots/throughput5n.png', bbox_inches='tight')

plt.clf()


plt.figure()
plt.title('Throughput (10 nodes)')
plt.plot(throughput10n4d, marker="v", label='10 nodes, 4 difficulty', color="tomato")
plt.plot(throughput10n5d, marker="^", label='10 nodes, 5 difficulty', color="orange")
plt.ylabel('Throughput')
plt.xlabel('Capacity')
plt.xticks(range(len(capacity)), capacity)
plt.legend()
plt.savefig('plots/throughput10n.png', bbox_inches='tight')


# ------------ Scalability ------------ #

number_of_nodes = [5, 10]

block_time4d01c = []
block_time5d01c = []
block_time4d05c = []
block_time5d05c = []
block_time4d10c = []
block_time5d10c = []

throughput4d01c = []
throughput5d01c = []
throughput4d05c = []
throughput5d05c = []
throughput4d10c = []
throughput5d10c = []

for i in number_of_nodes:
    block_time4d01c.append(results[f"{i}_nodes_4_difficulty_1_capacity"]["block_time"])
    block_time5d01c.append(results[f"{i}_nodes_5_difficulty_1_capacity"]["block_time"])
    block_time4d05c.append(results[f"{i}_nodes_4_difficulty_5_capacity"]["block_time"])
    block_time5d05c.append(results[f"{i}_nodes_5_difficulty_5_capacity"]["block_time"])
    block_time4d10c.append(results[f"{i}_nodes_4_difficulty_10_capacity"]["block_time"])
    block_time5d10c.append(results[f"{i}_nodes_5_difficulty_10_capacity"]["block_time"])
    
    throughput4d01c.append(results[f"{i}_nodes_4_difficulty_1_capacity"]["throughput"])
    throughput5d01c.append(results[f"{i}_nodes_5_difficulty_1_capacity"]["throughput"])
    throughput4d05c.append(results[f"{i}_nodes_4_difficulty_5_capacity"]["throughput"])
    throughput5d05c.append(results[f"{i}_nodes_5_difficulty_5_capacity"]["throughput"])
    throughput4d10c.append(results[f"{i}_nodes_4_difficulty_10_capacity"]["throughput"])
    throughput5d10c.append(results[f"{i}_nodes_5_difficulty_10_capacity"]["throughput"])


# Block time Scalability

plt.clf()

plt.figure()
plt.title('Block time scalability (difficulty 4)')
plt.plot(block_time4d01c, marker="v", label='1 capacity', color="tomato")
plt.plot(block_time4d05c, marker="o", label='5 capacity', color="limegreen")
plt.plot(block_time4d10c, marker=".", label='10 capacity', color="royalblue")
plt.ylabel('Block time (sec)')
plt.xlabel('Number of nodes')
plt.xticks(range(len(number_of_nodes)), number_of_nodes)
plt.legend()
plt.savefig('plots/scalability_block_time4d.png', bbox_inches='tight')


plt.clf()

plt.figure()
plt.title('Block time scalability (difficulty 5)')
plt.plot(block_time5d01c, marker="v", label='1 capacity', color="tomato")
plt.plot(block_time5d05c, marker="o", label='5 capacity', color="limegreen")
plt.plot(block_time5d10c, marker=".", label='10 capacity', color="royalblue")
plt.ylabel('Block time (sec)')
plt.xlabel('Number of nodes')
plt.xticks(range(len(number_of_nodes)), number_of_nodes)
plt.legend()
plt.savefig('plots/scalability_block_time5d.png', bbox_inches='tight')

# Throughput Scalability

plt.clf()

plt.figure()
plt.title('Throughput scalability (difficulty 4)')
plt.plot(throughput4d01c, marker="v", label='1 capacity', color="tomato")
plt.plot(throughput4d05c, marker="o", label='5 capacity', color="limegreen")
plt.plot(throughput4d10c, marker=".", label='10 capacity', color="royalblue")
plt.ylabel('Throughput')
plt.xlabel('Number of nodes')
plt.xticks(range(len(number_of_nodes)), number_of_nodes)
plt.legend()
plt.savefig('plots/scalability_throughput4d.png', bbox_inches='tight')


plt.clf()

plt.figure()
plt.title('Throughput scalability (difficulty 5)')
plt.plot(throughput5d01c, marker="v", label='1 capacity', color="tomato")
plt.plot(throughput5d05c, marker="o", label='5 capacity', color="limegreen")
plt.plot(throughput5d10c, marker=".", label='10 capacity', color="royalblue")
plt.ylabel('Throughput')
plt.xlabel('Number of nodes')
plt.xticks(range(len(number_of_nodes)), number_of_nodes)
plt.legend()
plt.savefig('plots/scalability_throughput5d.png', bbox_inches='tight')


