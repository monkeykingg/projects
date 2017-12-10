const  express=require('express');
const app=express();
const mongoose = require('mongoose');
const bodyParser = require("body-parser");
const methodOverride = require("method-override");
const cookieParser = require('cookie-parser');
var temp={};
require('./connect.js');
require('./model.js');
const User = mongoose.model('JFrogUser');  //model name
mongoose.Promise = global.Promise;
const PORT = process.env.PORT || 3000;

app.set("view engine", "ejs");

app.use(express.static(__dirname + '/assets'))
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(methodOverride("_method"));
app.use(cookieParser())

var adminmessages=[]
/*
admin api
 */

app.get('/api/messages',function(req,res){
    res.send(adminmessages)
})
app.post('/api/messages',function(req,res){
    var message = req.body
    console.log(message)
    adminmessages.push(message)
    res.send('You have successfully posted.')
})
app.get('/api/getmessage',function(req,res){
    var last = adminmessages[adminmessages.length-1]
    res.send(last)

})

app.delete('/api/messages/:id',function(req,res){
    var index = req.params.id
    adminmessages.splice(index-1,1)
    console.log(adminmessages)
    res.send('You have successfully deleted.')
})

/**
 * login
 */
app.get('/',function (req,res) {
    res.redirect('/login')
})

app.get('/login',function (req,res) {
    res.render('login')
})
app.post('/login',function (req,res) {
    var name=req.body.name;
    var pwd=req.body.pwd;
    User.findOne({name:name,pwd:pwd},function (error,result) {
        if (result==null)
        {
            res.render('fail');
        }else
        {
            res.cookie('name',name)
            res.redirect('/main');
        }
    })
})
app.get('/main',function(req,res){
    res.render('main',{username:req.cookies.name});
})
/**
 * register
 */
app.get('/register',function (req,res) {
    res.render('register')
})

app.post('/register',function (req,res) {

    if (req.body.name != '') {
        var name=req.body.name;
    }
    if (req.body.pwd != '') {
        var pwd=req.body.pwd;
    }

    if (req.body.name == '') {
        res.render('fail');
        return;
    }
    if (req.body.pwd == ''){
        res.render('fail');
        return;
    }

    var user=new User(
        {name:name,
            pwd:pwd
        }
    )

    var name_s = req.body.name;
    var pwd_s = req.body.pwd;

    User.findOne({name:name_s,pwd:pwd_s}, function (error,result) {
            if (result != null) {
                res.render('fail');
                return;
            }
        }
    )

    user.save(
        function (err,result) {
            if (req.body.name == '') {
                res.render('fail');
            } else if (req.body.pwd == ''){
                res.render('fail');
            } else if (result==null) {
                res.render('fail');
            } else {
                res.render('regsuccess');
            }
        }
    ).then((user) => {
        console.log(user);

            return User.find({}).exec();
        })
        .then((users) => {
            console.log(users);
        })

})
app.post('/detail',function(req,res){
    temp = req.body
})
app.get('/favourites/create',function(req,res){
    var resname = temp.resname
    res.render('favourites/create',{resname:resname})
})
app.get("/favourites/:resname/edit", (req, res) => {
    var resname = req.params.resname
    var username = req.cookies.name
    var promise = User.findOne({name:username,'favours.name':resname},'favours.$').lean().exec()
    promise.then((doc)=>{
        var data = {}
        data['resname'] = doc.favours[0].name
        data['comment'] = doc.favours[0].comment
        res.render("favourites/edit", {
        data:data
    });
        
    })


});

//RESTFUL
app.get('/favourites',function(req,res){
    var favours = []
    var username = req.cookies.name
    var promise = User.findOne({name:username}).lean().exec();
    promise.then((doc)=>{
        var data = {}
        var len = doc.favours.length
        for (i=0;i<len;i++){
            data[i] = doc.favours[i]
        }
        res.render("favourites/index",{data:data})
    })

})
app.post('/favourites',function(req,res){
    if (req.body.comment == '') {
        res.render('fail2');
        return;
    }
    User.update({
    name : req.cookies.name
    }, {
    $push: {
        favours: {name:req.body.resname,comment:req.body.comment}
    }
}).then((user)=>{return User.find({name:req.cookies.name}).exec();}).then((users) => {
        })
    res.redirect('/favourites')
})
app.put("/favourites/:resname", (req, res) => {

    if (req.body.comment == '') {
        res.render('fail2');
        return;
    }
    var resname = req.body.resname
    var comment = req.body.comment
    User.update({"name":req.cookies.name,"favours.name":resname},
        {"$set":{"favours.$.comment":comment}},function(err,post){
            if(err){console.log(err)}
            console.log(post)
            res.redirect('/favourites')

        }
);
    
});

app.delete("/favourites/:resname", (req, res) => {
    var resname = req.params.resname
    var username = req.cookies.name
    console.log(resname)
    User.findOne({"name":username,"favours.name":resname},'favours.$',function(err,post){
        User.findOneAndUpdate({name:username},{"$pull":{favours:{_id:post.favours[0]._id}}},function(err,post){
            console.log(post)
            res.redirect('/favourites')
        })
    
    })
  
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});