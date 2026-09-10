## 第三章 Windows PowerShell——用命令操作前两者

第二章结尾留了两个悬念：为什么 PowerShell 管道里流动的是**对象**而不是文本，以及**执行策略**为什么"防的是手滑，不是防坏人"。这一章就来回答这两个问题，顺便把另外两个新手最常撞上的墙一起拆掉：打开 PowerShell 就报"在此系统上禁止运行脚本"，以及中文显示成一片乱码。

本章内容偏概念，但每一节最后都能落到"你能敲的命令"上。如果你此刻最急迫的问题就是上面那两类报错，可以先跳到 3.6 和 3.7，读懂之后回头再补 3.1–3.5。

### 3.1 对象而不是文本：PowerShell 与 cmd 的根本差别

#### 3.1.1 先看一个场景，再看官方的那句话

假设你想知道"现在哪个进程占内存最多"。在 cmd（命令提示符）里，`tasklist` 会吐给你这么一片东西：

> 环境：cmd ｜ 版本：全版本适用 ｜ 权限：无需管理员

```text
映像名称                       PID 会话名              会话#       内存使用
========================= ======== ================ =========== ============
notepad.exe                   1234 Console                    1     12,345 K
explorer.exe                  5678 Console                    1     98,765 K
```

它是**一屏文字**。你说"我只要第 5 列"，cmd 帮不了你——它不知道"第 5 列"是什么，它只知道"这是一串字符"，你得自己按空格把每行切开、数到第 5 段、再去比大小。列宽一变、程序名里多一个空格，你数位置的办法就全废了。

PowerShell 不一样。官方的说法是：PowerShell 与其他 shell 的根本区别，是**接受并返回 .NET 对象而不是文本**，因此管道连接更省事 [C-2]。

这句话里的"**对象**"是本章第一个必须讲透的词。按本笔记一直用的三步走：

| 三步 | 内容 |
|---|---|
| 中文人话 | 命令返回的不是"一段文字"，而是**一排带名字的格子** |
| 官方术语 | .NET 对象（object） |
| 它到底指什么 | 每个结果项（比如一个进程）自带若干**属性**，每个属性都有名字，如 `Name`、`Id`、`Handles` [C-2]；除了"格子里装什么"，它还带一些可以执行的动作 |

关键差别在"**名字**"这两个字。文本管道里的东西没有名字，只有位置（第 1 列、第 2 列）；对象管道里的东西有名字（`Name`、`Id`），你想取哪一项，说的是**名字**，不是位置。

> [!tip] 大白话
> 把 **cmd 的管道想成一沓打印好的表格纸**：信息都在上面，但你要拿"第 5 列"，只能靠眼睛数，列一歪就数错。
> 把 **PowerShell 的管道想成一个带表头的 Excel 表**：每一列顶上写着 `Name`、`Id`、`Handles`，你要"内存那一列"，报的是表头的名字，不用管它排在第几位、中间有没有空格。
> 所以差别不在"谁更漂亮"，而在**后面的命令能不能靠名字直接拿到数据**——这正是下一节要讲的事。

#### 3.1.2 把好处说得再具体一点：文本要切，对象可以直接点

把两种做法并排看，差别就清楚了：

| | 文本管道（cmd / Bash 那一套） | 对象管道（PowerShell） |
|---|---|---|
| 管道里流动的 | 一行一行的**字符串** | 一个一个有结构的**对象** |
| 想取"某个字段" | 自己按分隔符切开、数第几段，还要处理列宽变化 | 直接按**属性名**取用 [C-2] |
| 想"筛掉不符合条件的" | 对字符串做匹配，容易误伤（比如名字里恰好含同样字符） | 按属性的值判断，判断的是数据本身 |

官方举的例子很能说明问题：因为管道里传的是**进程对象**，所以 `Get-Process notepad | Stop-Process` 这句里，后一条命令 `Stop-Process` **根本不需要你再告诉它进程的名字或编号**——上一个命令送过来的对象已经自带这些信息了 [C-1]。

> [!note] 一个提醒：不要再按"文本处理"的思路使唤 PowerShell
> 很多人从 cmd / Bash 过来，习惯先想办法"把输出切成文本再处理"。在 PowerShell 里这通常是绕远路：先`Get-Member`看看对象有哪些带名字的格子（3.3 会讲这条命令），比琢磨怎么切字符串省事得多。

### 3.2 管道怎么工作：一次一个对象

#### 3.2.1 `|` 到底做了什么

管道是由管道操作符 `|`（ASCII 码 124，键盘上就是那个竖线）连接起来的一串命令；**每个运算符把上一条命令的结果发给下一条命令**，整串按**从左到右**的顺序处理 [C-1]。

> 环境：PowerShell ｜ 版本：5.1 & 7 ｜ 权限：取决于目标进程（官方未说明）

```powershell
# 找到记事本进程，把它结束掉
# 注意：后面这条命令没有写 -Name，也没有写 -ID
Get-Process notepad | Stop-Process
```

#### 3.2.2 为什么接收端不用重新"点名"

承接 3.1 的结论：因为管道里流动的是**进程对象**，对象本身就带着名字和编号，`Stop-Process` 直接拿就行，所以它不需要 `-Name`、也不需要 `-ID` [C-1]。这一点刚开始会很不习惯——在 cmd 里，你几乎总要重复一遍"要操作谁"；在 PowerShell 里，**"要操作谁"是跟着对象一起流过去的**。

#### 3.2.3 成功流、错误流，以及一个"没有接进来"的东西

PowerShell 也有类似"标准输出 / 标准错误"的两条通道，官方称为**成功流**和**错误流**，作用确实跟 stdout / stderr 类似 [C-1]。但有一处反直觉：**标准输入（stdin）并没有接入 PowerShell 的管道** [C-1]。

也就是说，管道的主要作用是把"上一条命令产出的对象"送给下一条命令，而不是"把外部程序的输入接进来"。所以当你看到某个来自 Linux 世界的用法在 PowerShell 里怎么都不对时，先想想它是不是依赖了 stdin。

#### 3.2.4 接收端得"肯接"才行

不是随便什么命令都能接住上一个命令丢过来的东西。只有**带"接受管道输入"参数**的命令才能接 [C-1]。

那怎么知道某个命令肯不肯接、又该由哪个参数来接？官方给的办法是用帮助系统去查 [C-1]：`Get-Help <命令> -Full`，或者 `-Parameter *` 把参数列表全列出来。帮助里会写清两件事：**是哪个参数在接**、**按什么方式接**。

#### 3.2.5 两种"接住"的方式：按值，还是按属性名

这是本章第二个硬骨头。官方把接收方式分成两种 [C-1]：

| 接法 | 官方术语 | 中文人话 | 什么时候能接上 |
|---|---|---|---|
| 按值 | ByValue | 看**东西本身**能不能用 | 送来的对象的类型，正好是目标参数要的类型，或者能转换过去 |
| 按属性名 | ByPropertyName | 看**名字**对不对得上 | 送来的对象身上，有一个属性名正好等于目标参数的名字 |

比如上一个命令丢过来一个对象，它身上有 `Destination` 这个属性；而下游命令恰好有个叫 `-Destination` 的参数——这就是"按属性名"接上了。

