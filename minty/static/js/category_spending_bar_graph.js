function createCategorySpendingBarGraph(url) {
    $.ajax(url)
      .done(function (category_spending_data) {
        const labels = category_spending_data.map((e) => e.category_name);
        const current_transaction_totals = category_spending_data.map((e) => e.current_total_transaction_amount);
        const previous_transaction_totals = category_spending_data.map((e) => e.previous_total_transaction_amount);
  
        const config = {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Current Spending",
                data: current_transaction_totals,
              },
              {
                label: "Previous Spending",
                data: previous_transaction_totals
              }
            ],
          },
        };
  
        const elem = document
          .getElementById("category_spending_bar_graph")
          .getContext("2d");
        new Chart(elem, config);
      })
      .fail(function () {
        const elem = document
          .getElementById("category_spending_bar_graph")
          .getContext("2d");
        elem.text = "Cannot access category spending data";
      });
  }
  