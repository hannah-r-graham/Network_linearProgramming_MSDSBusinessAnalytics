# %% [markdown]
# Import Packages

# %%
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import matplotlib.pyplot as plt
import networkx as nx


# %% [markdown]
# Define data for all 3 scenarios, for order of tasks , and labels for tasks

# %%
activitiesBest = {
    'A': 4.25,
    'B': 6.8,
    'C': 5.1,
    'D': 0,
    'D1': 6.8,
    'D2': 6.8,
    'D3': 6.8,
    'D4': 40.8,
    'D5': 6.8,
    'D6': 13.6,
    'D7': 13.6,
    'D8': 6.8,
    'E': 20.4,
    'F': 10.2,
    'G': 13.6,
    'H': 6.8
}
activitiesExpected = {
    'A': 5,
    'B': 8,
    'C': 6,
    'D': 0,
    'D1': 8,
    'D2': 8,
    'D3': 8,
    'D4': 48,
    'D5': 8,
    'D6': 16,
    'D7': 16,
    'D8': 8,
    'E': 24,
    'F': 12,
    'G': 16,
    'H': 8
}
activitiesWorst = {
    'A': 5.75,
    'B': 9.2,
    'C': 6.9,
    'D': 0,
    'D1': 9.2,
    'D2': 9.2,
    'D3': 9.2,
    'D4': 55.2,
    'D5': 9.2,
    'D6': 18.4,
    'D7': 18.4,
    'D8': 9.2,
    'E': 27.6,
    'F': 13.8,
    'G': 18.4,
    'H': 9.2
}
precedences = {
    'A': [],
    'B': [],
    'C': ['A'],
    'D': [],
    'D1': ['A'],
    'D2': ['D1'],
    'D3': ['D1'],
    'D4': ['D2', 'D3'],
    'D5': ['D4'],
    'D6': ['D4'],
    'D7': ['D6'],
    'D8': ['D5', 'D7'],
    'E': ['B', 'C'],
    'F': ['D8', 'E'],
    'G': ['A', 'D8'],
    'H': ['F', 'G']
}

TaskLabels = {
    'A': 'Describe product',
    'B': 'Develop marketing strategy',
    'C': 'Design brochure',
    'D': 'Develop product prototype',
    'D1': 'Requirements analysis',
    'D2': 'Software design',
    'D3': 'System design',
    'D4': 'Coding',
    'D5': 'Write documentation',
    'D6': 'Unit testing',
    'D7': 'System testing',
    'D8': 'Package deliverables',
    'E': 'Survey potential market',
    'F': 'Develop pricing plan',
    'G': 'Develop implementation plan',
    'H': 'Write client proposal'
}

# %% [markdown]
# Best case scenario
# 

# %%
activities = activitiesBest 

# %%
# Create a list of the activities
activities_list = list(activities.keys())

# Create the LP problem
prob = LpProblem("Critical Path", LpMinimize)

# Create the LP variables
start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in activities_list}
end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in activities_list}

# Add the constraints
for activity in activities_list:
    prob += end_times[activity] == start_times[activity] + activities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        prob += start_times[activity] >= end_times[predecessor], f"{activity}_predecessor_{predecessor}"

# Set the objective function
prob += lpSum([end_times[activity] for activity in activities_list]), "minimize_end_times"

# Solve the LP problem
status = prob.solve()

