#$Mode clrcert - Clear certificates
Param
(
	[parameter(Mandatory=$false)][string]$Mode="up",
	[parameter(Mandatory=$false)][bool]$IsSimpleCertificate=$true
)
$ExitCode = 0
Write-Host "Batch mode="$Mode
Write-Host "Simple Certificate enable mode="$IsSimpleCertificate
$Projectpath = Convert-Path .

try{
	$res = Get-Process 'com.docker.proxy' -ErrorAction SilentlyContinue
	if([string]::IsNullOrEmpty($res)){
		Write-Host "DOCKER is not running. Visit and download https://docs.docker.com/docker-for-windows/install/ " -fore red
		Set-Location -Path $Projectpath
		exit -1
	}
	Set-Location -Path ./src
   
    if($Mode -eq "down"){
		docker-compose -f docker-compose.yml down
		docker-compose -f docker-compose.mssql.yml down
		docker-compose -f docker-compose.oracle.yml down
		Set-Location -Path $Projectpath
		exit 0
	}
	
	#Check docker folder sharing
	$PostgresFolder = $Projectpath +"\src"
	$Opts = "-v ${PostgresFolder}:/prj "
	Write-Host "Check shared project folder: "$PostgresFolder
	Write-Host "cmd: docker run --rm ${Opts} alpine ls /prj"

	$IsFolderSharing = $false
	Invoke-Expression -Command "docker run --rm ${Opts} alpine ls /prj" | ForEach-Object {
		Write-Host $_
		IF ($_.Contains("docker-compose.yml")){
			$IsFolderSharing = $true
		}
	}
	Write-Host "IsFolderSharing="$IsFolderSharing
	if(-Not $IsFolderSharing){
		Write-Host "Alpine container haven't access to the solution folder. Please check docker folder sharing setup."
		Set-Location -Path $Projectpath
		exit
	}
	

	if($Mode -eq "clrcert"){
		if (Test-Path -Path $Projectpath\src\srv\buildcertificate\rootca\rootCA.crt -PathType Leaf)
		{
			Write-Host "Delete rootCA.crt"
			Remove-Item -Recurse -Path $Projectpath\src\srv\buildcertificate\rootca\rootCA.crt -Force
		}
		if ((Test-Path -Path $Projectpath\src\srv\nginx\certs\host.docker.internal.crt -PathType Leaf))
		{
			Write-Host "Delete host.docker.internal.crt"
			Remove-Item -Recurse -Path $Projectpath\src\srv\nginx\certs\host.docker.internal.crt -Force
			Remove-Item -Recurse -Path $Projectpath\src\srv\buildcertificate\aspcertificat.pfx -Force
		}		
		exit
	}
	#Create self signet certificate
	Set-Location -Path $Projectpath\src\srv\buildcertificate
	./buildcrt.ps1 $IsSimpleCertificate
	if (-Not $LASTEXITCODE -eq 0)
    {
		Write-Host "Cant generate certificate host.docker.internal.crt"
    	exit -1
    }

	#Build main docker compose
	Set-Location -Path $Projectpath
	Set-Location -Path ./src
	if($Mode -eq "build"){
		docker-compose down
		docker-compose build  	
	}
	
	#You can check port 80
	#$check=Test-NetConnection $localhost -Port 80 -WarningAction SilentlyContinue
	#If ($check.tcpTestSucceeded -eq $true){
	#	Write-Host "Port 80 in use"
	#	netstat -ano -p tcp | Select-String "0.0.0.0:80"
	#	Set-Location -Path $Projectpath
	#	exit
	#}

	#Clean log folder
	$LogPath=$Projectpath+"/src/logs"
	if (Test-Path -Path $LogPath) {
		Write-Host "Remove old log"
		Remove-Item -Recurse -Path $LogPath -Force
		$LogPath=$Projectpath+"/src/images/airflow/logs"
		Remove-Item -Recurse -Path $LogPath -Force
	}

	New-Item -ItemType Directory -Force -Path $LogPath
	$LogPath=$Projectpath+"/src/logs/nginx"
	New-Item -ItemType Directory -Force -Path $LogPath
	Write-Host "docker-compose  start"
	
	docker-compose -f docker-compose.mssql.yml up -d
	docker-compose -f docker-compose.oracle.yml up -d

	docker-compose up 
	$ExitCode = 0
}
catch {
  
  Write-Host "An error occurred:" -fore red
  Write-Host $_ -fore red
  Write-Host "Stack:"
  Write-Host $_.ScriptStackTrace
  $ExitCode = -1
}
finally {
	Set-Location -Path $Projectpath
	exit $ExitCode
}

