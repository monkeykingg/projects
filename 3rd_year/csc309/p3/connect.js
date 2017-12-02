

var mongoose = require("mongoose"); 
var options = {
  useMongoClient: true,
  socketTimeoutMS: 0,
  keepAlive: true,
  reconnectTries: 30
};

/*var url = "mongodb://localhost/admin";   //my database*/
/*var url = "mongodb://jiayuli:jiayulee88@cluster0-shard-00-00-k0y76.mongodb.net:27017,cluster0-shard-00-01-k0y76.mongodb.net:27017,cluster0-shard-00-02-k0y76.mongodb.net:27017/test"*/
var url = "mongodb://csc309f:csc309fall@ds117316.mlab.com:17316/csc309db"
var db = mongoose.connect(url,options);   