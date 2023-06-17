function createMonthlyExpensesLineGraph(url) {
    $.ajax(url)
      .done(function (monthly_expenses_data) {
        const labels = monthly_expenses_data.map((e) => e.last_date_of_month);
        const monthly_expenses = monthly_expenses_data.map((e) => e.monthly_expenses);
  
        const config = {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Expenses",
                data: monthly_expenses,
              },
            ],
          },
        };
  
        const elem = document
          .getElementById("monthly_expense_graph")
          .getContext("2d");
        new Chart(elem, config);
      })
      .fail(function () {
        const elem = document
          .getElementById("monthly_expense_graph")
          .getContext("2d");
        elem.text = "Cannot access monthly expense data";
      });
  }
  