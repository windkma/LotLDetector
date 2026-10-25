"""
rules_constants.py
------------------
Cybersecurity domain knowledge bases used for Living-off-the-Land (LotL)
attack feature extraction.

References:
- LOLBAS Project   : https://lolbas-project.github.io
- GTFOBins Project : https://gtfobins.github.io
- MITRE ATT&CK     : https://attack.mitre.org
- Adobe libLOL     : https://github.com/adobe/libLOL (Apache-2.0)
"""

# ==============================================================================
# WINDOWS - LOLBins (Living off the Land Binaries)
# Source: https://lolbas-project.github.io
# ==============================================================================

WINDOWS_COMMANDS = [
    # Download & Remote Execution
    "appinstaller", "appinstaller.exe",
    "bitsadmin", "bitsadmin.exe",
    "certreq", "certreq.exe",
    "certutil", "certutil.exe",
    "curl", "curl.exe",
    "tar", "tar.exe",
    "winget", "winget.exe",
    "desktopimgdownldr", "desktopimgdownldr.exe",
    "dfsvc", "dfsvc.exe",
    "ieexec", "ieexec.exe",
    "mpcmdrun", "mpcmdrun.exe",
    "squirrel", "squirrel.exe",
    "update", "update.exe",
    "wuauclt", "wuauclt.exe",
    "hh", "hh.exe",

    # Arbitrary Code Execution
    "at", "at.exe",
    "atbroker", "atbroker.exe",
    "bash", "bash.exe",
    "cmd", "cmd.exe",
    "csc", "csc.exe",
    "cscript", "cscript.exe",
    "control", "control.exe",
    "dllhost", "dllhost.exe",
    "forfiles", "forfiles.exe",
    "ilasm", "ilasm.exe",
    "infdefaultinstall", "infdefaultinstall.exe",
    "installutil", "installutil.exe",
    "jsc", "jsc.exe",
    "makecab", "makecab.exe",
    "mavinject", "mavinject.exe",
    "mmc", "mmc.exe",
    "msbuild", "msbuild.exe",
    "mshta", "mshta.exe",
    "msiexec", "msiexec.exe",
    "odbcconf", "odbcconf.exe",
    "pcalua", "pcalua.exe",
    "powershell", "powershell.exe",
    "regasm", "regasm.exe",
    "regsvcs", "regsvcs.exe",
    "regsvr32", "regsvr32.exe",
    "rundll32", "rundll32.exe",
    "runonce", "runonce.exe",
    "runscripthelper", "runscripthelper.exe",
    "scriptrunner", "scriptrunner.exe",
    "schtasks", "schtasks.exe",
    "verclsid", "verclsid.exe",
    "wab", "wab.exe",
    "wmic", "wmic.exe",
    "wscript", "wscript.exe",
    "wsreset", "wsreset.exe",
    "xwizard", "xwizard.exe",
    "microsoft.workflow.compiler", "microsoft.workflow.compiler.exe",
    "python", "python.exe",

    # File Manipulation & Tunneling
    "diantz", "diantz.exe",
    "diskshadow", "diskshadow.exe",
    "esentutl", "esentutl.exe",
    "expand", "expand.exe",
    "extexport", "extexport.exe",
    "extrac32", "extrac32.exe",
    "ftp", "ftp.exe",
    "replace", "replace.exe",
    "wusa", "wusa.exe",
    "xcopy", "xcopy.exe",

    # Reconnaissance & Discovery
    "arp", "arp.exe",
    "chcp", "chcp.exe",
    "cmdkey", "cmdkey.exe",
    "dnscmd", "dnscmd.exe",
    "eventvwr", "eventvwr.exe",
    "findstr", "findstr.exe",
    "gpresult", "gpresult.exe",
    "net", "net.exe",
    "netsh", "netsh.exe",
    "nltest", "nltest.exe",
    "qwinsta", "qwinsta.exe",
    "reg", "reg.exe",
    "regedit", "regedit.exe",
    "sc", "sc.exe",
    "systeminfo", "systeminfo.exe",
    "tasklist", "tasklist.exe",
    "wevtutil", "wevtutil.exe",

    # Lateral Movement & Remote Execution
    "psexec", "psexec.exe",
    "telnet", "telnet.exe",
    "winrm", "winrm.exe",
    "winrs", "winrs.exe",
    "wsl", "wsl.exe",
    "ssh", "ssh.exe",
    "conhost", "conhost.exe",
    "vssadmin", "vssadmin.exe",
    "wbadmin", "wbadmin.exe",
    "bcdedit", "bcdedit.exe",

    # Credential Dumping & Post-Exploitation
    "gsecdump", "gsecdump.exe",
    "mimikatz", "mimikatz.exe",
    "procdump", "procdump.exe",
    "rubeus", "rubeus.exe",
    "sdelete", "sdelete.exe",
    "sharphound", "sharphound.exe",
    "sharpgpoabuse", "sharpgpoabuse.exe",
    "wce", "wce.exe",

    # Privilege Escalation
    "juicypotato", "juicypotato.exe",
    "roguepotato", "roguepotato.exe",

    # DLL Execution & Proxy Execution
    "advpack", "advpack.exe",
    "comsvcs", "comsvcs.exe",
    "ieadvpack", "ieadvpack.exe",
    "ieaframe", "ieaframe.exe",
    "mshtml", "mshtml.exe",
    "pcwutl", "pcwutl.exe",
    "setupapi", "setupapi.exe",
    "shell32", "shell32.exe",
    "syssetup", "syssetup.exe",
    "url", "url.exe",
    "zipfldr", "zipfldr.exe",

    # Developer Tools
    "adplus", "adplus.exe",
    "agentexecutor", "agentexecutor.exe",
    "bginfo", "bginfo.exe",
    "cdb", "cdb.exe",
    "devtoolslauncher", "devtoolslauncher.exe",
    "dnx", "dnx.exe",
    "dotnet", "dotnet.exe",
    "dxcap", "dxcap.exe",
    "excel", "excel.exe",
    "msdeploy", "msdeploy.exe",
    "msxsl", "msxsl.exe",
    "ntdsutil", "ntdsutil.exe",
    "powerpnt", "powerpnt.exe",
    "remote", "remote.exe",
    "sqldumper", "sqldumper.exe",
    "sqlps", "sqlps.exe",
    "te", "te.exe",
    "tracker", "tracker.exe",
    "vsjitdebugger", "vsjitdebugger.exe",
    "winword", "winword.exe",

    # Network Tools
    "nc", "nc.exe",
    "nmap", "nmap.exe",
]


