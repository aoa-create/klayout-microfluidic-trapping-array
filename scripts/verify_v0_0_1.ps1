[CmdletBinding()]
param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'

$requiredFiles = @(
    'AGENTS.md',
    'README.md',
    'THIRD_PARTY_NOTICES.md',
    'trapping_array_pcell.lym',
    'docs/PROJECT_EXECUTION_PROTOCOL.md',
    'docs/CURRENT_STATE.md',
    'docs/DELIVERY_PLAN.md',
    'docs/ROADMAP.md'
)

foreach ($relativePath in $requiredFiles) {
    $fullPath = Join-Path $RepositoryRoot $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Missing required V0.0.1 file: $relativePath"
    }
}

$macroPath = Join-Path $RepositoryRoot 'trapping_array_pcell.lym'
$macroHash = (Get-FileHash -LiteralPath $macroPath -Algorithm SHA256).Hash
$projectHead = git -C $RepositoryRoot rev-parse HEAD
$origin = git -C $RepositoryRoot remote get-url origin
$klayoutExecutable = Get-Command klayout, klayout_app -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $klayoutExecutable) {
    $knownInstall = Join-Path $env:APPDATA 'KLayout\klayout_app.exe'
    if (Test-Path -LiteralPath $knownInstall -PathType Leaf) {
        $klayoutExecutable = Get-Item -LiteralPath $knownInstall
    }
}

[pscustomobject]@{
    ProjectCommit  = $projectHead.Trim()
    Origin         = $origin.Trim()
    MacroSha256    = $macroHash
    KLayoutFound   = [bool]$klayoutExecutable
    KLayoutPath    = if ($klayoutExecutable) {
        if ($klayoutExecutable.Source) { $klayoutExecutable.Source } else { $klayoutExecutable.FullName }
    } else { $null }
} | Format-List