官方还给了**绑定成功必须同时满足的三个条件**（注意是"同时"）[C-1]：

1. 目标参数**确实接受管道输入**；
2. **类型匹配**（按值）或**属性名对得上**（按属性名）；
3. 这个参数**没有在命令里被显式写出来**——官方明确说，**无法建议或强制 PowerShell 绑定到某个特定参数**，绑不上这条命令就直接失败 [C-1]。

第 3 条最容易被忽略：**你一旦手写了某个参数，就等于把这个参数"占"了，管道就不会再往它上面绑了。**

#### 3.2.6 关键区别：一次送一个，还是整包一起送

这是本节最重要的一个细节，官方原话是——**"这种细微差异具有重大后果"** [C-1]。

- **走管道**时，PowerShell **一次发送一个对象**：上游有多少个进程，下游就被调用多少次（概念上如此），每次只看见一个。
- **改用 `-InputObject` 参数**时，整个集合是当作**一整个数组对象**送过去的 [C-1]。

落到能看见的差别上，就是这一对对照 [C-1]：

> 环境：PowerShell ｜ 版本：5.1 & 7 ｜ 权限：无需管理员

```powershell
# 第一种：走管道。一次一个对象，所以 Get-Member 看到的是"单个进程"的类型
Get-Process | Get-Member
# 输出里 TypeName: 一行显示
#   System.Diagnostics.Process

# 第二种：用 -InputObject。整个集合被当成一个数组对象送过去
Get-Member -InputObject (Get-Process)
# 输出里 TypeName: 一行显示
#   System.Object[]
```

一个告诉你"我看到的是一台进程"，另一个告诉你"我看到的是一整包东西"。**后者不是"更详细的进程信息"，而是完全换了一个观察对象**——这就是"重大后果"的含义。官方之所以要专门点出这条，正是因为写脚本时踩这个坑会得到莫名其妙的结果。

> [!tip] 大白话
> **管道像"一个一个递苹果"**：每递一个，对方都能把这个苹果的品种、大小看个清楚。
> **`-InputObject` 像"把整筐苹果一起递过去"**：对方一低头，看到的是"一筐"，至于筐里每个苹果什么样，它是看不见的。
> 所以 `Get-Member` 在两处的回答不是"一个详细一个简略"，而是**它盯着看的东西根本换了**。

#### 3.2.7 数组会被拆开，字符串和哈希表不会

还有一个反直觉的规则。官方说：管道执行时会自动把实现了 `IEnumerable` 的那类东西**逐个展开**，但有例外——**哈希表需要调用 `GetEnumerator()`**，而 **`System.String` 虽然也实现了这个接口，却不会被展开** [C-1]。

按本笔记的降维口径，这句话翻译成：

- **数组（以及一批结果）会被拆成一个个元素**，逐个往后传；
- **字符串不会被拆开**——它是一整个，不是"一串字符挨个往下传"；
- **哈希表也不会被拆开**，想逐个看，得先 `GetEnumerator()`。

用 `Get-Member` 去看"对方到底看见了什么"，一眼就能分辨：

> 环境：PowerShell ｜ 版本：5.1 & 7 ｜ 权限：无需管理员

```powershell
# 数组：被拆成一个元素逐个送过去，所以看到的是单个整数
1, 2, 3 | Get-Member
# 输出里 TypeName: 一行显示
#   System.Int32

# 字符串：不会被拆开，看到的是"整个字符串"
"abc" | Get-Member
# 输出里 TypeName: 一行显示
#   System.String

# 哈希表：不会被拆开，看到的是"整个哈希表"
@{a = 1} | Get-Member
# 输出里 TypeName: 一行显示
#   System.Collections.Hashtable

# 想逐个看哈希表里的元素，得先显式展开
@{a = 1}.GetEnumerator() | Get-Member
```

> [!warning] 绑定失败时的官方排查三步
> 如果你写下一条管道，报"输入对象无法绑定到任何参数"之类的错误，官方给的排查手段是这个顺序 [C-1]：
> 1. `Get-Help <下游命令> -Parameter <目标参数>` —— 看这个参数**是否接受管道输入**，以及它**按值还是按属性名**接；
> 2. `<上游命令> | Get-Member` —— 看上游送来的对象身上**有没有名字对得上的属性**；
> 3. `Trace-Command -Name ParameterBinding` —— 打开参数绑定的跟踪，看它到底试了哪些绑定、为什么失败。
>
> 下面这段是官方示例的结构（路径是假设的，不要照抄执行）：
>
> 环境：PowerShell ｜ 版本：5.1 & 7 ｜ 权限：取决于目标键（示例为假设的键）
>
> ```powershell
> # 打开参数绑定跟踪，看这次管道到底怎么绑的
> Trace-Command -Name ParameterBinding -PSHost -Expression {
>   Get-Item -Path HKLM:\Software\MyCompany\sales |
>     Move-ItemProperty -Path HKLM:\Software\MyCompany\design -Name product
> }
>
> # 看 Destination 参数是否按属性名接收管道输入
> Get-Help Move-ItemProperty -Parameter Destination
>
> # 看上游对象身上有没有 Destination 属性
> Get-Item -Path HKLM:\Software\MyCompany\sales | Get-Member
> ```

### 3.3 命令长什么样：Verb-Noun 与四个自举命令

#### 3.3.1 命令名是"动词-名词"

PowerShell 的命令正式名称叫 **cmdlet**（读作"命令莱特"），名字由 **Verb-Noun**（动词-名词）两部分组成，例如 `Get-Process`；动词部分应当取自 `Get-Verb` 返回的那张标准动词表 [C-2]。

> [!tip] 大白话
> 把命令名想成快递单上的"**动作 + 对象**"：`Get-Process` 是"取-进程"，`Stop-Process` 是"停-进程"，`Set-ItemProperty` 是"设置-项的属性"。
> 好处是**你没学过的命令也能猜个八九不离十**：看到 `Get-` 就知道是"读"，看到 `Set-` 就知道是"写"，后面的名词告诉你"对谁干"。

#### 3.3.2 四个自举命令，回答四个不同的问题

新手最常问的是"我怎么知道有这条命令、它怎么用"。官方给的答案是：这四个命令足够发现几乎所有内容 [C-2]：

| 命令 | 它回答的问题 | 有用的过滤参数 |
|---|---|---|
| `Get-Verb` | 有哪些**合法的动词** | —— |
| `Get-Command` | 这台机器上**装了哪些命令** | `-Name` / `-Verb` / `-Noun` / `-ParameterType` [C-2] |
| `Get-Member` | 这个**对象身上有什么**属性、方法 | —— |
| `Get-Help` | 这条命令**怎么用**、参数是什么 | 见 3.4 [C-6] |

注意这四个是**四个不同的问题**，不是四个可以互相替代的命令 [C-2][C-6]。新手最常见的错位是：想"查命令怎么用"，却去敲 `Get-Command`——它只告诉你"有这么条命令"，不会告诉你怎么用。

#### 3.3.3 官方推荐的"找命令"顺序

官方的推荐顺序是：**`Get-Command`（有哪些命令）→ `Get-Help`（怎么用）→ `Get-Member`（返回的对象有什么）** [C-2][C-6]。