# ==============================================================================
# WINDOWS - Sensitive System Paths
# ==============================================================================

WINDOWS_PATHS = [
    "C:\\Windows\\Microsoft.NET\\Framework64",
    "C:\\Windows\\Temp",
    "C:\\Windows\\System32",
    "C:\\Windows\\SysWOW64",
    "C:\\Windows\\System32\\svchost.exe",
    "C:\\Windows\\System32\\WScript.exe",
    "C:\\Windows\\System32\\cmd.exe",
    "C:\\Windows\\System32\\Rundll32.exe",
    "C:\\Windows\\System32\\mshta.exe",
    "C:\\Windows\\System32\\WindowsPowerShell",
    "C:\\ProgramData\\Microsoft",
    "C:\\Users\\Public",
    "ADMIN$",
    "C$",
    "IPC$",
]


# ==============================================================================
# WINDOWS - Sensitive Keywords
# Preserved empty list convention matching Adobe libLOL.
# Contextual keyword patterns are captured via WINDOWS_REGEX_LIST below.
# ==============================================================================

WINDOWS_KEYWORDS = [
]


# ==============================================================================
# WINDOWS - Regex Pattern Groups for Attack Behaviors
# ==============================================================================

WINDOWS_REGEX_LIST = [
    # Group 1: Download & Remote Execution
    (
        r"(?P<desktopimgdownldr_conn>desktopimgdownldr.*http)"
        r"|(?P<powershell_tcp_socket>New-Object.*Sockets.*TCPClient)"
        r"|(?P<certutil_downloader>certutil.*urlcache.*http)"
        r"|(?P<certutil_downloader_execute>certutil.*urlcache.*http.*InstallUtil)"
        r"|(?P<certutil_download_decode>certutil.*urlcache.*http.*decode)"
        r"|(?P<msbuild_get_execute>MSBuil.*\!MB.*autoresponse)"
        r"|(?P<msbuild_get_execute_lc>msbuil.*\!mb.*autoresponse)"
        r"|(?P<odbconf_regsvr>odbcconf[\s\w]+.*regsvr)"
        r"|(?P<regsvr32_download>regsvr32[\s\w\/]+.*http)"
        r"|(?P<regasm_download>regasm.*[\s\w\/]+)"
        r"|(?P<wmic_download>wmic.*os.*get.*http)"
        r"|(?P<rundll32_js_http>rundll32.*javascript.*http)"
        r"|(?P<mshta_http>mshta.*http)"
        r"|(?P<mshta_vbscript>mshta.*vbscript)"
        r"|(?P<cscript_jscript>cscript.*jscript)"
        r"|(?P<mshta_hta_script>mshta.*\.hta)"
        r"|(?P<cmd_k>cmd.*/k)"
        r"|(?P<exec_bypass>exec\s+bypass)"
        r"|(?P<powershell_execute_script>powershell.*\-c)"
        r"|(?P<powershell_net_client>Object.*Net.*WebClient)"
        r"|(?P<powershell_net_client_credentials>Object.*Net.*WebClient.*Credentials)"
        r"|(?P<powershell_write_bytes>io\.file.*WriteAllBytes)"
        r"|(?P<powershell_http_client>Object.*Net.*Http)"
        r"|(?P<bitsadmin_transfer_http>bitsadmin.*transfer.*http)"
        r"|(?P<bitsadmin_download_http>bitsadmin.*download.*http)"
        r"|(?P<powershell_iwr_http>iwr.*http)"
        r"|(?P<powershell_iwr_http_up>IWR.*http)"
        r"|(?P<powershell_invoke_web_request>Invoke\-WebRequest.*http)"
        r"|(?P<powershell_web_client_download>ystem.*eb.*lient.*ownload)"
        r"|(?P<powershell_http_requests_open>in.*ttp.*equest.*open)"
        r"|(?P<powershell_http_requests_get>in.*ttp.*equest.*GET)"
        r"|(?P<powershell_http_requests_post>in.*ttp.*equest.*POST)"
        r"|(?P<pubprn_http>pubprn.*http)"
        r"|(?P<pubprn_script>pubprn.*script)"
        r"|(?P<hh_http>HH.*http)"
        r"|(?P<ieexec_http>ieexec.*http)"
        r"|(?P<mpcmdrun_http>MpCmdRun.*http)"
        r"|(?P<mpcmdrun_downloadfile>MpCmdRun.*DownloadFile)"
        r"|(?P<ms_appinstaller_http>start.*appinstaller.*http)"
        r"|(?P<winword_http>winword.*http)"
        r"|(?P<squirrel_http>squirrel.*http)"
        r"|(?P<update_http>Update.*http)"
        r"|(?P<squirrel_download>squirrel.*download)"
        r"|(?P<powerpoint_http>owerpnt.*http)"
        r"|(?P<excel_http>excel.*http)"
        r"|(?P<DataSvcUtil_http>DataSvcUtil.*/uri)"
        r"|(?P<ConfigSecurityPolicy_http>onfig.*ecurity.*olicy.*http)"
        r"|(?P<cmstp_http>cmstp.*http)"
        r"|(?P<winrm_http>winrm.*http)"
        r"|(?P<wsl_exec>wsl.*exec)"
        r"|(?P<wsl_dev_tcp>wsl.*dev.*tcp)"
        r"|(?P<wsl_e>wsl.*\-e)"
        r"|(?P<tftp_I>tftp.*\-I)"
        r"|(?P<KEYWORD_http>http.{0,1}:\/\/)"
    ),

    # Group 2: Privilege Escalation & Credential Access
    (
        r"(?P<powershell_sherlock>powershell.*herlock)"
        r"|(?P<juicy_potato>uicy.*otato.*\-t\s+\*\s+\-p)"
        r"|(?P<rogue_potato>ogue.*otato.*\-r)"
        r"|(?P<mimikatz_piece>imikatz)"
        r"|(?P<mimikatz_kerberos>imikatz.*kerberos)"
        r"|(?P<mimikatz_dump>imikatz.*dump)"
        r"|(?P<mimikatz_sekurlsa>imikatz.*sekurlsa)"
        r"|(?P<kerberoasting>erberoast)"
        r"|(?P<kerberos_golden>kerberos.*golden)"
        r"|(?P<kerberos_rc4>kerberos.*rc4)"
        r"|(?P<kerberos_krbtgt>kerberos.*krbtgt)"
        r"|(?P<rubeus_kerberoast>ubeus.*kerberoast)"
        r"|(?P<rubeus_domain>ubeus.*domain)"
        r"|(?P<rubeus_creduser>ubeus.*creduser)"
        r"|(?P<rubeus_credpassword>ubeus.*credpassword)"
        r"|(?P<rubeus_asktgt>ubeus.*asktgt)"
        r"|(?P<rubeus_rc4>ubeus.*rc4)"
        r"|(?P<rubeus_aes>ubeus.*aes)"
        r"|(?P<NTLMHASH>NTLMHASH)"
        r"|(?P<tgsrepcrack>tgsrepcrack)"
        r"|(?P<python_tgsrepcrack>ython.*tgsrepcrack)"
        r"|(?P<KerberosRequestorSecurityToken>KerberosRequestorSecurityToken)"
        r"|(?P<DomainSPNTicket>DomainSPNTicket)"
        r"|(?P<bloodhound_invoke>lood.*ound)"
        r"|(?P<sharphound_invoke>harp.*ound)"
        r"|(?P<procdump_process>rocdump.*\-[\-\s\w]+)"
        r"|(?P<reg_save_hklm>reg.*save.*hklm)"
        r"|(?P<powershell_invoke_command_credentials>nvoke.*ommand.*redential)"
        r"|(?P<invoke_command_credential>nvoke.*ommand.*dential)"
        r"|(?P<powershell_system_credentials>bject.*ystem.*edential)"
        r"|(?P<powershell_new_ps_session_creds>ew\-.*s.*ession.*dential)"
        r"|(?P<powershell_enter_ps_session_creds>nter\-.*s.*ession.*dential)"
        r"|(?P<powershell_token_manipulation>nvoke.*oken.*pulation)"
        r"|(?P<powershell_token_impersonate>nvoke.*oken.*pulation.*mpersonate)"
        r"|(?P<powershell_token_create_process>nvoke.*oken.*pulation.*reate.*rocess)"
        r"|(?P<MS_RPRN_invoke>RPRN)"
        r"|(?P<chisel_client>chisel.*client)"
        r"|(?P<psexec_user>psexec.*\-u)"
        r"|(?P<psexec_password>psexec.*\-p)"
    ),

    # Group 3: Domain Reconnaissance (PowerView / BloodHound / WMI)
    (
        r"(?P<powershell_sql_query>powershell.*SQL.*uery)"
        r"|(?P<get_netuser_spn>Get-NetUser.*[\-\w]{3,10})"
        r"|(?P<powershell_get_domain_info>Get\-Domain)"
        r"|(?P<powershell_get_domain_computer>Get\-DomainComputer)"
        r"|(?P<powershell_get_domain_user>Get\-DomainUser)"
        r"|(?P<powershell_interesting_domain_acl>InterestingDomainAcl)"
        r"|(?P<powershell_spn>\-SPN)"
        r"|(?P<powershell_find_domain_user_location>ind\-DomainUserLocation)"
        r"|(?P<powershell_find_local_admin_access>ind\-LocalAdminAccess)"
        r"|(?P<powershell_applocker_policy>AppLockerPolicy)"
        r"|(?P<powershell_domain_object_acl>DomainObjectAcl)"
        r"|(?P<powershell_domain_gpo_local_group>DomainGPOLocalGroup)"
        r"|(?P<powershell_domain_gpo>Get\-DomainGPO)"
        r"|(?P<powershell_get_domain_ou>Get\-DomainOU)"
        r"|(?P<powershell_find_domain_share>Find\-DomainShare)"
        r"|(?P<powershell_get_domain_group>Get\-DomainGroup)"
        r"|(?P<powershell_forest_trust>Get\-ForestTrust)"
        r"|(?P<powershell_domain_trust>Get\-DomainTrust)"
        r"|(?P<powershell_add_object_acl>owershell.*Add\-ObjectACL)"
        r"|(?P<sharp_gpo_abuse>harp.*buse.*ommand)"
        r"|(?P<powershell_convert_to_base64>onvert.*64.*tring)"
        r"|(?P<powershell_encoding_get_bytes>ystem.*ncoding.*ytes)"
        r"|(?P<powershell_assembly_get_type>Assembly\.GetType)"
        r"|(?P<powershell_invoke_wmimethod>nvoke.*mi.*ethod)"
        r"|(?P<powershell_wmi_execute_encoded>nvoke.*mi.*ethod.*\-e)"
        r"|(?P<wmic_create>wmic.*create)"
        r"|(?P<wmic_shadowcopy>wmic.*shadowcopy)"
        r"|(?P<wmic_node>wmic.*node)"
        r"|(?P<wmic_process>wmic.*process)"
        r"|(?P<wmic_call>wmic.*call)"
        r"|(?P<wmic_user>wmic.*user)"
        r"|(?P<wmic_password>wmic.*password)"
        r"|(?P<wmic_list>wmic.*list)"
        r"|(?P<mklink_shadowcopy>mklink.*shadowcopy)"
        r"|(?P<diskshadow_list>diskshadow.*list)"
        r"|(?P<vssadmin_list>vssadmin.*list)"
        r"|(?P<powershell_backdoor>owershell.*ackdoor)"
        r"|(?P<powershell_select>owershell.*select)"
        r"|(?P<powershell_invoke_execution>IEX)"
        r"|(?P<powershell_invoke_execution_lc>iex)"
        r"|(?P<powershell_create_instance>CreateInstance)"
        r"|(?P<powershell_create_instance_mmc20>CreateInstance.*MMC20)"
        r"|(?P<powershell_create_instance_shell>CreateInstance.*ExecuteShellCommand)"
    ),

    # Group 4: Task Scheduling, Lateral Movement, Persistence
    (
        r"(?P<schtasks_s>schtasks.*/s)"
        r"|(?P<schtasks_schedule>schtasks.*/sc)"
        r"|(?P<schtasks_create>schtasks.*/create)"
        r"|(?P<schtasks_run>schtasks.*/run)"
        r"|(?P<schtasks_once>schtasks.*once)"
        r"|(?P<sc_start>sc.*start)"
        r"|(?P<sc_start_remote>sc.*\\\\.*start)"
        r"|(?P<sc_remote>sc.*\\\\)"
        r"|(?P<msbuild_remote>MSBuild.*\\\\)"
        r"|(?P<msbuild_remote_lc>msbuild.*\\\\)"
        r"|(?P<winrs_remote>winrs.*\-r)"
        r"|(?P<winrs_user>winrs.*\-u)"
        r"|(?P<winrs_password>winrs.*\-p)"
        r"|(?P<diantz_remote>diantz.*\\\\)"
        r"|(?P<dnscmd_remote>dnscmd.*\\\\)"
        r"|(?P<dnscmd_config>dnscmd.*config)"
        r"|(?P<makecab_remote>makecab.*\\\\)"
        r"|(?P<c_share>C\$)"
        r"|(?P<admin_share>ADMIN\$)"
        r"|(?P<ipc_share>IPC\$)"
        r"|(?P<netsh_advfirewall>netsh.*advfirewall)"
        r"|(?P<netsh_portproxy>netsh.*portproxy)"
        r"|(?P<netsh_v4tov4>netsh.*v4tov4)"
        r"|(?P<netsh_add_helper>netsh.*add.*helper)"
        r"|(?P<netsh_wlan>netsh.*wlan)"
        r"|(?P<netsh_firewall>netsh.*firewall)"
        r"|(?P<netsh_interface>netsh.*interface)"
        r"|(?P<nc_listener>nc.*\-l[npv]+)"
        r"|(?P<nc_reverse_shell>nc.*\-e.*cmd)"
        r"|(?P<nc_listener_to_shell>nc.*[\-lnpv]+.*\-e.*sh)"
        r"|(?P<wevutil_clear>wevtutil.*clear)"
        r"|(?P<runas_user>runas\s.*\/user)"
        r"|(?P<powershell_invoke_web_request_output_file>nvoke.*equest.*ut.*ile)"
        r"|(?P<certutil_decode>certutil.*decode)"
        r"|(?P<certutil_encode>certutil.*encode)"
        r"|(?P<bitsadmin_create>bitsadmin.*create)"
        r"|(?P<bitsadmin_addfile>bitsadmin.*addfile)"
        r"|(?P<esentutl_y>esentutl.*/y)"
        r"|(?P<explorer_root>explorer.*/root)"
        r"|(?P<findstr_v>findstr.*/V)"
        r"|(?P<ilasm_exe>ilasm.*/exe)"
        r"|(?P<mavinject_injectrunning>MavInject.*INJECTRUNNING)"
        r"|(?P<dxcap_c>xcap.*\-c)"
        r"|(?P<bginfo_popup>bginfo.*popup)"
        r"|(?P<rundll_open>rundll.*penURL)"
        r"|(?P<net_user>net\s.*user)"
        r"|(?P<net_localgroup>net\s.*localgroup)"
        r"|(?P<net_group>net*\sgroup)"
        r"|(?P<net_accounts>net\s.*accounts)"
        r"|(?P<net_computer>net\s.*computer)"
        r"|(?P<net_add>net\s.*/add)"
        r"|(?P<net_share>net\s.*share)"
        r"|(?P<net_use>net\s.*use\s)"
        r"|(?P<net_view>net\s.*view)"
        r"|(?P<wusa_kb>wusa.*kb)"
        r"|(?P<wusa_uninstall>wusa.*/uninstall)"
        r"|(?P<reg_query>reg\s.*query)"
        r"|(?P<ipconfig_all>ipconfig.*all)"
        r"|(?P<tasklist_status>tasklist.*STATUS)"
        r"|(?P<tasklist_fi>tasklist.*/fi)"
        r"|(?P<qwinsta_server>qwinsta.*/server)"
        r"|(?P<gpresult_s>gpresult.*/s)"
        r"|(?P<systeminfo_s>systeminfo.*/S)"
        r"|(?P<KEYWORD_New_Object>New\-Object)"
        r"|(?P<KEYWORD_WebClient>WebClient)"
        r"|(?P<KEYWORD_DownloadFile>DownloadFile)"
        r"|(?P<KEYWORD_DownloadString>DownloadString)"
        r"|(?P<KEYWORD_WinHttp>WinHttp)"
        r"|(?P<KEYWORD_WinHttpRequest>WinHttpRequest)"
        r"|(?P<KEYWORD_TCPClient>TCPClient)"
        r"|(?P<KEYWORD_GetStream>GetStream)"
        r"|(?P<KEYWORD_WriteAllBytes>WriteAllBytes)"
        r"|(?P<KEYWORD_ToBase64String>ToBase64String)"
        r"|(?P<KEYWORD_javascript>javascript)"
        r"|(?P<KEYWORD_mimikatz>mimikatz)"
        r"|(?P<KEYWORD_sekurlsa>sekurlsa)"
        r"|(?P<KEYWORD_shadowcopy>shadowcopy)"
        r"|(?P<KEYWORD_krbtgt>krbtgt)"
        r"|(?P<KEYWORD_Rubeus>Rubeus)"
        r"|(?P<KEYWORD_SharpHound>SharpHound)"
        r"|(?P<KEYWORD_vssadmin>vssadmin)"
        r"|(?P<KEYWORD_JuicyPotato>JuicyPotato)"
        r"|(?P<KEYWORD_RoguePotato>RoguePotato)"
        r"|(?P<KEYWORD_shell>shell)"
        r"|(?P<KEYWORD_invoke>invoke)"
        r"|(?P<KEYWORD_socket>socket)"
        r"|(?P<KEYWORD_bash>bash)"
        r"|(?P<dll_extension>\.dll$)"
        r"|(?P<hta_extension>\.hta)"
        r"|(?P<ps1_file>\.ps1)"
        r"|(?P<vbs_file>\.vbs)"
        r"|(?P<js_file>\.js)"
    ),

    # Group 5: Modern LOLBAS Techniques
    (
        r"(?P<curl_download_execute>curl.*(-o|-O).*http)"
        r"|(?P<curl_exfiltration>curl.*(-F|-d|--data).*http)"
        r"|(?P<tar_unc_extract>tar.*(-xf|-xvf).*\\\\)"
        r"|(?P<conhost_headless>conhost.*--headless)"
        r"|(?P<comsvcs_lsass_dump>rundll32.*comsvcs.*(MiniDump|#24))"
        r"|(?P<shadowcopy_delete>vssadmin.*delete\s+shadows)"
        r"|(?P<wbadmin_delete_catalog>wbadmin.*delete\s+catalog)"
        r"|(?P<bcdedit_recovery_disable>bcdedit.*recoveryenabled\s+no)"
        r"|(?P<mpcmdrun_remove_defs>mpcmdrun.*-RemoveDefinitions)"
        r"|(?P<ssh_reverse_tunnel>ssh.*-R.*(\d+:localhost|\d+:127\.0\.0\.1))"
        r"|(?P<winget_manifest_download>winget.*install.*--manifest.*http)"
    ),
]


