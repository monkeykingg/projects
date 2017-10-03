const request = require('request');
//var program = require('commander');

var place = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=43.661942,-79.395456&radius=500&types=food&name=cruise&key=AIzaSyD0FeEU0N0SoiNwVFLHAcNOKxfdVH_t1Gw";
var restaurant = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+Toronto&key=AIzaSyD0FeEU0N0SoiNwVFLHAcNOKxfdVH_t1Gw";

function getListOfItems(url) {

    request.get(url, function (err, res, body) {
    if (err) {
        console.log(err);
    } else {
        data = JSON.parse(body);
        var res = data.results;
        console.log(res);
    }
})
}

function getOneItemById(url, id) {

    request.get(url, function (err, res, body) {
    if (err) {
        console.log(err)
    } else {
        data = JSON.parse(body)
        var res = data.results;
        console.log(res[id-1]);
    }
})
}

function getOneAttributeFromItem(url, id, attribute) {

    request.get(url, function (err, res, body) {
    if (err) {
        console.log(err)
    } else {
        data = JSON.parse(body)
        var res = data.results;
        var output = res[id-1][attribute];
        console.log("The "+attribute+" of ID"+id+" is:")
        console.log(output);
    }
})
}

/*
program
    .usage('[function] [choice] [parameters]')    
    .option('-getListOfItems, --', 'a string argument')
    .option('-getOneItemById, --integer <n>', 'input a integet argument.', parseInt)
    .option('-getOneAttributeFromItem, --float <f>', 'input a float arg', parseFloat)
    .parse(process.argv)
    */
function help(){
        console.log("Usage:")
        console.log("[function choice][parameters]")
        //console.log("function names includes: place, restaurant")
        console.log("function choice includes:")
        console.log("   getListOfItems : no additional parameters in need")
        console.log("   getOneItemById : needs an id from 1 to 6")
        console.log("   getOneAttributeFromItem : needs an id from 1 to 6 and an attribute, attributes contains {geometry, icon, id, name, opening_hours, photos, place_id, rating, reference, scope, types, vicinity}")
        console.log("examples: node project1_v2.js getListOfItems")
        console.log("          node project1_v2.js getOneItemById 1")
        console.log("          node project1_v2.js getOneAttributeFromItem 2 geometry")
}

input = process.argv;
if (input.length == 3){
    if (input[2] == "getListOfItems"){
        getListOfItems(place);
    }
    else{
        console.log("Wrong input, try again.")
        help();
    }   
}

if (input.length == 4){
    if(input[2] == "getOneItemById"){
            getOneItemById(place, input[3])
    }       
    else if(input[2] == "getOneAttributeFromItem"){
            getOneAttributeFromItem(place, input[3])       
    }
    else{
        console.log("Wrong input, try again.")
        help();
    }
}

if (input.length == 5){
    if(input[2] == "getOneAttributeFromItem"){
            getOneAttributeFromItem(place, input[3], input[4])       
    }
    else{
        console.log("Wrong input, try again.")
        help();
    }
}

if (input.length == 2)
{
    help();
}
