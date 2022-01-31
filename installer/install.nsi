;--------------------------------
!include "MUI2.nsh"
!include x64.nsh
!include LogicLib.nsh

;--------------------------------

;General
;Name and file
Unicode True
Name "M&B II Bannelord - čeština"
OutFile "MaB2-Bannelord-Cestina.exe"

;Text in bottom of the installer
BrandingText "Mount and Blade II: Bannelord - čeština"

!define DEFAULT_PATH "Steam\steamapps\common\Mount & Blade II Bannerlord\"

;Default installation folder
InstallDir "$PROGRAMFILES\${DEFAULT_PATH}"

;Get installation folder from registry if available
InstallDirRegKey HKCU "Software\MaBII-Cestina" ""

;Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------

#general settings 
;!define MUI_PRODUCT "M&B II Bannelord - čeština"
!define MUI_FILE "savefile"
!define MUI_VERSION "1.0"
CRCCheck On

;Icon
!define MUI_ICON "bannerlord_icon.ico"

;Images
!define MUI_WELCOMEFINISHPAGE_BITMAP "bannelord_welcome.bmp"
 
; We should test if we must use an absolute path 
!include "${NSISDIR}\Contrib\Modern UI\System.nsh"
!Include 'MUI.nsh'

!define WELCOME_TITLE 'Vítejte u instalace češtiny do hry Mount & Blade II: Bannelord'

;--------------------------------
;Pages
!define MUI_WELCOMEPAGE_TITLE '${WELCOME_TITLE}'
;!define MUI_WELCOMEPAGE_TEXT "cz_license.txt"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "cz_license.rtf"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH
  
;--------------------------------
 
 
;--------------------------------
;Language
 
!insertmacro MUI_LANGUAGE "Czech"

;--------------------------------
;Installer Sections

Section "Čeština" MainSec
    SetOutPath "$INSTDIR"
  
    ;ADD YOUR OWN FILES HERE...
    File /r "preklad\*"
    
    ;Store installation folder
    WriteRegStr HKCU "Software\MaBII-Cestina" "" $INSTDIR
    
    ;Create uninstaller
    WriteUninstaller "$INSTDIR\Odinstalace_cestiny.exe"
SectionEnd 

;--------------------------------
;Descriptions

;Language strings
LangString DESC_MainSec ${LANG_CZECH} "Čeština"

;Assign language strings to sections
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${MainSec} $(DESC_MainSec)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

!include LogicLib.nsh
!include Sections.nsh

Function .onInit
    !insertmacro SetSectionFlag ${MainSec} ${SF_RO} 
    
    ;Check if system is 64 bit distibution. Need to change RegView if OS is 64 bit. 
    ${If} ${RunningX64}
        SetRegView 64
    ${EndIf}

    ;Check if previous version of czech language is installed. 
    ClearErrors
    ReadRegStr $0 HKCU "Software\MaBII-Cestina" ""
    ${If} ${Errors}
        ;Czech language is not installed. Try find steam path of game. TODO: Other distributions eg. Epic Games
        ClearErrors
        ReadRegStr $0 HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 261550" "InstallLocation"

        ${IfNot} !${Errors}
            ;MessageBox MB_OK "Value is: $0"
            StrCpy $INSTDIR "$0"
        ${EndIf}
    ${EndIf}
FunctionEnd

;--------------------------------
;Uninstaller Section
Section "Uninstall"
    Delete "$INSTDIR\Odinstalace_cestiny.exe"

    Delete "$INSTDIR\Modules\Native\ModuleData\Languages\CZ\*.*"
    Delete "$INSTDIR\Modules\SandBox\ModuleData\Languages\CZ\*.*"
    Delete "$INSTDIR\Modules\SandBoxCore\ModuleData\Languages\CZ\*.*"
    Delete "$INSTDIR\Modules\StoryMode\ModuleData\Languages\CZ\*.*"

    RMDir "$INSTDIR\Modules\Native\ModuleData\Languages\CZ"
    RMDir "$INSTDIR\Modules\SandBox\ModuleData\Languages\CZ"
    RMDir "$INSTDIR\Modules\SandBoxCore\ModuleData\Languages\CZ"
    RMDir "$INSTDIR\Modules\StoryMode\ModuleData\Languages\CZ"

    DeleteRegKey /ifempty HKCU "Software\MaBII-Cestina"
SectionEnd
