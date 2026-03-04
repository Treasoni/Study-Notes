---
tags: [wpf, xaml, dotnet, desktop, mvvm, c#]
created: 2026-03-04
updated: 2026-03-04
---

# WPF 常用操作指南

> [!info] 概述
> **WPF (Windows Presentation Foundation) 是微软的 Windows 桌面应用 UI 框架**，使用 XAML 定义界面，支持数据绑定、样式模板、动画等强大功能。本文档重点介绍常用的操作和最佳实践。

## 快速导航

| 我想... | 跳转章节 |
|---------|----------|
| 了解 WPF 基础 | [[#一、WPF 简介]] |
| 布局界面 | [[#二、布局控件]] |
| 使用常用控件 | [[#三、常用控件]] |
| 绑定数据 | [[#四、数据绑定]] |
| 实现 MVVM | [[#五、MVVM 模式]] |
| 自定义样式 | [[#六、样式与模板]] |
| 排查问题 | [[#七、常见问题]] |

---

## 一、WPF 简介

### 是什么

**WPF** 是微软推出的 Windows 桌面应用程序 UI 框架：
- 使用 **XAML** 定义用户界面
- 支持**数据绑定**、**样式模板**、**动画**
- 分离 UI 设计与业务逻辑
- **仅运行在 Windows 平台**

### 为什么选择 WPF

| 优势 | 说明 |
|------|------|
| **XAML** | 声明式 UI，设计器友好 |
| **数据绑定** | 强大的 MVVM 支持 |
| **样式模板** | 高度可定制的外观 |
| **矢量图形** | 支持缩放不失真 |
| **硬件加速** | DirectX 渲染 |

### 通俗理解

**🎯 比喻**：WPF 就像「装修工具箱」。XAML 是设计图纸，控件是家具，数据绑定是电线（自动连接数据源），样式模板是墙纸和油漆。

### 核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                    WPF 应用程序结构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │   XAML      │ ←→  │  代码后台    │ ←→  │  ViewModel  │   │
│  │  (界面定义)  │     │  (.xaml.cs) │     │  (业务逻辑)  │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│         ↓                   ↓                   ↓           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  数据绑定 (Binding)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│         ↓                   ↓                   ↓           │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │   Model     │     │   Service   │     │  数据源      │   │
│  │  (数据模型)  │     │  (服务层)    │     │             │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 来源
> - [WPF 官方概述](https://learn.microsoft.com/dotnet/desktop/wpf/overview/) - Microsoft Learn

---

## 二、布局控件

### 2.1 Grid - 网格布局

**最常用的布局控件**，使用行和列来组织子元素。

```xml
<!-- Grid 基础用法 -->
<Grid>
    <!-- 定义行 -->
    <Grid.RowDefinitions>
        <RowDefinition Height="Auto"/>  <!-- 自动高度 -->
        <RowDefinition Height="*"/>     <!-- 填充剩余空间 -->
        <RowDefinition Height="100"/>   <!-- 固定高度 -->
    </Grid.RowDefinitions>

    <!-- 定义列 -->
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="200"/>
        <ColumnDefinition Width="*"/>
    </Grid.ColumnDefinitions>

    <!-- 放置控件 -->
    <Button Grid.Row="0" Grid.Column="0" Content="按钮1"/>
    <Button Grid.Row="0" Grid.Column="1" Content="按钮2"/>
    <TextBox Grid.Row="1" Grid.ColumnSpan="2" Text="跨两列"/>
</Grid>
```

**常用属性**：

| 属性 | 说明 |
|------|------|
| `Grid.Row` | 所在行（从 0 开始） |
| `Grid.Column` | 所在列（从 0 开始） |
| `Grid.RowSpan` | 跨行数 |
| `Grid.ColumnSpan` | 跨列数 |
| `Height="*"` | 按比例填充 |
| `Height="Auto"` | 自动调整 |

### 2.2 StackPanel - 栈布局

**简单排列**，子元素水平或垂直排列。

```xml
<!-- 垂直排列（默认） -->
<StackPanel Orientation="Vertical" Margin="10">
    <Button Content="按钮1" Margin="0,0,0,5"/>
    <Button Content="按钮2" Margin="0,0,0,5"/>
    <Button Content="按钮3"/>
</StackPanel>

<!-- 水平排列 -->
<StackPanel Orientation="Horizontal">
    <TextBlock Text="姓名：" VerticalAlignment="Center"/>
    <TextBox Width="200"/>
</StackPanel>
```

**常用属性**：

| 属性 | 说明 |
|------|------|
| `Orientation` | `Vertical` 或 `Horizontal` |
| `Margin` | 外边距 |
| `Spacing` | 子元素间距（.NET 5+） |

### 2.3 DockPanel - 停靠布局

子元素**停靠到边缘**。

```xml
<DockPanel LastChildFill="True">
    <Button DockPanel.Dock="Top" Content="顶部"/>
    <Button DockPanel.Dock="Bottom" Content="底部"/>
    <Button DockPanel.Dock="Left" Content="左侧"/>
    <Button DockPanel.Dock="Right" Content="右侧"/>
    <Button Content="填充剩余空间"/>
</DockPanel>
```

### 2.4 Canvas - 画布布局

**绝对定位**，使用坐标控制位置。

```xml
<Canvas Width="400" Height="300">
    <Button Canvas.Left="50" Canvas.Top="100" Content="绝对定位"/>
    <Ellipse Canvas.Left="200" Canvas.Top="50" Width="100" Height="100" Fill="Blue"/>
</Canvas>
```

### 2.5 WrapPanel - 自动换行

子元素**自动换行/换列**。

```xml
<WrapPanel Orientation="Horizontal">
    <Button Content="1" Width="80" Margin="5"/>
    <Button Content="2" Width="80" Margin="5"/>
    <Button Content="3" Width="80" Margin="5"/>
    <!-- 超出宽度自动换行 -->
</WrapPanel>
```

### 布局选择指南

```
┌─────────────────────────────────────────────────────────────┐
│                    布局控件选择指南                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  需要什么样的布局？                                          │
│  │                                                          │
│  ├─ 表格式/复杂布局 ────────→ Grid                         │
│  │                                                          │
│  ├─ 简单水平/垂直排列 ─────→ StackPanel                    │
│  │                                                          │
│  ├─ 工具栏/状态栏布局 ─────→ DockPanel                     │
│  │                                                          │
│  ├─ 精确坐标定位 ─────────→ Canvas                         │
│  │                                                          │
│  └─ 自动换行排列 ─────────→ WrapPanel                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 来源
> - [WPF控件用法及数据绑定教程](https://m.blog.csdn.net/m0_74473517/article/details/155727952) - CSDN

---

## 三、常用控件

### 3.1 Button - 按钮

```xml
<!-- 基础按钮 -->
<Button Content="点击我"
        Width="100" Height="30"
        Click="Button_Click"/>

<!-- 带图标的按钮 -->
<Button>
    <StackPanel Orientation="Horizontal">
        <Image Source="icon.png" Width="16" Height="16"/>
        <TextBlock Text="保存" Margin="5,0,0,0"/>
    </StackPanel>
</Button>

<!-- 绑定命令 -->
<Button Content="提交" Command="{Binding SubmitCommand}"/>
```

### 3.2 TextBox - 文本输入

```xml
<!-- 基础文本框 -->
<TextBox Width="200" Height="30"
         Text="{Binding UserName, UpdateSourceTrigger=PropertyChanged}"
         MaxLength="50"/>

<!-- 多行文本框 -->
<TextBox TextWrapping="Wrap" AcceptsReturn="True"
         VerticalScrollBarVisibility="Auto"
         Height="100"/>

<!-- 密码框 -->
<PasswordBox Password="{Binding Password}"/>
```

**绑定更新触发方式**：

| UpdateSourceTrigger | 说明 |
|---------------------|------|
| `LostFocus` | 失去焦点时更新（默认） |
| `PropertyChanged` | 每次输入都更新 |
| `Explicit` | 手动调用更新 |

### 3.3 DataGrid - 数据表格

```xml
<!-- 自动生成列 -->
<DataGrid ItemsSource="{Binding Users}"
          AutoGenerateColumns="True"/>

<!-- 自定义列 -->
<DataGrid ItemsSource="{Binding Users}"
          AutoGenerateColumns="False"
          IsReadOnly="True">
    <DataGrid.Columns>
        <DataGridTextColumn Header="姓名" Binding="{Binding Name}" Width="*"/>
        <DataGridTextColumn Header="年龄" Binding="{Binding Age}" Width="100"/>
        <DataGridTemplateColumn Header="操作" Width="100">
            <DataGridTemplateColumn.CellTemplate>
                <DataTemplate>
                    <Button Content="删除" Command="{Binding DeleteCommand}"/>
                </DataTemplate>
            </DataGridTemplateColumn.CellTemplate>
        </DataGridTemplateColumn>
    </DataGrid.Columns>
</DataGrid>
```

> [!info] 来源
> - [将 WPF 控件绑定到数据](https://learn.microsoft.com/zh-cn/visualstudio/data-tools/bind-wpf-controls-to-data-in-visual-studio) - Microsoft Learn

### 3.4 ComboBox - 下拉框

```xml
<!-- 绑定枚举/列表 -->
<ComboBox ItemsSource="{Binding Categories}"
          SelectedItem="{Binding SelectedCategory}"
          DisplayMemberPath="Name"/>

<!-- 手动添加选项 -->
<ComboBox SelectedIndex="0">
    <ComboBoxItem Content="选项1"/>
    <ComboBoxItem Content="选项2"/>
    <ComboBoxItem Content="选项3"/>
</ComboBox>
```

### 3.5 ListView / ListBox - 列表视图

```xml
<ListBox ItemsSource="{Binding Items}"
         SelectedItem="{Binding SelectedItem}"
         DisplayMemberPath="Name"/>

<!-- 带模板的 ListView -->
<ListView ItemsSource="{Binding Users}">
    <ListView.View>
        <GridView>
            <GridViewColumn Header="姓名" DisplayMemberBinding="{Binding Name}"/>
            <GridViewColumn Header="邮箱" DisplayMemberBinding="{Binding Email}"/>
        </GridView>
    </ListView.View>
</ListView>
```

---

## 四、数据绑定

### 4.1 Binding 基础

**数据绑定是 WPF 的核心功能**，将 UI 与数据自动同步。

```xml
<!-- 基础绑定 -->
<TextBox Text="{Binding UserName}"/>

<!-- 双向绑定 -->
<TextBox Text="{Binding UserName, Mode=TwoWay}"/>

<!-- 绑定模式 -->
<TextBlock Text="{Binding Title, Mode=OneTime}"/>      <!-- 只读取一次 -->
<TextBlock Text="{Binding Title, Mode=OneWay}"/>       <!-- 单向（源→目标） -->
<TextBox Text="{Binding Title, Mode=TwoWay}"/>         <!-- 双向 -->
<TextBox Text="{Binding Title, Mode=OneWayToSource}"/> <!-- 单向（目标→源） -->
```

### 4.2 DataContext

**DataContext 是绑定的数据源**，子元素会继承父元素的 DataContext。

```csharp
// 在代码中设置 DataContext
public MainWindow()
{
    InitializeComponent();
    this.DataContext = new MainViewModel();
}
```

```xml
<!-- 在 XAML 中设置 DataContext -->
<Window.DataContext>
    <local:MainViewModel/>
</Window.DataContext>
```

### 4.3 INotifyPropertyChanged

**实现属性变更通知**，让 UI 自动更新。

```csharp
public class ViewModelBase : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

public class MainViewModel : ViewModelBase
{
    private string _userName;
    public string UserName
    {
        get => _userName;
        set
        {
            if (_userName != value)
            {
                _userName = value;
                OnPropertyChanged(); // 通知 UI 更新
            }
        }
    }
}
```

> [!info] 来源
> - [数据绑定概述](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/) - Microsoft Learn

### 4.4 ObservableCollection

**动态集合**，添加/删除元素时自动通知 UI。

```csharp
public class MainViewModel : ViewModelBase
{
    public ObservableCollection<User> Users { get; set; }

    public MainViewModel()
    {
        Users = new ObservableCollection<User>();
    }

    public void AddUser(User user)
    {
        Users.Add(user); // UI 自动更新
    }
}
```

```xml
<DataGrid ItemsSource="{Binding Users}" AutoGenerateColumns="False">
    <DataGrid.Columns>
        <DataGridTextColumn Header="姓名" Binding="{Binding Name}"/>
    </DataGrid.Columns>
</DataGrid>
```

---

## 五、MVVM 模式

### 5.1 MVVM 架构

**MVVM** = Model-View-ViewModel

| 层 | 职责 |
|------|------|
| **Model** | 数据模型、业务逻辑 |
| **View** | UI 界面（XAML） |
| **ViewModel** | 连接 Model 和 View，处理 UI 逻辑 |

```
┌─────────────────────────────────────────────────────────────┐
│                      MVVM 架构                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    View (XAML)          ViewModel (C#)         Model (C#)  │
│    ┌─────────┐          ┌─────────┐          ┌─────────┐  │
│    │ Button  │ Command  │ICommand │          │  Data   │  │
│    │ TextBox │←────────→│Property │←────────→│  Logic  │  │
│    │ DataGrid│ Binding  │Method   │          │         │  │
│    └─────────┘          └─────────┘          └─────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 ICommand 命令

**使用命令替代事件**，实现 UI 与逻辑分离。

```csharp
// RelayCommand 实现
public class RelayCommand : ICommand
{
    private readonly Action<object> _execute;
    private readonly Func<object, bool> _canExecute;

    public event EventHandler CanExecuteChanged;

    public RelayCommand(Action<object> execute, Func<object, bool> canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public bool CanExecute(object parameter) => _canExecute?.Invoke(parameter) ?? true;

    public void Execute(object parameter) => _execute(parameter);

    public void RaiseCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}

// ViewModel 中使用
public class MainViewModel : ViewModelBase
{
    public ICommand SubmitCommand { get; }

    public MainViewModel()
    {
        SubmitCommand = new RelayCommand(Submit, CanSubmit);
    }

    private void Submit(object parameter)
    {
        // 提交逻辑
    }

    private bool CanSubmit(object parameter)
    {
        // 判断是否可执行
        return !string.IsNullOrEmpty(UserName);
    }
}
```

```xml
<!-- XAML 中绑定命令 -->
<Button Content="提交" Command="{Binding SubmitCommand}"/>
```

> [!info] 来源
> - [WPF MVVM 最佳实践](https://m.blog.csdn.net/gitblog_06739/article/details/148205135) - CSDN
> - [ICommand 接口实现](https://blog.csdn.net/qq_46062107/article/details/148244194) - CSDN

### 5.3 ViewModel 完整示例

```csharp
public class UserViewModel : ViewModelBase
{
    private string _name;
    private ObservableCollection<User> _users;

    public string Name
    {
        get => _name;
        set { _name = value; OnPropertyChanged(); }
    }

    public ObservableCollection<User> Users
    {
        get => _users;
        set { _users = value; OnPropertyChanged(); }
    }

    public ICommand AddUserCommand { get; }
    public ICommand DeleteUserCommand { get; }

    public UserViewModel()
    {
        Users = new ObservableCollection<User>();
        AddUserCommand = new RelayCommand(AddUser);
        DeleteUserCommand = new RelayCommand(DeleteUser);
    }

    private void AddUser(object parameter)
    {
        if (!string.IsNullOrWhiteSpace(Name))
        {
            Users.Add(new User { Name = Name });
            Name = string.Empty;
        }
    }

    private void DeleteUser(object parameter)
    {
        if (parameter is User user)
        {
            Users.Remove(user);
        }
    }
}
```

---

## 六、样式与模板

### 6.1 Style - 样式

**统一定义控件外观**。

```xml
<!-- 定义样式 -->
<Window.Resources>
    <Style x:Key="MyButtonStyle" TargetType="Button">
        <Setter Property="Background" Value="#0078D4"/>
        <Setter Property="Foreground" Value="White"/>
        <Setter Property="Padding" Value="10,5"/>
        <Setter Property="BorderThickness" Value="0"/>
        <Setter Property="Cursor" Value="Hand"/>
        <Style.Triggers>
            <Trigger Property="IsMouseOver" Value="True">
                <Setter Property="Background" Value="#106EBE"/>
            </Trigger>
        </Style.Triggers>
    </Style>
</Window.Resources>

<!-- 应用样式 -->
<Button Content="保存" Style="{StaticResource MyButtonStyle}"/>
```

### 6.2 DataTemplate - 数据模板

**定义数据如何显示**。

```xml
<Window.Resources>
    <DataTemplate x:Key="UserTemplate" DataType="{x:Type local:User}">
        <StackPanel Orientation="Horizontal">
            <Ellipse Width="30" Height="30" Fill="Blue"/>
            <TextBlock Text="{Binding Name}" Margin="10,0,0,0" VerticalAlignment="Center"/>
        </StackPanel>
    </DataTemplate>
</Window.Resources>

<!-- 使用数据模板 -->
<ListBox ItemsSource="{Binding Users}"
         ItemTemplate="{StaticResource UserTemplate}"/>
```

### 6.3 ControlTemplate - 控件模板

**完全自定义控件外观**。

```xml
<ControlTemplate x:Key="RoundButtonTemplate" TargetType="Button">
    <Border Background="{TemplateBinding Background}"
            CornerRadius="15"
            Padding="{TemplateBinding Padding}">
        <ContentPresenter HorizontalAlignment="Center"
                          VerticalAlignment="Center"/>
    </Border>
</ControlTemplate>

<!-- 使用控件模板 -->
<Button Content="圆角按钮"
        Template="{StaticResource RoundButtonTemplate}"
        Background="#0078D4" Foreground="White"/>
```

### 6.4 资源字典

**统一样式管理**，便于复用。

```xml
<!-- Themes/Generic.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Style x:Key="PrimaryButton" TargetType="Button">
        <Setter Property="Background" Value="#0078D4"/>
        <Setter Property="Foreground" Value="White"/>
    </Style>
</ResourceDictionary>

<!-- App.xaml 中引用 -->
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <ResourceDictionary Source="Themes/Generic.xaml"/>
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

> [!info] 来源
> - [样式和模板示例](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/controls/) - Microsoft Learn

---

## 七、常见问题

### Q1：数据绑定不更新？

**检查清单**：
1. 属性是否实现了 `INotifyPropertyChanged`？
2. 集合是否使用了 `ObservableCollection`？
3. Binding Mode 是否正确？
4. DataContext 是否设置？

### Q2：如何调试绑定？

```xml
<!-- 使用 PresentationTraceSources -->
xmlns:diagnostics="clr-namespace:System.Diagnostics;assembly=WindowsBase"

<TextBlock Text="{Binding Name, diagnostics:PresentationTraceSources.TraceLevel=High}"/>
```

### Q3：如何跨线程更新 UI？

```csharp
// 使用 Dispatcher
Application.Current.Dispatcher.Invoke(() =>
{
    // 更新 UI 的代码
    Users.Add(newUser);
});
```

### Q4：如何在 ViewModel 中关闭窗口？

```csharp
// 方法1：使用接口
public interface ICloseable
{
    void Close();
}

// 方法2：使用 Attached Property
public static class WindowHelper
{
    public static readonly DependencyProperty DialogResultProperty =
        DependencyProperty.RegisterAttached("DialogResult", typeof(bool?),
            typeof(WindowHelper), new PropertyMetadata(null, OnDialogResultChanged));

    private static void OnDialogResultChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is Window window)
        {
            window.DialogResult = e.NewValue as bool?;
            window.Close();
        }
    }
}
```

### Q5：MVVM 框架推荐？

| 框架 | 特点 |
|------|------|
| **CommunityToolkit.Mvvm** | 微软官方，轻量 |
| **Prism** | 企业级，功能全面 |
| **MVVM Light** | 经典，社区活跃 |
| **ReactiveUI** | 响应式编程 |

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **MVVM 是核心**：理解 MVVM 模式是掌握 WPF 的关键
>
> 2. **数据绑定技巧**：
>    - 使用 `UpdateSourceTrigger=PropertyChanged` 实现实时更新
>    - 集合用 `ObservableCollection`
>    - 属性必须调用 `OnPropertyChanged`
>
> 3. **踩坑记录**：
>    - 忘记实现 INotifyPropertyChanged 导致绑定不更新
>    - 跨线程操作 UI 会报错
>    - DataContext 设置错误导致绑定失效
>
> 4. **最佳实践**：
>    - 使用 CommunityToolkit.Mvvm 简化代码
>    - 样式统一放在资源字典
>    - 复杂控件使用 DataTemplate

---

## 相关文档

- [[../../AI学习/00-索引/MOC]] - 知识库索引

---

## 参考资料

### 官方资源
- [WPF 官方文档](https://learn.microsoft.com/dotnet/desktop/wpf/overview/) - Microsoft Learn
- [WPF 数据绑定](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/data/) - Microsoft Learn
- [WPF 控件文档](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/controls/) - Microsoft Learn
- [将 WPF 控件绑定到数据](https://learn.microsoft.com/zh-cn/visualstudio/data-tools/bind-wpf-controls-to-data-in-visual-studio) - Visual Studio

### 社区资源
- [WPF MVVM 最佳实践](https://m.blog.csdn.net/gitblog_06739/article/details/148205135) - CSDN
- [WPF控件用法及数据绑定教程](https://m.blog.csdn.net/m0_74473517/article/details/155727952) - CSDN
- [ICommand 接口实现详解](https://blog.csdn.net/qq_46062107/article/details/148244194) - CSDN
- [WPF Prism 框架实践](https://blog.csdn.net/gitblog_06728/article/details/148183195) - CSDN

### 第三方文档
- [CommunityToolkit.Mvvm GitHub](https://github.com/CommunityToolkit/dotnet) - 微软官方 MVVM 工具包
- [Prism GitHub](https://github.com/PrismLibrary/Prism) - Prism 框架

---

**最后更新**：2026-03-04