# ==============================================================================
# LINUX - GTFOBins Commands
# Source: https://gtfobins.github.io
# ==============================================================================

LINUX_COMMANDS = [
    "cat", "chmod", "cp", "curl", "sqlite3", "postgres", "runuser",
    "ldapsearch", "adduser", "export", "ftp", "history", "ping",
    "egrep", "bzip", "ifconfig", "kill", "last", "mkdir", "mv",
    "passwd", "lsof", "ps", "rm", "sshd", "tar", "node", "uname",
    "unzip", "nc", "useradd", "userdel", "vi", "vim", "wget",
    "whoami", "w", "socat", "telnet", "pip", "easy_install",
    "nmap", "scp", "sftp", "smbclient", "tftp", "whois", "finger",
    "crontab", "cpan", "apt-get", "byebug", "cobc", "cpulimit",
    "rvim", "ltrace", "nohup", "top", "nice", "netstat", "find",
    "pwd", "ls", "ssh", "gdb", "sudo", "netdiscover", "chroot",
    "cut", "awk", "gawk", "openssl", "auditctl", "usermod",
    "groups", "chgrp", "emacs", "journalctl", "rsync", "strace",
    "mkfifo", "perl", "python", "python3", "arp", "php", "ruby",
    "jrunscript", "tcpdump", "echo", "strings", "mono", "mknod",
    "tee", "busybox", "exec", "route", "rlogin", "xxd", "view",
    "rpcclient", "dnsdomainname", "aria2c", "mysql", "debugfs",
    "iptables", "masscan", "bash", "tmux", "screen", "gcc", "grep",
    "gpg", "hostname", "sleep", "dpkg", "which", "env", "set",
    "base64", "sed", "dd", "ssh-keyscan", "locate", "unset",
    "printenv", "crash", "mount", "ldconfig", "ftp", "openvpn",
    "valgrind", "rpm", "xargs", "java", "ansible", "git", "docker",
    "slsh", "hexdump", "ghc", "showmount", "zsh", "go", "chattr",
    "sha1sum", "modprobe", "more", "traceroute", "mtr", "dirb",
]


