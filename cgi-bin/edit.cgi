#!/usr/bin/perl
open(DATABASE, "tempdata.dat") || die("Could not open file!");
@data = <DATABASE>;
close(DATABASE);
$vname = <STDIN>;
$vname =~ s/name=//;   #vname is name entered/selected from View.cgi
$vname =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;   # Convert %XX from hex numbers to alphanumeric
$vname =~ s/[^A-Za-z0-9]//g;   #remove all special characters with
#$vname =~ s/\b(\w)/\U$1/g;   #capitalizes only the first letter
$vname =~ s/(\w+)/\u\L$1/g;   #capitalizes the first letter and lower case for the rest
@vname = split(//, $vname);   #These next few lines chops of anything after 15 characters.
$vname = "";
foreach $v (0 .. 14){
   $vname .= @vname[$v];
}

print "Content-type: text/html\n\n";

foreach $i (1 .. $#data){  #1 instead of 0 because the first record is feild names
   @tdata = split(/,/, @data[$i]);
   $dname .= ",@tdata[0],";   #dname is names from the database. Commas used for full name search
   if ($vname eq @tdata[0]){
      @profile = @tdata;   #Save data that maches the name for loading the profile for edit.
   }
}

#Setting Lotable items
@bastok = ("None",'\$',"BRD","BST","BLM","DRG","DRK","MNK","PLD","RDM","SAM","SMN","THF");
@windurst = ("None",'\$',"BST","BLM","DRK","NIN","PLD","RNG","SAM","SMN","THF","WAR","WHM");
@sandoria = ("None",'\$',"BRD","BST","DRG","MNK","NIN","PLD","RDM","RNG","SMN","WAR","WHM");
@jeuno = ("None",'\$',"BRD","BLM","DRG","DRK","MNK","NIN","RDM","RNG","SAM","THF","WAR","WHM");
@beaucedine = ("None",'\$',"BRD","BST","BLM","DRG","DRK","MNK","NIN","PLD","RDM","RNG","SAM","SMN","THF","WAR","WHM");
@xarcabard = ("None",'\$',"BRD","BST","BLM","DRG","DRK","MNK","NIN","PLD","RDM","RNG","SAM","SMN","THF","WAR","WHM");

@area = ("bastok","sandoria","windurst","jeuno","beaucedine","xarcabard");
@Area = ("Bastok","San d'Oria","Windurst","Jeuno","Beaucedine","Xarcabard");

if ($dname =~ m/,$vname,/){

###############################EDIToutput###############################
print <<HTMLOUT;
Welcome $vname! Editing profile
<form method="post" action="input.cgi">
<input type="hidden" name="name" value="$vname">
<table><tr><td width="310"><hr></td><td><h2>Dynamis</h2></td><td width="310"><hr></td></table>
 <table border="1" style="color:000000">
  <col bgcolor="9999FF"><col bgcolor="FF9999"><col bgcolor="99CC99"><col bgcolor="CCCCCC"><col bgcolor="CCFFFF"><col bgcolor="CC99CC">
  <tr>
HTMLOUT

foreach $a (0 .. 5){
   $area = @area[$a];
   $b = $a + 1;
print <<HTMLOUT;
   <th width="120">
    @Area[$a]<br>
    <select multiple name="@area[$a]" size="4">
HTMLOUT

   foreach $i (0 .. $#$area){
      $item = @$area[$i];
      $pro = @profile[$b];   #Skip Name feild and start with bastok feild data for current user
      &profile;   #Sub adds selected option to option tag to pre-select values in users current profile
      if (@$area[$i] eq '\$'){
         print qq!    <option value="@$area[$i]"$sel>\$</opton>\n!;
      }else{
         print qq!    <option value="@$area[$i]"$sel>@$area[$i]</opton>\n!;
      }
   }
   print <<HTMLOUT;
    </select>
   </th>
HTMLOUT

}

print "  </tr>\n  <tr>\n";
$proW = join(',',@profile);
foreach $c (0 .. $#area){
   $win = substr("@area[$c]",0,2);
   if ($proW =~ m/W$win/){
      $check = " Checked";
   }
   if ($c == "0"){
      print qq!   <th>Need Win?<input type="checkbox" name="$win" value="W$win"$check></th>\n!;
   }else{
      print qq!   <th><input type="checkbox" name="$win" value="W$win"$check></th>\n!;
   }
   $check = "";
}

print <<HTMLOUT;
  </tr>
 </table>
<table><tr><td width="310"><hr></td><td><h2>Mission</h2></td><td width="310"><hr></td></table>
<table><tr><td><input type="submit" value="submit"></form></td><td width="100\%">&nbsp</td><td><form method="post" action="delete.cgi">Delete:<input type="submit" value="X"><input type="hidden" name="name" value="$vname"></form></td></tr></table>
</body>
</html>
HTMLOUT

}else{

###############################CREATEOUTPUT###############################
print <<HTMLOUT;
<h2>CREATING NEW PROFILE</h2>
<h3>Welcome $vname!</h3>
<form method="post" action="input.cgi">
<input type="hidden" name="name" value="$vname">
<table><tr><td width="310"><hr></td><td><h2>Dynamis</h2></td><td width="310"><hr></td></table>
 <table border="1" style="color:000000">
  <col bgcolor="EEEEFF"><col bgcolor="FFEEEE"><col bgcolor="EEFFEE"><col bgcolor="EEEEEE"><col bgcolor="EEFFFF"><col bgcolor="CCBBCC">
  <tr>
HTMLOUT

foreach $a (0 .. 5){
   $area = @area[$a];
   $b = $a + 1;
print <<HTMLOUT;
   <td>
    @Area[$a]<br>
    <select multiple name="@area[$a]" size="4">
HTMLOUT

   foreach $i (0 .. $#$area){
      $item = @$area[$i];
      &default;
      if (@$area[$i] eq '\$'){
         print qq!    <option value="@$area[$i]"$sel>\$</opton>\n!;
      }else{
         print qq!    <option value="@$area[$i]"$sel>@$area[$i]</opton>\n!;
      }
   }
   print <<HTMLOUT;
    </select>
   </td>
HTMLOUT

}

print "  </tr>\n  <tr>\n";
foreach $c (0 .. $#area){
   $win = substr(@area[$c],0,2);
   if ($c == "0"){
      print qq!   <th>Need Win?<input type="checkbox" name="$win" value="W$win"></th>\n!;
   }else{
      print qq!   <th><input type="checkbox" name="$win" value="W$win"></th>\n!;
   }
}

print <<HTMLOUT;
  </tr>
 </table>
<table><tr><td width="310"><hr></td><td><h2>Mission</h2></td><td width="310"><hr></td></table>
<input type="submit" value="submit">
</form>
</body>
</html>
HTMLOUT

}


#####SUBS#####
sub default{
   if ($item eq "none"){
      $sel = " selected";
   }else{
      $sel = "";
   }
}

sub profile{
   if ($pro =~ m/$item/){
      $sel = " selected";
   }else{
      $sel = "";
   }
}