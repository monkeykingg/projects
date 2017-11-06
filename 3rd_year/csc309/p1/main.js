/*
 * HW1 API testing. You should implement following 3 functioins.
 * - getListsOfItems:
 * 	   Find a RESTFUL API and use GET to retrive a list of items.
 * - getOneItemById:
 *     Retrieve a single item by id based on the list you get from 
 * 	   getListsOfItems().
 * - getOneAttributeFromItem:
 *     Return any attribute from the retrieved item. 
 *     Ex: Return the temperature.
 */

const request = require('request');
//var program = require('commander');

var place = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670,151.1957&radius=500&types=food&name=cruise&key=AIzaSyD0FeEU0N0SoiNwVFLHAcNOKxfdVH_t1Gw";
var restaurant = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+Sydney&key=AIzaSyD0FeEU0N0SoiNwVFLHAcNOKxfdVH_t1Gw";

var app={

        // Get the restaurant list of nearby restaurants with a particular range by Google Place API
        // You can know that we chose restaurants in Sydney by checking "place" and "restaurant" above
        getListOfItems:function (url) {

        request.get(url, function (err, res, body) {
            if (err) {
                console.log(err);
            } else {
                data = JSON.parse(body);
                var res = data.results;
                console.log("List of Restaurants: ")
                console.log(res);
                console.log("-----------------------------------------------------------------------------------------")
            }
        })
        },


        // Get one restaurant by ID.
        getOneItemById:function(url, id) {

            request.get(url, function (err, res, body) {
            if (err) {
                console.log(err)
            } else {
                data = JSON.parse(body)
                var res = data.results;
                console.log("One Restaurant by ID: ")
                console.log(res[id-1]);
                console.log("-----------------------------------------------------------------------------------------")
            }
        })
        },


        // Get "geometry" attribute from ID 1 restaurant.
        getOneAttributeFromItem: function (url, id, attribute) {

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
        },
}

app.getListOfItems(place);
setTimeout(app.getOneItemById, 1000, place, 1)
setTimeout(app.getOneAttributeFromItem, 2000, place, 1, "geometry")       

