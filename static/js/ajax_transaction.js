pageNo = 2;
    function fetchMore(accountId){
        url = "/account/api/" + accountId + "/transactions?page=" + pageNo;
        fetch(url)
            .then((response)=>response.json())            
            .then((json)=>{
                pageNo = pageNo + 1;
                json.forEach(tableElement);
            });
        
    }
    function tableElement(transaction) {
            document.querySelector('#posts-table tbody').innerHTML +=
                `<tr>
        <td>${transaction.Id}</td>
        <td>${transaction.Type}</td>
        <td>${transaction.Date}</td>
        <td>${transaction.Amount}</td>
        <td>${transaction.NewBalance}</td>
    </tr>`;
        }