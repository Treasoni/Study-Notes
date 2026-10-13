---
source_id: LB-6
origin: qbittorrent/qBittorrent.git (branch: master)
fetched_via: curl -sL https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/<path>
fetched_at: 2026-10-07
evidence_form: fetched (excerpts of upstream raw files; full files 1542-4454 lines, excerpts only)
tier: primary
---

# LB-6 · 「完成时运行外部程序」占位符定义（官方源码取证）

本文件为上游原始文件的**逐字片段**（用 sed/awk 直接截取，未重排、未改写）。每行前缀为该行在**上游原始文件中的行号**。

上游文件与规模：

- `src/app/application.cpp` — 1542 行
- `src/gui/optionsdialog.cpp` — 2320 行
- `src/gui/optionsdialog.ui` — 4454 行
- `src/base/preferences.cpp` — 2222 行

## 片段 1：`src/gui/optionsdialog.cpp` 行 721-746 —— UI 中展示给用户的“Supported parameters”占位符清单

721:     m_ui->groupBoxRunOnAdded->setChecked(pref->isAutoRunOnTorrentAddedEnabled());
722:     m_ui->groupBoxRunOnFinished->setChecked(pref->isAutoRunOnTorrentFinishedEnabled());
723:     m_ui->lineEditRunOnAdded->setText(pref->getAutoRunOnTorrentAddedProgram());
724:     m_ui->lineEditRunOnFinished->setText(pref->getAutoRunOnTorrentFinishedProgram());
725: #if defined(Q_OS_WIN)
726:     m_ui->autoRunConsole->setChecked(pref->isAutoRunConsoleEnabled());
727: #else
728:     m_ui->autoRunConsole->hide();
729: #endif
730:     const auto autoRunStr = u"%1\n    %2\n    %3\n    %4\n    %5\n    %6\n    %7\n    %8\n    %9\n    %10\n    %11\n    %12\n    %13\n    %14\n%15"_s
731:         .arg(tr("Supported parameters (case sensitive):")
732:             , tr("%N: Torrent name")
733:             , tr("%L: Category")
734:             , tr("%G: Tags (separated by comma)")
735:             , tr("%F: Content path (same as root path for multifile torrent)")
736:             , tr("%R: Root path (first torrent subdirectory path)")
737:             , tr("%D: Save path")
738:             , tr("%C: Number of files")
739:             , tr("%Z: Torrent size (bytes)"))
740:         .arg(tr("%T: Current tracker")
741:             , tr("%I: Info hash v1 (or '-' if unavailable)")
742:             , tr("%J: Info hash v2 (or '-' if unavailable)")
743:             , tr("%K: Torrent ID (either sha-1 info hash for v1 torrent or truncated sha-256 info hash for v2/hybrid torrent)")
744:             , tr("%M: Comment")
745:             , tr("Tip: Encapsulate parameter with quotation marks to avoid text being cut off at whitespace (e.g., \"%N\")"));
746:     m_ui->labelAutoRunParam->setText(autoRunStr);

## 片段 2：`src/app/application.cpp` 行 588-601 —— runExternalProgram 入口与替换循环