# ==============================================================================
# LINUX - Sensitive System Paths
# ==============================================================================

LINUX_PATHS = [
    "/dev/mem", "/dev/tcp", "/dev/udp", "/dev/kmem", "/dev/null",
    "/inet/tcp", "/bin/sh", "/inet/udp", "/etc/crontab",
    "/var/spool/cron", "/bin/bash", "/etc/passwd", "/etc/issue",
    "/etc/shadow", "/proc/version", "/etc/ssh/sshd_config",
    "/etc/services", "/etc/network/interfaces", "/etc/resolv.conf",
    "/etc/fstab", "/etc/group", "/etc/hostname", "/etc/hosts",
    "/etc/inetd.conf", "/boot", ".ssh/", "/etc/profile",
    "/tmp/bash", "/etc/sudoers", "/etc/vncpasswd", "/proc/",
    "/var/tmp/", "/dev/tty", "/bin/ssh", "/tmp/",
    "/usr/bin/yum",
]


# ==============================================================================
# LINUX - Sensitive Keywords
# ==============================================================================

LINUX_KEYWORDS = [
    "pty", "spawn", "pty.spawn", "password", "shadow", "passwd",
    "username", "pass", "ctypes", "cdll", "LoadLibrary", "fiddle",
    "dlopen", "http", "install", "ProxyCommand", "lua", "eval",
    "exec", "execute", "function", "-i", "-e", "-p", "-t", "-r",
    "-R", "-L", "-l", "-c", "-C", "-n", "fsockopen", "socket",
    "subprocess", "-nlvp", "-nvlp", "-user", "-perm", "-group",
    "shell", "os.execute", "-qc", "-sV", "-sC", "-O", "-T4",
    "-Pn", "-p-", "-oA", "+x", "TCP-LISTEN", "-N", "-ivh",
    "777", "677", "--allow-overwrite", "--on-download-complete",
    "os.getppid", "os.getpid", "nfs", "smb", "sh", "bash",
    "sudoers", "shell_exec", "system", "passthru", "popen",
    "proc_open", "ztcp", "bash_history", "kinsing", "passwordauth",
    "AF_INET", "SOCK_STREAM", "SOL_TCP", "TCPSocket",
]


