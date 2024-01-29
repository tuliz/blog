import express from 'express';
import bodyParser from 'body-parser';

const app = express();
app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static('public'));
const port = 3000;
const posts = [];

app.get('/',(req,res)=>{
    res.render('../views/index.ejs',{posts:posts});
});

app.post('/submitPost',(req,res)=>{
    let post ={
        subject:req.body.subject,
        message:req.body.message
    };

    posts.push(post);
    res.render('../views/index.ejs',{posts:posts});
});

app.listen(port, ()=>{
    console.log(`listening to port ${port}`);
});