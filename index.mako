<html>
<head>
    <link href='http://fonts.googleapis.com/css?family=Coda:400,800' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="images/bootstrap.min.css">
<style type="text/css">
body {
    background-image: url("images/bg.jpg");
    height:300%;
}
h1{
    font-weight: 800;
    font-family: 'Coda', cursive;
    color: #ffffff;
    font-size: 90;
    -webkit-text-stroke: 4px black;
}
.container {
    position: relative;
    width: 100%;
}
.container div {
    height: 300px;
}
.column-left {
    width: 25%;
    float: left;
    display: inline-block;
    font-family: 'Coda', cursive;
    text-align: center;
}
.column-center {
    width: 50%;
    float: left;
    font-size: 20;
    display: inline-block;
    background: rgba(0, 0, 0, 0.9);
    color: #ffffff;
    font-family: 'Coda', cursive;
    text-align: center;
    min-height: 100% !important;
    height: 100%;
}
.column-center td{
    color: #ffffff;
    font-family: 'Coda', cursive;
    font-size: 20;
    padding-left: 25px;
    padding-right: 10px;
}
.column-right {
    width: 25%;
    float: left;
    display: inline-block;
    text-align: center;
    font-family: 'Coda', cursive;
}
</style>

</head>



<body>

<%
    t=e_average+r_average
    ep="%.2f" % (float(e_average)/t*100)
    rp="%.2f" % (float(r_average)/t*100)

    %>


<div class="container">
    <div class="column-left">

        <h1>${rp}%</h1>
    <h1>${r_average}</h1>

    </div>


           <div class="column-center">
               <center>





                   <img src="images/bannerformCBRrev.png" width="100%"/>
                   <table width="100%" >
                   <tr>
                   <td>
                   <span style="color:#4595dd"> Resistance Agents: ${r_players}</span>
                   </td>
                   <td style="text-align: right">
                   <span style="color:#3bc455"> Enlightened Agents: ${e_players}</span>
                   </td>

                   </tr>

                   </table>
                   <br/>
               <table>
                   <tr>
                   %for c in ["Rank","Agent","Faction","Levels","AP",g_stat1Name,g_stat2Name]:

                       <td><h3>${c}</h3></td>
                   %endfor
                    </tr>


            % for i, a in enumerate(g_scoreboard):
               <tr>
                   <td>
                    ${i+1}
                    </td>
                   <%
                       if a[1]=="Enlightened":
                        f="#3bc455"
                       else:
                        f="#4595dd"
                       %>
                % for b in a:
                    <td>
                    <span style="color:${f}">${b}</span>
                    </td>

                    %endfor
                </tr>

            %endfor

              </table>

                   </center>

           </div>

   <div class="column-right">

        <h1>${ep}%</h1>
    <h1>${e_average}</h1>

       </div>


</div>
<meta http-equiv="refresh" content="31">
    <script src="images/jquery.min.js"></script>
    <script src="images/bootstrap.min.js"></script>
</body>
</html>