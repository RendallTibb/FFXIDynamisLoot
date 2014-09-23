#!/usr/bin/perl
($delete, $name) = split(/=/, <STDIN>);
print "Content-type: text/html\n\n";
if ($delete eq "name"){   #input came from input.cgi
   print "<div align=\"center\"><h3>!::WARNING::!</h3>$name will be completely removed from the database.<br>";
   print qq!<form method="post" action="delete.cgi"><input type="submit" value="DELETE"><input type="hidden" name="delete" value="$name"></form></div>!;
}elsif ($delete eq "delete"){  #input came from this form. Delete confirmed.
   open(DATABASE, "tempdata.dat") || die("Could not open file!");
   @csvdata = <DATABASE>;
   close(DATABASE);
   foreach $i (1 .. $#csvdata){   #Skip first record because it contains feild names
      @tdata = split(/,/, @csvdata[$i]);
      if ($name eq @tdata[0]){
         splice(@csvdata,$i,1);
      }
   }
   open(DATABASE, ">tempdata.dat") || die("Could not open file!");
   $fields = shift(@csvdata);
   @csvdata = sort(@csvdata);   #Sorts array. First record needs to be feilds so taken out for sort.
   unshift(@csvdata,$fields);
   foreach $l (0 .. $#csvdata){
      chomp(@csvdata[$l]);
      print DATABASE "@csvdata[$l]\n";
   }
   close(DATABASE);
   print 'Database updated <a href="view.cgi">view</a>';
}else{
print "ERROR";
}

