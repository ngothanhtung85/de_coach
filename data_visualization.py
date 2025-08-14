import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("clean_data.csv")

print(df.columns.tolist())

# Graph by Salary and Group - salary_unit = VND
#convert min and max to numeric
df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce')
df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce')

#calculate the average salary
df['avg_salary'] = df[['min_salary','max_salary']].mean(axis=1)

plt.figure(figsize=(12, 6))
sns.boxplot(x='Group', y='avg_salary', data=df[df['salary_unit'] == 'VND'])
plt.xticks(rotation=90)
plt.title("Phan bo theo luong va vi tri")
plt.xlabel("Group")
plt.ylabel("Avg Salary")
plt.tight_layout()
plt.show()

#Heat graph by working area
#count the job by district
district_count = df['district'].value_counts()

heatmap_data = pd.DataFrame(district_count).reset_index()
heatmap_data.columns = ['District', 'Count']
heatmap_data.set_index('District', inplace=True)
heatmap_2d = heatmap_data.T

plt.figure(figsize=(12,2))
sns.heatmap(heatmap_2d, annot=False, cmap="YlGnBu", cbar=True, linewidths=0.5)

plt.title("Phan bo khu vuc lam viec")
plt.xlabel("District")
plt.ylabel("")
plt.tight_layout()
plt.show()

#Graph by trending group
plt.figure(figsize=(10, 6))
df['Group'].value_counts().head(10).plot(kind='pie')
plt.title("Top 10 trending group")
plt.title("Quantity of open jobs")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

