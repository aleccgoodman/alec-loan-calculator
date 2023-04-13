from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)


class Loan:
    def __init__(self, loanAmount, numberYears, annualRate):
        self.loanAmount = loanAmount
        self.annualRate = annualRate
        self.numberOfPmts = numberYears * 12  # monthly pmts
        self.periodicIntRate = self.annualRate / 12
        self.discountFactor = 0.0
        self.loanPmt = 0

    def getDiscountFactor(self):
        return self.discountFactor

    def calculateDiscountFactor(self):
        self.discountFactor = (
            ((1.0 + self.periodicIntRate) ** self.numberOfPmts) - 1.0
        ) / (self.periodicIntRate * (1.0 + self.periodicIntRate) ** self.numberOfPmts)

    def calculateLoanPmt(self):
        self.calculateDiscountFactor()
        print("discount factor: ", self.discountFactor)
        self.loanPmt = self.loanAmount / self.getDiscountFactor()
        print("loan payment: ", self.loanPmt)

    def getLoanAmount(self):
        return self.loanAmount

    def getLoanPmt(self):
        return self.loanPmt

    def getPeriodicIntRate(self):
        return self.periodicIntRate


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def mnthlyPmt():
    if request.method == "POST":
        form = request.form
        loanAmt = float(form["loanAmt"])
        numberYears = float(form["lengthOfLoan"])
        annualRate = float(form["intRate"])

        loan = Loan(loanAmt, numberYears, annualRate)

        loan.calculateLoanPmt()

        monthlyLoanPayment = loan.getLoanPmt()
        formattedMonthlyPayment = "${0:,.2f}".format(monthlyLoanPayment)

        # amortization schedule variables
        monthlyBeginningBalance = loan.getLoanAmount()
        totalInterestPaid = 0.0
        amoritzation = []

        # amortization schedule
        for i in range(1, int(loan.numberOfPmts) + 1):
            month = i
            monthlyInterestPayment = monthlyBeginningBalance * loan.getPeriodicIntRate()
            paymentToPrincipal = monthlyLoanPayment - monthlyInterestPayment
            monthlyLoanBalance = monthlyBeginningBalance - paymentToPrincipal
            totalInterestPaid = totalInterestPaid + monthlyInterestPayment

            amortization_dict = {
                "month": month,
                "monthlyLoanPayment": "${0:,.2f}".format(monthlyLoanPayment),
                "paymentToPrincipal": "${0:,.2f}".format(paymentToPrincipal),
                "monthlyInterestPayment": "${0:,.2f}".format(monthlyInterestPayment),
                "monthlyLoanBalance": "${0:,.2f}".format(monthlyLoanBalance),
                "totalInterestPaid": "${0:,.2f}".format(totalInterestPaid),
            }
            amoritzation.append(amortization_dict)

            monthlyBeginningBalance = monthlyLoanBalance

        return render_template(
            "index.html",
            payment=formattedMonthlyPayment,
            amortization=amoritzation,
        )

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