# Print the results
print("Critical Path time:")
for activity in activities_list:
    if value(start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(end_times[activity]) == max([value(end_times[activity]) for activity in activities_list]):
        print(f"{activity} ends at {value(end_times[activity])} hours in duration")

# Create a list to store the variable names and their values
solution_data = []

# Print solution and populate the list
# print("\nSolution variable values:")
for var in prob.variables():
    if var.name != "_dummy":
        # print(var.name, "=", var.varValue)
        solution_data.append({'Variable': var.name, 'Value': var.varValue})

# Convert the list to a DataFrame
Best_case_solution_df = pd.DataFrame(solution_data)

# Print the DataFrame
print("\Best Case DataFrame:")
print(Best_case_solution_df)

# %%
# Extract start and end times
start_times_values = {activity: value(start_times[activity]) for activity in activities_list}
end_times_values = {activity: value(end_times[activity]) for activity in activities_list}

# Calculate durations
durations = {activity: end_times_values[activity] - start_times_values[activity] for activity in activities_list}

# Create the Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

for i, activity in enumerate(activities_list):
    ax.barh(activity, durations[activity], left=start_times_values[activity], color='skyblue')

ax.set_xlabel('Time')
ax.set_ylabel('Activities')
ax.set_title('Gantt Chart Best Case Scenario')
plt.show()

# %%
CPGraph = nx.DiGraph()

# Add nodes with start and end times as attributes
for activity in activities_list:
    CPGraph.add_node(activity, start=start_times_values[activity], end=end_times_values[activity])

# Add edges based on precedences
for activity, predecessors in precedences.items():
    for predecessor in predecessors:
        CPGraph.add_edge(predecessor, activity)

# Draw the graph
pos = nx.spring_layout(CPGraph)
nx.draw(CPGraph, pos, with_labels=False, node_size=1000, node_color='skyblue', font_size=8, font_weight='bold')
node_labels = {node: f"{node}\n{start_times_values[node]}-{end_times_values[node]}" for node in CPGraph.nodes()}
plt.title('Critical Path Best Case Scenario')
nx.draw_networkx_labels(CPGraph, pos, labels=node_labels, font_size=6)
plt.show()

# %% [markdown]
# Scenario 2: Expected Scenario

# %%
activities = activitiesExpected 
# Create a list of the activities
activities_list = list(activities.keys())

# Create the LP problem
prob = LpProblem("Critical Path", LpMinimize)

# Create the LP variables
start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in activities_list}
end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in activities_list}

# Add the constraints
for activity in activities_list:
    prob += end_times[activity] == start_times[activity] + activities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        prob += start_times[activity] >= end_times[predecessor], f"{activity}_predecessor_{predecessor}"

# Set the objective function
prob += lpSum([end_times[activity] for activity in activities_list]), "minimize_end_times"

# Solve the LP problem
status = prob.solve()