> 环境：PowerShell ｜ 版本：5.1 & 7 ｜ 权限：无需管理员

```powershell
# 0. 先确认自己在哪个版本里（5.1 与 7 的行为有差异，见 3.8）
$PSVersionTable

# 1. 有哪些命令：找"动词是 Get、名词以 U 开头"的命令
Get-Command -Verb Get -Noun U*

# 1b. 合法的动词表长什么样
Get-Verb

# 2. 这条命令怎么用
Get-Help Get-ChildItem

# 3. 这条命令返回的对象有什么属性和方法
Get-Process notepad | Get-Member
```

### 3.4 让 PowerShell 自己教你怎么用：Get-Help 与 Update-Help

#### 3.4.1 一个反直觉的前提：帮助文件不是天生就在的

`Get-Help` 是从**本机的帮助文件**里取内容的；**如果没有帮助文件，它只显示基本信息**（大概就是语法那一小段）。关键在于：**从 PowerShell 3.0 起，Windows 自带的模块不再包含帮助文件**，要用 `Update-Help` 下载，或者改用 `-Online` 去看网页版 [C-6]。

所以"`Get-Help` 查不到东西"通常不是命令坏了，而是**帮助文件还没装**。

#### 3.4.2 哪些参数要有帮助文件才管用

`-Detailed` / `-Full` / `-Examples` / `-Parameter` 这几个参数，**只有在计算机装了帮助文件时才有效**；而且它们**对 `about_` 开头的概念文章无效** [C-6]。

另外 `-Online` 是去浏览器里打开网页版帮助，它**不能在远程会话中使用** [C-6]。

#### 3.4.3 概念文章的名字必须用英语

`about_` 开头的概念文章（比如 `about_Execution_Policies`）**必须以英语输入，即使你用的是非英语版 PowerShell** [C-6]。想看全部概念文章，敲 `Get-Help about_*` 就会列出来 [C-6]。

> [!tip] 大白话
> 帮助系统像一个**随软件的说明书柜**：柜子是空的（3.0 之后不自带说明书），你得先跑一趟 `Update-Help` 把说明书搬回来。搬回来之前，除了封面上那几行"用法"，别的都翻不到。
> 而概念文章的**文件名是固定的英文**——就像图书馆的索书号，不管馆里放的是中文书还是英文书，索书号都长一个样。

#### 3.4.4 `Update-Help` 的两条硬限制

这两条在中文社区的文章里几乎从不提，但官方写得很明确 [C-7]：

1. **不加 `-Force` 时，`Update-Help` 每 24 小时只运行一次**；
2. **每个模块的下载上限是 1 GB 未压缩内容**。

官方还特意解释了为什么限制"每天一次"：**正是为了让用户能放心地把它写进配置文件**（这样每次开 PowerShell 尝试更新一次，也不会变成持续占用带宽的操作）[C-7]。

#### 3.4.5 `Update-Help` 的权限按版本不同（这是本章要盯住的一处 5.1 / 7 差异）

- **PowerShell 6.0 及更低版本**（含本章说的 5.1）：`Update-Help` **需要管理员权限**；
- **6.1 及更高版本**（含 7）：`-Scope` 的**默认值是 `CurrentUser`**，也就是默认只给当前用户装；但**如果更新的是 `$PSHOME\Modules` 里的模块，仍然需要"以管理员身份运行"** [C-7]。

按本笔记的降维口径翻译：**只有装在系统目录里的那部分帮助需要管理员；你自己装的模块，普通账户就能更新** [C-7]。

#### 3.4.6 下载失败：系统语言不受支持

`en-US` 的帮助文件**始终会发布**。如果你的系统区域是 en-GB 这类不受支持的语言，可能报 `The specified culture is not supported`，这时要**显式指定**语言 [C-7]。

> 环境：PowerShell ｜ 版本：5.1 & 7 ｜ 权限：5.1 需管理员；7 默认只装当前用户（更新系统目录中的模块仍需管理员）

```powershell
# 首次：下载本机帮助文件（PowerShell 6.1+ 默认只装当前用户）
Update-Help -Verbose

# 系统区域不是 en-US 而下载失败（报 The specified culture is not supported）时
Update-Help -UICulture en-US -Force

# 查命令怎么用
Get-Help Get-ChildItem
Get-Help Get-ChildItem -Examples              # 只看示例（要有帮助文件）
Get-Help Get-ChildItem -Parameter Path        # 只看某个参数
Get-Help Get-ChildItem -Online                # 浏览器版；不能在远程会话中用
Get-ChildItem -?                              # 等价于 Get-Help，但只对 cmdlet 有效

# 查概念文章（名字必须用英语），以及列出全部概念文章
Get-Help about_Execution_Policies
Get-Help about_*

# 查某个"提供程序"的专属帮助（见 3.5）
Get-Help Registry
Get-Help Certificate
```

> [!warning] 中文社区常见建议漏掉了什么
> 你大概会看到"把 `Update-Help` 写进 `$PROFILE`，每次开机自动更新"这类建议。它本身是可行的（官方也确实这么解释"每天一次"的设计），但社区文章普遍不提两条硬限制：**每 24 小时只运行一次** 和 **每模块 1 GB 上限** [C-7]。不知道这两条，你会以为"我写了自动更新但它没生效，是不是坏了"。

### 3.5 Provider 与 PSDrive：把一切变成"盘"

#### 3.5.1 八个内置的"盘"

Provider（提供程序）的作用是**把专用的数据存储，以"驱动器"的形式暴露出来**，路径的写法和使用方式跟硬盘一样 [C-5]。PowerShell 内置 8 个 [C-5]：

| Provider | 它把什么变成了"盘" | 平台 |
|---|---|---|
| FileSystem | 磁盘上的文件与目录 | 全平台 |
| Registry | 注册表 | **仅 Windows** |
| Certificate | 证书存储 | **仅 Windows** |
| WSMan | WS-Management 配置 | **仅 Windows** |
| Alias | 别名（命令的短名字） | 全平台 |
| Environment | 环境变量 | 全平台 |
| Function | 已定义的函数 | 全平台 |
| Variable | 变量 | 全平台 |

有 3 个是**仅 Windows 平台可用**：Certificate、Registry、WSMan [C-5]。

#### 3.5.2 同一批命令，可以作用在任何"盘"上

这是 Provider 模型最漂亮的地方：**同一批 cmdlet 可以作用于任何 Provider 的数据**。官方举的例子是 `New-Item`——在 `C:` 上是建文件，在注册表上是建键，在 `Alias:` 上是建别名，**用法完全一样** [C-5][C-15]。

分层数据的导航方式也和硬盘一致：用 `drive:\location\child-location` 这种写法；**路径里含空格就必须加双引号**；`.` 和 `..` 分别表示当前层和上一层 [C-5][C-15]。

> 环境：PowerShell ｜ 版本：5.1 & 7 ｜ 权限：写系统位置（HKLM、系统目录）需要管理员；其余官方未说明