# ==============================================================================
# LINUX - Regex Pattern Groups for Attack Behaviors
# ==============================================================================

LINUX_REGEX_LIST = [
    (
        r"(?P<pip_install_shell>echo.*import.*pip.*install)"
        r"|(?P<python_spawn>python.*import.*spawn)"
        r"|(?P<iptables_input>iptables.*\-A.*INPUT)"
        r"|(?P<ghc_process>ghc.*\-e.*Process)"
        r"|(?P<find_for_perm>find.*\-perm[^\w])"
        r"|(?P<atobm_awk>atobm.*awk)"
        r"|(?P<comm>comm.*dev.*)"
        r"|(?P<rlwrap_remote>rlwrap.*\-l)"
        r"|(?P<python_import_os>python.*\-c.*import.*[\s\,\;]{1,10}os)"
        r"|(?P<lua_socket>lua.*socket)"
        r"|(?P<gcc_E>gcc.*\-E)"
        r"|(?P<http_con>http:\/\/)"
        r"|(?P<https_con>https:\/\/)"
        r"|(?P<apt_invoke_sh>apt.*update.*Invoke.*sh)"
        r"|(?P<openssl_passwd>openssl.*passwd)"
        r"|(?P<crash_sh>crash.*\!.{0,10}[^\.\w][ba]{0,2}sh)"
        r"|(?P<mysql_execute>mysql.*\-e)"
        r"|(?P<ssh_N>ssh.*\-N)"
        r"|(?P<sh_dev_tcp_i>sh.*\-i.*dev.*tcp)"
        r"|(?P<php_get_env>php.*\-r.*getenv)"
        r"|(?P<node_file_manipulation>node.*\-e.*fs)"
        r"|(?P<nmap_p>nmap.*-p)"
        r"|(?P<ruby_rsocket>ruby.*\-rsocket)"
        r"|(?P<jar_script>\.jar[\s\;\|\>\<]{1}|\.jar$)"
        r"|(?P<tar_tcp>tar.*dev.*tcp)"
        r"|(?P<busybox_sh>busybox\s+sh)"
        r"|(?P<netstat_flags>netstat\s+\-[punta]+)"
        r"|(?P<socat_tcp_listen>socat.*TCP\-LISTEN)"
        r"|(?P<socat_tcp4_listen>socat.*TCP4\-LISTEN)"
        r"|(?P<bash_script>\.bash[\s\;\|\>\<]{1}|\.bash\"|\.bash$)"
        r"|(?P<emacs_shell>emacs.*eval.*sh)"
        r"|(?P<unshare_sh>unshare.*\/bin\/[ba]{0,2}sh)"
        r"|(?P<gpg_file>\.gpg[\s\;\|\>\<]{1}|\.gpg$)"
        r"|(?P<path_etc>\s+\/etc\/)"
        r"|(?P<tcp_connect>tcp\-connect)"
        r"|(?P<tcp_listen>tcp\-listen)"
        r"|(?P<unix_connect>unix\-connect)"
    ),
    (
        r"(?P<nc_e_sh>[^\w]nc\s.*\-e.*[^\.]sh[^\w])"
        r"|(?P<cat_passwd>cat\s.*\/etc\/passwd)"
        r"|(?P<finger_file_base64>finger.*base64)"
        r"|(?P<tcpdump_manipulation>tcpdump.*\-[\-lnw\s]{1,10})"
        r"|(?P<rb_script>\.rb[\s\;\|\>\<]{1}|\.rb$)"
        r"|(?P<vim_execute>vim.*\-c.*execute)"
        r"|(?P<socat_tcp>socat.*tcp)"
        r"|(?P<import_pty>import\s+.*pty)"
        r"|(?P<docker_chroot>docker.*run.*chroot.*sh)"
        r"|(?P<jrunscript_execute>jrunscript.*\-e)"
        r"|(?P<proxytunnel_p>proxytunnel.*\-p)"
        r"|(?P<nmap_O>nmap.*-O)"
        r"|(?P<nc_listener_to_shell>[^\w]nc\s+\-[lnpv]+.*\-e.*sh[^\w])"
        r"|(?P<arp_a>arp.*\-a)"
        r"|(?P<nmap_sU>nmap.*-sU)"
        r"|(?P<rview_execute_shell>rview.*\-c.*execute.*sh)"
        r"|(?P<cpan_Fetch>cpan.*\!.*Fetch)"
        r"|(?P<ln_shell>[^\w]ln\s.*\-s.*[^\.\w][ba]{0,2}sh[^\w])"
        r"|(?P<rsync_aH>rsync.*\-[aH]{2})"
        r"|(?P<ssh_proxy_command>ssh.*\-o.*ProxyCommand)"
        r"|(?P<crontab_remove>crontab\s+\-r)"
        r"|(?P<perl_shell>perl.{0,200}\-e.{1,200}sh)"
        r"|(?P<node_shell>node.*\-e.*\/bin\/[ba]{0,2}sh[^\w])"
        r"|(?P<xargs_exec_shell>xargs.*[\-Ix].*\-c.*exec.*sh)"
        r"|(?P<boot_manipulation>boot.*vmlinuz)"
        r"|(?P<gdb_python>gdb.*python)"
        r"|(?P<python_pty>python.*pty)"
        r"|(?P<openssl_shell>mkfifo.*sh.*openssl)"
        r"|(?P<base32_decode>base32.*decode)"
        r"|(?P<grep_user>grep.*\-i.*user)"
        r"|(?P<exec_bin_sh>[^\w]exec[^\w].*\/bin\/[ba]{0,2}sh)"
        r"|(?P<man_sh>man.*\!.*sh)"
        r"|(?P<php_remote_shell>php.*\-r.*sock.*sh)"
        r"|(?P<irb_download>irb.*download)"
        r"|(?P<python_spawn2>python.*import.*spawn)"
    ),
    (
        r"(?P<whois_remote>whois.*\-h.*\-p)"
        r"|(?P<ssh_R>ssh.*\-R)"
        r"|(?P<java_shell>java.*\/bin\/[ba]{0,2}sh.*Socket)"
        r"|(?P<nmap_sC>nmap.*-sC)"
        r"|(?P<python_install_exec>import\s+os.*execl.*sh)"
        r"|(?P<socat_tcp_connect>socat.*\-u.*tcp\-connect)"
        r"|(?P<python_system_shell>python.*\-c.*system.*sh)"
        r"|(?P<find_for_user>find.*\-user[^\w])"
        r"|(?P<tar_udp>tar.*dev.*udp)"
        r"|(?P<composer_script>composer.*run\-script)"
        r"|(?P<gcc_shell_wrapper>gcc.*\-wrapper.*sh)"
        r"|(?P<mysql_shell>mysql.*\-e.*\!.*sh)"
        r"|(?P<ld_so_sh>ld.so.*\/bin\/sh)"
        r"|(?P<crontab_edit>crontab\s+\-e)"
        r"|(?P<awk_inet_tcp>awk.*inet.*tcp)"
        r"|(?P<mail_shell>mail\(\).*sh)"
        r"|(?P<ruby_shell>ruby.*\-e[^\w].*exec.*sh[^\w])"
        r"|(?P<valgrind_shell>valgrind.{0,10}[^\.\w][ba]{0,2}sh)"
        r"|(?P<route_add>route.*add.*net)"
        r"|(?P<byebug_sh>system.*\/bin\/sh.*byebug)"
        r"|(?P<node_fs_stream>fs\.createWriteStream)"
        r"|(?P<openssl_salt>openssl.*passwd.*salt)"
        r"|(?P<env_shell>env.*\/bin\/sh)"
        r"|(?P<iptables_list>iptables.*\-L)"
        r"|(?P<nice_sh>nice.*sh)"
        r"|(?P<php_listener>php.*\-S)"
        r"|(?P<ar_r>ar\s+r)"
        r"|(?P<pipe_sh>\|\s{0,5}\w{0,3}sh)"
        r"|(?P<pipe_bin_sh>\|\s{0,5}\/bin\/\w{0,3}sh)"
        r"|(?P<kinsing>kinsing)"
        r"|(?P<kinsing_tmp>\/tmp\/kdevtmp)"
    ),
    (
        r"(?P<history_r>history.*\-r)"
        r"|(?P<apt_get_bin_sh>apt-get.*\!\/bin\/[ba]{0,2}sh.*)"
        r"|(?P<smbclient_shell>smbclient.*\!.*sh)"
        r"|(?P<zsh_script>\.zsh[\s\;\|\>\<]{1}|\.zsh\"|\.zsh$)"
        r"|(?P<ssh_D>ssh.*\-D)"
        r"|(?P<php_system_shell>php\s+\-r.*system)"
        r"|(?P<ftp_put>ftp.*[^\w]put[^\w])"
        r"|(?P<ruby_file_manipulation>ruby.*\-e.*File)"
        r"|(?P<nohup_shell>nohup.*sh.*\-c.*\<.*\>)"
        r"|(?P<iptables_masquerade>iptables.*MASQUERADE)"
        r"|(?P<cupsfilter_stream>cupsfilter.*\-i.*stream)"
        r"|(?P<chroot_sh>chroot.*\/bin\/[ba]{0,2}sh)"
        r"|(?P<gem_shell>gem.*\-e.*sh)"
        r"|(?P<echo_shell_top>echo.*\-e.*sh.*>.*top)"
        r"|(?P<bundler_shell>bundler.*\!.*sh)"
        r"|(?P<nmap_shell>nmap.*\!.*sh[^\w])"
        r"|(?P<python_shell>python.*\/bin\/.{0,2}sh)"
        r"|(?P<bash_history>bash\_history)"
        r"|(?P<ksh_tcp>ksh.*-c.*dev.*tcp)"
        r"|(?P<netcat_listener>nc\s+\-l[npv]+)"
        r"|(?P<rlogin_p>rlogin.*\-p)"
        r"|(?P<irb_shell>irb.*exec.*sh)"
        r"|(?P<more_sh>more.*\/bin\/[ba]{0,2}sh)"
        r"|(?P<logsave_shell>logsave.*sh.*\-i)"
        r"|(?P<cpio_shell>cpio.*sh.*\-F)"
        r"|(?P<php_file_put>php.*\-r.*file\_put\_contents)"
        r"|(?P<sftp_shell>sftp.*\!.*[^\w]{1}b{0,1}a{0,1}sh)"
        r"|(?P<python_crypt>import.*crypt)"
        r"|(?P<find_bash>find.*bin\/[ba]{0,2}sh)"
        r"|(?P<time_sh>time\s.*\/bin\/[ba]{0,2}sh)"
        r"|(?P<tar_curl_file>tar.*curl.*\-F)"
    ),
    (
        r"(?P<restic_backup>restic.*backup)"
        r"|(?P<nmap_Pn>nmap.*-Pn)"
        r"|(?P<node_spawn_process>node.*\-e.*spawn)"
        r"|(?P<gdb_python_ctypes>gdb.*python.*ctypes)"
        r"|(?P<irb_exec>irb.*exec)"
        r"|(?P<js_script>\.js[\s\;\|\>\<]{1}|\.js$)"
        r"|(?P<xxd_c_p>xxd.*-p.*-c)"
        r"|(?P<base64_decode>base64.*decode)"
        r"|(?P<flock_sh>flock.*\-u.*sh)"
        r"|(?P<nc_pipe_to_listener>[^\w^\d^\-^\_]nc[^\w^\d^\-^\_].*\-l.*\<)"
        r"|(?P<rsync_shell>rsync.*\-e.*sh.*\<.*\>)"
        r"|(?P<php_script>\.php[\s\;\|\>\<]{1}|\.php$)"
        r"|(?P<masscan_port>masscan.*\-p)"
        r"|(?P<cat_shadow>cat\s.*\/etc\/shadow)"
        r"|(?P<vim_execute_shell>vim.*\-c.*execute.*sh)"
        r"|(?P<perl_socket>perl.*\-e.*socket)"
        r"|(?P<rvim_execute>rvim.*\-c.*execute)"
        r"|(?P<bridge_b>bridge\s+\-b)"
        r"|(?P<openvpn_shell>openvpn.*sh.*\-c)"
        r"|(?P<socat_u>socat.*\-u)"
        r"|(?P<sshuttle_r>sshuttle.*\-r)"
        r"|(?P<hexdump_c>hexdump\s+\-C)"
        r"|(?P<csh_script>\.csh[\s\;\|\>\<]{1}|\.csh\"|\.csh$)"
        r"|(?P<dpkg_sh>dpkg.*\!.*sh)"
        r"|(?P<import_socket>import\s+.*socket)"
        r"|(?P<localhost_ref>localhost)"
        r"|(?P<telnet_sh>telnet.*\/bin\/[ba]{0,2}sh)"
        r"|(?P<arp_e>arp.*\-e)"
        r"|(?P<exec_tcp>exec.*dev.*tcp)"
        r"|(?P<cpan_server>cpan.*HTTP.*Server)"
        r"|(?P<nmap_sV>nmap.*-sV)"
        r"|(?P<python_pty_c>python.*\-c.*pty)"
        r"|(?P<bin_bash_i_shell>\/bin\/[ba]{0,2}sh.{1,10}\-i[^\w])"
    ),

    # Group 6: Modern GTFOBins & Cloud/Container Escape
    (
        r"(?P<openssl_reverse_shell>openssl.*s_client.*-connect)"
        r"|(?P<socat_reverse_shell>socat.*exec.*bash.*tcp)"
        r"|(?P<container_chroot_escape>docker.*-v\s+\/:\/host.*chroot)"
        r"|(?P<nsenter_host_escape>nsenter.*-t\s+1.*\/bin\/bash)"
        r"|(?P<pipeline_exfil_shadow>(cat|tar).*(\/etc\/shadow|\/etc\/passwd).*curl)"
        r"|(?P<awk_tcp_reverse>awk.*inet\/tcp\/.*getline)"
    ),
]
