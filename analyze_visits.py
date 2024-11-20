import pandas as pd
import numpy as np

df = pd.read_csv('./ms_data.csv')
df['visit_date'] = pd.to_datetime(df['visit_date'])
df['patient_id'] = df['patient_id'].astype(str)
df['age'] = df['age'].astype(float)
df['education_level'] = df['education_level'].astype('category')
df['walking_speed'] = df['walking_speed'].astype(float)
# sort by patient_id and visit_date
df = df.sort_values(by=['patient_id', 'visit_date'])
df.dropna()


with open("./insurance.lst",'r') as f:
    insurance = f.read().splitlines()
    insurance = insurance[1:]


unique_patient_id = df['patient_id'].unique()
np.random.seed(123)
patient_insurance = {pid: np.random.choice(insurance) for pid in unique_patient_id}

# print(set(patient_insurance.values()))

df['insurance_type'] = df['patient_id'].map(patient_insurance)

insurance_costs = {ins : int(100 * np.random.random()) + 50 for ins in insurance}

df['visit_cost'] = df['insurance_type'].map(insurance_costs).apply(lambda x : x + int(np.random.uniform(-20,+20)))
# print(df['visit_cost'].head())

mean_walking_speed_by_education = df.groupby('education_level')['walking_speed'].mean()
mean_costs_by_insurance_type = df.groupby('insurance_type')['visit_cost'].mean()
age_effects_on_walking_speed = df.groupby('age')['walking_speed'].mean()

print("Mean Walking Speed by Education Level:")
print(mean_walking_speed_by_education)
print("\nMean Costs by Insurance Type:")
print(mean_costs_by_insurance_type)
print("\nAge Effects on Walking Speed:")
print(age_effects_on_walking_speed)

df.to_csv('./ms_data.csv', index=False)