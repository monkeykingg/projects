
var mongoose = require('mongoose');
var favourSchema = new mongoose.Schema({
	name: String,
	comment: String
})
var UserSchema = new mongoose.Schema({
    name: String,
    pwd: String,
    favours:[favourSchema]

});

mongoose.model('JFrogUser',UserSchema);