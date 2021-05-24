// const jquery360 = require("./jquery-3.6.0");

//const jquery360 = require("./jquery-3.6.0");

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

// function runScript(text) {
//     console.log("Why do you leave me");
//     var $j = jQuery.noConflict();
//     //jQuery.ajaxSetup()
//     res = JSON.parse(getJSON("https://meduza.io/"))
//     console.log(res.id);
//     jQuery.ajax({
//         // type: "GET",
//         url: '{{article_download}}', //The URL you defined in urls.py
//         data: {text:text},
//         success: function(data) {
//             console.log("ajax runScript activated");
//           //If you wish you can do additional data manipulation here.
//         },
//         failure: function(data) { 
//             console.log('Got an error dude');
//         }
//     });
// }
//https://www.youtube.com/watch?v=qLyeIU8iSfI&ab_channel=IanWilson
//https://medium.com/coding-with-carla/build-a-card-that-flips-on-click-with-html-css-and-vanilla-javascript-part-1-937cd2242c90
//table.appendChild(createCard("The cards of different media will be located here"));
//create top number div

//create bottom number div with "right class"