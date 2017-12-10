

var mongoose = require("mongoose"); 
var options = {
  useMongoClient: true,
  socketTimeoutMS: 0,
  keepAlive: true,
  reconnectTries: 30
};


var url = "mongodb://csc309f:csc309fall@ds117316.mlab.com:17316/csc309db"
var db = mongoose.connect(url,options);   