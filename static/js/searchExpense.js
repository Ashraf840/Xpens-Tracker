const usernameInput = document.getElementById("searchField");

// Show/Display Output Divs
const paginationOutput = document.getElementById("pagination-container");

const tableDefault = document.getElementById("table-default");
const tableOutput = document.getElementById("table-output");
const tableOutputbody = document.getElementById("table-output-body");
// tableOutput.style.display = "none";     // By default, it'll be hidden, utill anythin is being searched using the search-box, doesn't use this here, directly hide it from the html page using inline css.


usernameInput.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if (searchValue.length > 0) {
        // Before making any API call, clear the table-output-body first
        tableOutputbody.innerHTML = "";
        fetch('../../search-expense/', {
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
            }else{
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
    }else{
        tableDefault.style.display = "inline-block";
        tableOutput.style.display = "none";
        paginationOutput.style.display = 'inline-block';
    }
});