```powershell
# 看看这台机器上有哪些"盘"（含 Provider 驱动器）
Get-PSDrive
Get-PSProvider

# 同一个 New-Item：在文件系统里建目录
New-Item -Path "C:\" -Name "Logfiles" -ItemType "Directory"

# 同一个 New-Item：在注册表里建键（写入位置决定要不要管理员）
New-Item -Path "HKLM:\Software\ContosoCompany"

# 同一个 New-Item：在 Alias 盘里建别名
New-Item -Path "Alias:np" -Value "notepad.exe"

# 切换位置：可以切到任何 Provider 的路径
Set-Location HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion

# 路径含空格时要加双引号；. 和 .. 分别表示当前层与上一层
Set-Location "C:\Program Files"
Set-Location ..
```

> [!tip] 大白话
> 把 Provider 想成**给不同仓库统一装上了同一种门牌系统**：文件仓库、注册表仓库、证书仓库，本来各有各的找法；装上之后，**都用 `C:`、`HKLM:`、`Cert:` 这样的"盘符"进门，都用同一套 `dir` / `cd` / `New-Item` 逛**。
> 你不需要记住"注册表有别的一套命令"，只要记住"换个盘符，命令照旧"。

#### 3.5.3 只有文件系统这一种"盘"有"家目录"

FileSystem 是**唯一有默认 Home 的 Provider**（值等于 `$HOME`），所以 `~` 表示 Home 目录；**没有 Home 的 Provider，用 `~` 会报错** [C-5]。

#### 3.5.4 有些参数，只在特定的"盘"里出现

官方管这叫**动态参数**：只在配合特定 Provider 时才出现。典型例子是在 `Cert:` 盘里，`Get-ChildItem` 会多出一个 `-CodeSigningCert` 参数 [C-5]。

想知道某个 Provider 有哪些动态参数，官方给的办法是 `Get-Help <provider-name>`（例如 `Get-Help Certificate`）[C-5]——这也正好接上 3.4.6 命令清单里的最后两条。

> [!tip] 大白话
> 动态参数像**只有在特定仓库里才会递到你手上的专用工具**：你在普通仓库里翻遍工具箱都找不到它，一走进证书仓库，门口就多摆了一个"只看签名证书"的筛子。所以"这个参数我昨天怎么没见过"很正常——**换盘再看**。

#### 3.5.5 这些"盘"，别的地方看不见

`Get-PSDrive` 能看到 `New-PSDrive` 创建的**会话级驱动器**；而 `net use`、`[System.IO.DriveInfo]::GetDrives()`、`Get-CimInstance` **都看不到它们** [C-13]。

换句话说，PowerShell 里的"盘"有一部分是**PowerShell 自己造的**，出了 PowerShell 就没了。

#### 3.5.6 预告一下：这些命令，第 4 章要正式排队上场

> [!note] 本章只管"有这些命令"，用法留给第 4 章
> 你已经在 3.5.2 见过 `New-Item` 了。文件系统与注册表的常用 cmdlet 主体（`Get-ChildItem`、`Get-Item`、`Get-ItemProperty`、`Get-ItemPropertyValue`、`Set-ItemProperty`、`Remove-Item`、`Remove-ItemProperty`、`Clear-Item`、`Set-Location` 等）**全部放在第 4 章**，因为它们正好是把前两章内容串起来的那批命令。本章只先记住一件事：**它们能用同一套写法，同时作用在文件系统和注册表上** [C-5][C-9][C-11][C-12][C-15]。

### 3.6 执行策略：它防的是手滑，不是防坏人

#### 3.6.1 官方明说：它不是安全边界

这是本章最需要纠正的一个流行误解。官方对执行策略的定位说得非常直白：**执行策略不是安全边界**，它是一种"深层防御"——因为**当用户无法运行脚本时，直接在命令行里把脚本内容粘贴进去就能绕过它** [C-3]。

> [!warning] 执行策略是"防误运行的便利机制"，不是安全方案
> 中文社区普遍把它当成一种"安全设置"来讲，甚至建议换成最严的档位来"提高安全性"。**官方口径不是这样**：它明确说执行策略不是安全边界，防的是"随手运行来路不明脚本"这类**手滑**，不是防有意绕过的人 [C-3]。
>
> 落到行动上就是两句话：**别为了"看起来安全"把它调到最严**（那只会让你天天被自己的脚本挡住）；也**别因为它"不是安全"就随手关掉**——它确实帮你挡了一次误运行。

#### 3.6.2 `Restricted` 拦的是什么

`Restricted` 是"允许单个命令、但**阻止所有脚本文件**"的档位。注意"所有脚本文件"包括 `.ps1`、`.ps1xml`、`.psm1`，以及 **PowerShell 的配置文件** [C-3]——这一点很重要，因为新手遇到的第一个报错往往就是配置文件被拦。

#### 3.6.3 从网上下载的脚本，会被贴一张标签

从 Internet 下载的脚本会被标记为"**来自 Internet**"。在 `RemoteSigned` 下，**未签名的这类文件不会被运行**；要放行，可以用 `Unblock-File` 解除标记 [C-3]。

有一条容易踩的细节：**并不是所有下载方式都会带上这张标签**。官方明确说，用 `curl.exe`、`Invoke-RestMethod`、`Invoke-WebRequest` 下载的文件**不会**带这个标记 [C-3]。所以"我明明是从网上下的，怎么没被拦"和"我这个明明是本地生成的，怎么被拦了"两种情况都可能出现。

#### 3.6.4 默认值到底是什么

官方给出的默认是：策略 `Default` **在客户端和服务器上都是 `RemoteSigned`**；而如果所有作用域都是 `Undefined`，那么**客户端**的有效策略是 **`Restricted`**、**服务器**是 **`RemoteSigned`** [C-3]。

> [!warning] 默认与推荐都是 `RemoteSigned`，不是 `AllSigned`
> 社区文章常把 `AllSigned` 列为"建议"、把 `RemoteSigned` 说成"折中方案"；**官方默认是 `RemoteSigned`** [C-3]。本笔记按官方口径写：**默认与推荐都用 `RemoteSigned`**，`AllSigned` 只作为一种"可选更严档位"在这里提一句——你只有在确实需要"所有脚本都必须签名"的场景（比如统一的受控环境）才需要考虑它。
>
> 同一件事还有第二层：**`Undefined` 不等于"没有限制"**。如果各级作用域都还是 `Undefined`，客户端上的实际效果是 `Restricted`（也就是"禁止运行脚本"）[C-3]——这正是 3.6.2 那个报错的来源之一。

#### 3.6.5 作用域：先只记一条 `CurrentUser`

执行策略有多个"作用域"（scope），不同作用域存在不同地方、优先级也不同。官方给的优先级是：`Process`（最高）> `CurrentUser` > `LocalMachine`，并且**组策略的设置覆盖所有作用域** [C-3]。

对零基础读者，**先只记 `CurrentUser` 这一条就够了**：

- **`CurrentUser` 只影响你自己**，而且 **`Set-ExecutionPolicy -Scope CurrentUser` 不需要管理员权限** [C-3]。

另外有一个好用的档位是 `Process`：它只对**当前这个会话**生效，而且**不写注册表**——它改的是环境变量 `$Env:PSExecutionPolicyPreference` [C-3]。适合"我只想让这个窗口能跑脚本，关掉窗口就恢复原样"的场景。

