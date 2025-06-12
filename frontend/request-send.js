document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // يمنع إعادة تحميل الصفحة

    // جمع البيانات من النموذج
    const name = document.getElementById("name").value.trim();
    const income = document.getElementById("income").value.trim();
    const loanAmount = document.getElementById("loanAmount").value.trim();
    const employment = document.getElementById("employment").value;
    const creditHistory = document.getElementById("creditHistory").value;

    // التحقق من الحقول الفارغة
    if (!name || !income || !loanAmount || !employment || !creditHistory) {
        alert("Please fill in all fields before submitting.");
        return;
    }

    // إنشاء كائن البيانات
    const data = { name, income, loanAmount, employment, creditHistory };

    // إرسال البيانات إلى FastAPI
    fetch("http://localhost:8000/apply-loan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("Server Response:", result);
        showSuccessMessage(); // عرض رسالة التأكيد
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error submitting application. Please try again."); // رسالة خطأ في حالة فشل الإرسال
    });
});

// وظيفة عرض رسالة التأكيد بعد نجاح الإرسال
function showSuccessMessage() {
    const successDiv = document.createElement("div");
    successDiv.className = "alert alert-success text-center mt-3";
    successDiv.textContent = "Loan application submitted successfully!";
    
    document.querySelector("form").appendChild(successDiv);

    // إخفاء الرسالة بعد 3 ثوانٍ
    setTimeout(() => successDiv.remove(), 3000);
}
