import pandas as pd

# تحميل البيانات
df = pd.read_csv("loan_prediction.csv")

# معالجة القيم المفقودة
df["Gender"] = df["Gender"].fillna(df["Gender"].mode()[0])
df["Married"] = df["Married"].fillna(df["Married"].mode()[0])  # معالجة القيم المفقودة في Married
df["Dependents"] = df["Dependents"].replace("3+", 3).fillna(df["Dependents"].mode()[0])
df["Self_Employed"] = df["Self_Employed"].fillna(df["Self_Employed"].mode()[0])
df["Credit_History"] = df["Credit_History"].fillna(df["Credit_History"].median())
df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].mean())
df["Loan_Amount_Term"] = df["Loan_Amount_Term"].fillna(df["Loan_Amount_Term"].mode()[0])

# تحويل القيم الفئوية إلى بيانات عددية
df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})
df["Married"] = df["Married"].map({"No": 0, "Yes": 1})
df["Education"] = df["Education"].map({"Graduate": 1, "Not Graduate": 0})
df["Self_Employed"] = df["Self_Employed"].map({"No": 0, "Yes": 1})
df["Property_Area"] = df["Property_Area"].map({"Urban": 0, "Semiurban": 1, "Rural": 2})
df["Loan_Status"] = df["Loan_Status"].map({"N": 0, "Y": 1})

# عرض البيانات بعد المعالجة
print(df.head())
print(df.isnull().sum())  # للتأكد من عدم وجود قيم مفقودة

# حفظ البيانات في ملف جديد بعد التنظيف
df.to_csv("cleaned_loan_data.csv", index=False)

print("تم حفظ البيانات في cleaned_loan_data.csv بنجاح! ✅")


# # استعراض بعض السجلات
# print(df.head())

# # فحص القيم المفقودة
# print(df.isnull().sum())

# # عرض معلومات عن الأعمدة
# print(df.info())
