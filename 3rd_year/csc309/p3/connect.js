

var mongoose = require("mongoose"); 
var options = {
  useMongoClient: true,
  socketTimeoutMS: 0,
  keepAlive: true,
  reconnectTries: 30
};

var url = "mongodb://localhost/admin";   //my database
var db = mongoose.connect(url,options);   