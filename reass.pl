#!/usr/bin/perl
use strict;
use Regexp::Assemble;
 
my $ra = Regexp::Assemble->new;
while (<>)
{
  $_ =~ /^\s*$/ and next;
  $_ =~ /^#/ and next;
  $ra->add($_);
}
print $ra->as_string() . "\n";