588: void Application::runExternalProgram(const QString &programTemplate, const BitTorrent::Torrent *torrent) const
589: {
590:     // Cannot give users shell environment by default, as doing so could
591:     // enable command injection via torrent name and other arguments
592:     // (especially when some automated download mechanism has been setup).
593:     // See: https://github.com/qbittorrent/qBittorrent/issues/10925
594: 
595:     const auto replaceVariables = [torrent](QString str) -> QString
596:     {
597:         for (qsizetype i = (str.length() - 2); i >= 0; --i)
598:         {
599:             if (str[i] != u'%')
600:                 continue;
601: 

## 片段 3：`src/app/application.cpp` 行 603-654 —— 占位符 -> 实际值的 switch 实现

603:             switch (specifier)
604:             {
605:             case u'C':
606:                 str.replace(i, 2, QString::number(torrent->filesCount()));
607:                 break;
608:             case u'D':
609:                 str.replace(i, 2, torrent->savePath().toString());
610:                 break;
611:             case u'F':
612:                 str.replace(i, 2, torrent->contentPath().toString());
613:                 break;
614:             case u'G':
615:                 str.replace(i, 2, Utils::String::joinIntoString(torrent->tags(), u","_s));
616:                 break;
617:             case u'I':
618:                 str.replace(i, 2, (torrent->infoHash().v1().isValid() ? torrent->infoHash().v1().toString() : u"-"_s));
619:                 break;
620:             case u'J':
621:                 str.replace(i, 2, (torrent->infoHash().v2().isValid() ? torrent->infoHash().v2().toString() : u"-"_s));
622:                 break;
623:             case u'K':
624:                 str.replace(i, 2, torrent->id().toString());
625:                 break;
626:             case u'L':
627:                 str.replace(i, 2, torrent->category());
628:                 break;
629:             case u'M':
630:                 str.replace(i, 2, torrent->comment());
631:                 break;
632:             case u'N':
633:                 str.replace(i, 2, torrent->name());
634:                 break;
635:             case u'R':
636:                 str.replace(i, 2, torrent->rootPath().toString());
637:                 break;
638:             case u'T':
639:                 str.replace(i, 2, torrent->currentTracker());
640:                 break;
641:             case u'Z':
642:                 str.replace(i, 2, QString::number(torrent->totalSize()));
643:                 break;
644:             default:
645:                 // do nothing
646:                 break;
647:             }
648: 
649:             // decrement `i` to avoid unwanted replacement, example pattern: "%%N"
650:             --i;
651:         }
652: 
653:         return str;
654:     };

## 片段 4：`src/app/application.cpp` 行 777-792 —— 触发点：torrentAdded / torrentFinished

777: void Application::torrentAdded(const BitTorrent::Torrent *torrent) const
778: {
779:     const Preferences *pref = Preferences::instance();
780: 
781:     // AutoRun program
782:     if (pref->isAutoRunOnTorrentAddedEnabled())
783:         runExternalProgram(pref->getAutoRunOnTorrentAddedProgram().trimmed(), torrent);
784: }
785: 
786: void Application::torrentFinished(const BitTorrent::Torrent *torrent)
787: {
788:     const Preferences *pref = Preferences::instance();
789: 
790:     // AutoRun program
791:     if (pref->isAutoRunOnTorrentFinishedEnabled())
792:         runExternalProgram(pref->getAutoRunOnTorrentFinishedProgram().trimmed(), torrent);

## 片段 5：`src/base/preferences.cpp` 行 1245-1310 —— 配置键名与默认值

1245: bool Preferences::isAutoRunOnTorrentAddedEnabled() const
1246: {
1247:     return value(u"AutoRun/OnTorrentAdded/Enabled"_s, false);
1248: }
1249: 
1250: void Preferences::setAutoRunOnTorrentAddedEnabled(const bool enabled)
1251: {
1252:     if (enabled == isAutoRunOnTorrentAddedEnabled())
1253:         return;
1254: 
1255:     setValue(u"AutoRun/OnTorrentAdded/Enabled"_s, enabled);
1256: }
1257: 
1258: QString Preferences::getAutoRunOnTorrentAddedProgram() const
1259: {
1260:     return value<QString>(u"AutoRun/OnTorrentAdded/Program"_s);
1261: }
1262: 
1263: void Preferences::setAutoRunOnTorrentAddedProgram(const QString &program)
1264: {
1265:     if (program == getAutoRunOnTorrentAddedProgram())
1266:         return;
1267: 
1268:     setValue(u"AutoRun/OnTorrentAdded/Program"_s, program);
1269: }
1270: 
1271: bool Preferences::isAutoRunOnTorrentFinishedEnabled() const
1272: {
1273:     return value(u"AutoRun/enabled"_s, false);
1274: }
1275: 
1276: void Preferences::setAutoRunOnTorrentFinishedEnabled(const bool enabled)
1277: {
1278:     if (enabled == isAutoRunOnTorrentFinishedEnabled())
1279:         return;
1280: 
1281:     setValue(u"AutoRun/enabled"_s, enabled);
1282: }
1283: 
1284: QString Preferences::getAutoRunOnTorrentFinishedProgram() const
1285: {
1286:     return value<QString>(u"AutoRun/program"_s);
1287: }
1288: 
1289: void Preferences::setAutoRunOnTorrentFinishedProgram(const QString &program)
1290: {
1291:     if (program == getAutoRunOnTorrentFinishedProgram())
1292:         return;
1293: 
1294:     setValue(u"AutoRun/program"_s, program);
1295: }
1296: 
1297: #if defined(Q_OS_WIN)
1298: bool Preferences::isAutoRunConsoleEnabled() const
1299: {
1300:     return value(u"AutoRun/ConsoleEnabled"_s, false);
1301: }
1302: 
1303: void Preferences::setAutoRunConsoleEnabled(const bool enabled)
1304: {
1305:     if (enabled == isAutoRunConsoleEnabled())
1306:         return;
1307: 
1308:     setValue(u"AutoRun/ConsoleEnabled"_s, enabled);
1309: }
1310: #endif

## 片段 6：`src/gui/optionsdialog.ui` 行 1774-1826 —— 选项 UI 结构（Run on torrent added / finished）

1774:             <item>
1775:              <widget class="QGroupBox" name="autoRunBox">
1776:               <property name="title">
1777:                <string>Run external program</string>
1778:               </property>
1779:               <layout class="QVBoxLayout" name="verticalLayout_19">
1780:                <item>
1781:                 <widget class="QGroupBox" name="groupBoxRunOnAdded">
1782:                  <property name="title">
1783:                   <string>Run on torrent added:</string>
1784:                  </property>
1785:                  <property name="checkable">
1786:                   <bool>true</bool>
1787:                  </property>
1788:                  <property name="checked">
1789:                   <bool>false</bool>
1790:                  </property>
1791:                  <layout class="QVBoxLayout" name="verticalLayout_39">
1792:                   <item>
1793:                    <widget class="QLineEdit" name="lineEditRunOnAdded"/>
1794:                   </item>
1795:                  </layout>
1796:                 </widget>
1797:                </item>
1798:                <item>
1799:                 <widget class="QGroupBox" name="groupBoxRunOnFinished">
1800:                  <property name="title">
1801:                   <string>Run on torrent finished:</string>
1802:                  </property>
1803:                  <property name="checkable">
1804:                   <bool>true</bool>
1805:                  </property>
1806:                  <property name="checked">
1807:                   <bool>false</bool>
1808:                  </property>
1809:                  <layout class="QVBoxLayout" name="verticalLayout_36">
1810:                   <item>
1811:                    <widget class="QLineEdit" name="lineEditRunOnFinished"/>
1812:                   </item>
1813:                  </layout>
1814:                 </widget>
1815:                </item>
1816:                <item>
1817:                 <widget class="QCheckBox" name="autoRunConsole">
1818:                  <property name="text">
1819:                   <string>Show console window</string>
1820:                  </property>
1821:                 </widget>
1822:                </item>
1823:                <item>
1824:                 <widget class="QLabel" name="labelAutoRunParam">
1825:                  <property name="wordWrap">
1826:                   <bool>true</bool>
