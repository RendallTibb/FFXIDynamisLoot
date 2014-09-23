#!/usr/bin/perl
print "Content-type: text/html\n\n";
print "<html>\n";
print '<head><link rel="stylesheet" type="text/css" href="../style.css" /></head>';
print "\n<body><h1>Linshell Statistics</h1>\n";
open(DATABASE, "tempdata.dat") || die("Could not open file!");
@data = <DATABASE>;
close(DATABASE);
print <<HTMLOUT;
<table border=1 bgcolor="FFFFFF" style="color:000000">
<col><col bgcolor="EEEEFF"><col bgcolor="FFEEEE"><col bgcolor="EEFFEE"><col bgcolor="EEEEEE"><col bgcolor="EEFFFF"><col bgcolor="CCBBCC">
HTMLOUT

print "<tr><th>Jobs</th>";
#PRINTS FEILDS
@fcolors = ('',' bgcolor="9999FF"',' bgcolor="FF9999"',' bgcolor="99CC99"',' bgcolor="CCCCCC"',' bgcolor="CCFFFF"',' bgcolor="CC99CC"','');
chomp(@data[0]);
@tdata = split(/,/, @data[0]);
foreach $i (1 .. 6){
   print "<th@fcolors[$i]>@tdata[$i]</th>";
}
print "<th>Totals</th></tr>\n";

@job = ("","BRD","BST","BLM","DRG","DRK","MNK","NIN","PLD","RDM","RNG","SAM","SMN","THF","WAR","WHM",'\$',);
#PRINTS DATA
foreach $j (1 .. $#job){   #foreach job (brd,bst,blm..etc.)
   if (@job[$j] eq '\$'){
      print '<tr><th>$</th>';
   }else{
      print "<tr><th>@job[$j]</th>";
   }
   $job = @job[$j];
   $total = 0;
   foreach $f (1 .. 6){   #foreach feild (dynamis bas,win,san,jeu..etc.)
      @$job[$f] = 0;
      foreach  $p (1 .. $#data){   #foreach user profile except feilds record.
         @tdata = split(/,/, @data[$p]);
         @rules = split(/\//, @tdata[$f]);
         if (@rules[0] eq '$' || @rules[1] eq '$'){   #Can't lot money(default) and AF
            @tdata[$f] = '$';
         }elsif ($f == "5" || $f == "6"){   #1 AF for beau or xarc
            @tdata[$f] = "@rules[0]";
         }elsif ($#rules > "1"){   #no more than 2 AF
            @tdata[$f] = "@rules[0]/@rules[1]";
         }
         if (@tdata[$f] =~ m/@job[$j]/){
            @$job[$f]++;
         }
         #Only 1 win per run.  This following will show total AF needed for 1 run.
         #$perun = "@rules[0]";
         #if ($perun =~ m/@job[$j]/){
         #   $tperun++;
         #}
      }
      print "<th>@$job[$f]</th>";
      $total += @$job[$f];
      @total[$f] += @$job[$f]; 
   }
   print "<th>$total</th></tr>\n";
}
print "<tr><th colspan=\"8\">AF/Money Totals and Wins Needed</th></tr>\n";
print '<tr><th>AF & $</th>';   #AF and money totals
foreach $t (1 .. $#total){
   print "<th>@total[$t]</th>";
   $tt += @total[$t];
}
print "<th>$tt</th></tr>\n";
$tt = 0;
print "<tr><th>AF</th>";   #AF totals/area
$job = @job[16];
foreach $T (1 .. $#total){
   @total[$T] -= @$job[$T];
   print "<th>@total[$T]</th>";
   $tt += @total[$T];
}
print "<th>$tt</th></tr>\n";
$tt = 0;
@area = ("ba","sa","wi","je","be","xa");   #Win totals
print "<tr><th>WIN</th>";
foreach $a (0 .. $#area){
   foreach $d (1 .. @data){
      if (@data[$d] =~ m/@area[$a]/){
         @twin[$a]++
      }
   }
   print "<th>@twin[$a]</th>";
   $tt += @twin[$a];
}
print "<th>$tt</th></tr>\n";
#print qq!</table>If only one AF allowed in cities then total AF & \$ = $tperun<br><a href="view.cgi">View</a></body></html>!;
print '</table><a href="view.cgi">View</a></body></html>';