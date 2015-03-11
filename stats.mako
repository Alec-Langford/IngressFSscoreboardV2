<html>
<head>
    <link href='http://fonts.googleapis.com/css?family=Coda:400,800' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="images/bootstrap.min.css">

 <style type="text/css">
body {
    background-color: #000;
    height:100%;
    color: #fff;
}
h1{
    font-weight: 800;
    font-family: 'Coda', cursive;
    color: #ffffff;
    font-size: 90;
    -webkit-text-stroke: 4px black;
}
</style>

%for item in sorted(context.keys()):
    %if item[1]=="_":

    ${item}: ${context[item]}

    %endif
    <br/>

   %endfor