document.getElementById('loanForm').addEventListener('submit', async function (event) {
  // Prevent the default form submission (which would reload the page)
  event.preventDefault();

  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = 'Processing...';

  // --- Data Mapping & Conversion ---
  // Convert form text values to numbers that the backend API expects.
  const genderMap = { "Male": 1, "Female": 0 };
  const marriedMap = { "Yes": 1, "No": 0 };
  const educationMap = { "Graduate": 1, "Not Graduate": 0 };
  const selfEmployedMap = { "Yes": 1, "No": 0 };
  const propertyAreaMap = { "Urban": 2, "Semiurban": 1, "Rural": 0 };

  // Handle '3+' for dependents
  const dependentsValue = document.getElementById('dependents').value;
  const dependents = dependentsValue === '3+' ? 3 : parseInt(dependentsValue, 10);

  // --- Construct the Payload ---
  // Create a JavaScript object with keys that match the Pydantic model in main.py
  const formData = {
    name: document.getElementById('name').value,
    Gender: genderMap[document.getElementById('gender').value],
    Married: marriedMap[document.getElementById('married').value],
    Dependents: dependents,
    Education: educationMap[document.getElementById('education').value],
    Self_Employed: selfEmployedMap[document.getElementById('selfEmployed').value],
    ApplicantIncome: parseFloat(document.getElementById('applicantIncome').value),
    CoapplicantIncome: parseFloat(document.getElementById('coapplicantIncome').value),
    LoanAmount: parseFloat(document.getElementById('loanAmount').value),
    Loan_Amount_Term: parseInt(document.getElementById('loanAmountTerm').value, 10),
    Credit_History: parseInt(document.getElementById('creditHistory').value, 10),
    Property_Area: propertyAreaMap[document.getElementById('propertyArea').value]
  };

  try {
    // --- Send Data to FastAPI Backend ---
    const response = await fetch('/apply-loan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    // --- Handle the Response ---
    if (response.ok) {
      const data = await response.json();
      const message = `${data.name}, your loan has been <strong>${data.result}</strong>!`;
      resultDiv.innerHTML = `<div class="alert alert-success">${message}</div>`;
    } else {
      const errorData = await response.json();
      const errorMessage = `Application failed: ${errorData.detail || 'Unknown error'}`;
      resultDiv.innerHTML = `<div class="alert alert-danger">${errorMessage}</div>`;
      console.error('Error:', errorData);
    }
  } catch (error) {
    resultDiv.innerHTML = `<div class="alert alert-danger">An error occurred while submitting the form. Please try again.</div>`;
    console.error('Fetch Error:', error);
  }
});