# Print the results
print("Critical Path time:")
for activity in activities_list:
    if value(start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(end_times[activity]) == max([value(end_times[activity]) for activity in activities_list]):
        print(f"{activity} ends at {value(end_times[activity])} hours in duration")

# Create a list to store the variable names and their values
solution_data = []

# Print solution and populate the list
# print("\nSolution variable values:")
for var in prob.variables():
    if var.name != "_dummy":
        # print(var.name, "=", var.varValue)
        solution_data.append({'Variable': var.name, 'Value': var.varValue})

# Convert the list to a DataFrame
activitiesExpected_solution_df = pd.DataFrame(solution_data)

# Print the DataFrame
print("\ActivitiesExpected DataFrame:")
print(activitiesExpected_solution_df)


# Extract start and end times
start_times_values = {activity: value(start_times[activity]) for activity in activities_list}
end_times_values = {activity: value(end_times[activity]) for activity in activities_list}

# Calculate durations
durations = {activity: end_times_values[activity] - start_times_values[activity] for activity in activities_list}

# Create the Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

for i, activity in enumerate(activities_list):
    ax.barh(activity, durations[activity], left=start_times_values[activity], color='skyblue')

ax.set_xlabel('Time')
ax.set_ylabel('Activities')
ax.set_title('Gantt Chart EXPECTED Scenario')
plt.show()

# %%
CPGraph = nx.DiGraph()

# Add nodes with start and end times as attributes
for activity in activities_list:
    CPGraph.add_node(activity, start=start_times_values[activity], end=end_times_values[activity])

# Add edges based on precedences
for activity, predecessors in precedences.items():
    for predecessor in predecessors:
        CPGraph.add_edge(predecessor, activity)

# Draw the graph
pos = nx.spring_layout(CPGraph)
nx.draw(CPGraph, pos, with_labels=False, node_size=1000, node_color='skyblue', font_size=8, font_weight='bold')
node_labels = {node: f"{node}\n{start_times_values[node]}-{end_times_values[node]}" for node in CPGraph.nodes()}
plt.title('Critical Path Expected Scenario')
nx.draw_networkx_labels(CPGraph, pos, labels=node_labels, font_size=6)
plt.show()

# %% [markdown]
# Scenario 3: Worse Case Scenario

# %%
activities = activitiesWorst 
# Create a list of the activities
activities_list = list(activities.keys())

# Create the LP problem
prob = LpProblem("Critical Path", LpMinimize)

# Create the LP variables
start_times = {activity: LpVariable(f"start_{activity}", 0, None) for activity in activities_list}
end_times = {activity: LpVariable(f"end_{activity}", 0, None) for activity in activities_list}

# Add the constraints
for activity in activities_list:
    prob += end_times[activity] == start_times[activity] + activities[activity], f"{activity}_duration"
    for predecessor in precedences[activity]:
        prob += start_times[activity] >= end_times[predecessor], f"{activity}_predecessor_{predecessor}"

# Set the objective function
prob += lpSum([end_times[activity] for activity in activities_list]), "minimize_end_times"

# Solve the LP problem
status = prob.solve()

# Print the results
print("Critical Path time:")
for activity in activities_list:
    if value(start_times[activity]) == 0:
        print(f"{activity} starts at time 0")
    if value(end_times[activity]) == max([value(end_times[activity]) for activity in activities_list]):
        print(f"{activity} ends at {value(end_times[activity])} hours in duration")

# Create a list to store the variable names and their values
solution_data = []

# Print solution and populate the list
# print("\nSolution variable values:")
for var in prob.variables():
    if var.name != "_dummy":
        # print(var.name, "=", var.varValue)
        solution_data.append({'Variable': var.name, 'Value': var.varValue})

# Convert the list to a DataFrame
wworseCase_solution_df = pd.DataFrame(solution_data)

# Print the DataFrame
print("\Worse Case DataFrame:")
print(wworseCase_solution_df)

# Extract start and end times
start_times_values = {activity: value(start_times[activity]) for activity in activities_list}
end_times_values = {activity: value(end_times[activity]) for activity in activities_list}

# Calculate durations
durations = {activity: end_times_values[activity] - start_times_values[activity] for activity in activities_list}

# Create the Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

for i, activity in enumerate(activities_list):
    ax.barh(activity, durations[activity], left=start_times_values[activity], color='skyblue')

ax.set_xlabel('Time')
ax.set_ylabel('Activities')
ax.set_title('Gantt Chart Worse Case Scenario')
plt.show()

# %%
CPGraph = nx.DiGraph()

# Add nodes with start and end times as attributes
for activity in activities_list:
    CPGraph.add_node(activity, start=start_times_values[activity], end=end_times_values[activity])

# Add edges based on precedences
for activity, predecessors in precedences.items():
    for predecessor in predecessors:
        CPGraph.add_edge(predecessor, activity)

# Draw the graph
pos = nx.spring_layout(CPGraph)
nx.draw(CPGraph, pos, with_labels=False, node_size=1000, node_color='skyblue', font_size=8, font_weight='bold')
node_labels = {node: f"{node}\n{start_times_values[node]}-{end_times_values[node]}" for node in CPGraph.nodes()}
plt.title('Critical Path Worse Case Scenario')
nx.draw_networkx_labels(CPGraph, pos, labels=node_labels, font_size=6)
plt.show()

# %%
# Merge the solution dataframes
merged_df = Best_case_solution_df.merge(activitiesExpected_solution_df, on='Variable', suffixes=('_Best', '_Expected'))
merged_df = merged_df.merge(wworseCase_solution_df, on='Variable')
merged_df.rename(columns={'Value': 'Value_Worst'}, inplace=True)

# Print the merged dataframe
print(merged_df)


