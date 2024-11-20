import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, ttest_ind

df = pd.read_csv('./ms_data.csv')
df['visit_date'] = pd.to_datetime(df['visit_date'])
df['patient_id'] = df['patient_id'].astype(str)
df['age'] = df['age'].astype(float)
df['education_level'] = df['education_level'].astype('category')
df['walking_speed'] = df['walking_speed'].astype(float)
# sort by patient_id and visit_date
df = df.sort_values(by=['patient_id', 'visit_date'])
df.dropna()


scaler = StandardScaler()
df[['age', 'walking_speed']] = scaler.fit_transform(df[['age', 'walking_speed']])

model = mixedlm(
    "walking_speed ~ age + education_level",
    df,
    groups = df['patient_id']
)
result = model.fit(reml=False, method='nm', maxiter=100)

print(result.summary())


mean_costs_by_insurance = df.groupby('insurance_type')['visit_cost'].mean()
std_costs_by_insurance = df.groupby('insurance_type')['visit_cost'].std()
count_by_insurance = df.groupby('insurance_type')['visit_cost'].count()

print("Mean Costs by Insurance Type:")
print(mean_costs_by_insurance)
print("\nStandard Deviation of Costs by Insurance Type:")
print(std_costs_by_insurance)
print("\nCount of Visits by Insurance Type:")
print(count_by_insurance)

plt.figure(figsize=(10, 6))
sns.boxplot(x='insurance_type', y='visit_cost', data=df)
plt.title('Visit Costs by Insurance Type')
plt.xlabel('Insurance Type')
plt.ylabel('Visit Cost')
plt.show()

def cohen_d(x, y):
    return (np.mean(x) - np.mean(y)) / np.sqrt((np.std(x, ddof=1) ** 2 + np.std(y, ddof=1) ** 2) / 2)

insurance_types = df['insurance_type'].unique()
effect_sizes = {}

for i, ins1 in enumerate(insurance_types):
    for ins2 in insurance_types[i+1:]:
        d = cohen_d(df[df['insurance_type'] == ins1]['visit_cost'], df[df['insurance_type'] == ins2]['visit_cost'])
        effect_sizes[f'{ins1} vs {ins2}'] = d

print("\nEffect Sizes (Cohen's d):")
for comparison, d in effect_sizes.items():
    print(f'{comparison}: {d:.2f}')