// Intialize the variables
const totalTransactions = document.getElementById("total-transactions");
const totalAmount = document.getElementById("total-amount");
const tableItems = document.getElementById("table-items");
const tableBody = document.getElementById("table-body");
const searchInput = document.getElementById("search");
const amountInput = document.getElementById("amount");
const datePicker = document.getElementById("date");
const typeSelect = document.getElementById("type-section");
const totalComing = document.getElementById("total-coming");
const loadingPage = document.getElementById("hover-loading");
// Intialize the requestParams object to store the query parameters for the
// filtering
const requestParams = {};

// Store the pie chart and bar chart instance
let pieChart = null;
let barchart = null;

// render bar chart of the total amount by month
function renderBarChart(data) {
  const canvas = document.getElementById("bar-chart");
  const totalAmountByMonth = new Map();

  data.forEach((element) => {
    // get the date from the data
    const date = new Date(element.date);

    // format the date to month and year
    const month = date.toLocaleString("en-us", { month: "short" });
    const year = date.toLocaleString("en-us", { year: "numeric" });

    // Format the date to month and year to use as the key in the hashmap
    let time = `${month}-${year}`;

    // Check if the time is already in the hashmap
    if (totalAmountByMonth.has(time)) {
      totalAmountByMonth.set(
        time,
        totalAmountByMonth.get(time) + element.amount
      );
    } else {
      totalAmountByMonth.set(time, element.amount);
    }
  });

  if (barchart) {
    barchart.destroy();
  }

  barchart = new Chart(canvas, {
    type: "bar",
    data: {
      labels: [...totalAmountByMonth.keys()],
      datasets: [
        {
          label: "Total Transaction by month",
          data: [...totalAmountByMonth.values()],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

// Function to render the pie chart of coming and going transactions
function renderPieChart(data) {
  const canvas = document.getElementById("pie-chart");

  // get the coming transactions
  const getComingData = data.filter((item) => {
    return item.category === "Coming";
  });
  // get the going transactions
  const getGoingData = data.filter((item) => {
    return item.category === "Going";
  });

  if (pieChart) {
    pieChart.destroy();
  }

  // Create a new pie chart and add the instance to the pieChart variable
  pieChart = new Chart(canvas, {
    type: "pie",
    data: {
      labels: ["Coming", "Going"],
      datasets: [
        {
          label: "Total Transactions",
          data: [`${getComingData.length}`, `${getGoingData.length}`],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      // maintainAspectRatio: false,
    },
  });
}

function fetchData() {
  // clear the table before fetching new data
  tableBody.innerHTML = "";
  loadingPage.style.display = "flex";
  // Convert the requestParams object to URLSearchParams
  // and append it to the URL for the filtering
  const urlParams = new URLSearchParams(requestParams).toString();

  // Fetch the data from the API
  fetch(`https://momo-dashboard.onrender.com/sms?${urlParams}`)
    .then((response) => response.json())
    .then((data) => {
      // close the loading page
      loadingPage.style.display = "none";
      // Render the pie chart according to the data
      renderPieChart(data);

      // Render the bar chart according to the data
      renderBarChart(data);

      // Calculate the total amount
      const total = data.filter((item) => {
        return item.category === "Coming";
      });
      totalComing.innerHTML = total.length;

      // Attach the data to the table
      data.forEach((element, index) => {
        // Create a new row
        const newRow = document.createElement("tr");
        newRow.classList.add("table-item");

        // Create a new cell
        const newCell1 = document.createElement("td");
        const newCell2 = document.createElement("td");
        const newCell3 = document.createElement("td");
        const newCell4 = document.createElement("td");
        const newCell5 = document.createElement("td");
        const messageDisplay = document.createElement("p");

        // Add class to the cell message display
        messageDisplay.classList.add("message-display");

        // Add data to the cell
        newCell1.innerHTML = index + 1;
        newCell2.innerHTML = element.amount;
        // Format the date
        newCell5.innerHTML = new Date(element.date).toLocaleString("en-us", {
          month: "short",
          day: "numeric",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });
        newCell4.innerHTML = element.message_type;
        newCell3.innerHTML = element.category;

        // messageDisplay.innerHTML = element.message;
        messageDisplay.innerText = element.message;

        // Append cell to the row
        newRow.appendChild(newCell1);
        newRow.appendChild(newCell2);
        newRow.appendChild(newCell3);
        newRow.appendChild(newCell4);
        newRow.appendChild(newCell5);
        newRow.appendChild(messageDisplay);

        // Append row to the table
        tableBody.appendChild(newRow);
      });

      // Calculate total amount
      totalTransactions.innerHTML = data.length;
    });
}

fetchData();

// Debounce function to help avoid multiple requests when typing or inputting
// data
function debounce(callback, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      callback.apply(this, args);
    }, delay);
  };
}

// Handle search input
const handleSearch = (e) => {
  const value = e.target.value;
  requestParams.search = value;
  fetchData();
};

// Add event listener to the search input field
// and debounce the input to avoid multiple requests
// with a delay of 1s
searchInput.addEventListener("input", debounce(handleSearch, 1000));

// Handle amount input
const handleAmount = (e) => {
  const value = e.target.value;
  requestParams.amount = value;
  fetchData();
};

// Add event listener to the amount input field
// and debounce the input to avoid multiple requests
amountInput.addEventListener("input", debounce(handleAmount, 1000));

// Handle date change
const handleDate = (e) => {
  // If the date is empty remove the date key from the requestParams object
  // and fetch the data
  if (!e.target.value) {
    delete requestParams.date;
    fetchData();
    return;
  }

  const value = e.target.value;
  requestParams.date = value;
  fetchData();
};

// Add event listener to the date picker
datePicker.addEventListener("change", debounce(handleDate, 1000));

// Handle type change
const handleType = (e) => {
  if (!e.target.value) {
    delete requestParams.type;
    fetchData();
    return;
  }
  const value = e.target.value;
  requestParams.type = value;
  fetchData();
};

// Add event listener to the type select field
typeSelect.addEventListener("change", debounce(handleType, 1000));

// // Render the chart on page load
// document.addEventListener("DOMContentLoaded", function () {
//   renderChart();
// });
