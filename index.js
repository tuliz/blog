import express from 'express';
import bodyParser from 'body-parser';

const app = express();
app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static('public'));
const port = 3000;
const posts = [];

app.get('/',(req,res)=>{
    res.render('../views/index.ejs');
});

app.post('/submitForm',(req,res)=>{

});

app.listen(port, ()=>{
    console.log(`listening to port ${port}`);
});