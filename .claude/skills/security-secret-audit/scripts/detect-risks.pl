use strict;
use warnings;

my $label = 'input';
my $path = '';

while (@ARGV) {
    my $arg = shift @ARGV;
    if ($arg eq '--label') {
        die "missing value for --label\n" unless @ARGV;
        $label = shift @ARGV;
    }
    elsif ($arg eq '--path') {
        die "missing value for --path\n" unless @ARGV;
        $path = shift @ARGV;
    }
    else {
        die "unknown option: $arg\n";
    }
}

sub is_source_or_config_path {
    return 1 if $path eq '';
    return $path =~ /\.(?:cjs|conf|config|cts|env|ini|java|js|json|jsx|mjs|mts|php|properties|py|rb|sh|tf|toml|ts|tsx|ya?ml)$/i;
}

my $found = 0;
my $line_number = 0;

while (my $line = <STDIN>) {
    ++$line_number;
    last if index($line, "\0") >= 0;
    next unless is_source_or_config_path();

    my @rules;
    push @rules, 'transport-security-disabled'
        if $line =~ /(?:verify\s*=\s*False|rejectUnauthorized\s*:\s*false|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*["']?0)/i;
    push @rules, 'shell-command-execution'
        if $line =~ /(?:os\.system\s*\(|child_process\.exec(?:Sync)?\s*\(|(?:subprocess|Popen|run|call)\s*\([^\n]*shell\s*=\s*True)/i;
    push @rules, 'permissive-cors-origin'
        if $line =~ /(?:access-control-allow-origin\s*[:=]\s*["']?\*|origin\s*:\s*["']\*)/i;
    push @rules, 'world-writable-permissions'
        if $line =~ /\bchmod\s+(?:0?777)\b/i;
    push @rules, 'sensitive-data-logging'
        if $line =~ /(?:console\.log|logger\.(?:debug|error|info|warn)|print)\s*\([^\n]*(?:api[_ -]?key|password|secret|token)/i;

    my %seen;
    for my $rule (@rules) {
        next if $seen{$rule}++;
        print "$label:$line_number:$rule\n";
        $found = 1;
    }
}

exit($found ? 2 : 0);
