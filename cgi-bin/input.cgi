#!/usr/bin/perl
open(DATABASE, "tempdata.dat") || die("Could not open file!");
@csvdata = <DATABASE>;
close(DATABASE);
$e = 0;  #Used to determin if edit or not
@data = split(/&/, <STDIN>);   #@data is now name=value pairs
foreach $i (0 .. $#data){
   ($name, $value) = split(/=/, @data[$i]);   #splits name and value pairs into sperate scalars
   $value =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;   # Convert %XX from hex numbers to alphanumeric
   if ($name eq name){  #Name feild, requires special attention because user types it in.
      $value =~ s/[^A-Za-z0-9]//g;   #remove all special characters 
      #$value =~ s/\b(\w)/\U$1/g;   #capitalizes only the first letter
      $value =~ s/(\w+)/\u\L$1/g;   #capitalizes the first letter and lower case for the rest
      foreach $j (1 .. $#csvdata){   #Skip first record because it contains feild names
         @tdata = split(/,/, @csvdata[$j]);
         if ($value eq @tdata[0]){  #Determins an edit or create.
            $k = $j;
            $e = 1; 
         }
      }
   }
   if ($value eq '\$'){
   $value = "\$";
   }
   $t = $i + 1;   #$t = the next data set in @data. Required to put a / befor next item if multiple
   ($tname, $tvalue) = split(/=/, @data[$t]);
   if ($tname eq $name){
      $profile .= "$value/";
   }else{
      $profile .= "$value,";
   }
}
open(DATABASE, ">tempdata.dat") || die("Could not open file!");
#validate name feild in databas (for user error in editing the database)
foreach $v (0 .. $#csvdata){
@v = split(/,/, @csvdata[$v]);
      @v[0] =~ s/[^A-Za-z0-9]//g;   #remove all special characters 
      #@v[0] =~ s/\b(\w)/\U$1/g;   #capitalizes only the first letter
      @v[0] =~ s/(\w+)/\u\L$1/g;   #capitalizes the first letter and lower case for the rest
@csvdata[$v] = join(",",@v);
}
if ($e == 1){   #edit
   @csvdata[$k] = $profile;
}else{   #create
   push(@csvdata,"$profile");
}
$fields = shift(@csvdata);
@csvdata = sort(@csvdata);   #Sorts array. First record needs to be feilds so taken out for sort.
unshift(@csvdata,$fields);
foreach $l (0 .. $#csvdata){
   chomp(@csvdata[$l]);
   print DATABASE "@csvdata[$l]\n";
}
close(DATABASE);

print "Content-type: text/html\n\n";
print 'Database updated <a href="view.cgi">view</a>';
