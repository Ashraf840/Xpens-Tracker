// Testing Purpose
// window.onload = (event) => {
//     console.log('page is fully loaded');
//     alert("Hello! I am an alert box!!");
// };


// Search-Bar Input Field
const usernameInput = document.getElementById("searchField");

// Show/Display Output Divs
const paginationOutput = document.getElementById("pagination-container");

// Table Div
const tableDefault = document.getElementById("table-default");
const tableOutput = document.getElementById("table-output");
const tableOutputbody = document.getElementById("table-output-body");
// tableOutput.style.display = "none";     // By default, it'll be hidden, utill anythin is being searched using the search-box, doesn't use this here, directly hide it from the html page using inline css.


usernameInput.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    // console.log(searchValue);

    if (searchValue.length > 0) {
        // Before making any API call, clear the table-output-body first
        tableOutputbody.innerHTML = "";

        // Explanation: "../../"" means it will route back to main project directory (expensewebsite/expensewebsite), 
        //then it goues to the "urls.py" file of that root project directory. Then it routes to "income/" path wchich 
        //routes to incomeapp.urls, in the incomeapp's "urls.py" file, it'll search for "search-income/" which will lead 
        //to the method "search_income" of this apps "views.py".
        fetch('../../income/search-income/', {
            method:"POST",
            body: JSON.stringify({ 'searchText':searchValue, }),
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data);

            // clear the table-output-body first
            tableOutputbody.innerHTML = "";
            paginationOutput.style.display = 'none';
            // Once anything is searched, hide the current table & display the table-output
            tableDefault.style.display = "none";
            tableOutput.style.display = "inline-block";

            if (data.length === 0) {
                tableOutputbody.innerHTML = "<tr><td colspan='6'>No result found!</td></tr>";
                // console.log("result not found!");
            }else{
                // console.log("result found!");
                data.forEach( (item) => {
                    tableOutputbody.innerHTML += `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        <td class='text-center'>${item.amount}</td>
                    </tr>`;
                });
            }
        });
    }
    else{
        tableDefault.style.display = "inline-block";
        tableOutput.style.display = "none";
        paginationOutput.style.display = 'inline-block';
    }
});