至于 `LocalMachine` 和组策略，先放着，等 3.6.7 那个"改了不生效"的场景再回来看。**`LocalMachine` 需要管理员**，这一点官方是明确写了的 [C-3]。

#### 3.6.6 命令清单

> 环境：PowerShell ｜ 版本：5.1 & 7（5.1 用 `powershell.exe`，7 用 `pwsh.exe`）｜ 权限：`CurrentUser` / `Process` 无需管理员；`LocalMachine` 需要管理员 [C-3]

```powershell
# 只看不写：当前生效策略，以及各作用域的实际取值
Get-ExecutionPolicy
Get-ExecutionPolicy -List

# 官方推荐的最小改动：只影响当前用户，不需要管理员
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 只对当前会话生效，不落盘（改的是 $Env:PSExecutionPolicyPreference）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 起一个"只这一次"的会话（7 用 pwsh.exe；5.1 换成 powershell.exe）
pwsh.exe -ExecutionPolicy RemoteSigned

# 解除"来自 Internet"标记（下载的脚本被 RemoteSigned 拦下时）
Unblock-File -Path .\downloaded.ps1

# 恢复默认：删掉当前用户的设置，回到系统默认值
Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser
```

> [!example] 你可能见过的那个报错
> 现象：一打开 PowerShell 就弹出一行红字，大意是"**无法加载文件 …\profile.ps1，因为在此系统上禁止运行脚本**"，后面还跟着 `CategoryInfo: SecurityError … PSSecurityException` [C-17]（现象）。
>
> 原理在官方文档里：`Restricted` 会**阻止 `.ps1` 配置文件**；而在所有作用域都是 `Undefined` 时，客户端的有效策略就是 `Restricted` [C-3]（原理）。
>
> 所以这不是"你的电脑中毒了"，也不是"PowerShell 装坏了"，而是**配置文件被执行策略挡住了**。要在理解 3.6.1 的前提下处理：如果你确实要用配置文件，按 3.6.6 把 `CurrentUser` 作用域设成 `RemoteSigned`。

> [!note] 两条我们不写进结论的情形
> 一是 **UNC 路径在 `RemoteSigned` 下的限制**：官方原文的限定语是"在无法将 UNC 路径与 Internet 路径区分开来的系统上"，**它对平台有依赖，本章不写成通用结论** [C-3]。二是 **Server Core 上的 `AuthorizationManager check failed`**：那是依赖 `explorer.exe` 提供区域检查 API 的场景，对零基础读者属极边缘，本章刻意剔除 [C-3]。

#### 3.6.7 改了不生效怎么办（排错小节）

如果在一台**公司统一管理的电脑**上，你按 3.6.6 把 `CurrentUser` 设成了 `RemoteSigned`，`Get-ExecutionPolicy` 却还显示别的值，或者你设完又被改回去——那大概率不是你没敲对，而是**更高优先级的作用域在压着它**。

按优先级从高到低看 [C-3]：

| 优先级 | 作用域 | 存在哪 | 特点 |
|---|---|---|---|
| 最高 | `Process` | 环境变量 `$Env:PSExecutionPolicyPreference` | **不写注册表**，只影响当前会话 [C-3] |
| 中 | `CurrentUser` | 用户的 `powershell.config.json` | **不需要管理员**，只影响你自己 [C-3] |
| 低 | `LocalMachine` | `$PSHOME/powershell.config.json` | **需要管理员**，影响全机 [C-3] |
| 覆盖一切 | 组策略 | 由域策略下发 | **组策略设置覆盖所有作用域** [C-3] |

排查顺序建议是：

1. `Get-ExecutionPolicy -List` 把各作用域的实际取值列出来，**先看清到底是谁在生效**；
2. 如果你要的档位被 `Process` 压着，看看是不是启动命令里带了 `-ExecutionPolicy`，或者当前会话的环境变量被设过；
3. 如果是**组策略**在压着，那 `Set-ExecutionPolicy` 改哪个作用域都没用——官方明说组策略覆盖所有作用域 [C-3]。这时正确的动作是**找管理员**，而不是反复重试命令。

### 3.7 编码与中文乱码：三条独立通道

这一节要解决"中文乱码"。但必须先把一个错误期待掐掉：**不存在"改一个设置就好"的万能开关**。官方在同一页里就先说了"通常 Windows PowerShell 默认使用 Unicode UTF-16LE 编码"，紧接着又说"**Windows PowerShell 中 cmdlet 使用的默认编码不一致**" [C-8]——所以本章的写法是：**把编码拆成三条互不相干的通道，哪条出问题就修哪条**。

#### 3.7.1 前提

Windows 既支持 Unicode 也支持传统字符集；PowerShell **默认使用 Unicode**，并且**多个 cmdlet 都带 `-Encoding` 参数**，可以指定成别的字符集 [C-8]。

#### 3.7.2 通道一：脚本源码本身是什么编码

这一条管的是"**你写的那份 `.ps1` 文件，本身用什么编码存**"。

- 在 **Windows PowerShell（5.1）** 里，**除 `UTF7` 以外，任何 Unicode 编码总是会创建 BOM** [C-8]；
- 在 **PowerShell（v6 及以上，含 7）** 里，**默认对所有文本输出使用 `utf8NoBOM`** [C-8]。

> [!tip] 大白话：什么是 BOM
> BOM 是**文件开头多出来的 3 个看不见的字节**，作用是告诉读它的程序："我是 UTF-8"。
> 你打开文件看不到它们，但程序第一眼看到的就是它们。5.1 存脚本时**默认会加上这 3 个字节**；7 默认**不加**。这就是为什么同一份中文脚本在 5.1 里正常、在 7 里也正常，但换一种存法就可能变乱码。

#### 3.7.3 通道二：`-Encoding` 参数与各 cmdlet 的默认值（5.1 最坑的一块）

这一条管的是"**命令把内容写进文件时用什么编码**"。注意：**在 5.1 里没有"统一的默认编码"这回事**，必须**按 cmdlet 分别判断** [C-8]：

| 写法 | 5.1 的默认编码 | 7 的默认编码 |
|---|---|---|
| `Out-File`，以及重定向 `>` / `>>` | **UTF-16LE** | `utf8NoBOM` |
| `Export-Csv` | **ASCII** | `utf8NoBOM` |
| `New-Item -Type File -Value` | **不带 BOM 的 UTF-8** | `utf8NoBOM` |
| `Add-Content` / `Set-Content`（目标文件为空或不存在时） | `Default`（系统 ANSI 旧代码页） | `utf8NoBOM` |

后三行和第一行放在一起看，你就明白为什么"5.1 默认是 XX 编码"这句话是错的：同一个版本里，**不同 cmdlet 出来的文件编码各不相同** [C-8]。5.1 上写中文文件，最稳妥的办法是**每次都显式写 `-Encoding`**。

#### 3.7.4 通道三：控制台，以及"对外部程序说话"用的编码

这一条管的是"**你在窗口里看到的字符，和 PowerShell 传给外部程序的东西，用什么编码**"。

官方的关键说明是：自动变量 `$OutputEncoding` **只影响 PowerShell 与外部程序通信时的编码，不影响重定向运算符，也不影响 cmdlet 写文件时的编码** [C-8]。

