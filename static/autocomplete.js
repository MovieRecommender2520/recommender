// display results
const resultsBox = document.querySelector(".result-box");

// search box
const inputBox = document.getElementById("input-box");

// enter
const searchButton = document.getElementById("search-button");

inputBox.onkeyup = function(){
    let result = [];
    let input = inputBox.value;
    if(input.length){
        result = availableKeywords.filter((keyword)=>{
            return keyword.toLowerCase().includes(input.toLowerCase());
        });
        console.log(result);
    }
    display(result);

    if(!result.length){
        resultsBox.innerHTML = '';
    }
}

// ENTER KEY -> trigger button click
inputBox.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        searchButton.click();
    }
});

function displayRecommendations(movies) {
    const recommendationsBox = document.getElementById("recommendations");
    const content = movies.map(title => `<li>${title}</li>`).join("");
    recommendationsBox.innerHTML = `
        <h3>Recommended Movies:</h3>
        <ul>${content}</ul>
    `;
}

// BUTTON CLICK -> fetch recommendations
searchButton.addEventListener('click', function () {
    const movie = inputBox.value;
    if (movie) {
        fetch(`/recommend?movie=${encodeURIComponent(movie)}`)
            .then(response => response.json())
            .then(data => {
                displayRecommendations(data);
            })
    }
});


function display(result){
    const content = result.map((list)=>{
        return `<li onclick=selectInput(this)>${list}</li>`;
    });

    resultsBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInput(list){
    inputBox.value = list.innerHTML;
    resultsBox.innerHTML = '';
}