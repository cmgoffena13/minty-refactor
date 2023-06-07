function createCategorySpendingBarGraph(url) {
    $.ajax(url)
      .done(function (category_spending_data) {
        const labels = category_spending_data.map((e) => e.category_name);
        const transaction_totals = category_spending_data.map((e) => e.total_transaction_amount);
  
        const config = {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Total Spending",
                data: transaction_totals,
              },
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
  