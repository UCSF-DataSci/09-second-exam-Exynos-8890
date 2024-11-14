python -u "./generate_dirty_data.py"
# cat ms_data_dirty.csv | grep "#"
sed -i '' '/^#/d;/^$/d' ms_data_dirty.csv
sed -i '' 's/,,/,/g' ms_data_dirty.csv
cut -d',' -f1,2,4,5,6 ms_data_dirty.csv > ms_data.csv
echo "insurance_type
Basic
Premium
Platinum
Travel
Pet
Disability
Liability" > insurance.lst
tail -n +2 ms_data.csv | wc -l
head --lines 10 ms_data.csv