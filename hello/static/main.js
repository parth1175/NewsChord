console.log("starting script");

//select the table div
const table = document.getElementsByClassName('table')[0];
console.log(table);
//create the card div
function createCard(number){
    const card = document.createElement('div');
    card.className = "card";

    const topNumber = document.createElement('div');
    const bottomNumber = document.createElement('div'); 
    bottomNumber.className = "right"
    bottomNumber.innerText = number

    card.append(topNumber);
    card.append(bottomNumber);

    return card;
}

//https://www.youtube.com/watch?v=qLyeIU8iSfI&ab_channel=IanWilson
//https://medium.com/coding-with-carla/build-a-card-that-flips-on-click-with-html-css-and-vanilla-javascript-part-1-937cd2242c90
table.appendChild(createCard(5));
table.appendChild(createCard(6));
table.appendChild(createCard(7));
//create top number div

//create bottom number div with "right class"