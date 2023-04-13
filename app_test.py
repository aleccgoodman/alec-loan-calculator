# test_app.py

# assert expression
## if true nothing happens
## if false raises AssertionError

# create virtual environment and activate
# pip install pytest
# pip install pytest-cov

# run tests with python -m pytest -s
# compare -s and -v when running the tests
# run coverage tests with python -m pytest --cov

import pytest
from app import app, Loan


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Unit Tests
def test_loan_discount_factor():
    """
    GIVEN a user enters their loan details
    WHEN the loan object's calculateDiscountFactor method is called
    THEN the discount factor is accurately calculated
    """
    loan = Loan(loanAmount=100000, numberYears=30, annualRate=0.06)
    loan.calculateDiscountFactor()
    print("\r")
    print(" -- calculateDiscountFactor method unit test")
    assert loan.getDiscountFactor() == pytest.approx(
        166.79, rel=1e-3
    )  # approx two decimal places


def test_loan_payment():
    """
    GIVEN a user enters their loan details
    WHEN the loan object's calculateLoanPmt method is called
    THEN the loan payment is accurately calculated
    """
    loan = Loan(loanAmount=100000, numberYears=30, annualRate=0.06)
    loan.calculateLoanPmt()
    print("\r")
    print(" -- calculateLoanPmt method unit test")
    assert loan.getLoanPmt() == pytest.approx(
        599.55, rel=1e-3
    )  # approx two decimal places


# Functional Tests
def test_home_page(client):
    """
    GIVEN a user visits the home page
    WHEN the page loads
    THEN the user sees "Loan Calculator" in the page body
    """
    response = client.get("/")
    assert response.status_code == 200
    print("\r")
    print(" -- home page loads functional test")
    assert b"Loan Calculator" in response.data


def test_calculate_loan_payment(client):
    """
    GIVEN a user enters their loan details
    WHEN the user clicks the calculate button
    THEN the user sees the monthly payment for their loan
    """
    response = client.post(
        "/", data={"loanAmt": "100000", "lengthOfLoan": "30", "intRate": "0.06"}
    )
    print("\r")
    print(" -- calculate loan functional test")
    assert response.status_code == 200
    assert b"$599.55" in response.data


# Integration Test
def test_full_loan_calculation(client):
    """
    GIVEN a user enters their loan details
    WHEN the user clicks the calculate button
    THEN the user sees the monthly payment for their loan and the amortization table
    """
    response = client.post(
        "/", data={"loanAmt": "100000", "lengthOfLoan": "30", "intRate": "0.06"}
    )
    assert response.status_code == 200

    data = {
        "month": "1",
        "monthlyLoanPayment": "$599.55",
        "paymentToPrincipal": "$99.55",
        "monthlyInterestPayment": "$500.00",
        "monthlyLoanBalance": "$99,900.45",
        "totalInterestPaid": "$500.00",
    }
    print("\r")
    print(" -- full loan calculation and amortization table integration test")
    for field, value in data.items():
        assert value.encode() in response.data
