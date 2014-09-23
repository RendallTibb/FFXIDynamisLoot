#!/usr/bin/perl
print "Content-type: text/html\n\n";
print "<html>\n";
print '<head><link rel="stylesheet" type="text/css" href="../style.css" /></head>';
print "\n<body><h1>Dynamis info</h1>\n";
open(DATABASE, "tempdata.dat") || die("Could not open file!");
@data = <DATABASE>;
close(DATABASE);
print <<HTMLOUT;
<form method="post" action="edit.cgi">Enter your name to create or modify:<input type="text" name="name"><input type="submit" value="submit"></form>
<form method="post" action="edit.cgi">
<table border=1 bgcolor="FFFFFF" style="color:000000">
<col><col bgcolor="EEEEFF"><col bgcolor="FFEEEE"><col bgcolor="EEFFEE"><col bgcolor="EEEEEE"><col bgcolor="EEFFFF"><col bgcolor="CCBBCC">
HTMLOUT

print '<tr>';
#PRINTS FEILDS
@fcolors = ('',' bgcolor="9999FF"',' bgcolor="FF9999"',' bgcolor="99CC99"',' bgcolor="CCCCCC"',' bgcolor="CCFFFF"',' bgcolor="CC99CC"');
chomp(@data[0]);
@tdata = split(/,/, @data[0]);
foreach $i (0 .. $#tdata){
   print "<th@fcolors[$i]>@tdata[$i]</th>";
}
print "</tr>\n";

#PRINTS DATA
@area = ("ba","sa","wi","je","be","xa");
foreach $i (1 .. $#data){
   chomp(@data[$i]);
   print '<tr align="center">';
   @tdata = split(/,/, @data[$i]);
   foreach $j (0 .. 6){
      if ($j == 0){
         print qq!<td><input type="submit" name="name" value="@tdata[0]"></td>!;
      }else{
         @rules = split(/\//, @tdata[$j]);
         if (@rules[0] eq "none"){   #No AF or Money
            print '<td>none</td>';
         }elsif (@rules[0] eq "\$" || @rules[1] eq "\$"){   #Can't lot money(default) and AF
            print '<td>$</td>';
         }elsif ($j == "5" || $j == "6"){   #1 AF for beau or xarc
            print "<td>@rules[0]</td>";
         }elsif ($#rules > "1"){   #no more than 2 AF
            print "<td>@rules[0]/@rules[1]</td>";
         }else{
            print "<td>@tdata[$j]</td>";
         }
      }
   }
   print '<td>';
   foreach $a (0 .. $#area){   #This part is for WIN feild.
      if ("@tdata[7]" eq "W@area[$a]"){
         if ("@area[$a]" eq "be"){
            print "B";
            splice(@tdata,7,1);
         }else{
            $win = substr(@area[$a],0,-1);
            print "$win";
            splice(@tdata,7,1);
         }
      }else{
         print '/';
      }
   }
   print "</td></tr>\n";
}


print '</font></table></form><a href="statistics.cgi">Statistics</a></body></html>';
