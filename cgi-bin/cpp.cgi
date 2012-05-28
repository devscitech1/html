#! /usr/bin/perl
#use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use Data::UUID;
use JSON;
my $request = new CGI;
my $ug = Data::UUID->new;
my $uuid=$ug->create_str();
my $file=$ug->to_string($uuid);
my $incode=$request->param('code');

my $codefile="/var/www/html/cpp/tmp/$file.cpp";
my $errorfile="/var/www/html/cpp/tmp/$file.err";
my $binary="bin";
my $results;
my $flag_save1=$request->param('flag_save1');
my $filename1=$request->param('filename1');
noguimode();
sub noguimode{
	open CODE,">$codefile";
	print CODE $incode;
	close CODE;
	print "Content-type: text/html\n\n";
	my $path=$ENV{'PATH'};
	$< = 0;
	$ENV{'HOME'}="/var/www/html/cpp";
	$ENV{'DISPLAY'}=":0.0";
	if($flag_save1==0)
	{
	my $cmd="g++ $codefile -o bin 2>&1";
	open (CMD,"$cmd|");
	my @data1=<CMD>;
	close CMD;

	my $cmd="./bin";
	open (CMD,"$cmd|");
	my @data2=<CMD>;
	close CMD;
	my $error;
	if (-e $errorfile){
		open (ERROR,$errorfile);
		my @error=<ERROR>;
		close ERROR;
		$error=join("",@error);
	}
	my $output=join("",@data1," ",@data2);
	$output =~ s/exit\(\);//g;
	$output =~ s/-->catch//g;
	$results->{"output"}=$output;
	$results->{"image"}=0;
	$results->{"imagefile"}="";
	$results->{"error"}=$error;
	my $json=objToJson($results);
	print $json;
	}
	if($flag_save1)
	{
	system("/bin/cp /var/www/html/cpp/tmp/$file.cpp /var/www/html/$filename1.cpp");
	}
	unlink $codefile;
	unlink $binary;
}