<#
  run-atomics.ps1
  Convenience runner for the Windows-side atomics used in this lab.
  Run as Administrator on the victim VM after Invoke-AtomicRedTeam is installed.
#>

param(
  [switch]$Cleanup
)

$tests = @(
  @{ Id = "T1059.001"; Num = 3 },  # Encoded PowerShell
  @{ Id = "T1053.005"; Num = 1 },  # Scheduled task creation
  @{ Id = "T1003.001"; Num = 1 }   # LSASS dump via comsvcs.dll
)

foreach ($t in $tests) {
  Write-Host "=== $($t.Id) test $($t.Num) ===" -ForegroundColor Cyan
  if ($Cleanup) {
    Invoke-AtomicTest $t.Id -TestNumbers $t.Num -Cleanup
  } else {
    Invoke-AtomicTest $t.Id -TestNumbers $t.Num
    Start-Sleep -Seconds 5
  }
}