换句话说，**通道三和通道二互不覆盖**：

- `$OutputEncoding` 管"**和外部程序说话**"；
- `-Encoding` 参数，以及 `$PSDefaultParameterValues` 管"**存到文件**" [C-8]。

还有一条把两边搭上桥的事实：**从 5.1 起，`>` 和 `>>` 内部是调用 `Out-File` 来实现的**，所以设置 `$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'` 可以**同时**管住"写文件"和"重定向"这两种写法 [C-8]。

> [!tip] 大白话
> 把三条通道想成**三根独立的水管**：一根进水（脚本源码存成什么编码）、一根出水到文件（`-Encoding`）、一根接到外部程序（`$OutputEncoding` / 控制台）。
> 只拧一根，另外两根不会跟着变。所以"乱码"要**先判断是哪根漏的**：是文件打开就乱，还是只在某个外部程序输出里乱？

#### 3.7.5 BOM 到底加不加：按文件类型分开

官方的建议看起来是"两个相反方向"，其实是**针对两类不同文件**，必须分开表述 [C-8]：

| 文件类型 | 建议 | 依据 |
|---|---|---|
| **脚本源码**（尤其是 5.1 的 `$PROFILE`） | **用带 BOM 的 UTF-8** | 含非 ASCII 字符的脚本在 5.1 下**需要 BOM**，否则会被误读为"过时的 ANSI 代码页"，中文就乱了 [C-8] |
| **纯数据文件** | **用不带 BOM 的 UTF-8** | 为获得最佳整体兼容性，官方建议避免在 UTF-8 文件中使用 BOM（跨平台工具链通常不认它）[C-8] |

> [!warning] BOM 的两条建议是"分工"，不是"打架"
> 你如果把"避免 BOM"和"必须用 BOM"两条建议放在一起看，会得出互相矛盾的结论。**正确的读法是按文件类型分工**：**脚本源码（5.1 的 `$PROFILE`）用 BOM；纯数据文件不用 BOM** [C-8]。
>
> 中文社区的文章通常只讲后一半（脚本要 BOM），照着做之后再拿这个文件去喂 Linux 上的工具，又会被 BOM 坑到 [C-18]（现象）。

#### 3.7.6 诊断与落盘的命令清单

**第一步永远是诊断**：先把"当前三根管子的状态"看清楚，再决定改哪根 [C-8]。

> 环境：PowerShell ｜ 版本：5.1 & 7（默认编码行为不同）｜ 权限：无需管理员

```powershell
# —— 第一步：诊断。看当前代码页与三条编码通道 —— 5.1 & 7
chcp                        # 当前控制台代码页
[Console]::OutputEncoding   # 控制台"输出"用什么编码
[Console]::InputEncoding    # 控制台"输入"用什么编码
$OutputEncoding             # 与外部程序通信用什么编码

# —— 第二步：写文件时显式指定编码（最不容易错）—— 5.1 & 7
'你好' | Out-File -FilePath .\a.txt -Encoding utf8
'你好' | Set-Content -Path .\a.txt -Encoding utf8

# —— 会话级默认：让 cmdlet 的 -Encoding 都走 utf8 —— 5.1 & 7
# （从 5.1 起 > 和 >> 内部调用 Out-File，所以这一行也管住了重定向）
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# —— 会话级：控制台与对外部程序的编码（临场救急用）—— 5.1 & 7
# 注意：$OutputEncoding 只影响与外部程序通信，不影响写文件
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$OutputEncoding           = [System.Text.Encoding]::UTF8

# —— 第三步：把设置落盘到配置文件（永久生效）—— 5.1 & 7
Test-Path $PROFILE
New-Item -Path $PROFILE -ItemType File -Force   # 不存在时先创建
notepad $PROFILE                                # 用记事本打开编辑
```

> [!warning] 不要在 `$PROFILE` 里只写 `chcp 65001`
> 中文社区最常见的方案是"把代码页改成 65001（UTF-8）"，理由是"代码页 936 与 UTF-8 不一致" [C-18]（现象）。
>
> 对应到官方原理上，这类方案**只能覆盖通道三的一部分**：它管的是控制台与外部程序那一头，**管不到 cmdlet 写文件时用的编码**（那是通道二，要靠 `-Encoding` 或 `$PSDefaultParameterValues`）[C-8]（原理）。
>
> 所以会出现一个典型的失败场景：**"写出来的文件正常了，但调用某个外部程序时输出还是乱码"**——这不是方案错了，而是它**只修了三条通道里的一条** [C-8]。

> [!example] 你可能见过的乱码长什么样
> 现象：正常的中文被显示成 `UTF-8 缂栫爜宸查厤缃畬鎴愶紒` 这一类谁也看不懂的字符，社区把它归因于"控制台代码页 936（GBK）与脚本文件 UTF-8 不一致" [C-18]（现象）。
>
> 原理要回到官方：5.1 的 `Out-File` / `>` / `>>` 默认写 **UTF-16LE**，而 `Export-Csv` 默认写 **ASCII**，再加上 `$OutputEncoding` 只管对外部程序——是**这几条通道各自为政**造成的 [C-8]（原理）。
>
> 明白这一点，你就知道为什么"换一个文本编辑器打开文件"有时看起来是好的：**编辑器按自己的猜测解码了**，文件本身并没有变对。

> [!warning] 中文目录里第三方程序报 `Error 3`：只能说成"某些第三方程序的已知限制"
> 有一条现象值得知道：**在中文目录下，某些第三方 native 组件会报 `Error 3: The system cannot find the path specified.`，而同一路径在资源管理器里明明看得见** [C-19]（现象）。
>
> **这一条只有 C 级的第三方 issue，没有 A 级的官方原理**，所以本章**只把它写成"某些第三方程序的已知限制"，绝不解释成 PowerShell 的原理**。遇到它时，可用的做法是换个纯英文路径试试——这是绕过，不是修复。

> [!note] 本章刻意留下的空白
> 本轮素材里有两条与"中文环境"相关的疑点，都因为**没有可用的来源**而**本章不写**：
> 1. 有一条与"**用户名/路径含非 ASCII 字符时的模块搜索路径**"有关的疑点，三个来源尝试全部抓取失败，**既无现象来源也无原理来源**，按 P2 决策，正文里**不写现象、不写原理、也不做推断** [C-14]；
> 2. 中文路径下 `Error 3` 的**原理**（现象已在上面提及，但原理没有 A 级支撑）[C-19]。
>
> 这两处请不要当成结论使用。可用的相邻 A 级事实只有一条：**Documents 的位置会被文件夹重定向和 OneDrive 改变**，官方给的验证命令是 `[Environment]::GetFolderPath('MyDocuments')` [C-14]。

### 3.8 PowerShell 5.1 与 7：两个版本可以一起装

#### 3.8.1 两套并存，各有各的名字和路径

这两个版本**并行安装、并行运行**，各有**独立的安装路径、可执行文件名、`PSModulePath`、配置文件和事件日志** [C-4]：

