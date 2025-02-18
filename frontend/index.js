// fetch user data
// fetch user data
//
//
//
//
//
//
function fetchData() {
  let amount;

  // this are the params
  const params = {
    amount: amount,
    type: amount,
  };

  const urlParams = new encodeURIComponent(params);

  fetch(`http://127.0.0.1:5000/sms?${urlParams}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}
