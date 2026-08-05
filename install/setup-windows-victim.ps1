<#
  setup-windows-victim.ps1
  Full automated setup for the Windows victim VM:
    1. Wazuh agent, pointed at the manager
    2. Sysmon with SwiftOnSecurity's community config
    3. Sysmon localfile + Security channel wired into ossec.conf
    4. Advanced audit policy for scheduled task creation (Event 4698)
    5. PowerShell Script Block Logging
    6. Atomic Red Team (invoke-atomicredteam + atomics library)

  Run as Administrator. Usage:
    .\setup-windows-victim.ps1 -ManagerIp 192.168.56.10
#>

param(
  [Parameter(Mandatory = $true)]
  [string]$ManagerIp
)

$ErrorActionPreference = "Stop"
$work = "$env:TEMP\siem-lab-setup"
New-Item -ItemType Directory -Force -Path $work | Out-Null

Write-Host "[1/6] Installing Wazuh agent..." -ForegroundColor Cyan
$agentMsi = "$work\wazuh-agent.msi"
Invoke-WebRequest -Uri "https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.0-1.msi" -OutFile $agentMsi
Start-Process msiexec.exe -ArgumentList "/i `"$agentMsi`" /q WAZUH_MANAGER='$ManagerIp'" -Wait
Start-Service -Name WazuhSvc

Write-Host "[2/6] Installing Sysmon (SwiftOnSecurity config)..." -ForegroundColor Cyan
Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Sysmon.zip" -OutFile "$work\Sysmon.zip"
Expand-Archive "$work\Sysmon.zip" -DestinationPath "$work\Sysmon" -Force
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml" -OutFile "$work\sysmonconfig.xml"
& "$work\Sysmon\Sysmon64.exe" -accepteula -i "$work\sysmonconfig.xml"

Write-Host "[3/6] Wiring Sysmon/PowerShell/Security channels into ossec.conf..." -ForegroundColor Cyan
$ossecConf = "C:\Program Files (x86)\ossec-agent\ossec.conf"
$snippet = Get-Content "$PSScriptRoot\..\config\ossec-agent-snippet.conf" -Raw
if (Test-Path $ossecConf) {
  $content = Get-Content $ossecConf -Raw
  $content = $content -replace "</ossec_config>", "$snippet`n</ossec_config>"
  Set-Content -Path $ossecConf -Value $content
  Restart-Service -Name WazuhSvc
} else {
  Write-Warning "ossec.conf not found at expected path — add the localfile snippet manually."
}

Write-Host "[4/6] Enabling advanced audit policy for scheduled task creation (Event 4698)..." -ForegroundColor Cyan
auditpol /set /subcategory:"Other Object Access Events" /success:enable | Out-Null

Write-Host "[5/6] Enabling PowerShell Script Block Logging..." -ForegroundColor Cyan
$sblPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
New-Item -Path $sblPath -Force | Out-Null
Set-ItemProperty -Path $sblPath -Name "EnableScriptBlockLogging" -Value 1

Write-Host "[6/6] Installing Atomic Red Team..." -ForegroundColor Cyan
Install-PackageProvider -Name NuGet -Force -Scope CurrentUser | Out-Null
Install-Module -Name invoke-atomicredteam, powershell-yaml -Scope CurrentUser -Force
Import-Module invoke-atomicredteam -Force
Install-AtomicRedTeam -getAtomics -Force

Write-Host "`nSetup complete. Verify:" -ForegroundColor Green
Write-Host "  - Agent shows 'Active' in Wazuh Dashboard > Agents"
Write-Host "  - Get-WinEvent -ListLog 'Microsoft-Windows-Sysmon/Operational' returns a log"
Write-Host "  - auditpol /get /subcategory:`"Other Object Access Events`" shows Success enabled"
Write-Host "  - Invoke-AtomicTest T1082 -ShowDetailsBrief lists tests without executing"