| | Windows PowerShell 5.1 | PowerShell 7 |
|---|---|---|
| 可执行文件 | `powershell.exe` | `pwsh.exe` |
| 安装位置 | `$Env:windir\System32\WindowsPowerShell\v1.0` | `$Env:ProgramFiles\PowerShell\7` |

> [!tip] 大白话
> 把它想成**同一栋楼里住着两位同名不同姓的管家**：一位叫 `powershell.exe`，一位叫 `pwsh.exe`，各管各的房间、各用各的记事本。
> 所以"我明明装了 7，怎么还是旧行为"这种问题，十有八九是**你打开的是 5.1 那位管家**——看窗口标题、或者敲 `$PSVersionTable` 就能分辨。

#### 3.8.2 模块搜索路径 `PSModulePath` 的差别

`PSModulePath` 是 PowerShell 找模块时依次去看的目录清单。两版本的差别是 [C-4][C-14]：

- **PowerShell 7** 的 `$Env:PSModulePath` **额外包含 Windows PowerShell 的路径**，这是为了支持模块自动加载；
- **5.1** 的默认模块路径是 `$HOME\Documents\WindowsPowerShell\Modules` 与 `$Env:ProgramFiles\WindowsPowerShell\Modules` [C-14]。

#### 3.8.3 配置文件改了位置

| | 配置文件位置 |
|---|---|
| 5.1 | `$HOME\Documents\WindowsPowerShell` |
| 7 | `$HOME\Documents\PowerShell` |

路径变了，所以**你在 5.1 里写的那份配置，7 不会自动读**。想知道当前这位管家实际用的是哪一份，用这条命令看 [C-4]：

> 环境：PowerShell ｜ 版本：5.1 & 7（输出路径不同）｜ 权限：无需管理员

```powershell
# 查看当前会话实际使用的配置文件路径
$PROFILE | Select-Object *Host* | Format-List

# 确认自己在哪个版本里
$PSVersionTable

# 看本版本的模块搜索路径（7 会额外包含 5.1 的路径）
$Env:PSModulePath
```

#### 3.8.4 地基不同：.NET 版本与 ISE

- PowerShell **7.4 基于 .NET 8.0**，**5.1 基于 .NET Framework 4.x**；版本差异**可能改变脚本行为**（尤其是脚本里直接调用 .NET 方法的时候）[C-4]。
- **ISE（集成脚本环境）仅支持 5.1，且没有更新计划**；官方推荐改用 VS Code 的 PowerShell 扩展 [C-4]。

按本笔记的降维口径，版本号这一条不用记，只记**后果**：**如果你要跑一个只支持 5.1 的老模块，见 3.8.5。**

#### 3.8.5 老模块怎么办：兼容开关

PowerShell 7 提供了兼容开关 `Import-Module -UseWindowsPowerShell`，用来跑那些只支持 5.1 的模块 [C-4]。

> 环境：PowerShell ｜ 版本：7（5.1 无此需求）｜ 权限：官方未说明

```powershell
# 用兼容层导入一个只支持 Windows PowerShell 5.1 的老模块
Import-Module -UseWindowsPowerShell <模块名>
```

> [!warning] 全程要盯住的四项版本差异
> 这两个版本在**四个行为上不同**，是本章乃至全书最容易出错的地方，本章全程都做了 `5.1` / `7` 标注 [C-4][C-7][C-8]：
> 1. **默认编码**（3.7.3：5.1 各 cmdlet 不一致，7 统一 `utf8NoBOM`）
> 2. **配置文件路径**（3.8.3：`WindowsPowerShell` vs `PowerShell`）
> 3. **`PSModulePath`**（3.8.2：7 额外包含 5.1 的路径）
> 4. **`Update-Help` 权限**（3.4.5：5.1 需要管理员，7 默认只装当前用户）
>
> 另外多记一条**只在 7 上存在**的功能：**位置历史 `cd -` / `cd +`**（PowerShell 6.2 起可用，5.1 不能用），第 4 章会正式用到它 [C-10]。

> [!warning] "迁移简单、快速且安全"这句话，要降级来读
> 官方在迁移页开头称迁移"简单、快速且安全"，但同一页也说明：**ISE 不再更新、部分模块需要 `Import-Module -UseWindowsPowerShell` 兼容层、.NET 版本差异可能改变脚本行为** [C-4]（矛盾）。
>
> 对零基础读者，本章把这句话降级为：**"5.1 与 7 可以共存，所以可以慢慢迁"**——你不需要"先卸掉 5.1 再装 7"，两者互不干扰 [C-4]。

> [!note] 一个问题，本章不给结论
> "**新手该默认用 7 吗？**"——本轮素材中**没有官方倾向来源**（官方只说明两者可以并行、迁移简单，没有给出"新手就用哪个"的推荐）[C-4]。所以本章**不给"就用 7"的结论**，请你按自己的场景决定。另外两处时效性留白也一并说明：本轮抓取的 **8 张 cmdlet 参考页没有 `Last updated` 字段**（时效不可考）[C-6][C-7][C-9]–[C-13][C-15]；**PowerShell 7 的当前稳定版本号未确认**，所以全篇版本标注统一写 `7`，不写具体小版本 [C-4]。

### 3.9 一张表看懂 PowerShell / cmd / Bash 的差别

#### 3.9.1 十个维度逐项对照

