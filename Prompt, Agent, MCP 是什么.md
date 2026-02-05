
# Prompt（提示词）

在Openai刚刚发布gpt(ai刚兴起的时候)，这个时候的ai就像一个聊天框，我们通过聊天框给AI模型发布消息，AI模型会自动生成一个回复给我们。这里我们给AI模型发布的信息就是用户提示词（user
prompt）。

!![](assets/Prompt,%20Agent,%20MCP%20是什么/file-20260205122434067.png)

但是这样的聊天，AI模型只能给出一个通用的回答，当我们如果想要AI加上人设，我们可以这样发消息，比如：你是我的女朋友，我的肚子痛。这样的话AI就可以根据如果我是你的女朋友我会如何回答的人角度回复消息，这样就做到了不同人设做出不同回答。但是这种要指明信息的格式不方便，于是把人设等不方便直接写出来的信息制作成一种提示词system
prompt(系统提示词)。
就这样我们只要预先设置好系统提示词后，之后我们在发布消息（user
prompt）时会自动把系统提示词也发给AI模型

!![](assets/Prompt,%20Agent,%20MCP%20是什么/file-20260205122444835.png)

# Agent

按照上面的模型，AI模型可以根据不同的人设作出不同的回答，但是我们不想只把AI模型当成一个聊天的东西，我们想让他能够实现一个功能。因此就出现了Agent
tools（一些函数，他们会把自己的函数功能和描述注册到Agent）,agent会根据Agent
tools发过来的信息生成一个system
prompt（其中包括了用户给大模型那些工具，那些工具是干什么的，AI大模型要使用他们应该返回什么格式）。然后agent会把system
prompt和user
prompt一起发送给AI大模型。AI模型就会根据要求返回一个调用某个函数的消息
，然后agent就会把这个请求发给需要调用的函数，函数执行完后就会返回一个格式给agent，agent把这个内容给AI大模型，然后AI大模型会根据这个内容生成内容后再执行下一步（如果不是最终的信息就会重复上面的操作），最后就是AI大模型把最终信息发给agent，再由agent把内容呈现给用户

![](assets/Prompt,%20Agent,%20MCP%20是什么/file-20260205122453248.png)
# Function calling

上面这个是通过自然语言（就是大白话）给AI模型说明白了该用什么格式返回，但AI是一个概率模型（不一定会要求返回信息）因此可能这步会执行多次。为了解决这种问题就出现了Function
calling（就是实现了统一格式，实现规范描述）。比如之前我们使用自然语言进行描述的，我们就把每个TOOL都用一个json对象来进行描述。然后也规定了AI使用工具是应该返回的格式。这用system
prompt就被function calling代替了。

!![](assets/Prompt,%20Agent,%20MCP%20是什么/file-20260205122501551.png)

但这由于不同大模型大厂的function
calling不同导致没有统一个格式（每家大厂的API都不一样），因此现在还是system
prompt和funciton calling这两种方式并用。

# MCP

但是上面的只是agent和AI大模型之间调用的方式不同。但我们如果用agent去调用agent
tools则统一了格式就是用mcp。于是agent tools就变成了mcp
server，而agent就变成了mcp client。Mcp规定了mcp server如何和mcp
client通讯和mcp server应该提供哪些接口（比如用来查询MCP
Server中有那些tool,tool的功能，要的参数等）。

# 总结

!![](assets/Prompt,%20Agent,%20MCP%20是什么/file-20260205122509266.png)

用户给agent用户提示词user prompt，同时agent（MCP Client）会与MCP
Server进行连接从mcp
server中获得所有TOOL的信息，Agent会把这些信息转化成system
prompt或者function calling和user
prompt一起打包给AI大模型，这是AI大模型发现用用到一个TOOL，于是通过普通回复或者function
calling的格式给Agent,Agent（MCP Client）通过这个请求去TOOL(MCP
Server)中找到相应的TOOL去调用函数并返还结果格agent，agent把消息给到AI大模型生成内容再返还给agent，最后有agent把内容给到用户。

# 如何写agent代码

先写好你的工具函数，最好是单独用一个文件去写。

然后配置你的大语言模型，python中用pydantic_ai这个库去配置的，然后要获得你这个大模型的API才行，但直接放在代码中不安全，我们一般是放在.env文件中，然后用dotenv中的load_dotenv把你部署的环境放入你的环境变量中

!![](assets/Prompt,%20Agent,%20MCP%20是什么/file-20260205122520132.png)

Agent就配置好了agent对象，这里可以填的参数一般是模型，系统提示词或者function
calling，你的工具函数

这里的主程序是先获得用户的输入，然后用agent.run_sync去运行最后返还结果

!![](assets/Prompt,%20Agent,%20MCP%20是什么/file-20260205122526685.png)

我们如果想让它记住之前的内容，就用一个变量保存resp.all_messages()，然后当成参数给到agent.run_sync中当成一个参数。
