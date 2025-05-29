import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات النظيفة
df = pd.read_csv("cleaned_loan_data.csv")

# توزيع المتغير المستهدف (Loan_Status)
sns.countplot(x="Loan_Status", data=df)
plt.title("توزيع حالات الموافقة والرفض للقروض")
plt.show()

# توزيع السجل الائتماني (Credit_History) وتأثيره على الموافقة
sns.countplot(x="Credit_History", hue="Loan_Status", data=df)
plt.title("تأثير السجل الائتماني على القرض")
plt.show()

# توزيع المبلغ المطلوب للقرض
sns.histplot(df["LoanAmount"], bins=30, kde=True)
plt.title("توزيع مبلغ القرض")
plt.xlabel("مبلغ القرض")
plt.ylabel("عدد الطلبات")
plt.show()