| 维度 | PowerShell 5.1（`powershell.exe`） | PowerShell 7（`pwsh.exe`） | cmd.exe | Bash |
|---|---|---|---|---|
| 管道传的东西 | 对象 | 对象 | 文本 | 文本 |
| 命令名风格 | Verb-Noun（`Get-ChildItem`）+ 别名（`dir` / `ls`） | 同 5.1 | 独立小工具（`dir`） | 独立小工具（`ls`） |
| 路径分隔符 | `\`（多数场景 `/` 也可用） | `\`（`/` 可用） | `\` | `/` |
| 盘符 | `C:`，另有 Provider 盘符 `HKLM:`、`Cert:`、`Env:` | 同 5.1 | `C:` | 无（挂载点） |
| 变量语法 | `$name`；环境变量 `$Env:NAME` | 同 5.1 | `%NAME%` | `$name` / `${name}` |
| 脚本扩展名 | `.ps1`（另有模块 `.psm1`、清单 `.psd1`） | `.ps1` | `.bat` / `.cmd` | `.sh`（常无扩展名） |
| 脚本执行前提 | 受执行策略约束（默认 `RemoteSigned`） | 受执行策略约束 | 不受执行策略约束 | 需 `chmod +x` |
| 默认文本输出编码 | **因 cmdlet 而异**（如 `Out-File` = UTF-16LE） | 统一 `utf8NoBOM` | 系统 ANSI 代码页 | UTF-8 |
| 配置文件 | `$HOME\Documents\WindowsPowerShell\*profile.ps1` | `$HOME\Documents\PowerShell\*profile.ps1` | 无 | `~/.bashrc` 等 |
| 运行位置 | 仅 Windows | Windows / macOS / Linux | 仅 Windows | 类 Unix |

#### 3.9.2 这张表怎么来的

> [!note] 来源说明
> **本表为本文整理，没有官方对照专页** [C-16]。各格依据分别来自：[C-2]（对象 vs 文本、Verb-Noun）、[C-4]（可执行名、配置文件路径、跨平台、`PSModulePath`）、[C-5]（Provider 盘符）、[C-8]（默认编码）、[C-3]（执行策略）。
>
> 需要提醒的是：其中"**变量语法**"和"**路径分隔符**"两行，来源是间接推论而不是官方成文对照，**溯源强度弱于其他行**，请只作为心智模型使用 [C-16]。

> [!warning] 根本差别不在命令名
> 你会看到 PowerShell 里也有 `dir`、`ls`、`cd` 这些眼熟的写法——但那些只是**别名**。与 cmd / Bash 的根本差别**不在命令名，而在管道里流动的是对象还是文本** [C-2]。只记别名，你会继续用"切字符串"的思路写 PowerShell 脚本，也就用不上它真正的省事之处。

### 本章小结

> [!summary] 小结
> - **对象而不是文本**：PowerShell 接收并返回**对象**而不是文本，所以管道连接更省事；文本管道只能传字符串、取字段要自己切，对象管道里的每个项自带 `Name`、`Id`、`Handles` 这类**带名字的格子** [C-2]
> - **管道一次一个对象**：`|` 从左到右把上一条的结果发给下一条；因为传的是对象，`Get-Process notepad | Stop-Process` 不必再写 `-Name` / `-ID`；stdin **没有**接入 PowerShell 管道 [C-1]
> - **参数绑定**：接收端必须有"接受管道输入"的参数，接法分**按值**（ByValue）和**按属性名**（ByPropertyName）；绑上要同时满足三条，且**无法强制绑定到特定参数** [C-1]
> - **`-InputObject` 的坑**：管道一次送**一个**对象，`-InputObject` 把集合当**一整个数组**送——官方称"这种细微差异具有重大后果"：`Get-Process | Get-Member` 显示 `System.Diagnostics.Process`，而 `Get-Member -InputObject (Get-Process)` 显示 `System.Object[]` [C-1]
> - **数组会拆、字符串和哈希表不拆**：自动枚举有例外——哈希表要 `GetEnumerator()`，`System.String` 不会被枚举 [C-1]
> - **四个自举命令**：`Get-Verb`（合法动词）、`Get-Command`（有哪些命令）、`Get-Member`（对象有什么）、`Get-Help`（怎么用）；官方推荐顺序是 `Get-Command` → `Get-Help` → `Get-Member` [C-2][C-6]
> - **帮助系统**：3.0 起 Windows 自带模块**不含帮助文件**，要 `Update-Help` 下载或用 `-Online`；`Update-Help` **每 24 小时只运行一次**、**每模块上限 1 GB**；权限按版本不同（5.1 需管理员，7 默认只装当前用户）[C-6][C-7]
> - **Provider 把一切变成"盘"**：内置 8 个（Certificate / Registry / WSMan **仅 Windows 可用**）；同一批 cmdlet 可作用于任何 Provider；FileSystem 是唯一有默认 Home 的；动态参数只在特定盘里出现 [C-5][C-13]
> - **执行策略不是安全边界**：它是**防误运行的便利机制**，粘贴脚本内容即可绕过；**默认与推荐都是 `RemoteSigned`**（不是 `AllSigned`）；**`CurrentUser` 不需要管理员**，`LocalMachine` 需要，**组策略覆盖所有作用域** [C-3]
> - **编码是三条独立通道**：① 脚本源码编码（5.1 除 `UTF7` 外总是创建 BOM；7 默认 `utf8NoBOM`）② `-Encoding` 参数与各 cmdlet 默认值（5.1 **按 cmdlet 分别判断**：`Out-File` / `>` / `>>` = UTF-16LE，`Export-Csv` = ASCII，`New-Item -Type File -Value` = 无 BOM 的 UTF-8，空文件的 `Add-Content` / `Set-Content` = 系统 ANSI）③ 控制台与对外部程序编码（`$OutputEncoding`，**不管写文件**）[C-8]
> - **BOM 按文件类型分工**：**脚本源码（尤其 5.1 的 `$PROFILE`）用带 BOM 的 UTF-8；纯数据文件用不带 BOM 的 UTF-8** [C-8]
> - **5.1 与 7 可以共存**：各有独立路径、可执行名、`PSModulePath`、配置文件、事件日志；四项行为差异要全程盯住（默认编码、配置文件路径、`PSModulePath`、`Update-Help` 权限）；`cd -` **仅 7 可用** [C-4][C-10]
> - **官方未说明的位置**`（本章一律不推断）`：`Unblock-File`、`Import-Module -UseWindowsPowerShell`、`Set-ItemProperty` 写注册表值、`New-Item` 建文件/键、`Trace-Command`、`chcp` 与 `[Console]::*Encoding` 修改的**管理员权限要求**均**官方未说明**
> - **本章刻意留白**：与"用户名/路径含非 ASCII 字符时的模块搜索路径"相关的疑点**零可用来源，不写**；中文路径下 `Error 3` **只有 C 级现象、无 A 级原理**，只作"某些第三方程序的已知限制"提及 [C-19][C-14]

下一章把这一章和前两章接起来：用同一套 PowerShell 命令，**同时**操作文件系统和注册表——列目录、读值、写值、备份、回滚，一条完整的链路走一遍。

---

### 本章来源对照

| ID | 官方页面 |
|---|---|
| C-1 | [about_Pipelines（关于管道）](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_pipelines) |
| C-2 | [发现 PowerShell](https://learn.microsoft.com/zh-cn/powershell/scripting/discover-powershell) |
| C-3 | [about_Execution_Policies（执行策略）](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies) |
| C-4 | [从 Windows PowerShell 5.1 迁移到 PowerShell 7](https://learn.microsoft.com/zh-cn/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7) |
| C-5 | [about_Providers（提供程序）](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_providers) |
| C-6 | [Get-Help](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/get-help) |
| C-7 | [Update-Help](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/update-help) |
| C-8 | [about_Character_Encoding（字符编码）](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_character_encoding) |
| C-9 | [Get-ChildItem](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-childitem) |
| C-10 | [Set-Location](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-location) |
| C-11 | [Get-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-itemproperty) |
| C-12 | [Set-ItemProperty](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/set-itemproperty) |
| C-13 | [Get-PSDrive](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/get-psdrive) |
| C-14 | [about_PSModulePath](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_psmodulepath) |
| C-15 | [New-Item](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.management/new-item) |
| C-16 | PowerShell 与 cmd / Bash 逐项对照表（**本文整理，无官方对照专页**；逐格依据见 C-2 / C-4 / C-5 / C-8 / C-3） |
| C-17 | [Windows 中打开 powershell 后，出现报错"无法加载文件 xxxx，因为在此系统上禁止运行脚本"](https://www.cnblogs.com/geekbruce/articles/18905587)（C 级 · 经验型，仅用于现象） |
| C-18 | [解决 PowerShell 中文乱码问题](https://blog.csdn.net/chao_666666/article/details/156590250)（C 级 · 经验型，仅用于现象） |
| C-19 | [Encoding Failure in Windows PowerShell with Chinese Directory Paths（GitNexus issue #1811）](https://github.com/abhigyanpatwari/GitNexus/issues/1811)（C 级 · 经验型，仅用于现象） |
