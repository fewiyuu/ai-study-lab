from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def h(text: str) -> str:
    return html.escape(text, quote=True)


def slug_name(no: int, title: str) -> str:
    safe = re.sub(r'[\\/:*?"<>|]', "", title)
    safe = safe.replace(" ", "")
    return f"{no:02d}_{safe}"


COMMON_MISCONCEPTIONS = [
    ("把训练循环当成背诵模板", "模板能跑不等于能诊断。每一行都要知道它读什么、写什么、改变哪个状态。", "把每行标成前向、loss、清梯度、反向或更新。"),
    ("只看 loss 下降", "loss 下降只能说明优化目标变小，还要检查数据、标签、输出形状和评估指标是否对应任务。", "同时检查验证集指标和预测样例。"),
    ("混用训练和评估状态", "`model.train()` 和 `model.eval()` 会影响 Dropout、BatchNorm 等层，评估时还要配合 `torch.no_grad()`。", "训练和评估写成两个清楚的函数。"),
]


LESSONS = [
    {
        "no": 1,
        "title": "课程概览与深度学习实践路线",
        "source": "P1【1. Overview】",
        "goal": "看懂这门课的学习路线，知道深度学习实践不是从公式开始，而是围绕数据、模型、损失、优化和评估形成可执行流程。",
        "focus": "把课程全景、工具版本、学习方法和开发闭环放在一张图里。",
        "sections": [
            {
                "title": "这门课到底要训练什么能力",
                "paras": [
                    "这门课的目标不是把深度学习的所有数学推导讲完，而是让你能把一个神经网络任务做出来。做出来并不只是复制代码运行。它包括读懂数据从哪里来、模型如何把输入变成输出、损失函数在衡量什么、优化器改动了哪些参数，以及结果为什么可信或不可信。",
                    "课程开头反复强调“实践课”，这句话很重要。实践不是降低难度，而是把难度放到工程链路上：遇到一个任务时，你要能把它拆成数据集、模型、损失、优化、训练、测试这些部分。只会背一个 API 名字，到了换数据、换任务、换模型时就会断。",
                    "所以第一讲最值得带走的不是某个具体函数，而是学习姿势。以后看到一段 PyTorch 代码，先不要急着问这一层有多高级，先问它在四步流程里的位置：准备数据、设计模型、构造损失与优化器、训练和评估。你现在应该能判断一段深度学习代码大致属于哪一环。"
                ],
            },
            {
                "title": "版本变化与稳定概念",
                "paras": [
                    "视频使用的是较早期的 PyTorch 写法。今天再学时，不需要拘泥于旧版本的细节，但要抓住稳定概念。`Tensor`、自动求导、`nn.Module`、优化器、数据加载器这些东西到现在仍然是核心。API 的细节会变，训练链路没变。",
                    "工具版本的正确态度是：学习基础概念时可以看旧课，写新代码时查当前官方文档。比如早期课程可能用 `.data` 取值或手动处理变量，现在更常见的是 `loss.item()`、`with torch.no_grad()` 和清晰的 `model.train()` / `model.eval()` 切换。",
                    "成熟技术和热门工具的节奏不同。学校课程常讲稳定底层，因为它们迁移性更强；企业项目会追新工具，因为它们服务当前效率。学习时不要把“新”误当成“必须先学”，也不要把“旧课”误当成“没有价值”。你现在应该能区分 API 版本细节和长期稳定的训练思想。"
                ],
            },
            {
                "title": "深度学习任务的五个固定部件",
                "paras": [
                    "一个最小深度学习任务通常有五个部件。数据给出输入和标签，模型把输入映射成预测，损失函数把预测和标签比较成一个标量，优化器根据梯度修改参数，评估逻辑检查模型在未见数据上的表现。",
                    "这五个部件之间有方向。数据进入模型，模型输出预测，预测和标签进入损失函数，损失通过反向传播产生梯度，优化器读取梯度并更新参数。任何一步形状不对、含义不对或顺序不对，训练都会变得不可解释。",
                    "你以后读代码时可以按这条链路画箭头。不要先陷进每个类的参数表里，而要先看对象之间怎么连接。你现在应该能用一句话讲清“深度学习代码为什么不是一堆互不相关的 API 调用”。"
                ],
            },
            {
                "title": "为什么先从线性模型开始",
                "paras": [
                    "线性模型简单，是因为它的预测形式容易看见：输入乘权重，再加偏置。正因为简单，它适合作为训练流程的显微镜。你可以清楚看到预测、误差、梯度和参数更新之间的关系。",
                    "后面的逻辑斯蒂回归、多分类、CNN、RNN 都不会推翻这个流程。它们只是换了模型结构、输出含义、损失函数和数据形状。先学线性模型，是为了把训练循环这个骨架固定住。",
                    "如果一上来就写复杂网络，你可能看到很多层，却不知道哪一步出了问题。线性模型把噪声降到最低，让你先学会判断：模型有没有参数，loss 是否是标量，梯度有没有清零，优化器有没有更新。你现在应该能说明为什么“简单模型”不是过时内容。"
                ],
            },
            {
                "title": "读代码要读数据流，不只读语法",
                "paras": [
                    "深度学习代码有大量固定词：`forward`、`backward`、`loss`、`optimizer`、`DataLoader`。只认识这些词不够。关键是知道每一行输入什么、输出什么、改变什么状态。",
                    "例如 `loss.backward()` 不是“求一下 loss”，它会沿着计算图把梯度写到参与计算的参数上。`optimizer.step()` 不是“再算一次”，它会读取参数上的 `.grad` 并修改参数值。`optimizer.zero_grad()` 也不是可有可无，它是在下一次反向传播前清掉旧梯度。",
                    "读代码时把状态变化标出来：哪些对象只是新建，哪些对象被写入，哪些对象被原地修改。你现在应该能从“代码能跑”往前走一步，开始问“这行代码改变了什么”。"
                ],
            },
            {
                "title": "从课程路线看后续依赖",
                "paras": [
                    "这套课大致沿着“从手写训练到框架化训练，再到不同数据结构的网络”推进。前几讲建立线性模型、梯度下降、反向传播和 PyTorch 训练范式；中段把任务扩展到二分类、多维特征、数据加载和多分类；后段进入 CNN 和 RNN。",
                    "依赖关系很直接。没有线性模型，就很难理解 `nn.Linear`；没有梯度下降，就很难理解优化器；没有反向传播，就无法判断 `backward()` 做了什么；没有数据加载，就很难处理真实数据集；没有多分类，就很难理解 MNIST、CNN 和名字分类。",
                    "你学习时可以把每讲当成一个功能部件，而不是孤立视频。学完一讲要问：它给训练链路新增了什么能力？你现在应该能把 13 讲放在一条逐步扩展的路线里。"
                ],
            },
        ],
        "terms": [
            ("实践课", "以能搭建、训练、诊断模型为目标的学习方式，不等于只会运行代码。", "误以为实践课不用理解原理。"),
            ("训练链路", "数据、模型、损失、梯度、优化、评估之间的执行关系。", "只记 API，不看对象之间的数据流。"),
            ("稳定概念", "跨版本长期存在的思想和对象，例如 Tensor、Module、autograd。", "把旧版本写法和稳定概念混在一起。"),
            ("迁移能力", "把一个任务中的流程迁移到新任务的能力。", "只会在原代码里改数字。"),
        ],
        "code_examples": [
            {
                "label": "最小训练链路：先看对象关系",
                "code": """# 这不是完整项目，只用来读清训练链路
for x, y in loader:
    pred = model(x)          # 数据进入模型，得到预测
    loss = criterion(pred, y) # 预测和标签比较成标量
    optimizer.zero_grad()    # 清掉上一轮梯度
    loss.backward()          # 把梯度写到参数上
    optimizer.step()         # 根据梯度更新参数""",
            },
            {
                "label": "现代 PyTorch 常见评估写法",
                "code": """model.eval()
correct = 0
with torch.no_grad():
    for x, y in test_loader:
        logits = model(x)
        pred = logits.argmax(dim=1)
        correct += (pred == y).sum().item()""",
            },
        ],
        "misconceptions": [
            ("把旧课等同于旧知识", "旧课中的部分 API 习惯可能过时，但训练链路和核心对象仍然有价值。", "写代码时查新文档，理解概念时抓稳定结构。"),
            ("以为实践就是少学数学", "实践课仍然要理解预测、损失、梯度和优化，只是先从可执行链路进入。", "每学一个 API 都问它在训练链路里负责什么。"),
            ("认为深度学习只是在堆网络层", "网络层只是模型部分，数据、损失、优化和评估同样决定结果。", "读项目时先画五个部件，再看网络细节。"),
            ("忽略评估阶段", "训练 loss 下降不代表泛化好，也不代表推理写法正确。", "评估时切 `eval()`，关梯度，并使用任务对应指标。"),
            ("只会照抄完整代码", "照抄无法处理形状变化、任务变化和报错。", "把代码拆成数据流和状态变化来读。"),
        ],
        "confusions": [
            ("课程版本", "视频中的代码环境", "不是今天必须照抄的安装版本"),
            ("核心概念", "训练流程中长期稳定的对象和关系", "不是某一版 API 的拼写细节"),
            ("实践能力", "能搭建并诊断任务", "不是只会点运行"),
        ],
        "questions": [
            ("基础概念", "选择", "这门课的主要目标更接近哪一项？", ["掌握开发深度神经网络的基本流程", "背完所有优化理论证明", "只了解 AI 新闻"], "选出最贴近实践课目标的一项。"),
            ("基础概念", "判断", "PyTorch 旧版本课程完全没有学习价值。", None, "从稳定概念和 API 细节的区别判断。"),
            ("基础概念", "填空", "一个训练任务通常包含数据、模型、损失函数、______ 和评估。", None, "填训练中负责更新参数的部件。"),
            ("链路理解", "排序", "把训练循环中的动作排序：计算 loss / 清梯度 / 前向预测 / 反向传播 / 更新参数。", None, "按一次 mini-batch 的正常顺序写。"),
            ("链路理解", "匹配", "把 `loss.backward()`、`optimizer.step()`、`model.eval()` 分别匹配到它们改变或影响的对象。", None, "从梯度、参数、层状态三个角度答。"),
            ("代码阅读", "短答", "解释 `pred = model(x)` 在训练链路中的位置。", None, "说清输入、输出和后续会进入哪里。"),
            ("代码阅读", "短答", "为什么评估时常配合 `with torch.no_grad()`？", None, "从是否需要梯度、内存和计算图回答。"),
            ("错误诊断", "诊断", "有人说“我能跑通一份 CNN 代码，所以已经掌握深度学习实践”。这句话哪里不稳？", None, "从迁移和诊断能力回答。"),
            ("错误诊断", "诊断", "训练 loss 下降，但测试集很差。至少提出两个排查方向。", None, "别只说调参，先看数据、评估模式和过拟合。"),
            ("版本判断", "短答", "看旧课程时，哪些内容应该查当前官方文档再写？", None, "举 2-3 类 API 或写法。"),
            ("迁移应用", "场景", "如果把回归任务换成分类任务，训练链路中哪些部件最可能要换？", None, "从模型输出、损失函数和指标回答。"),
            ("迁移应用", "场景", "你拿到一个陌生 PyTorch 项目，第一轮阅读会先找哪五类代码？", None, "按课程主线列。"),
            ("概念区分", "短答", "“模型结构”和“训练策略”有什么区别？", None, "可以用网络层和优化器作例子。"),
            ("概念区分", "判断", "只要模型结构足够复杂，数据加载和评估写错也没关系。", None, "判断并说明后果。"),
            ("面试追问", "短答", "为什么深度学习课程常从线性模型开始？", None, "用 2-3 句话回答。"),
            ("面试追问", "短答", "你如何解释 `forward → loss → backward → step` 这条主线？", None, "不要只翻译英文。"),
            ("检查清单", "清单", "写出你以后读 PyTorch 训练代码时的 5 项检查清单。", None, "每项要能落到代码位置。"),
            ("开放复盘", "短答", "这节课最容易被忽略但很重要的学习习惯是什么？", None, "写你自己的判断。"),
            ("费曼解释", "费曼", "用 6-9 句话向初学者解释：为什么学 PyTorch 要先抓训练链路，而不是先背 API。", None, "串联数据、模型、损失、梯度、优化、评估和版本变化。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写成可执行动作，不写空泛感受。"),
        ],
    },
]


def lesson(
    no: int,
    title: str,
    source: str,
    goal: str,
    focus: str,
    sections: list[tuple[str, list[str]]],
    terms: list[tuple[str, str, str]],
    code_examples: list[tuple[str, str]],
    misconceptions: list[tuple[str, str, str]],
    confusions: list[tuple[str, str, str]],
    questions: list[tuple[str, str, str, list[str] | None, str]],
) -> dict:
    return {
        "no": no,
        "title": title,
        "source": source,
        "goal": goal,
        "focus": focus,
        "sections": [{"title": a, "paras": b} for a, b in sections],
        "terms": terms,
        "code_examples": [{"label": a, "code": b} for a, b in code_examples],
        "misconceptions": misconceptions,
        "confusions": confusions,
        "questions": questions,
    }


LESSONS.extend([
    lesson(
        2,
        "线性模型：从假设函数到损失曲面",
        "P2【2.线性模型】",
        "理解线性模型如何用参数表达预测，为什么要用损失函数衡量好坏，以及穷举搜索和训练优化之间的区别。",
        "把 `y = wx + b`、MSE、参数搜索、预测误差和可视化损失曲面连成一条线。",
        [
            ("线性模型先解决预测形式问题", [
                "线性模型先回答一个朴素问题：如果输入是 `x`，模型准备怎样给出预测 `y_hat`？最简单的回答是 `y_hat = x * w`，或者带偏置的 `y_hat = x * w + b`。这里的 `w` 和 `b` 不是普通常数，而是要从数据里学出来的参数。",
                "这节课里的数据很小，例如输入 1、2、3，对应输出 2、4、6。你可以一眼看出 `w=2` 很合适，但训练程序不能靠人眼猜。程序需要一个统一办法判断某个 `w` 好不好，然后在很多可能的 `w` 里挑更好的。",
                "所以线性模型的第一层意义是“提出假设函数”。你现在应该能看到一组数据后，写出一个最小模型形式，并指出哪些量是输入、哪些量是参数、哪些量是预测。"
            ]),
            ("损失函数把好坏变成一个数", [
                "模型给出预测后，还要知道预测错了多少。均方误差 MSE 的做法是：每个样本计算预测值和真实值的差，平方后再平均。平方有两个作用：正负误差不会互相抵消，大误差会被惩罚得更明显。",
                "损失函数必须返回一个标量，也就是一个单独的数。因为优化器要比较“这个参数更好还是那个参数更好”，如果损失是一串向量，方向就不清楚。标量损失让训练目标变成“让这个数尽量小”。",
                "不要把损失函数理解成准确率。回归任务里，预测 5.8 和真实 6.0 很接近，但没有“对/错”这种离散判断。MSE 更适合表达连续误差。你现在应该能解释为什么训练需要损失函数，而不是只看几个预测样例。"
            ]),
            ("穷举搜索能说明目标，但不是训练方法", [
                "课程里会用穷举法试不同的 `w`，然后画出每个 `w` 对应的 loss。这个做法适合教学，因为它把“参数不同，损失也不同”展示得很直观。你能看到某个位置 loss 最小，这个位置就是更合适的参数。",
                "但真实模型不会靠穷举搜索。一个线性模型如果只有一个 `w`，还勉强能试；如果有百万级参数，穷举空间会爆炸。穷举法的价值是帮你看见损失曲面，不是让你以后这么训练神经网络。",
                "更实际的训练方法是利用梯度告诉参数应该往哪个方向移动。第二讲先让你知道“有一个损失地形”，第三讲再讲“怎么沿着地形往低处走”。你现在应该能区分教学用的参数扫描和真正的优化算法。"
            ]),
            ("偏置项让模型不必穿过原点", [
                "只有 `y = wx` 的模型被限制为穿过原点。如果数据的规律是 `y = 2x + 1`，没有偏置项的模型无论怎么改 `w` 都会别扭。偏置 `b` 给模型增加了整体平移能力。",
                "带偏置后，损失不再只和一个参数有关，而是和 `w`、`b` 两个参数有关。你可以把它想成一个二维平面上的地形：每个坐标 `(w, b)` 都有一个 loss 高度。训练的目标是找到低谷。",
                "这件事也解释了为什么模型参数越多，搜索越困难。多一个参数，就多一个方向；深度网络的参数空间更高维。你现在应该能判断什么时候线性模型需要 bias，以及 bias 错漏会造成什么限制。"
            ]),
            ("训练样本、模型容量和泛化", [
                "在小样本例子里，一个正确的线性关系很容易被看出来。真实项目中，数据有噪声，样本不一定完全落在一条线上。模型不是记住每个样本，而是学一个能解释多数样本的规律。",
                "线性模型容量低，表达能力有限。它的好处是简单、可解释、很难无端变复杂；坏处是遇到非线性关系时可能欠拟合。欠拟合是指模型太简单，训练集都解释不好。过拟合则相反，模型太贴训练数据，在新数据上表现差。",
                "线性模型是理解泛化的起点。你现在应该能用训练误差和测试误差区分“模型太简单”和“模型太会记”。"
            ]),
            ("从线性模型过渡到神经网络", [
                "神经网络不是突然冒出来的黑盒。最基础的神经元就像一个线性模型再接一个激活函数。线性层负责加权求和，激活函数负责引入非线性，多层堆起来才有更强表达能力。",
                "这节课暂时不急着堆层，而是先把预测、损失和参数这三件事钉牢。后面用 PyTorch 写 `nn.Linear(1, 1)` 时，它做的仍然是线性变换，只是框架帮你管理参数和计算图。",
                "你现在应该能从 `y_hat = wx + b` 过渡到 `nn.Linear`，知道它不是魔法，而是可学习的权重矩阵和偏置。"
            ]),
        ],
        [
            ("假设函数", "模型对输入和输出关系的表达式，例如 `y_hat = wx + b`。", "误以为它是已经正确的规律。"),
            ("参数", "训练中要被学习和更新的量，如 `w`、`b`。", "把输入 `x` 和参数混为一谈。"),
            ("MSE", "预测误差平方后的平均值，常用于回归。", "把它当成分类准确率。"),
            ("损失曲面", "不同参数组合对应不同 loss 的地形。", "以为只适用于二维图，忘了高维模型也有类似目标面。"),
        ],
        [
            ("从一个权重读懂线性预测", """x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]

def forward(x, w):
    return x * w

for w in [1.0, 2.0, 3.0]:
    preds = [forward(x, w) for x in x_data]
    print(w, preds)"""),
            ("MSE 把一组预测压成一个训练目标", """def mse_loss(xs, ys, w):
    total = 0.0
    for x, y in zip(xs, ys):
        y_hat = x * w
        total += (y_hat - y) ** 2
    return total / len(xs)"""),
            ("带偏置的模型多一个可学习方向", """def forward_with_bias(x, w, b):
    return x * w + b

# w 控制斜率，b 控制整体上下平移
y_hat = forward_with_bias(x=3.0, w=2.0, b=1.0)"""),
        ],
        [
            ("认为 `w=2` 是人眼看出来就够了", "训练程序需要通用评价标准，不能依赖人眼观察。", "用损失函数评价每个参数。"),
            ("把 MSE 当成分类指标", "MSE 衡量连续误差，不回答类别是否选对。", "回归用 MSE，分类通常用交叉熵和准确率等指标。"),
            ("以为穷举搜索就是深度学习训练", "参数维度高时穷举不可行。", "用梯度下降沿着损失下降方向更新。"),
            ("漏掉偏置项", "模型被迫穿过原点，表达能力受限。", "根据数据关系判断是否需要 `b`。"),
            ("只看训练样本上的 loss", "训练集小或噪声低时容易误判泛化能力。", "保留测试集或验证集评估新数据表现。"),
        ],
        [
            ("输入", "已知样本特征", "不是训练要改的参数"),
            ("参数", "模型要学习的权重和偏置", "不是标签"),
            ("损失", "衡量当前参数好坏的标量", "不是模型预测本身"),
        ],
        [
            ("基础概念", "选择", "在线性模型 `y_hat = wx + b` 中，训练要学习的量通常是哪些？", ["w 和 b", "x 和 y", "样本数量"], "区分输入、标签和参数。"),
            ("基础概念", "判断", "MSE 越小，说明当前参数在训练数据上的预测越接近标签。", None, "只针对训练数据上的损失判断。"),
            ("基础概念", "填空", "只有 `y=wx` 的模型会被限制为必须经过 ______。", None, "想一想 x=0 时 y 是多少。"),
            ("损失理解", "短答", "为什么损失函数通常要返回一个标量？", None, "从优化目标是否明确回答。"),
            ("损失理解", "计算", "若真实值为 4，预测值为 5，单样本平方误差是多少？", None, "写出差值和平方。"),
            ("代码阅读", "短答", "在 `total += (y_hat - y) ** 2` 中，`y_hat` 和 `y` 分别代表什么？", None, "说明预测和标签。"),
            ("代码阅读", "短答", "如果把 `(y_hat - y) ** 2` 改成 `y_hat - y`，会有什么问题？", None, "考虑正负误差抵消。"),
            ("概念区分", "匹配", "匹配：`x` / `w` / `loss` 分别属于输入、参数、评价目标中的哪一类。", None, "按训练中是否会被更新判断。"),
            ("概念区分", "短答", "穷举参数搜索和梯度下降的核心区别是什么？", None, "从是否尝试所有参数回答。"),
            ("错误诊断", "诊断", "有人只用训练集 loss 评价模型好坏，这可能漏掉什么问题？", None, "说出泛化或过拟合。"),
            ("错误诊断", "诊断", "数据规律是 `y=2x+1`，模型却写成 `y=wx`。后果是什么？", None, "从偏置缺失回答。"),
            ("场景应用", "场景", "房价预测更适合用回归损失还是分类准确率？为什么？", None, "说明输出是连续值。"),
            ("场景应用", "场景", "如果数据明显不是直线关系，线性模型可能出现什么现象？", None, "用欠拟合解释。"),
            ("可视化理解", "短答", "损失曲面上的低谷表示什么？", None, "对应参数和 loss 的关系。"),
            ("面试追问", "短答", "为什么线性模型适合作为深度学习入门模型？", None, "从训练流程可见性回答。"),
            ("面试追问", "短答", "`nn.Linear` 和 `y=wx+b` 有什么关系？", None, "联系权重矩阵和偏置。"),
            ("检查清单", "清单", "拿到一个回归问题时，设计最小线性模型前先检查哪 4 件事？", None, "覆盖输入、标签、损失、评估。"),
            ("迁移应用", "短答", "为什么模型参数更多时，穷举搜索会迅速不可行？", None, "从组合空间回答。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：线性模型如何通过损失函数判断参数好坏。", None, "串联假设函数、预测、标签、MSE、参数搜索和泛化。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个能动手完成的动作。"),
        ],
    ),
    lesson(
        3,
        "梯度下降：沿着损失下降的方向更新参数",
        "P3【03.梯度下降算法】",
        "理解梯度为什么能指示参数更新方向，能手写一维线性回归的梯度更新，并识别学习率、局部最优和随机梯度的常见问题。",
        "把导数、学习率、批量梯度、随机梯度和参数更新公式讲清楚。",
        [
            ("梯度下降先解决“往哪改参数”", [
                "第二讲用穷举搜索看到了不同参数对应不同损失。第三讲要解决的问题是：不把所有参数都试一遍，怎样知道参数应该往哪里动？梯度就是答案。它告诉你在当前位置，损失对参数变化有多敏感，以及往哪个方向会变大。",
                "对一个参数 `w` 来说，如果当前梯度是正的，说明 `w` 增大时 loss 倾向于增大，那就应该让 `w` 往小的方向走；如果梯度是负的，说明 `w` 增大时 loss 倾向于减小，那就应该让 `w` 往大的方向走。",
                "更新公式 `w = w - learning_rate * grad` 的减号来自这里。它不是随便写的，而是沿着让损失下降的方向移动。你现在应该能解释为什么不是 `w = w + lr * grad`。"
            ]),
            ("学习率决定每一步走多远", [
                "学习率 `learning_rate` 控制参数更新步长。梯度告诉方向和坡度，学习率决定你每次迈多大步。学习率太小，训练会很慢；学习率太大，参数可能跨过低谷，在两边来回震荡，甚至让 loss 变得越来越大。",
                "初学时容易把学习率当成随便设的数字。更准确地说，它是一个训练稳定性参数。它和数据尺度、损失曲面、模型结构都有关系。同样的模型，输入特征尺度不同，合适学习率也可能不同。",
                "如果训练 loss 上下乱跳，第一反应不该是立刻换复杂模型，而是检查学习率、数据归一化和梯度是否异常。你现在应该能根据 loss 曲线初步判断学习率可能太大还是太小。"
            ]),
            ("批量梯度用所有样本估计方向", [
                "批量梯度下降会把所有训练样本的损失都算进去，再求平均梯度。这样得到的方向比较稳定，因为它综合了全部样本的信息。缺点也明显：数据很大时，每更新一步都要看完全部数据，成本高。",
                "在线性回归例子里，MSE 对 `w` 的梯度可以手算。每个样本贡献一部分误差方向，平均后得到整体方向。这个平均很重要，因为单个样本可能带噪声，全部样本更能代表整体目标。",
                "你现在应该能读懂一个手写梯度函数：循环样本、计算预测、计算误差、累加导数、除以样本数。"
            ]),
            ("随机梯度和 mini-batch 是效率折中", [
                "随机梯度下降 SGD 最极端的做法是每次只用一个样本估计梯度。它便宜、更新快，但方向噪声更大。mini-batch 则每次用一小批样本，通常是深度学习训练里的常用折中。",
                "SGD 的“随机”不是训练随便乱来，而是用样本子集估计总体梯度。噪声有时反而有好处，它可能帮助参数跳出一些不好的局部区域。但噪声太大也会让收敛不稳定。",
                "你现在应该能区分 batch gradient descent、stochastic gradient descent 和 mini-batch gradient descent，并知道它们主要差在每次更新看多少样本。"
            ]),
            ("局部最优、鞍点和非凸问题", [
                "简单线性回归的损失通常比较规整，容易找到全局最小。深度网络的损失曲面更复杂，可能有局部最优、平坦区域和鞍点。局部最优是附近最低但不一定全局最低；鞍点是某些方向像低谷、另一些方向像山坡。",
                "这并不意味着深度学习不能训练。实际中，初始化、mini-batch 噪声、优化器和网络结构都会影响路径。课程早期先讲最基础梯度下降，是为了让你看清核心机制，再逐步接受复杂情况。",
                "你现在应该能说明：梯度下降不是保证一步到位的精确搜索，而是一种利用局部斜率逐步改参数的方法。"
            ]),
            ("手写梯度的价值在于诊断", [
                "后面 PyTorch 会自动帮你求梯度。既然有自动求导，为什么还要手写一遍？因为手写梯度能让你知道 `.backward()` 背后在算什么。你不需要永远手推复杂网络，但要知道梯度不是凭空出现的。",
                "很多训练 bug 都和梯度有关：loss 不是标量、参数没有参与计算图、梯度没有清零、学习率过大、输入尺度异常。懂手写梯度后，看到 `.grad` 为 None 或 loss 不动时，你更容易定位问题。",
                "你现在应该能用线性回归的手写更新解释 PyTorch 中 `backward()` 和 `optimizer.step()` 的意义。"
            ]),
        ],
        [
            ("梯度", "损失函数对参数的导数，表示当前位置损失变化最快的方向。", "把梯度当成 loss 本身。"),
            ("学习率", "每次参数沿梯度方向移动的步长系数。", "设得越大越快越好。"),
            ("批量梯度下降", "每次用全部样本计算梯度再更新。", "以为 batch 一定指 mini-batch。"),
            ("随机梯度下降", "每次用一个或少量样本估计梯度。", "以为随机就是没有目标。"),
        ],
        [
            ("手写一维线性回归梯度", """def grad(xs, ys, w):
    total = 0.0
    for x, y in zip(xs, ys):
        y_hat = x * w
        total += 2 * x * (y_hat - y)
    return total / len(xs)

w = 1.0
lr = 0.01
for epoch in range(20):
    w -= lr * grad([1, 2, 3], [2, 4, 6], w)"""),
            ("学习率过大时的典型信号", """# 如果 loss 在训练中越来越大或剧烈震荡，
# 先尝试减小学习率，而不是马上换模型。
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)"""),
            ("mini-batch 更新的直觉", """for x_batch, y_batch in train_loader:
    pred = model(x_batch)
    loss = criterion(pred, y_batch)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()"""),
        ],
        [
            ("把梯度方向理解反了", "沿正梯度走会让 loss 增大。", "参数更新用 `参数 -= 学习率 * 梯度`。"),
            ("学习率越大越好", "步子太大会越过低谷甚至发散。", "看 loss 曲线，必要时减小学习率。"),
            ("随机梯度没有理论含义", "它是在用样本子集估计总体梯度。", "理解随机性带来的效率和噪声。"),
            ("只会调用优化器，不知道它读什么", "无法诊断参数不更新的问题。", "`step()` 读取参数 `.grad` 并修改参数。"),
            ("忘记数据尺度影响梯度", "特征过大可能导致梯度大、训练不稳。", "必要时标准化或归一化输入。"),
        ],
        [
            ("loss", "当前位置模型的错误程度", "不是更新方向"),
            ("grad", "loss 对参数的变化率", "不是参数新值"),
            ("learning rate", "控制更新步长", "不是训练轮数"),
        ],
        [
            ("基础概念", "选择", "梯度在参数更新中主要告诉我们什么？", ["损失对参数变化的方向和敏感度", "训练集有多少样本", "模型有多少层"], "别把梯度和 loss 值混为一谈。"),
            ("基础概念", "判断", "学习率越大，训练一定越快越稳定。", None, "考虑跨过低谷和发散。"),
            ("基础概念", "填空", "梯度下降常见更新公式是 `w = w - ______ * grad`。", None, "填控制步长的超参数。"),
            ("公式理解", "短答", "为什么更新公式里是减号？", None, "从正梯度方向会让 loss 增大回答。"),
            ("公式理解", "计算", "若 `w=1.0`、`lr=0.1`、`grad=-2.0`，更新后 `w` 是多少？", None, "代入 `w - lr * grad`。"),
            ("代码阅读", "短答", "手写 `grad` 函数中为什么要对样本求平均？", None, "从整体训练目标和样本数量尺度回答。"),
            ("代码阅读", "短答", "`optimizer.step()` 和 `loss.backward()` 谁先谁后？为什么？", None, "说清梯度先被写入，优化器再读取。"),
            ("概念区分", "匹配", "匹配 batch / SGD / mini-batch：每次分别用全部样本、一个样本、一小批样本。", None, "按每次更新看多少数据分。"),
            ("错误诊断", "诊断", "loss 剧烈震荡甚至变大，优先检查什么？", None, "至少提学习率和数据尺度。"),
            ("错误诊断", "诊断", "有人把 `w += lr * grad` 写进训练循环，可能发生什么？", None, "从方向反了回答。"),
            ("场景应用", "场景", "数据集特别大时，为什么很少每一步都用全量样本算梯度？", None, "从计算成本回答。"),
            ("场景应用", "场景", "mini-batch 的噪声可能有什么好处和坏处？", None, "两面都说。"),
            ("概念区分", "短答", "局部最优和全局最优有什么区别？", None, "用损失曲面回答。"),
            ("迁移应用", "短答", "为什么先手写梯度有助于理解自动求导？", None, "联系 `.backward()`。"),
            ("面试追问", "短答", "如何向别人解释学习率？", None, "不要只说超参数。"),
            ("面试追问", "短答", "SGD 中的随机性来自哪里？", None, "从样本或 batch 选择回答。"),
            ("检查清单", "清单", "训练不收敛时，列出 5 个和梯度下降有关的排查点。", None, "覆盖学习率、梯度、清零、数据尺度、loss。"),
            ("代码修正", "诊断", "训练中 `.grad` 一直是 None，可能是什么原因？", None, "从计算图和参数参与计算回答。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：梯度下降怎样让线性模型逐步变好。", None, "串联损失、梯度、学习率、更新、batch 和收敛。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个能动手验证的动作。"),
        ],
    ),
])


def formula_html(lesson_data: dict) -> str:
    no = lesson_data["no"]
    if no in {2, 3}:
        return """
        <div class="formula">
          <div><b>线性预测</b>：<span class="math">ŷ = wx + b</span></div>
          <div><b>均方误差</b>：<span class="math">MSE = (1 / n) Σ(ŷᵢ - yᵢ)²</span></div>
          <div><b>梯度更新</b>：<span class="math">w ← w - η · ∂Loss/∂w</span></div>
        </div>
        """
    if no == 4:
        return """
        <div class="formula">
          <div><b>链式法则</b>：<span class="math">∂Loss/∂w = ∂Loss/∂y · ∂y/∂w</span></div>
          <div>反向传播做的事，就是把每个局部导数沿计算图乘回去，并把结果累积到参数梯度上。</div>
        </div>
        """
    if no == 6:
        return """
        <div class="formula">
          <div><b>sigmoid</b>：<span class="math">σ(z) = 1 / (1 + e⁻ᶻ)</span></div>
          <div><b>BCE</b>：<span class="math">Loss = -[y log(p) + (1-y) log(1-p)]</span></div>
        </div>
        """
    if no == 9:
        return """
        <div class="formula">
          <div><b>softmax</b>：<span class="math">pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)</span></div>
          <div><b>交叉熵</b>：真实类别对应的概率越低，loss 越大。</div>
        </div>
        """
    if no == 10:
        return """
        <div class="formula">
          <div><b>无 padding、stride=1 时</b>：<span class="math">H_out = H_in - kernel_size + 1</span></div>
          <div>通道数由 <code>out_channels</code> 决定，池化通常只改变高宽。</div>
        </div>
        """
    if no in {12, 13}:
        return """
        <div class="formula">
          <div><b>循环更新</b>：<span class="math">hₜ = RNN(xₜ, hₜ₋₁)</span></div>
          <div>序列分类常把最后隐藏状态送入线性层，得到类别 logits。</div>
        </div>
        """
    return """
    <div class="formula">
      <div><b>训练主线</b>：数据 → 模型预测 → 标量 loss → backward 写梯度 → optimizer.step 更新参数 → eval 检查泛化。</div>
    </div>
    """


def visual_html(lesson_data: dict) -> str:
    no = lesson_data["no"]
    if no in {1, 5, 8}:
        labels = ["数据", "模型", "损失", "梯度", "优化", "评估"]
    elif no in {2, 3, 4}:
        labels = ["参数", "预测", "误差", "损失", "梯度", "更新"]
    elif no in {6, 9}:
        labels = ["logits", "概率", "标签", "交叉熵", "梯度", "预测类别"]
    elif no in {10, 11}:
        labels = ["NCHW", "卷积", "通道", "池化", "展平", "分类头"]
    else:
        labels = ["序列", "编码", "隐藏状态", "GRU/RNN", "最后状态", "分类"]
    nodes = "".join(f'<span class="node">{h(label)}</span>' + ('' if i == len(labels)-1 else '<span class="arrow">→</span>') for i, label in enumerate(labels))
    return f"""
    <div class="map">{nodes}</div>
    <div class="viz-panel">
      <div class="viz-grid">
        <div class="viz-cell">
          <b>先看输入</b>
          <p>确认数据形状、标签形式和 dtype。许多训练错误在进入模型前已经发生。</p>
        </div>
        <div class="viz-cell">
          <b>再看变换</b>
          <p>逐层追踪输出形状和语义，别只看 API 名字。每一层都应该能回答“它把什么变成什么”。</p>
        </div>
        <div class="viz-cell">
          <b>最后看目标</b>
          <p>确认 loss 的输入约定、输出是否是标量，以及评估指标是否对应真实任务。</p>
        </div>
      </div>
      <p class="viz-note">判断句：如果你说不清某一行读入什么、输出什么、改变什么状态，就先不要急着调参。</p>
    </div>
    """


def render_sections(lesson_data: dict) -> str:
    parts = []
    for idx, section in enumerate(lesson_data["sections"], 1):
        paras = "".join(f"<p>{h(p)}</p>" for p in section["paras"])
        parts.append(f"""
        <div class="lesson-block">
          <h3>{idx}. {h(section["title"])}</h3>
          {paras}
          <p class="can-do">读到这里，你应该能：{h(can_do(section["title"]))}</p>
        </div>
        """)
    return "\n".join(parts)


def can_do(title: str) -> str:
    if "形状" in title or "维" in title:
        return "拿到一段代码后先检查输入、输出和层间维度是否对齐。"
    if "损失" in title or "Loss" in title:
        return "判断当前任务该用什么损失函数，以及它需要什么输入形式。"
    if "训练" in title or "循环" in title:
        return "把训练 step 拆成前向、loss、清梯度、反向和更新。"
    if "数据" in title or "Dataset" in title:
        return "区分样本读取、batch 组织和模型训练三件事。"
    if "序列" in title or "隐藏" in title:
        return "沿时间步追踪输入、隐藏状态和最终输出。"
    return "用这一小节的判断规则去检查相关代码。"


def render_terms(lesson_data: dict) -> str:
    rows = []
    for term, intuition, mistake in lesson_data["terms"]:
        rows.append(f"<tr><td>{h(term)}</td><td>{h(intuition)}</td><td>{h(mistake)}</td></tr>")
    return "\n".join(rows)


def render_confusions(lesson_data: dict) -> str:
    rows = []
    for a, b, c in lesson_data["confusions"]:
        rows.append(f"<tr><td>{h(a)}</td><td>{h(b)}</td><td>{h(c)}</td></tr>")
    return "\n".join(rows)


def render_code_examples(lesson_data: dict) -> str:
    parts = []
    for item in lesson_data["code_examples"]:
        label = item["label"]
        code = item["code"].strip("\n")
        kind = "错误示例" if "错误" in label else "示例代码"
        parts.append(f"""
        <div class="codebar"><span class="label">{h(label)}</span><span class="kind">{kind}</span></div>
        <pre><code>{h(code)}</code></pre>
        """)
    return "\n".join(parts)


def render_misconceptions(lesson_data: dict) -> str:
    boxes = []
    items = list(lesson_data["misconceptions"]) + COMMON_MISCONCEPTIONS
    for title, consequence, fix in items[:8]:
        boxes.append(f"""
        <div class="box warn">
          <h3>{h(title)}</h3>
          <p><b>后果：</b>{h(consequence)}</p>
          <p><b>修法：</b>{h(fix)}</p>
        </div>
        """)
    return "\n".join(boxes)


def render_questions(lesson_data: dict) -> tuple[str, str]:
    grouped: dict[str, list[tuple[int, tuple[str, str, str, list[str] | None, str]]]] = {}
    for i, q in enumerate(lesson_data["questions"], 1):
        grouped.setdefault(q[0], []).append((i, q))
    groups_html = []
    question_js = []
    for group_name, items in grouped.items():
        q_html = []
        for idx, (group, qtype, prompt, options, hint) in items:
            name = f"q{idx}"
            question_js.append({
                "group": group,
                "title": f"{idx}. {prompt}",
                "name": name,
                "type": "radio" if options else "text",
                "hint": hint,
            })
            if options:
                inputs = "".join(f'<label><input type="radio" name="{name}" value="{h(opt)}">{h(opt)}</label>' for opt in options)
                control = f'<div class="choices">{inputs}</div>'
            else:
                rows = "5" if qtype == "费曼" else "3"
                control = f'<textarea name="{name}" rows="{rows}"></textarea>'
            q_html.append(f"""
            <div class="q {'full' if qtype in {'费曼', '清单', '诊断'} else ''}" data-title="{h(str(idx)+'. '+prompt)}">
              <div class="q-meta"><span class="pill">{h(qtype)}</span><span class="pill">{h(group)}</span></div>
              <h3>{idx}. {h(prompt)}</h3>
              <div class="solve-note">{h(hint)}</div>
              {control}
            </div>
            """)
        groups_html.append(f"""
        <div class="practice-group">
          <div class="group-head">
            <div><h3>{h(group_name)}</h3><p>这一组用来检查你是否能把概念落到判断、代码阅读和排错上。</p></div>
            <div class="quick-review"><b>作答提示</b>先说判断依据，再说后果或修法。遇到代码题时，写清输入、输出和状态变化。</div>
          </div>
          <div class="drill-grid">
            {''.join(q_html)}
          </div>
        </div>
        """)
    return "\n".join(groups_html), repr(question_js)


CSS = r"""
:root{
  --navy:#1b2a4a;--cyan:#00a9f4;--bg:#f4f6f9;--paper:#fff;--ink:#172033;--muted:#5d6878;--line:#d8dee8;
  --soft:#eef7f4;--warn:#fff6df;--info:#eef4ff;--redsoft:#fff0ed;--code:#111827;--codeText:#e5e7eb;
  --sans:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",Arial,sans-serif;
  --serif:"Noto Serif CJK SC","Songti SC","STSong","SimSun",serif;
  --mono:"Cascadia Code","Consolas","SFMono-Regular",monospace;
}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:linear-gradient(90deg,rgba(27,42,74,.045) 1px,transparent 1px) 0 0/60px 60px,linear-gradient(rgba(27,42,74,.035) 1px,transparent 1px) 0 0/60px 60px,var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.72;-webkit-font-smoothing:antialiased}
.progress{position:fixed;left:0;top:0;height:4px;width:0;background:linear-gradient(90deg,var(--cyan),var(--navy));z-index:10}
.layout{display:grid;grid-template-columns:308px minmax(0,1fr);min-height:100vh}
aside{position:sticky;top:0;height:100vh;overflow:auto;background:var(--navy);color:#fff;padding:30px 22px;background-image:repeating-linear-gradient(90deg,transparent,transparent 59px,rgba(255,255,255,.045) 59px,rgba(255,255,255,.045) 60px),repeating-linear-gradient(0deg,transparent,transparent 59px,rgba(255,255,255,.035) 59px,rgba(255,255,255,.035) 60px)}
.brand{border-bottom:1px solid rgba(255,255,255,.36);padding-bottom:22px;margin-bottom:20px}.brand strong{display:block;color:#fff;font-family:var(--serif);font-size:27px;line-height:1.22}.brand span{display:block;color:rgba(255,255,255,.72);font-size:13px;margin-top:8px}
nav{display:grid}.nav-title{margin:20px 0 8px;color:rgba(255,255,255,.54);font-family:var(--mono);font-size:11px;letter-spacing:.12em}
nav a{display:flex;gap:10px;align-items:center;color:rgba(255,255,255,.82);text-decoration:none;border-bottom:1px solid rgba(255,255,255,.13);padding:10px 0;font-size:13px}
nav a:hover,nav a.active{color:#fff;border-color:rgba(255,255,255,.42);font-weight:700}.dot{width:6px;height:6px;background:var(--cyan);opacity:.62;flex:0 0 auto}.side-note{margin-top:24px;padding:13px;border:1px solid rgba(255,255,255,.22);color:rgba(255,255,255,.74);font-size:13px;line-height:1.8}
main{max-width:1420px;padding:34px 44px}.hero,section{background:var(--paper);border:1px solid var(--line);box-shadow:0 14px 28px rgba(27,42,74,.08)}.hero{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 390px;gap:24px;padding:42px;border-top:6px solid var(--navy)}.kicker{font-family:var(--mono);font-size:12px;color:#738197;letter-spacing:.16em;text-transform:uppercase;margin-bottom:14px}
h1{margin:0;font-family:var(--serif);font-size:44px;line-height:1.15;color:#111;letter-spacing:0}h2{margin:0;font-family:var(--serif);font-size:30px;line-height:1.25;color:#111}h3{margin:0 0 8px;font-size:18px;color:#111}p{margin:8px 0}.muted,.hero p{color:var(--muted)}section{margin-top:18px;padding:30px 34px}.head{display:flex;justify-content:space-between;gap:16px;align-items:start;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--line)}.tag,.pill{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:#69788d;background:#edf2f8;border:1px solid var(--line);padding:3px 7px}
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.8fr);gap:14px}.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.box,.route,.viz-cell,.q,.review-card{background:#fff;border:1px solid var(--line);padding:16px}.soft{background:var(--soft)}.warn{background:var(--warn)}.info{background:var(--info)}.redsoft{background:var(--redsoft)}
.route h3,.box h3,.viz-cell b{font-family:var(--serif);font-weight:800}.lesson-block{border-left:4px solid var(--navy);padding:4px 0 12px 18px;margin:18px 0}.lesson-block h3{font-family:var(--serif);font-size:22px}.can-do{background:#f0f7fb;border-left:4px solid var(--cyan);padding:10px 12px;color:#334155}
.map{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:18px 0}.node{background:#eef4ff;border:1px solid #cbd8ec;color:#1b2a4a;padding:8px 10px;font-weight:800}.arrow{color:#7c8798}
.viz-panel{border:1px solid var(--line);background:#f8fbff;padding:18px;margin:14px 0}.viz-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.viz-note{font-size:14px;color:#475569;border-top:1px solid var(--line);padding-top:12px}
table{width:100%;border-collapse:collapse;margin:14px 0;background:#fff}th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}th{background:#eef4ff;color:#1b2a4a}
code{background:#e8eef6;color:#172033;padding:2px 5px;border-radius:4px;font-family:var(--mono);font-size:.92em}
.formula{background:#fffdfa;border:1px solid #d9d0bf;border-left:6px solid var(--navy);padding:17px 20px;margin:14px 0;font-family:"Cambria Math","Times New Roman",var(--serif);font-size:18px;line-height:1.75;overflow:auto}.math{white-space:nowrap}
.codebar{margin-top:16px;background:#252526;color:#cbd5e1;border:1px solid #3c3c3c;border-bottom:0;padding:8px 12px;display:flex;gap:12px;align-items:center;font-family:var(--mono);font-size:13px}.codebar:before{content:"";width:34px;height:10px;flex:0 0 auto;background:radial-gradient(circle at 5px 5px,#f87171 0 4px,transparent 4.5px),radial-gradient(circle at 17px 5px,#fbbf24 0 4px,transparent 4.5px),radial-gradient(circle at 29px 5px,#34d399 0 4px,transparent 4.5px)}.codebar .label{color:#93c5fd;margin-right:auto}.codebar .kind{color:#9ca3af}
.copy-code{border:1px solid #3c3c3c;background:#2d2d30;color:#dbeafe;padding:3px 7px;font-family:var(--mono);font-size:12px;cursor:pointer}
pre{margin:0 0 14px;background:var(--code);color:var(--codeText);border:1px solid #3c3c3c;padding:16px;overflow:auto;font-family:var(--mono);font-size:14px;line-height:1.65}pre code{background:transparent;color:inherit;padding:0}
.practice-intro{display:grid;grid-template-columns:1fr 1fr;gap:14px}.practice-group{border:1px solid var(--line);margin-top:18px;background:#fff}.group-head{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:14px;padding:18px 20px;background:#eef7fb;border-bottom:1px solid var(--line)}.group-head h3{font-family:var(--serif);font-size:23px}.quick-review{border-left:4px solid var(--navy);padding-left:13px;color:#475569}.quick-review b{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:#64748b}.drill-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--line)}.q{border:0}.q.full{grid-column:1/-1}.q-meta{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}.q h3{font-size:16px;line-height:1.55}.choices label{display:block;margin:7px 0}.solve-note{background:#fff6df;border-left:4px solid #c28a17;color:#5c4618;padding:8px 10px;font-size:13px;margin:8px 0}textarea,input[type=text]{width:100%;border:1px solid #cbd5e1;background:#fff;color:var(--ink);padding:10px;font:inherit;resize:vertical}textarea{min-height:74px}input[type=radio]{accent-color:var(--navy);margin-right:7px}
.answer{white-space:pre-wrap;background:#fff;border:1px dashed #9aa7bb;padding:14px;max-height:380px;overflow:auto}.quality{display:none;white-space:pre-wrap;background:#fff6df;border:1px solid #d7b66b;color:#5c4618;padding:12px;margin:12px 0}.actions{position:sticky;bottom:0;display:flex;gap:10px;justify-content:flex-end;padding-top:14px;margin-top:18px;background:linear-gradient(transparent,var(--bg) 38%)}button{border:0;background:var(--navy);color:#fff;padding:9px 13px;font:inherit;cursor:pointer}.ghost{background:#fff;color:var(--navy);border:1px solid var(--navy)}
@media(max-width:960px){.layout{grid-template-columns:1fr}aside{position:static;height:auto}.hero,.grid2,.grid3,.practice-intro,.group-head,.viz-grid{grid-template-columns:1fr}main{padding:18px}.hero,section{padding:22px 18px}h1{font-size:31px}.drill-grid{grid-template-columns:1fr}.q.full{grid-column:auto}}
"""


def render_lesson(lesson_data: dict) -> str:
    nav_items = [
        ("goal", "学习目标"),
        ("map", "概念骨架"),
        ("lecture", "讲义"),
        ("terms", "术语表"),
        ("examples", "代码与例子"),
        ("pitfalls", "误区诊断"),
        ("practice", "练习区"),
        ("export", "导出"),
    ]
    nav_html = "".join(f'<a href="#{id_}"><span class="dot"></span>{label}</a>' for id_, label in nav_items)
    q_html, q_js = render_questions(lesson_data)
    title = f"{lesson_data['no']:02d}｜{lesson_data['title']}"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{h(title)}</title>
  <style>{CSS}</style>
</head>
<body>
<div class="progress" id="progress"></div>
<div class="layout">
  <aside>
    <div class="brand">
      <strong>{h(title)}</strong>
      <span>PyTorch 深度学习实践｜刘二大人课程学习页</span>
    </div>
    <div class="nav-title">CONTENTS</div>
    <nav>{nav_html}</nav>
    <div class="side-note">来源：{h(lesson_data["source"])}。本页按当前 PyTorch 习惯整理，旧课写法中容易过时的部分已换成更稳的表达。</div>
  </aside>
  <main>
    <section class="hero" id="goal">
      <div>
        <div class="kicker">PYTORCH STUDY PAGE · LESSON {lesson_data['no']:02d}</div>
        <h1>{h(lesson_data["title"])}</h1>
        <p>{h(lesson_data["goal"])}</p>
      </div>
      <div class="route">
        <h3>这节课抓一件事</h3>
        <p>{h(lesson_data["focus"])}</p>
        <ol>
          <li>先看对象之间的数据流。</li>
          <li>再看每一步的形状、类型和状态变化。</li>
          <li>最后用练习题检查自己能不能诊断错误。</li>
        </ol>
      </div>
    </section>

    <section id="map">
      <div class="head"><h2>概念骨架</h2><span class="tag">先搭主线</span></div>
      {visual_html(lesson_data)}
      {formula_html(lesson_data)}
    </section>

    <section id="lecture">
      <div class="head"><h2>讲义</h2><span class="tag">慢读这一部分</span></div>
      {render_sections(lesson_data)}
      <div class="box soft">
        <h3>完整知识链路</h3>
        <p>{h(lesson_data["focus"])} 它仍然落在同一条 PyTorch 主线上：先准备能被模型读取的数据，再让模型输出符合任务的张量，用合适的损失函数得到标量 loss，反向传播写入梯度，优化器更新参数，最后在评估模式下检查结果。换任务时，最先变化的是输入形状、模型输出含义和 loss 输入约定。</p>
      </div>
    </section>

    <section id="terms">
      <div class="head"><h2>术语表</h2><span class="tag">别混词</span></div>
      <table>
        <thead><tr><th>术语</th><th>直觉与定义</th><th>常见误解</th></tr></thead>
        <tbody>{render_terms(lesson_data)}</tbody>
      </table>
      <h3>易混概念对照</h3>
      <table>
        <thead><tr><th>概念</th><th>准确含义</th><th>不要混成</th></tr></thead>
        <tbody>{render_confusions(lesson_data)}</tbody>
      </table>
    </section>

    <section id="examples">
      <div class="head"><h2>代码与例子</h2><span class="tag">逐行读语义</span></div>
      <p class="muted">读代码时先标出输入、输出和状态变化。能解释这些，才算真正看懂。</p>
      {render_code_examples(lesson_data)}
    </section>

    <section id="pitfalls">
      <div class="head"><h2>误区诊断</h2><span class="tag">错因 / 后果 / 修法</span></div>
      <div class="grid2">{render_misconceptions(lesson_data)}</div>
    </section>

    <section id="practice">
      <div class="head"><h2>练习区</h2><span class="tag">20 题</span></div>
      <div class="practice-intro">
        <div class="review-card"><strong>怎么写答案</strong><p>选择和判断题先给结论；短答题写 1-3 句话；诊断题按“错因、后果、修法”回答；最后的费曼题用完整段落串起主线。</p></div>
        <div class="review-card"><strong>检查重点</strong><p>每个答案尽量落到形状、数据流、loss 输入约定或参数状态上。只写“因为不对”通常不够。</p></div>
      </div>
      {q_html}
    </section>

    <section id="export">
      <div class="head"><h2>导出练习记录</h2><span class="tag">复盘用</span></div>
      <p class="muted">完成练习后生成记录，方便后续复盘。</p>
      <div class="actions"><button onclick="generateRecord()">生成练习记录</button><button class="ghost" onclick="copyRecord()">复制记录</button></div>
      <div id="quality" class="quality"></div>
      <div id="record" class="answer">练习记录会显示在这里。</div>
    </section>
  </main>
</div>
<script>
const navLinks = [...document.querySelectorAll("nav a[href^='#']")];
const sections = navLinks.map(a => document.querySelector(a.getAttribute("href"))).filter(Boolean);
const progress = document.getElementById("progress");
function updateReadingState(){{
  const max = document.documentElement.scrollHeight - innerHeight;
  progress.style.width = max > 0 ? `${{Math.min(100, scrollY / max * 100)}}%` : "0";
  let current = sections[0]?.id;
  for (const section of sections) {{
    const rect = section.getBoundingClientRect();
    if (rect.top < innerHeight * 0.36) current = section.id;
  }}
  navLinks.forEach(a => a.classList.toggle("active", a.getAttribute("href") === `#${{current}}`));
}}
addEventListener("scroll", updateReadingState, {{passive:true}});
addEventListener("resize", updateReadingState);
updateReadingState();
document.querySelectorAll(".codebar").forEach(bar => {{
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "copy-code";
  btn.textContent = "复制";
  btn.addEventListener("click", () => {{
    const code = bar.nextElementSibling?.innerText || "";
    navigator.clipboard.writeText(code).then(() => {{
      btn.textContent = "已复制";
      setTimeout(() => btn.textContent = "复制", 1200);
    }}).catch(() => {{
      btn.textContent = "失败";
      setTimeout(() => btn.textContent = "复制", 1200);
    }});
  }});
  bar.appendChild(btn);
}});
const questions = {q_js};
function valueOf(q){{
  if(q.type === "radio"){{
    const el = document.querySelector(`input[name="${{q.name}}"]:checked`);
    return el ? el.value : "";
  }}
  const el = document.querySelector(`[name="${{q.name}}"]`);
  return el ? el.value.trim() : "";
}}
function generateRecord(){{
  const groups = {{}};
  const missing = [];
  questions.forEach(q => {{
    const v = valueOf(q);
    if(!v) missing.push(q.title);
    if(!groups[q.group]) groups[q.group] = [];
    groups[q.group].push({{title:q.title, answer:v || "（未填写）", hint:q.hint}});
  }});
  let out = "# {h(title)}｜练习记录\\n\\n";
  Object.keys(groups).forEach(group => {{
    out += `## ${{group}}\\n\\n`;
    groups[group].forEach(item => {{
      out += `### ${{item.title}}\\n提示：${{item.hint}}\\n\\n${{item.answer}}\\n\\n`;
    }});
  }});
  document.getElementById("record").textContent = out;
  const warnings = [];
  if(missing.length) warnings.push(`还有 ${{missing.length}} 题未填写。`);
  const feynman = questions.filter(q => q.title.includes("费曼")).map(valueOf).join("\\n");
  if(feynman && feynman.length < 120) warnings.push("费曼解释偏短，建议讲成 6-9 句话。");
  const quality = document.getElementById("quality");
  quality.style.display = "block";
  quality.textContent = warnings.length ? warnings.join("\\n") : "练习记录完整，可以用于复盘。";
}}
function copyRecord(){{
  navigator.clipboard.writeText(document.getElementById("record").textContent).catch(() => alert("复制失败，请手动复制。"));
}}
</script>
</body>
</html>
"""


def render_index() -> str:
    cards = []
    for item in sorted(LESSONS, key=lambda x: x["no"]):
        folder = slug_name(item["no"], item["title"])
        cards.append(f"""
        <a class="card" href="{h(folder)}/学习页.html">
          <span>{item['no']:02d}</span>
          <strong>{h(item['title'])}</strong>
          <em>{h(item['focus'])}</em>
        </a>
        """)
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>PyTorch 深度学习实践学习资料索引</title>
<style>
body{{margin:0;background:#f4f6f9;color:#172033;font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif;line-height:1.7}}
main{{max-width:1100px;margin:0 auto;padding:42px 24px}}h1{{font-family:"Noto Serif CJK SC","Songti SC",serif;font-size:42px;line-height:1.15;margin:0 0 12px}}p{{color:#5d6878}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:26px}}.card{{display:grid;grid-template-columns:54px 1fr;gap:8px 14px;text-decoration:none;color:#172033;background:#fff;border:1px solid #d8dee8;padding:18px;box-shadow:0 12px 24px rgba(27,42,74,.06)}}.card:hover{{border-color:#1b2a4a}}.card span{{grid-row:1/3;font-family:Consolas,monospace;color:#00a9f4;font-size:22px;font-weight:800}}.card strong{{font-size:18px}}.card em{{font-style:normal;color:#5d6878;font-size:14px}}@media(max-width:760px){{.grid{{grid-template-columns:1fr}}h1{{font-size:31px}}}}
</style></head><body><main>
<h1>PyTorch 深度学习实践｜学习资料索引</h1>
<p>共 {len(LESSONS)} 讲。每讲包含自学讲义、代码例子、误区诊断、20 道练习和练习记录导出。</p>
<div class="grid">{''.join(cards)}</div>
</main></body></html>"""


def main() -> None:
    for item in sorted(LESSONS, key=lambda x: x["no"]):
        folder = ROOT / slug_name(item["no"], item["title"])
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "学习页.html").write_text(render_lesson(item), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")
    print(f"generated {len(LESSONS)} lessons in {ROOT}")


LESSONS.extend([
    lesson(
        12,
        "循环神经网络基础：序列、隐藏状态与 RNNCell",
        "P12【12.循环神经网络（基础篇）】",
        "理解 RNN 如何按时间步处理序列，掌握 input、hidden、batch_first、RNNCell/RNN 的形状约定，以及序列任务中的训练循环变化。",
        "从固定长度图像转向按时间展开的序列数据。",
        [
            ("RNN 先解决顺序依赖问题", [
                "全连接网络和 CNN 主要处理固定形状输入。序列数据的特点是顺序有意义，比如一句话、一个名字、时间序列。第 1 个字符和第 5 个字符不是可随便打乱的列，它们的位置影响整体含义。",
                "RNN 的基本想法是逐步读序列。每个时间步接收当前输入和上一步隐藏状态，输出新的隐藏状态。隐藏状态像模型对已经读过内容的压缩记忆。",
                "你现在应该能解释：RNN 不是一次性看完整个输入，而是沿时间步不断更新隐藏状态。"
            ]),
            ("隐藏状态是序列信息的载体", [
                "隐藏状态 `h_t` 保存到当前时间步为止的信息。第 t 步会读取 `x_t` 和 `h_{t-1}`，生成 `h_t`。如果任务只需要整个序列的分类结果，常用最后一个隐藏状态做分类。",
                "隐藏状态不是标签，也不是 loss。它是模型内部表示，会随着序列输入一步步变化。不同 batch、不同层数、不同方向的 RNN，隐藏状态形状也不同。",
                "你现在应该能把 `input_t`、`hidden_prev`、`hidden_next` 三者的关系讲清楚。"
            ]),
            ("RNNCell 展示单步，RNN 封装整段序列", [
                "`nn.RNNCell` 只处理一个时间步，你需要自己写循环，把序列按时间步喂进去。`nn.RNN` 则一次接收整段序列，内部帮你循环，返回所有时间步输出和最后隐藏状态。",
                "RNNCell 适合教学，因为它把时间展开过程暴露出来。真实项目里更常用 `nn.RNN`、`nn.GRU` 或 `nn.LSTM`，因为它们封装更完整，也更高效。",
                "你现在应该能区分：Cell 是一步，RNN 是一串时间步。"
            ]),
            ("形状约定是 RNN 最大门槛之一", [
                "PyTorch RNN 默认输入形状是 `[seq_len, batch, input_size]`。如果设置 `batch_first=True`，输入形状就是 `[batch, seq_len, input_size]`。很多报错都来自这两个约定混用。",
                "隐藏状态形状通常是 `[num_layers * num_directions, batch, hidden_size]`。如果是单层单向 RNN，就是 `[1, batch, hidden_size]`。这和输入的 batch 维必须一致。",
                "你现在应该能在写 RNN 前先决定是否使用 `batch_first=True`，并据此检查输入和 hidden shape。"
            ]),
            ("one-hot 输入高维稀疏，后续会引入 embedding", [
                "字符或词不能直接进入神经网络，需要先变成数值向量。最朴素方法是 one-hot：词表有多大，向量就有多长，目标字符位置为 1，其余为 0。",
                "one-hot 容易理解，但维度高、稀疏，而且不同字符之间没有可学习的相似性。下一讲会用 embedding 把离散符号映射成低维稠密向量。",
                "你现在应该能说明：one-hot 是把类别符号变成向量的起点，但不是处理自然语言的最终方案。"
            ]),
            ("序列分类与逐步输出的区别", [
                "有些序列任务每个时间步都需要输出，例如语言模型预测下一个字符；有些任务只需要整个序列一个输出，例如名字分类。两类任务使用 RNN 的方式不同。",
                "如果只做序列分类，可以取最后隐藏状态接线性层；如果每步都要预测，就要对每个时间步输出做映射并计算损失。不要把所有 RNN 任务都写成同一种输出形式。",
                "你现在应该能判断一个序列任务需要“每步输出”还是“整段输出”。"
            ]),
        ],
        [
            ("序列", "有顺序依赖的一串输入，如字符、词或时间点。", "把它当成无序特征列。"),
            ("隐藏状态", "RNN 对已读序列信息的内部表示。", "误以为它是最终标签。"),
            ("RNNCell", "单个时间步的循环单元。", "以为它自动处理完整序列。"),
            ("batch_first", "控制 RNN 输入是否把 batch 放在第一维。", "和默认 `[seq,batch,feature]` 混淆。"),
        ],
        [
            ("RNNCell 手写时间循环", """cell = nn.RNNCell(input_size=4, hidden_size=8)
hidden = torch.zeros(batch_size, 8)

for t in range(seq_len):
    x_t = sequence[:, t, :]  # batch_first=True 的手写序列
    hidden = cell(x_t, hidden)"""),
            ("nn.RNN 封装整段序列", """rnn = nn.RNN(input_size=4, hidden_size=8, batch_first=True)
output, hidden = rnn(sequence)
# output: [batch, seq_len, hidden_size]
# hidden: [num_layers, batch, hidden_size]"""),
            ("错误示例：混用形状约定", """# 错误示例
rnn = nn.RNN(input_size=4, hidden_size=8)  # 默认不是 batch_first
sequence = torch.randn(32, 10, 4)          # 这是 [batch, seq, feature]
output, hidden = rnn(sequence)             # RNN 会把 32 当 seq_len"""),
        ],
        [
            ("混用 batch_first", "RNN 把 batch 和 seq 读反，结果或 shape 都不对。", "明确设置并按约定准备输入。"),
            ("把 hidden 当输出类别", "隐藏状态还需要接分类层或解码层。", "按任务决定如何映射输出。"),
            ("RNNCell 不写时间循环", "只处理了一个时间步。", "Cell 外部手动 for 循环。"),
            ("忽略 hidden 初始形状", "层数、方向、batch 不匹配。", "按 `[layers*directions,batch,hidden]` 准备。"),
            ("把序列打乱成普通特征", "顺序信息丢失。", "保留时间步维度。"),
        ],
        [
            ("input_size", "每个时间步输入向量长度", "不是序列长度"),
            ("seq_len", "时间步数量", "不是 batch size"),
            ("hidden_size", "隐藏状态向量长度", "不是类别数"),
        ],
        [
            ("基础概念", "选择", "RNN 的隐藏状态主要保存什么？", ["已经读过的序列信息", "优化器学习率", "数据集大小"], "从序列记忆回答。"),
            ("基础概念", "判断", "`nn.RNNCell` 会自动处理完整序列，不需要循环。", None, "Cell 是一步还是整段？"),
            ("基础概念", "填空", "设置 `batch_first=True` 后，输入形状常写为 `[batch, ______, input_size]`。", None, "填时间步维。"),
            ("形状判断", "短答", "`[32,10,4]` 在 batch_first=True 下分别表示什么？", None, "解释三维。"),
            ("形状判断", "短答", "单层单向 RNN 的 hidden 形状通常是什么？", None, "写 `[1,batch,hidden_size]`。"),
            ("代码阅读", "短答", "手写 RNNCell 循环中，为什么每一步都更新 hidden？", None, "从序列记忆回答。"),
            ("代码阅读", "短答", "`output` 和 `hidden` 的区别是什么？", None, "所有时间步 vs 最后隐藏状态。"),
            ("错误诊断", "诊断", "RNN 默认输入却喂 `[batch,seq,feature]`，会有什么问题？", None, "把 batch 当 seq。"),
            ("错误诊断", "诊断", "隐藏状态 batch 维和输入 batch 不一致，会怎样？", None, "形状报错。"),
            ("错误诊断", "诊断", "把名字字符顺序打乱再训练，可能损失什么信息？", None, "序列模式。"),
            ("场景应用", "场景", "股票日序列和房屋特征表，哪个更自然适合 RNN？为什么？", None, "从时间顺序回答。"),
            ("场景应用", "场景", "名字分类是每步输出还是整段输出？", None, "只需要一个国家类别。"),
            ("概念区分", "匹配", "匹配 input_size / seq_len / hidden_size：单步向量长度、时间步数、隐藏向量长度。", None, "按含义写。"),
            ("概念区分", "短答", "RNNCell 和 RNN 的区别是什么？", None, "一步 vs 整段。"),
            ("面试追问", "短答", "为什么 RNN 适合序列数据？", None, "提顺序和隐藏状态。"),
            ("面试追问", "短答", "one-hot 的问题是什么？", None, "提高维稀疏和不可学习相似性。"),
            ("检查清单", "清单", "写 RNN 前列 5 项 shape 检查。", None, "覆盖 batch_first、seq_len、input_size、hidden、output。"),
            ("代码修正", "诊断", "默认 RNN 收到 `[batch,seq,feature]`，给出两种修法。", None, "设置 batch_first 或 transpose。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：RNN 如何沿时间步处理序列。", None, "串联序列、x_t、hidden、RNNCell、RNN、batch_first、输出。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
    lesson(
        13,
        "循环神经网络高级篇：Embedding、GRU 与变长序列分类",
        "P13【13.循环神经网络（高级篇）】",
        "掌握名字分类任务的完整数据流：字符/名字编码、Embedding、GRU、最后隐藏状态、线性分类、padding/packing 与变长序列处理。",
        "把 RNN 基础应用到真实的名字分类器。",
        [
            ("名字分类是整段序列分类任务", [
                "这一讲的任务是根据名字拼写判断所属语言或国家类别。输入看起来是一列名字，但每个名字本身是一串字符。模型要读完整个字符序列，再输出一个类别。",
                "这类任务和 MNIST 一样是分类，但输入结构完全不同。MNIST 是图像张量，名字是变长字符序列。输出仍然可以是 `[batch, num_classes]` logits，标签仍然可以是类别索引。",
                "你现在应该能把名字分类放进通用训练链路：序列输入、RNN/GRU 编码、线性层输出类别 logits、交叉熵训练。"
            ]),
            ("Embedding 把离散字符变成稠密向量", [
                "字符首先要映射成整数 id。`nn.Embedding(num_embeddings, embedding_dim)` 会把每个 id 查表成一个可学习向量。相比 one-hot，embedding 更低维，也能在训练中学到字符之间对任务有用的表示。",
                "Embedding 的输入通常是 long 类型索引，输出会多出 embedding 维。例如输入 `[batch, seq_len]`，输出 `[batch, seq_len, embedding_dim]`。",
                "你现在应该能说明为什么不能把字符串直接喂给 GRU，以及 embedding 在数据流中的位置。"
            ]),
            ("GRU 用门控机制改善普通 RNN", [
                "普通 RNN 在长序列上容易遗忘或梯度变弱。GRU 引入门控机制，控制哪些信息保留、哪些信息更新。你不需要先手推门控公式，也要知道它的作用：让隐藏状态更新更可控。",
                "PyTorch 的 `nn.GRU` 接收 embedding 后的序列，返回所有时间步输出和最后隐藏状态。做名字分类时，常取最后隐藏状态，再送入线性层得到类别 logits。",
                "你现在应该能区分：Embedding 处理离散输入，GRU 处理序列依赖，Linear 处理分类输出。"
            ]),
            ("变长序列需要 padding 和长度信息", [
                "名字长短不一样，但一个 batch 里的张量必须能堆叠成矩形。常见做法是把短序列 padding 到同一长度，同时保留每个序列真实长度。",
                "如果直接把 padding 当真实字符喂给 RNN，模型会读到很多无意义的 pad。`pack_padded_sequence` 可以告诉 RNN 每条序列真实长度，让它跳过 padding 部分。使用时要注意长度排序或设置 `enforce_sorted=False`。",
                "你现在应该能说明 padding 解决 batch 对齐，packing 解决 RNN 不该学习 pad。"
            ]),
            ("双向和多层会改变 hidden 形状", [
                "GRU 可以设置多层和双向。双向会同时从左到右、从右到左读序列，最后 hidden 的第一维会变成 `num_layers * num_directions`。分类时需要清楚取哪一层、哪一方向，或者把方向拼接起来。",
                "如果设置 `bidirectional=True`，线性层输入维度常要变成 `hidden_size * 2`。这是高级 RNN 中常见 shape 坑。",
                "你现在应该能在看到 GRU 参数后，推断分类层输入维度是否要乘以 2。"
            ]),
            ("训练和推理要保留同一套词表", [
                "字符到 id 的映射必须固定。训练时用的词表，推理新名字时也要用同一套。否则同一个字符可能变成不同 id，embedding 查表含义就乱了。",
                "还要处理未知字符。真实名字可能包含训练集中没见过的字符，通常需要 `<unk>` 之类的特殊 id。padding 也最好有单独 `<pad>` id，并在处理长度时排除它。",
                "你现在应该能把序列分类的工程检查扩展到词表、padding、未知字符和长度。"
            ]),
        ],
        [
            ("Embedding", "把离散 id 映射为可学习稠密向量的查表层。", "误以为输入可以是原始字符串。"),
            ("GRU", "带门控的循环网络单元，用于处理序列依赖。", "和普通全连接层混淆。"),
            ("padding", "把短序列补齐到同一长度。", "误以为 pad 是真实字符。"),
            ("packing", "把变长序列和真实长度交给 RNN，减少 padding 干扰。", "以为只 padding 就够了。"),
        ],
        [
            ("名字分类模型骨架", """class NameClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x, lengths):
        emb = self.embedding(x)
        packed = nn.utils.rnn.pack_padded_sequence(
            emb, lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        _, hidden = self.gru(packed)
        last = hidden[-1]
        return self.fc(last)"""),
            ("Embedding 输入输出形状", """ids = torch.tensor([[1, 5, 9, 0], [2, 7, 0, 0]], dtype=torch.long)
emb = embedding(ids)
print(ids.shape)  # [batch, seq_len]
print(emb.shape)  # [batch, seq_len, embedding_dim]"""),
            ("双向 GRU 分类头要改维度", """self.gru = nn.GRU(embed_dim, hidden_size, batch_first=True, bidirectional=True)
self.fc = nn.Linear(hidden_size * 2, num_classes)"""),
        ],
        [
            ("把原始字符串传给 Embedding", "Embedding 需要 long 类型 id。", "先建立字符表并编码。"),
            ("padding 后不保留真实长度", "RNN 会把 pad 当成有效时间步。", "记录 lengths，必要时 pack。"),
            ("双向 GRU 后 Linear 维度没乘 2", "分类头输入维度不匹配。", "根据 directions 调整。"),
            ("推理时重建词表", "字符 id 映射变了，embedding 含义错乱。", "保存并复用训练词表。"),
            ("标签不是 long 类别索引", "CrossEntropyLoss 输入约定不匹配。", "国家/语言类别编码成 long。"),
        ],
        [
            ("Embedding", "字符 id -> 向量", "不处理时间依赖"),
            ("GRU", "序列向量 -> 隐藏状态", "不直接给类别概率"),
            ("Linear", "隐藏状态 -> 类别 logits", "不读取原始字符串"),
        ],
        [
            ("基础概念", "选择", "`nn.Embedding` 的输入通常是什么？", ["long 类型的整数 id", "原始字符串列表", "float 概率"], "查表层需要索引。"),
            ("基础概念", "判断", "padding 后的 `<pad>` 应该被当成真实字符学习。", None, "判断 pad 的语义。"),
            ("基础概念", "填空", "双向 GRU 的方向数是 ______。", None, "单向是 1。"),
            ("形状判断", "短答", "输入 ids `[32,12]` 经过 embedding_dim=20 后形状是什么？", None, "增加 embedding 维。"),
            ("形状判断", "短答", "单层单向 GRU 最后 hidden `hidden[-1]` 形状通常是什么？", None, "写 `[batch, hidden_size]`。"),
            ("代码阅读", "短答", "`pack_padded_sequence` 为什么需要 lengths？", None, "说明真实长度。"),
            ("代码阅读", "短答", "`padding_idx=0` 有什么作用？", None, "从 pad 向量和训练回答。"),
            ("错误诊断", "诊断", "Embedding 报错 expected LongTensor，应该检查什么？", None, "输入 dtype。"),
            ("错误诊断", "诊断", "双向 GRU 后 Linear 报 shape mismatch，可能漏了什么？", None, "hidden_size * 2。"),
            ("错误诊断", "诊断", "推理时新建了字符表，为什么预测会乱？", None, "id 映射不一致。"),
            ("场景应用", "场景", "名字长度不同，为什么不能直接堆成普通二维数组？", None, "需要 padding 对齐。"),
            ("场景应用", "场景", "未知字符应该怎样处理？", None, "用 `<unk>`。"),
            ("概念区分", "匹配", "匹配 embedding / GRU / linear：查表、读序列、分类。", None, "按数据流写。"),
            ("概念区分", "短答", "padding 和 packing 的区别是什么？", None, "一个补齐，一个告诉 RNN 真实长度。"),
            ("面试追问", "短答", "GRU 相比普通 RNN 主要改进什么？", None, "提门控和长依赖。"),
            ("面试追问", "短答", "为什么名字分类可以只取最后隐藏状态？", None, "整段序列一个类别。"),
            ("检查清单", "清单", "写变长序列分类器前列 5 项检查。", None, "覆盖词表、dtype、padding、lengths、hidden shape。"),
            ("代码修正", "诊断", "使用 `pack_padded_sequence` 但 lengths 在 GPU 上导致问题，如何处理？", None, "常见做法是 `lengths.cpu()`。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：名字分类器如何从字符串得到国家类别。", None, "串联词表、id、embedding、padding、GRU、hidden、linear、CrossEntropy。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
])


LESSONS.extend([
    lesson(
        10,
        "卷积神经网络基础：通道、卷积核与池化",
        "P10【10.卷积神经网络（基础篇）】",
        "理解 CNN 为什么保留图像空间结构，掌握 NCHW 输入、Conv2d 输出形状、通道变化、池化和全连接分类头的衔接。",
        "从展平图像转向利用空间结构的卷积网络。",
        [
            ("CNN 先解决全连接丢空间结构的问题", [
                "全连接 MNIST 会把 `[1,28,28]` 展平成 784 个数。这样能训练，但原来相邻像素的空间关系被打散了。图像任务里，局部结构很重要，例如边缘、角点、笔画和纹理都出现在局部区域。",
                "卷积层直接在二维空间上滑动卷积核。它不需要把图像一开始就拉直，而是在局部窗口里提取特征。这样模型能更自然地利用相邻像素之间的关系。",
                "你现在应该能解释：CNN 不是为了让代码更复杂，而是为了保留并利用图像的空间结构。"
            ]),
            ("PyTorch 图像输入默认是 NCHW", [
                "PyTorch 的 `Conv2d` 常见输入形状是 `[N, C, H, W]`。`N` 是 batch size，`C` 是通道数，`H` 和 `W` 是高度和宽度。MNIST 灰度图通道数是 1，彩色 RGB 图像通道数是 3。",
                "很多教材或图片库会以 HWC 表示图像，即 `[H, W, C]`。进入 PyTorch 卷积前要转成 CHW，再由 DataLoader 组成 NCHW。通道维放错会导致形状报错或模型学到错误含义。",
                "你现在应该能看到 `[64,1,28,28]` 并读成 64 张单通道 28×28 图像。"
            ]),
            ("卷积层会改变通道数和空间尺寸", [
                "`nn.Conv2d(in_channels, out_channels, kernel_size)` 中，`in_channels` 必须和输入通道数一致，`out_channels` 是卷积核组数，也就是输出特征图通道数。卷积核大小、padding、stride 会影响输出高宽。",
                "例如 MNIST 输入 `[N,1,28,28]` 经过 `Conv2d(1,10,kernel_size=5)`，如果不 padding，空间尺寸会从 28 变成 24，输出是 `[N,10,24,24]`。通道变成 10，是因为有 10 个卷积核组在提取不同特征。",
                "你现在应该能用 `in_channels`、`out_channels`、`kernel_size` 解释卷积层输出为什么会变。"
            ]),
            ("池化减少空间尺寸，不改变通道数", [
                "池化层常用于降低特征图的空间尺寸，减少计算量，也让特征对局部小位移更稳。`MaxPool2d(2)` 通常会把高宽减半，例如 `[N,10,24,24]` 变成 `[N,10,12,12]`。",
                "注意池化一般不改变通道数。它是在每个通道内部做下采样，不会把 10 个通道变成 20 个通道。通道变化主要由卷积层的 `out_channels` 决定。",
                "你现在应该能区分卷积和池化：卷积学特征并可改通道，池化压缩空间尺寸。"
            ]),
            ("卷积后接全连接要算展平维度", [
                "CNN 最后做分类时，常把卷积和池化后的特征图展平，再送入全连接层。这里最容易错的是 `Linear` 的输入维度。你必须根据前面每个卷积和池化后的形状，算出 `channels * height * width`。",
                "如果前面两次 5×5 卷积和 2×2 池化，MNIST 尺寸可能从 28 到 24 到 12，再到 8 到 4。若最后通道是 20，展平维度就是 `20*4*4=320`。这就是很多示例里 `Linear(320, 10)` 的来源。",
                "你现在应该能手算一个 CNN 分类头的输入维度，而不是把 320 当成神秘数字背下来。"
            ]),
            ("CNN 训练循环仍然没变", [
                "换成 CNN 后，训练循环仍然是 DataLoader 提供 batch，模型前向输出 logits，CrossEntropyLoss 计算 loss，zero_grad、backward、step 更新参数。变的是模型内部结构和输入形状，不是训练主线。",
                "这也是课程反复强调四步流程的原因。你可以换线性层、卷积层、池化层，但数据、模型、损失、优化、评估这条链不变。",
                "你现在应该能把 CNN 放回通用训练链路里，不会因为多了卷积层就忘记 loss 和 optimizer 的分工。"
            ]),
        ],
        [
            ("NCHW", "PyTorch 卷积常用图像 batch 形状：样本数、通道、高、宽。", "和 HWC 混淆。"),
            ("卷积核", "在局部窗口上提取特征的可学习权重。", "误以为它只是在压缩图片。"),
            ("特征图", "卷积层输出的多通道空间表示。", "把它当成单张普通图片。"),
            ("池化", "对每个通道做空间下采样。", "误以为会改变通道数。"),
        ],
        [
            ("基础 CNN 结构", """class CnnNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.pool = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.fc = nn.Linear(320, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))  # [N,10,12,12]
        x = self.pool(torch.relu(self.conv2(x)))  # [N,20,4,4]
        x = x.view(x.size(0), -1)
        return self.fc(x)"""),
            ("形状检查", """x = torch.randn(64, 1, 28, 28)
out = model.conv1(x)
print(out.shape)  # [64, 10, 24, 24]"""),
            ("错误示例：通道数接不上", """# 错误示例
self.conv1 = nn.Conv2d(1, 10, 5)
self.conv2 = nn.Conv2d(1, 20, 5)  # 应该接收 conv1 的 10 个通道"""),
        ],
        [
            ("把 NCHW 写成 NHWC", "Conv2d 读错通道维或直接报错。", "确认输入是 `[N,C,H,W]`。"),
            ("conv2 的 in_channels 写错", "第二个卷积层接不上第一个输出。", "上一层 out_channels 等于下一层 in_channels。"),
            ("池化后还按原尺寸算 Linear", "全连接层输入维度报错。", "逐层计算 H、W。"),
            ("认为池化会改通道数", "形状推导错误。", "池化通常只改 H、W。"),
            ("忘记展平", "Linear 收到 4D 特征图。", "进入全连接前 `view(x.size(0), -1)`。"),
        ],
        [
            ("卷积", "提取局部特征并可改通道数", "不是分类器全部"),
            ("池化", "压缩空间尺寸", "通常不学参数"),
            ("全连接头", "把特征映射到类别 logits", "不保留空间结构"),
        ],
        [
            ("基础概念", "选择", "PyTorch Conv2d 常见输入形状是哪一种？", ["[N,C,H,W]", "[N,H,W,C]", "[C,N,H,W]"], "按 PyTorch 约定。"),
            ("基础概念", "判断", "MaxPool2d(2) 通常会改变通道数。", None, "判断池化作用。"),
            ("基础概念", "填空", "RGB 图像的输入通道数通常是 ______。", None, "灰度是 1，彩色常见是几？"),
            ("形状推导", "短答", "`[64,1,28,28]` 经过 `Conv2d(1,10,5)` 无 padding 后形状是什么？", None, "高宽各减 4。"),
            ("形状推导", "短答", "`[N,10,24,24]` 经过 `MaxPool2d(2)` 后形状是什么？", None, "高宽减半，通道不变。"),
            ("代码阅读", "短答", "`x.view(x.size(0), -1)` 在 CNN 里做什么？", None, "从展平回答。"),
            ("代码阅读", "短答", "为什么第二个卷积层 `in_channels` 要等于第一个卷积层 `out_channels`？", None, "从通道衔接回答。"),
            ("错误诊断", "诊断", "报错说 expected input to have 10 channels, but got 1，可能哪里写错？", None, "从 conv2 输入通道回答。"),
            ("错误诊断", "诊断", "Linear 输入维度写错，通常如何排查？", None, "打印展平前 shape。"),
            ("错误诊断", "诊断", "把图像先展平再送 Conv2d，会有什么问题？", None, "Conv2d 需要空间维。"),
            ("场景应用", "场景", "把 MNIST 换成 RGB 32×32 图片，第一层 in_channels 该怎么改？", None, "从通道数回答。"),
            ("场景应用", "场景", "为什么卷积适合图像？", None, "从局部结构和权重共享回答。"),
            ("概念区分", "匹配", "匹配 Conv / Pool / Linear：提特征、降尺寸、分类输出。", None, "按功能写。"),
            ("概念区分", "短答", "特征图和原图有什么区别？", None, "从通道和语义回答。"),
            ("面试追问", "短答", "CNN 相比全连接处理图像的优势是什么？", None, "提空间结构。"),
            ("面试追问", "短答", "为什么卷积层参数比全连接少？", None, "提局部连接和权重共享。"),
            ("检查清单", "清单", "调试 CNN shape 时列 5 项检查。", None, "覆盖 NCHW、通道、H/W、展平、Linear。"),
            ("代码修正", "诊断", "给出 `conv1=Conv2d(1,10,5)` 后 `conv2=Conv2d(1,20,5)` 的修正。", None, "改 in_channels。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：CNN 如何把一张 MNIST 图像变成十类 logits。", None, "串联 NCHW、卷积、通道、池化、展平、Linear、CrossEntropy。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
    lesson(
        11,
        "卷积神经网络高级篇：Inception、残差与读代码",
        "P11【11.卷积神经网络（高级篇）】",
        "理解复杂 CNN 结构如何通过模块化减少重复，掌握 Inception 多分支、1x1 卷积、残差连接和阅读开源模型代码的基本方法。",
        "从单一路径 CNN 扩展到模块化、多分支和跳连结构。",
        [
            ("复杂网络先需要模块化", [
                "CNN 变深后，如果把所有卷积层都堆在一个 `forward` 里，代码会很长，也很难检查。模块化的做法是把重复结构写成小的 `nn.Module`，再在大模型中复用。",
                "模块化不是为了炫技，而是为了降低认知负担。你可以先读一个 block 的输入输出，再读整体网络如何串联这些 block。后续读 ResNet、Inception、DenseNet 都需要这种方法。",
                "你现在应该能把复杂模型拆成“模块内部”和“模块之间”两层来读。"
            ]),
            ("Inception 的核心是多分支并行", [
                "Inception 模块的想法是：同一份输入可以走不同尺度的卷积分支，例如 1x1、3x3、5x5 和池化分支。每个分支提取不同感受野的特征，最后在通道维拼接起来。",
                "这里最重要的 shape 判断是：分支输出的高宽必须一致，才能在通道维 `dim=1` 拼接。拼接后通道数等于各分支通道数之和。",
                "你现在应该能解释 Inception 为什么是“宽”的结构，以及 `torch.cat(outputs, dim=1)` 为什么沿通道维拼接。"
            ]),
            ("1x1 卷积常用于改变通道数", [
                "1x1 卷积不看邻域，只在同一个空间位置上混合通道。它常用于降维或升维，减少后续大卷积的计算量，也能增加非线性组合。",
                "例如先用 1x1 把通道从 192 降到 16，再接 5x5 卷积，就比直接对 192 通道做 5x5 便宜得多。这里的“降维”是降通道，不是降图像高宽。",
                "你现在应该能说清 1x1 卷积不是没用的小卷积，而是通道变换工具。"
            ]),
            ("残差连接解决深层网络难训练问题", [
                "网络很深时，直接堆层可能出现训练困难。残差连接让模块学习 `F(x)`，再把输入 `x` 加回输出，形成 `F(x) + x`。如果额外层暂时学不到好东西，至少可以接近恒等映射。",
                "残差相加要求形状一致。如果通道数或空间尺寸不同，需要用 1x1 卷积或 stride 调整 shortcut。否则直接相加会报 shape 错误。",
                "你现在应该能判断残差连接中的主分支和 shortcut 是否能相加。"
            ]),
            ("读开源模型先看 forward 数据流", [
                "课程后半提醒不要只追求“跑通代码”，要先读代码。读复杂模型时，第一轮不要陷入每个参数，而是沿 `forward` 画数据流：输入经过哪些模块，在哪些地方分支，在哪些地方拼接或相加。",
                "第二轮再看每个模块的输入输出通道。第三轮看训练代码和损失函数。这样读会比从文件第一行一路看到最后更稳。",
                "你现在应该能拿一个陌生 CNN，先画出主干路径、分支点、合并点和分类头。"
            ]),
            ("复杂结构仍服务于同一个训练目标", [
                "Inception、残差、1x1 卷积都是模型结构层面的改进。它们不会改变训练链路：输出 logits，交叉熵计算 loss，反向传播更新参数。",
                "不要因为结构高级，就忽略基础检查。复杂网络出错时，shape、dtype、训练/评估模式、loss 输入约定仍然是第一批排查点。",
                "你现在应该能把高级 CNN 结构放回普通 PyTorch 训练流程，而不是把它们当成孤立技巧。"
            ]),
        ],
        [
            ("Inception", "多分支卷积模块，提取不同尺度特征后拼接。", "误以为只是多堆几层。"),
            ("1x1 卷积", "在每个空间位置上混合通道，常用于通道变换。", "以为没有空间窗口就没有意义。"),
            ("残差连接", "把输入通过 shortcut 加到模块输出上。", "忽略相加前 shape 必须一致。"),
            ("模块化", "把重复网络结构封装为可复用 Module。", "误以为只是代码风格问题。"),
        ],
        [
            ("Inception 拼接示意", """class InceptionBlock(nn.Module):
    def __init__(self, in_ch):
        super().__init__()
        self.b1 = nn.Conv2d(in_ch, 16, kernel_size=1)
        self.b2 = nn.Conv2d(in_ch, 24, kernel_size=3, padding=1)
        self.b3 = nn.Conv2d(in_ch, 24, kernel_size=5, padding=2)

    def forward(self, x):
        y1 = torch.relu(self.b1(x))
        y2 = torch.relu(self.b2(x))
        y3 = torch.relu(self.b3(x))
        return torch.cat([y1, y2, y3], dim=1)  # 通道数相加"""),
            ("残差连接要求形状一致", """def forward(self, x):
    identity = x
    out = torch.relu(self.conv1(x))
    out = self.conv2(out)
    out = out + identity
    return torch.relu(out)"""),
            ("用 1x1 卷积调整 shortcut", """self.shortcut = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=2)
# 当主分支改变通道或空间尺寸时，shortcut 也要同步调整"""),
        ],
        [
            ("分支高宽不一致还拼接", "torch.cat 会报 shape 错误。", "用 padding/stride 保持高宽一致。"),
            ("拼接维度写错", "沿 batch 或空间维拼接会破坏语义。", "CNN 通道拼接通常 `dim=1`。"),
            ("残差相加前 shape 不同", "无法逐元素相加。", "用 1x1 conv 调整 shortcut。"),
            ("以为 1x1 卷积没用", "忽略通道混合和降维作用。", "从通道维理解它。"),
            ("只跑代码不读结构", "换模型或排错时无从下手。", "先沿 forward 画数据流。"),
        ],
        [
            ("cat", "通道拼接，通道数相加", "不是逐元素相加"),
            ("add", "残差逐元素相加", "要求 shape 一致"),
            ("1x1 conv", "改变通道", "通常不改高宽，除非 stride 改变"),
        ],
        [
            ("基础概念", "选择", "Inception 多分支输出通常沿哪个维度拼接？", ["通道维 dim=1", "batch 维 dim=0", "高度维 dim=2"], "按 NCHW 判断。"),
            ("基础概念", "判断", "残差连接相加前两个张量 shape 可以随意不同。", None, "逐元素相加要求什么？"),
            ("基础概念", "填空", "1x1 卷积常用于改变 ______ 数。", None, "不是高宽，主要是哪个维度？"),
            ("形状推导", "短答", "三个分支输出通道分别是 16、24、24，高宽一致，拼接后通道数是多少？", None, "通道相加。"),
            ("代码阅读", "短答", "`torch.cat([y1,y2,y3], dim=1)` 为什么要求高宽一致？", None, "除拼接维外其他维要一致。"),
            ("代码阅读", "短答", "残差代码里 `identity = x` 的作用是什么？", None, "说明 shortcut。"),
            ("错误诊断", "诊断", "Inception 拼接时报 size mismatch，优先检查什么？", None, "分支高宽和 padding。"),
            ("错误诊断", "诊断", "ResNet block 相加时报通道不一致，如何修？", None, "用 1x1 conv。"),
            ("错误诊断", "诊断", "把 `torch.cat` 误写成 `+` 会改变什么语义？", None, "拼接 vs 相加。"),
            ("场景应用", "场景", "为什么 5x5 卷积分支前常放 1x1 卷积？", None, "从降通道和计算量回答。"),
            ("场景应用", "场景", "读陌生开源 CNN 时第一步看什么？", None, "从 forward 数据流回答。"),
            ("概念区分", "匹配", "匹配 Inception / ResNet / 1x1 conv：多分支、跳连、通道变换。", None, "按结构功能写。"),
            ("概念区分", "短答", "拼接和残差相加的 shape 规则有什么不同？", None, "说明 cat 与 add。"),
            ("面试追问", "短答", "残差连接为什么有助于训练深层网络？", None, "提恒等映射和梯度路径。"),
            ("面试追问", "短答", "模块化对读代码有什么帮助？", None, "提局部输入输出。"),
            ("检查清单", "清单", "调试多分支 CNN 时列 5 项检查。", None, "覆盖分支 shape、cat dim、通道、shortcut、输出。"),
            ("代码修正", "诊断", "两个残差分支空间尺寸不同，不能相加，给出一种修法。", None, "调整 stride 或 shortcut。"),
            ("迁移应用", "短答", "为什么高级 CNN 结构仍然可以用普通 CrossEntropy 训练？", None, "输出仍是 logits。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：Inception 和残差连接分别解决什么问题。", None, "串联多尺度、拼接、1x1、深层训练、shortcut、shape。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
])



LESSONS.extend([
    lesson(
        8,
        "加载数据集：Dataset、DataLoader 与 mini-batch",
        "P8【08.加载数据集】",
        "掌握 PyTorch 数据加载的基本分工，理解 epoch、batch size、shuffle、Dataset、DataLoader 如何配合训练循环。",
        "把小数组训练扩展为可迭代的数据管道。",
        [
            ("mini-batch 是训练效率和稳定性的折中", [
                "真实数据集通常不能一次全部塞进模型训练，也不适合每次只看一个样本。mini-batch 的做法是每次取一小批样本，算一次 loss 和梯度，更新一次参数。",
                "一轮 epoch 表示把训练集完整看一遍。batch size 表示每次取多少样本。iteration 通常指一个 mini-batch 的训练 step。三者容易混，但含义不同。",
                "你现在应该能看懂训练日志里的 epoch、batch index 和 loss，不会把 batch size 当成训练轮数。"
            ]),
            ("Dataset 负责“一个样本怎么取”", [
                "`Dataset` 的职责是描述数据集本身。自定义数据集通常实现 `__len__` 和 `__getitem__`。`__len__` 返回样本总数，`__getitem__(idx)` 返回第 idx 个样本和标签。",
                "Dataset 不负责打乱顺序，也不负责组 batch。它像一本可按页码取内容的书。每次给一个索引，就返回一个样本。",
                "你现在应该能判断：读取 CSV、取特征列、取标签列这些工作更适合放在 Dataset 里。"
            ]),
            ("DataLoader 负责“怎样批量迭代”", [
                "`DataLoader` 包装 Dataset，并根据 `batch_size`、`shuffle`、`num_workers` 等设置产生 batch。训练循环里常写 `for x, y in train_loader:`，每次拿到的就是一个 mini-batch。",
                "`shuffle=True` 常用于训练集，让每个 epoch 的样本顺序变化，减少顺序带来的偏差。测试集一般不需要 shuffle，因为评估不更新参数，顺序不该影响指标。",
                "你现在应该能解释 Dataset 和 DataLoader 的分工：一个定义数据，一个定义迭代方式。"
            ]),
            ("训练循环从全量数据改成 batch 数据", [
                "使用 DataLoader 后，训练循环会多一层 batch 迭代。外层遍历 epoch，内层遍历 loader。每个 batch 都执行前向、loss、清梯度、反向、更新。",
                "这个变化看似只是多了一个 `for`，实际影响很大。loss 通常是当前 batch 的平均损失，梯度也是当前 batch 估计出来的方向。一个 epoch 内会更新很多次参数。",
                "你现在应该能数清：如果 1000 个样本、batch size 100，一个 epoch 内大约有 10 次参数更新。"
            ]),
            ("数据类型和形状仍然要在入口处保证", [
                "DataLoader 只是帮你批量取数据，不会替你修正语义。Dataset 返回的特征应该是模型能接收的 float 张量，标签应该符合损失函数要求。比如 BCE 标签用 float，CrossEntropy 标签用 long 类别索引。",
                "很多训练错误其实从 Dataset 就埋下了。CSV 读出的数组可能是 double，标签维度可能多了一列，特征和标签切片可能错位。入口处的 shape 和 dtype 检查非常重要。",
                "你现在应该能在 DataLoader 的第一批数据上打印 `x.shape`、`y.shape`、`x.dtype`、`y.dtype`。"
            ]),
            ("现成数据集和自定义数据集的边界", [
                "PyTorch 生态里有 torchvision、torchtext 等工具，提供 MNIST 这类现成数据集。现成数据集适合教学和基准测试，自定义 Dataset 则适合你自己的 CSV、图片、文本或业务数据。",
                "不管数据来自哪里，进入训练循环后都要变成 `(input, target)` 形式的 batch。理解这一点，后面换 MNIST、图像数据、名字序列时就不会迷路。",
                "你现在应该能把数据加载视为训练链路的一部分，而不是独立的文件读取小事。"
            ]),
        ],
        [
            ("Dataset", "定义数据集长度和单个样本读取方式。", "以为它负责训练循环。"),
            ("DataLoader", "把 Dataset 组织成可迭代 mini-batch。", "以为它会自动设计特征。"),
            ("epoch", "完整遍历训练集一次。", "和 iteration 混淆。"),
            ("batch size", "每次训练 step 使用的样本数。", "误以为越大越好。"),
        ],
        [
            ("自定义 Dataset 骨架", """from torch.utils.data import Dataset, DataLoader

class DiabetesDataset(Dataset):
    def __init__(self, data):
        self.x = torch.tensor(data[:, :-1], dtype=torch.float32)
        self.y = torch.tensor(data[:, [-1]], dtype=torch.float32)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]"""),
            ("DataLoader 接入训练循环", """dataset = DiabetesDataset(data)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for epoch in range(100):
    for x_batch, y_batch in loader:
        pred = model(x_batch)
        loss = criterion(pred, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()"""),
            ("先检查第一批数据", """x_batch, y_batch = next(iter(loader))
print(x_batch.shape, x_batch.dtype)
print(y_batch.shape, y_batch.dtype)"""),
        ],
        [
            ("把 Dataset 和 DataLoader 混成一件事", "职责不清，代码难扩展。", "Dataset 管样本，DataLoader 管 batch。"),
            ("训练集不 shuffle", "样本顺序可能影响梯度路径。", "训练 DataLoader 常设 `shuffle=True`。"),
            ("标签 dtype 和 loss 不匹配", "BCE、CrossEntropy 对标签要求不同。", "按损失函数检查 dtype。"),
            ("最后一个 batch 大小不同没处理", "手写代码若假设固定 batch 可能出错。", "用 `x.size(0)` 或让模型支持变 batch。"),
            ("把 batch size 当 epoch", "误读训练进度。", "区分完整遍历和单次更新。"),
        ],
        [
            ("Dataset", "按索引返回单样本", "不是 batch 生成器"),
            ("DataLoader", "按设置返回 batch", "不是模型"),
            ("epoch", "看完整个训练集一次", "不是一条样本"),
        ],
        [
            ("基础概念", "选择", "`Dataset.__getitem__` 通常返回什么？", ["一个样本及其标签", "优化器", "训练轮数"], "从 Dataset 职责回答。"),
            ("基础概念", "判断", "一个 epoch 表示模型更新一次参数。", None, "考虑一个 epoch 内有多少 batch。"),
            ("基础概念", "填空", "`DataLoader(dataset, batch_size=32)` 表示每次迭代最多返回 ______ 个样本。", None, "填 batch 大小。"),
            ("概念区分", "匹配", "匹配 Dataset / DataLoader / optimizer：取样本、组 batch、更新参数。", None, "按职责写。"),
            ("代码阅读", "短答", "`len(dataset)` 在 DataLoader 中有什么用？", None, "从样本总数和迭代回答。"),
            ("代码阅读", "短答", "为什么训练集常设 `shuffle=True`？", None, "从顺序偏差回答。"),
            ("计算", "短答", "1000 个样本，batch size 128，一个 epoch 大约多少个 batch？", None, "注意最后可能不足 128。"),
            ("形状判断", "短答", "为什么要先打印第一批 `x_batch.shape` 和 `y_batch.shape`？", None, "从入口排错回答。"),
            ("错误诊断", "诊断", "BCE 训练时报 label 类型错误，你会检查什么？", None, "提 float 标签和形状。"),
            ("错误诊断", "诊断", "手写代码假设每个 batch 都是 32，最后一批报错，原因是什么？", None, "最后 batch 可能不足。"),
            ("错误诊断", "诊断", "CSV 切片把最后一列标签放进了特征，可能带来什么问题？", None, "从数据泄漏和训练失真回答。"),
            ("场景应用", "场景", "你有一个图片文件夹和标签 CSV，自定义 Dataset 应该负责哪些事？", None, "列读取图片、变换、取标签。"),
            ("场景应用", "场景", "测试集 DataLoader 是否需要 shuffle？为什么？", None, "评估顺序不影响指标。"),
            ("面试追问", "短答", "mini-batch 相比全量 batch 有什么优势？", None, "提效率和更新频率。"),
            ("面试追问", "短答", "`num_workers` 大致影响什么？", None, "从数据加载并行回答。"),
            ("检查清单", "清单", "写 DataLoader 前列 5 项数据检查。", None, "覆盖长度、getitem、shape、dtype、shuffle。"),
            ("代码修正", "诊断", "`__len__` 返回特征列数而不是样本数，会怎样？", None, "DataLoader 迭代长度错误。"),
            ("迁移应用", "短答", "为什么现成 MNIST 和自定义 CSV 最后都能进入同一种训练循环？", None, "都返回 input/target batch。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：Dataset 和 DataLoader 怎样把数据送进训练循环。", None, "串联样本、batch、epoch、shuffle、shape、训练 step。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
    lesson(
        9,
        "多分类问题：Softmax、交叉熵与 MNIST",
        "P9【09.多分类问题】",
        "理解多分类输出为什么是 logits 向量，掌握 softmax、NLL、CrossEntropyLoss、类别索引标签和训练/测试循环。",
        "从二分类概率扩展到十类数字分类。",
        [
            ("多分类输出是一组类别分数", [
                "二分类可以用一个 logit 表示正类倾向，多分类通常输出一个长度等于类别数的向量。MNIST 有 10 个数字类别，模型输出形状常是 `[batch, 10]`。每一列对应一个类别的原始分数。",
                "这些原始分数叫 logits。它们不要求在 0 到 1 之间，也不要求相加等于 1。预测类别时，通常取 logits 最大的位置，也就是 `argmax(dim=1)`。",
                "你现在应该能看到 `[batch, 10]` 输出，并判断每行代表一个样本的 10 个类别分数。"
            ]),
            ("softmax 把 logits 变成概率分布", [
                "softmax 会对一组 logits 做指数归一化，得到每个类别的概率，所有类别概率相加为 1。某个 logit 越大，对应概率越高。它适合表达“十个类别中选一个”。",
                "但训练时不一定要在模型里显式写 softmax。PyTorch 的 `CrossEntropyLoss` 内部已经包含 `log_softmax` 和 `NLLLoss`。如果你先 softmax 再传给 `CrossEntropyLoss`，反而会让输入语义不对。",
                "你现在应该能区分：展示概率时可以 softmax，训练 CrossEntropyLoss 时传 logits。"
            ]),
            ("标签不是 one-hot，而是类别索引", [
                "`CrossEntropyLoss` 默认要求目标标签是 `LongTensor` 类别索引，形状通常是 `[batch]`。例如数字 7 的标签就是整数 7，不需要写成 `[0,0,0,0,0,0,0,1,0,0]`。",
                "这是多分类新手最常见的坑之一。输出是 `[batch, num_classes]`，标签却是 `[batch]`。二者形状不同是正常的，因为输出给每个类别打分，标签只告诉正确类别编号。",
                "你现在应该能解释为什么 MNIST 标签不是 one-hot，也能检查标签 dtype 是否是 long。"
            ]),
            ("全连接 MNIST 先把图像展平", [
                "MNIST 图像原始形状通常是 `[batch, 1, 28, 28]`。如果用全连接层处理，需要先展平成 `[batch, 784]`。这里的 784 来自 `1 * 28 * 28`。",
                "展平会丢掉二维空间结构，但它让我们能先用全连接网络理解多分类流程。后面的 CNN 会重新利用图像的空间结构。",
                "你现在应该能说明为什么全连接 MNIST 要 `view(-1, 784)`，以及 `-1` 代表让 PyTorch 自动推断 batch 维。"
            ]),
            ("训练和测试要分开写", [
                "训练循环负责更新参数：前向、loss、清梯度、反向、step。测试循环只负责评估：切 `eval()`、关梯度、前向、取预测、统计正确数。",
                "如果测试时忘记 `no_grad()`，结果可能仍然对，但会浪费内存。如果忘记 `eval()`，含 Dropout 或 BatchNorm 的模型结果会不稳定。虽然这节的全连接网络可能没有这些层，也要养成习惯。",
                "你现在应该能写出一个最小 test loop，并说明它和 train loop 哪几行不同。"
            ]),
            ("多分类错误常来自维度和损失函数", [
                "多分类训练最常见错误有三个：模型输出维度不是类别数，标签用了 one-hot 或 float，训练前手动 softmax 再用 `CrossEntropyLoss`。这些错误都不是数学难题，而是输入约定不清。",
                "调试时先看三件事：`logits.shape == [batch, num_classes]`，`target.shape == [batch]`，`target.dtype == torch.long`。这三项对了，多分类损失一般就能工作。",
                "你现在应该能用这三项检查快速定位多数 CrossEntropyLoss 报错。"
            ]),
        ],
        [
            ("logits", "模型输出的原始类别分数。", "误以为它们已经是概率。"),
            ("softmax", "把一组类别分数归一化为概率分布。", "训练 CrossEntropyLoss 前重复使用。"),
            ("CrossEntropyLoss", "多分类常用损失，内部包含 log_softmax 和 NLLLoss。", "把 one-hot float 标签直接传入默认用法。"),
            ("argmax", "取分数最大的位置作为预测类别。", "误以为它可用于反向训练。"),
        ],
        [
            ("MNIST 全连接模型", """class MnistNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 512)
        self.fc2 = nn.Linear(512, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)  # logits"""),
            ("CrossEntropyLoss 的输入约定", """logits = model(images)          # [batch, 10]
target = labels.long()          # [batch]
loss = nn.CrossEntropyLoss()(logits, target)"""),
            ("测试循环", """model.eval()
correct = 0
with torch.no_grad():
    for images, labels in test_loader:
        logits = model(images)
        pred = logits.argmax(dim=1)
        correct += (pred == labels).sum().item()"""),
        ],
        [
            ("先 softmax 再 CrossEntropyLoss", "输入约定错误，数值效果变差。", "训练时传 logits。"),
            ("标签写成 one-hot", "默认 CrossEntropyLoss 期望类别索引。", "用 `[batch]` long 标签。"),
            ("忘记展平图像", "全连接层收到 4D 输入可能不符合预期。", "进入 Linear 前变成 `[batch, 784]`。"),
            ("argmax 维度写错", "可能沿 batch 维取最大，预测全乱。", "多分类通常 `dim=1`。"),
            ("测试时仍在训练模式", "含特定层时评估结果不稳定。", "测试前 `model.eval()`。"),
        ],
        [
            ("logits", "训练损失的输入", "不是归一化概率"),
            ("softmax 概率", "解释或可视化用", "通常不传给 CrossEntropyLoss"),
            ("类别索引", "正确答案编号", "不是 one-hot 向量"),
        ],
        [
            ("基础概念", "选择", "MNIST 十分类模型最后输出维度通常是多少？", ["10", "1", "784"], "每个类别一个分数。"),
            ("基础概念", "判断", "`CrossEntropyLoss` 默认输入应该是 softmax 后概率。", None, "判断内部是否包含 log_softmax。"),
            ("基础概念", "填空", "MNIST 图像 `[1,28,28]` 展平后特征数是 ______。", None, "计算乘积。"),
            ("形状判断", "短答", "logits `[64,10]`、labels `[64]` 对 CrossEntropyLoss 是否合理？为什么？", None, "说明输出和目标约定。"),
            ("代码阅读", "短答", "`x.view(x.size(0), -1)` 中 `x.size(0)` 保留什么？", None, "保留 batch。"),
            ("代码阅读", "短答", "`argmax(dim=1)` 为什么沿 dim=1？", None, "dim=1 是类别维。"),
            ("错误诊断", "诊断", "把标签做成 one-hot 后传给 CrossEntropyLoss，哪里不稳？", None, "说默认目标要求。"),
            ("错误诊断", "诊断", "模型最后输出 `[batch,1]` 却做 MNIST 十分类，会怎样？", None, "类别分数不够。"),
            ("错误诊断", "诊断", "测试循环忘记 `no_grad()` 的后果是什么？", None, "从计算图和内存回答。"),
            ("场景应用", "场景", "如果分类任务有 18 类，最后一层应该输出多少维？", None, "类别数对应输出维。"),
            ("场景应用", "短答", "什么时候需要 softmax 概率？", None, "展示置信度或阈值分析。"),
            ("概念区分", "匹配", "匹配 logits / softmax / argmax：原始分数、概率分布、预测类别。", None, "按顺序写。"),
            ("概念区分", "短答", "二分类 BCE 和多分类 CrossEntropy 的标签形式有什么不同？", None, "从 float 0/1 与 long 类别索引回答。"),
            ("面试追问", "短答", "为什么全连接处理图像要展平？", None, "从 Linear 输入要求回答。"),
            ("面试追问", "短答", "为什么 CNN 后面才重新讲图像空间结构？", None, "全连接展平会丢空间关系。"),
            ("检查清单", "清单", "调试 CrossEntropyLoss 前列 5 项检查。", None, "覆盖 logits shape、label shape、dtype、softmax、类别数。"),
            ("代码修正", "诊断", "代码中 `loss = criterion(torch.softmax(logits, dim=1), labels)` 应怎样改？", None, "传 logits。"),
            ("迁移应用", "短答", "从 MNIST 10 类换成 26 个字母分类，需要改哪些地方？", None, "输出层、标签范围、指标。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：多分类模型如何从图像输出一个类别。", None, "串联展平、logits、softmax、CrossEntropy、标签索引、argmax、测试。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
])



LESSONS.extend([
    lesson(
        6,
        "逻辑斯蒂回归：把线性输出变成二分类概率",
        "P6【06.逻辑斯蒂回归】",
        "理解二分类任务为什么不能直接用线性回归输出，掌握 sigmoid、二分类交叉熵、阈值判断和 PyTorch 中 `BCELoss` / `BCEWithLogitsLoss` 的区别。",
        "从回归数值过渡到分类概率。",
        [
            ("分类任务先改变输出含义", [
                "线性回归输出的是连续数值，比如预测房价、温度或 `y=2x` 里的数。二分类任务输出的是类别，例如是否患病、是否垃圾邮件、是否通过。类别不是任意实数，通常要表达为概率或标签。",
                "逻辑斯蒂回归在形式上仍然先做线性变换：`z = xw + b`。不同的是，它会把 `z` 送入 sigmoid 函数，把任意实数压到 0 到 1 之间。这个数可以解释为属于正类的概率。",
                "你现在应该能说清：逻辑斯蒂回归不是“线性回归换个名字”，它改变了输出解释和损失函数。"
            ]),
            ("sigmoid 负责把分数压成概率", [
                "sigmoid 的公式是 `1 / (1 + exp(-z))`。当 `z` 很大时，输出接近 1；当 `z` 很小时，输出接近 0；当 `z=0` 时，输出是 0.5。它把线性分数变成可以用阈值判断的概率。",
                "这个概率通常是正类概率。如果模型输出 0.8，可以理解为模型更倾向于正类；输出 0.2，则更倾向于负类。默认阈值常取 0.5，但真实项目里阈值可以根据误报和漏报成本调整。",
                "你现在应该能看到一个 sigmoid 输出，并判断它对应正类还是负类，也能说明阈值不是模型参数，而是决策规则。"
            ]),
            ("二分类交叉熵比 MSE 更适合分类", [
                "二分类交叉熵会惩罚“对真实类别给低概率”的情况。真实标签是 1 时，模型越接近 1，loss 越小；真实标签是 0 时，模型越接近 0，loss 越小。它直接服务于概率分类。",
                "如果用 MSE 训练 sigmoid 分类器，也不是完全不能算，但梯度性质通常不如交叉熵适合分类。交叉熵对自信但错误的预测惩罚更强，这正是分类任务需要的信号。",
                "你现在应该能解释为什么回归常用 MSE，而二分类更常用 BCE。"
            ]),
            ("PyTorch 写法要注意 logits 和概率", [
                "`BCELoss` 要求输入已经是 sigmoid 后的概率。`BCEWithLogitsLoss` 则要求输入原始 logits，它内部会做 sigmoid 和 BCE，并且数值稳定性更好。现代 PyTorch 中更推荐后者。",
                "这两个损失最常见的错误是重复 sigmoid，或者把 logits 直接喂给 `BCELoss`。重复 sigmoid 会让梯度变弱； logits 直接进 `BCELoss` 则不满足输入范围要求。",
                "你现在应该能判断：如果模型最后一层没有 sigmoid，就用 `BCEWithLogitsLoss`；如果模型 forward 已经 sigmoid，就用 `BCELoss`。"
            ]),
            ("标签形状和类型要对齐", [
                "二分类标签常写成 0 或 1，但进入 BCE 时通常要是浮点张量，形状也要和模型输出对齐。例如输出是 `[batch, 1]`，标签最好也是 `[batch, 1]` 的 float。",
                "标签如果是整数类别索引，交给 BCE 可能出现类型或广播问题。广播有时不会报错，却会让 loss 计算含义变坏。训练前打印 `pred.shape` 和 `target.shape` 是很朴素但有效的习惯。",
                "你现在应该能在写二分类训练前检查：输出范围、损失函数、标签 dtype、标签 shape 和阈值规则。"
            ]),
            ("二分类评估不只看 loss", [
                "训练时看 loss，评估时还要看准确率、精确率、召回率等指标。尤其是类别不平衡时，准确率可能很骗人。比如 95% 都是负类，模型全预测负类也有 95% 准确率，但没有识别正类能力。",
                "阈值会影响最终指标。阈值低，正类预测更多，召回可能上升，误报也可能增加；阈值高，模型更保守，精确率可能上升，漏报也可能增加。",
                "你现在应该能把“模型输出概率”和“业务做出分类决策”分开看。"
            ]),
        ],
        [
            ("logit", "sigmoid 之前的原始线性分数，可取任意实数。", "误以为它已经是概率。"),
            ("sigmoid", "把实数压到 0-1 区间的函数。", "以为输出一定校准可信。"),
            ("BCE", "二分类交叉熵，衡量预测概率和 0/1 标签的差距。", "把它用于多分类类别索引。"),
            ("阈值", "把概率转成类别标签的决策边界。", "误以为阈值一定必须是 0.5。"),
        ],
        [
            ("二分类模型：推荐 logits 写法", """class BinaryClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(8, 1)

    def forward(self, x):
        return self.linear(x)  # 返回 logits，不在这里 sigmoid

criterion = nn.BCEWithLogitsLoss()"""),
            ("评估时再把 logits 变成概率和标签", """model.eval()
with torch.no_grad():
    logits = model(x)
    prob = torch.sigmoid(logits)
    pred = (prob >= 0.5).float()"""),
            ("错误示例：重复 sigmoid", """# 错误示例
prob = torch.sigmoid(model(x))
loss = nn.BCEWithLogitsLoss()(prob, y)
# BCEWithLogitsLoss 内部已经包含 sigmoid"""),
        ],
        [
            ("把 logits 当概率", "logits 可能小于 0 或大于 1，不能直接阈值为概率。", "先 sigmoid，或用带 logits 的损失。"),
            ("重复 sigmoid", "梯度可能变弱，训练变慢。", "模型输出和 loss 输入约定保持一致。"),
            ("标签 dtype 不对", "BCE 需要 float 标签，整数类别常导致问题。", "把标签转成 `float()` 并对齐形状。"),
            ("只看准确率", "类别不平衡时会误判模型有效。", "同时看召回率、精确率或混淆矩阵。"),
            ("阈值永远固定 0.5", "业务成本不同，最佳阈值可能不同。", "根据误报/漏报成本调阈值。"),
        ],
        [
            ("logit", "未压缩的模型分数", "不是概率"),
            ("probability", "sigmoid 后的 0-1 值", "不是最终业务动作"),
            ("label", "0/1 真实类别", "不是损失函数"),
        ],
        [
            ("基础概念", "选择", "sigmoid 的主要作用是什么？", ["把任意实数映射到 0-1", "把类别变成 one-hot", "清空梯度"], "关注输出范围。"),
            ("基础概念", "判断", "logits 可以直接当成概率解释。", None, "看 logits 的取值范围。"),
            ("基础概念", "填空", "二分类中，默认常用阈值是 ______，但它可以按业务成本调整。", None, "填常见概率分界。"),
            ("损失理解", "短答", "为什么二分类更常用 BCE 而不是 MSE？", None, "从概率和错误惩罚回答。"),
            ("代码阅读", "短答", "`BCEWithLogitsLoss` 的输入应该是 logits 还是 sigmoid 后概率？", None, "说明内部包含什么。"),
            ("代码阅读", "短答", "如果使用 `BCELoss`，模型 forward 最后一层通常要做什么？", None, "说出 sigmoid。"),
            ("形状判断", "短答", "二分类输出 `[batch, 1]` 时，标签最好是什么形状和 dtype？", None, "回答 shape 和 float。"),
            ("错误诊断", "诊断", "把 sigmoid 后的概率传给 `BCEWithLogitsLoss`，错在哪？", None, "说明重复 sigmoid。"),
            ("错误诊断", "诊断", "类别极不平衡时只看准确率有什么问题？", None, "举全预测多数类的例子。"),
            ("错误诊断", "诊断", "模型输出 0.8 但仍预测负类，可能是什么设置导致的？", None, "考虑阈值。"),
            ("场景应用", "场景", "医疗筛查中阈值调低可能带来什么好处和代价？", None, "从召回和误报回答。"),
            ("场景应用", "场景", "垃圾邮件识别中误报成本高时，阈值可能怎样调？", None, "从减少误报回答。"),
            ("概念区分", "匹配", "匹配 logit / probability / prediction：原始分数、概率、阈值后的类别。", None, "按处理顺序回答。"),
            ("概念区分", "短答", "逻辑斯蒂回归和线性回归的相同点与不同点是什么？", None, "至少提线性部分、输出含义、损失。"),
            ("面试追问", "短答", "为什么 sigmoid 输出可以用于二分类？", None, "从 0-1 和阈值回答。"),
            ("面试追问", "短答", "`BCEWithLogitsLoss` 为什么通常更推荐？", None, "提数值稳定和少犯错。"),
            ("检查清单", "清单", "写二分类模型前列 5 项检查。", None, "覆盖 logits/prob、loss、label shape、dtype、threshold。"),
            ("代码修正", "诊断", "标签是 `[batch]`，输出是 `[batch,1]`，可能有什么隐患？", None, "提广播和形状不一致。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：逻辑斯蒂回归如何把线性模型变成二分类模型。", None, "串联 logit、sigmoid、概率、BCE、阈值、评估。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个能动手检查的动作。"),
        ],
    ),
    lesson(
        7,
        "多维特征输入：矩阵形状与前馈网络",
        "P7【07.处理多维特征的输入】",
        "理解多维特征如何进入线性层，掌握 batch 维、特征维、层间维度匹配和多层网络 forward 的形状推导。",
        "从单特征线性模型扩展到多特征、多层网络。",
        [
            ("多维特征先改变输入形状", [
                "真实任务很少只有一个输入特征。糖尿病预测这类数据通常有多个指标，每个样本是一行，每列是一个特征。把数据送进模型前，你要知道张量形状通常是 `[batch_size, num_features]`。",
                "`batch_size` 表示一次送进模型的样本数，`num_features` 表示每个样本有多少个特征。线性层关心的是最后一维，也就是特征数。`nn.Linear(8, 6)` 表示每个样本有 8 个输入特征，输出 6 个新特征。",
                "你现在应该能看到一个二维张量，分清哪一维是样本数，哪一维是特征数。"
            ]),
            ("线性层本质是矩阵乘法", [
                "对多维输入来说，线性层不再是简单的 `x*w`，而是矩阵乘法加偏置。输入 `[N, in_features]` 乘上权重转置后得到 `[N, out_features]`。batch 维 `N` 会保留，特征维会被线性层改写。",
                "这就是为什么层与层之间必须维度对齐。上一层输出多少特征，下一层的 `in_features` 就应该是多少。写错会报形状不匹配，或者更隐蔽地让网络结构不符合你的设计。",
                "你现在应该能从一串 `Linear` 层推导每一层输出形状。"
            ]),
            ("多层网络需要非线性激活", [
                "如果只是把多个线性层连续相乘，中间没有激活函数，整体仍然等价于一个线性变换。多层网络真正变强，是因为在线性层之间插入 sigmoid、ReLU 等非线性激活。",
                "课程里用 sigmoid 演示前馈网络。现代实践中，隐藏层更常用 ReLU 或其变体，因为 sigmoid 在深层网络中更容易出现梯度变小。输出层是否用 sigmoid 取决于任务和 loss。",
                "你现在应该能说明：多层不是为了看起来复杂，而是为了通过非线性组合表达更复杂关系。"
            ]),
            ("forward 写的是数据路径", [
                "`forward` 不是简单把层罗列出来，而是定义数据从输入到输出的路径。每一步的输出都会成为下一步输入。你需要保证形状对齐，也要知道激活函数放在哪里。",
                "例如 `x = self.sigmoid(self.linear1(x))` 先做线性变换，再把结果压到 0-1。后面接 `linear2` 时，`linear2` 的输入特征数必须等于 `linear1` 的输出特征数。",
                "你现在应该能逐行解释一个多层 `forward`：这一行读入什么形状，输出什么形状，为什么下一层能接上。"
            ]),
            ("特征尺度会影响训练", [
                "多维特征常有不同单位和范围。一个特征可能在 0-1，另一个可能在几百。未经处理的尺度差异会影响梯度大小和优化稳定性，让某些特征在训练中占据过大影响。",
                "课程重点是结构，但真实项目里通常要做标准化或归一化。标准化不是为了让数据好看，而是让优化过程更稳定，让不同特征在相近尺度上参与训练。",
                "你现在应该能在训练不稳定时想到检查输入特征尺度，而不是只改网络层数。"
            ]),
            ("从单层到多层，调试重点转向 shape", [
                "多层网络的 bug 很多来自 shape。输入列数、隐藏层宽度、输出维度、标签形状，每一处都要对上。打印形状是最有效的调试方法之一。",
                "不要害怕在 `forward` 里临时打印 `x.shape`。等结构稳定后再删掉。复杂网络中，形状推导是读代码的基本功。",
                "你现在应该能用表格写出一个网络的层、输入形状、输出形状和激活函数。"
            ]),
        ],
        [
            ("batch 维", "一次送入模型的样本数量维度。", "误以为它是特征数。"),
            ("特征维", "每个样本包含的输入变量数量。", "和 batch 维混淆。"),
            ("隐藏层", "位于输入和输出之间的可学习变换层。", "以为层越多一定越好。"),
            ("激活函数", "给网络引入非线性的函数。", "认为多层线性层本身就足够非线性。"),
        ],
        [
            ("多维输入的三层网络", """class DiabetesModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(8, 6)
        self.linear2 = nn.Linear(6, 4)
        self.linear3 = nn.Linear(4, 1)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = torch.relu(self.linear2(x))
        return self.linear3(x)"""),
            ("形状推导", """x = torch.randn(32, 8)   # 32 个样本，每个 8 个特征
h1 = model.linear1(x)    # [32, 6]
h2 = model.linear2(torch.relu(h1))  # [32, 4]"""),
            ("错误示例：层间维度接不上", """# 错误示例
self.linear1 = nn.Linear(8, 6)
self.linear2 = nn.Linear(8, 4)  # 应该接收 6，而不是 8"""),
        ],
        [
            ("混淆 batch 和 feature", "Linear 的 `in_features` 写错。", "看输入最后一维。"),
            ("层间维度不连续", "矩阵乘法形状报错。", "上一层 out_features 等于下一层 in_features。"),
            ("多层线性不加激活", "整体仍等价于一层线性。", "隐藏层之间加入非线性激活。"),
            ("忽略特征尺度", "训练可能慢或不稳定。", "对输入做标准化或归一化。"),
            ("输出维度和任务不符", "loss 和标签对不上。", "回归/二分类/多分类分别检查输出维度。"),
        ],
        [
            ("batch size", "一次处理多少样本", "不是每个样本有多少列"),
            ("in_features", "每个样本输入特征数", "不是样本总数"),
            ("out_features", "该层输出的新特征数", "不是类别标签本身"),
        ],
        [
            ("基础概念", "选择", "`nn.Linear(8, 6)` 中 8 表示什么？", ["每个样本输入特征数", "batch size", "训练轮数"], "看 Linear 的参数名。"),
            ("基础概念", "判断", "输入形状 `[32, 8]` 中，32 通常是特征数。", None, "判断 batch 和 feature。"),
            ("基础概念", "填空", "上一层 `Linear(8, 6)` 的输出接下一层时，下一层的 `in_features` 应该是 ______。", None, "填上一层输出特征数。"),
            ("形状推导", "短答", "输入 `[16, 8]` 经过 `Linear(8, 4)` 后形状是什么？", None, "batch 维保留。"),
            ("形状推导", "短答", "为什么线性层通常看输入最后一维？", None, "从特征维回答。"),
            ("代码阅读", "短答", "解释 `x = torch.relu(self.linear1(x))` 的两步操作。", None, "先线性，再激活。"),
            ("代码阅读", "短答", "为什么多个线性层之间要加激活函数？", None, "说明没有激活仍等价线性。"),
            ("错误诊断", "诊断", "`mat1 and mat2 shapes cannot be multiplied` 常见原因是什么？", None, "从层间维度回答。"),
            ("错误诊断", "诊断", "输入特征尺度差异很大可能导致什么训练问题？", None, "从梯度和优化稳定性回答。"),
            ("错误诊断", "诊断", "二分类模型最后输出 `[batch,4]`，但标签是 `[batch,1]`，哪里不对？", None, "从任务输出维度回答。"),
            ("场景应用", "场景", "糖尿病数据有 8 个特征，第一层该怎么写？", None, "写出一个 Linear。"),
            ("场景应用", "场景", "如果新增 2 个特征，模型第一层需要改哪里？", None, "从 in_features 回答。"),
            ("概念区分", "匹配", "匹配 batch size / in_features / out_features 到样本数、输入列数、输出列数。", None, "按 shape 含义写。"),
            ("概念区分", "短答", "隐藏层宽度和输出类别数有什么区别？", None, "从中间表示和任务输出回答。"),
            ("面试追问", "短答", "为什么多维输入本质上是矩阵乘法？", None, "用 `[N,in] -> [N,out]` 解释。"),
            ("面试追问", "短答", "多层网络比单层线性模型强在哪里？", None, "提非线性组合。"),
            ("检查清单", "清单", "调试多层网络 shape 时列 5 项检查。", None, "覆盖输入、每层、输出、标签、loss。"),
            ("代码修正", "诊断", "给出 `Linear(8,6)` 后接 `Linear(8,4)` 的修正。", None, "写正确 in_features。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：多维特征怎样通过多层网络变成预测。", None, "串联 batch、feature、Linear、activation、shape、output。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
])



LESSONS.extend([
    lesson(
        4,
        "反向传播：计算图里的链式法则",
        "P4【04.反向传播】",
        "理解前向传播如何建立计算图，反向传播如何按链式法则把梯度传回参数，并能解释 `backward()`、叶子张量和梯度累积。",
        "把计算图、局部梯度、链式法则、标量 loss 和梯度清零讲透。",
        [
            ("反向传播先依赖一次前向传播", [
                "反向传播不是单独发生的。你必须先做前向传播：输入经过一连串计算得到预测，再由预测和标签得到 loss。这个过程中，每个中间结果都会记录它来自哪些运算，形成一张计算图。",
                "计算图像一条有方向的账本。前向时记录“谁由谁算出来”；反向时从 loss 出发，沿着图往回算每个参数对 loss 的影响。没有前向建立的图，反向就不知道该沿哪条路径传梯度。",
                "你现在应该能解释：`loss.backward()` 不是重新前向计算，而是在已有计算图上反向传播梯度。"
            ]),
            ("链式法则把局部影响连成整体影响", [
                "一个参数通常不会直接变成 loss，中间会经过多步计算。链式法则说，如果 `w` 影响 `y_hat`，`y_hat` 又影响 loss，那么 loss 对 `w` 的影响可以由这些局部影响相乘得到。",
                "反向传播的高效之处在于复用中间梯度。每个节点只需要知道上游传来的梯度和本地运算的导数，就能把梯度继续传给自己的输入。复杂网络也是这个原则，只是节点更多。",
                "你现在应该能用“局部导数 × 上游梯度”解释反向传播，而不是只把它背成一个黑盒算法。"
            ]),
            ("PyTorch 自动求导记录的是张量运算", [
                "在 PyTorch 里，如果一个张量设置了 `requires_grad=True`，并参与可求导运算，框架就会记录计算图。最终对标量 loss 调用 `backward()` 后，梯度会写到需要梯度的叶子张量的 `.grad` 上。",
                "叶子张量通常是你直接创建并要求求梯度的参数。中间张量默认不保留 `.grad`，因为它们不是优化器要更新的对象。这个设计减少内存，也让参数更新目标更清楚。",
                "你现在应该能判断：为什么 `w.grad` 有值，而某个中间变量的 `.grad` 可能是空。"
            ]),
            ("loss 通常必须是标量", [
                "调用 `backward()` 时，最常见写法是对标量 loss 调用。标量 loss 对所有参数都有一个清晰的优化目标。如果 loss 是向量，PyTorch 需要你额外提供反向传播的初始梯度，否则不知道向量的每一项该怎样合成目标。",
                "这也是损失函数默认会做 reduction 的原因。比如 MSE 可以对每个样本算误差，再求均值。均值后的 loss 是一个标量，就能自然地驱动所有参数更新。",
                "你现在应该能说明为什么训练代码里常见 `loss = criterion(pred, target)` 之后直接 `loss.backward()`。"
            ]),
            ("梯度会累积，清零不是装饰", [
                "PyTorch 的梯度默认是累积的。每次 `backward()` 会把新梯度加到已有 `.grad` 上，而不是自动覆盖。这样设计是为了支持梯度累积等高级用法，但初学训练循环里通常每个 batch 前都要清零。",
                "如果忘记 `optimizer.zero_grad()`，参数更新会混入上一批数据的梯度。loss 可能仍然变化，但方向已经不是当前 batch 的真实梯度，训练会变得难以解释。",
                "你现在应该能把 `zero_grad()` 放在正确位置，并解释它为什么通常在 `backward()` 前。"
            ]),
            ("反向传播和优化器分工不同", [
                "`backward()` 只负责算梯度并写入 `.grad`，它不会自动改参数。`optimizer.step()` 才会根据这些梯度更新参数。把这两件事分开，是 PyTorch 训练循环的基本分工。",
                "这也解释了很多常见错误：只 `backward()` 不 `step()`，参数不会动；只 `step()` 不 `backward()`，优化器没有新梯度可读；清零位置错了，梯度会被提前抹掉或错误累积。",
                "你现在应该能读懂一次训练 step 的状态变化：loss 建图，backward 写梯度，step 改参数，zero_grad 清理旧梯度。"
            ]),
        ],
        [
            ("计算图", "记录张量运算依赖关系的有向图。", "以为它是手动画出来才存在。"),
            ("反向传播", "从 loss 出发按链式法则计算各参数梯度。", "以为它会直接更新参数。"),
            ("叶子张量", "通常是用户创建、需要求梯度、优化器会更新的张量。", "把所有中间变量都当成参数。"),
            ("梯度累积", "多次 backward 的梯度会加到 `.grad` 上。", "误以为每次 backward 自动清空。"),
        ],
        [
            ("最小 autograd 示例", """import torch

w = torch.tensor([1.0], requires_grad=True)
x = torch.tensor([2.0])
y = torch.tensor([4.0])

y_hat = x * w
loss = (y_hat - y) ** 2
loss.backward()
print(w.grad)  # tensor([-8.])"""),
            ("错误示例：忘记清零梯度", """for x, y in loader:
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
    # 少了 optimizer.zero_grad()
    # 下一轮 backward 会把新梯度加到旧梯度上"""),
            ("推荐训练顺序", """for x, y in loader:
    pred = model(x)
    loss = criterion(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()"""),
        ],
        [
            ("认为 backward 会更新参数", "`backward()` 只写梯度，参数值不变。", "调用 `optimizer.step()` 才更新。"),
            ("忘记清零梯度", "新旧梯度累积，更新方向混乱。", "每个 batch 通常先 `optimizer.zero_grad()`。"),
            ("对非标量 loss 直接 backward", "PyTorch 可能不知道初始梯度。", "先 reduce 成标量或显式提供 gradient。"),
            ("以为所有 `.grad` 都有值", "中间张量默认不保留梯度。", "关注叶子参数的 `.grad`。"),
            ("用 `.data` 随意改参数", "可能绕开 autograd，破坏计算图语义。", "用优化器或 `torch.no_grad()` 下的明确更新。"),
        ],
        [
            ("forward", "建立计算图并得到预测/loss", "不是参数更新"),
            ("backward", "沿计算图写入梯度", "不是优化器"),
            ("step", "根据梯度改参数", "不是计算梯度"),
        ],
        [
            ("基础概念", "选择", "`loss.backward()` 的主要作用是什么？", ["沿计算图计算梯度并写到参数 `.grad`", "立刻清空梯度", "加载下一批数据"], "区分 backward 和 optimizer。"),
            ("基础概念", "判断", "PyTorch 默认会在每次 `backward()` 前自动清空旧梯度。", None, "想想为什么要写 `zero_grad()`。"),
            ("基础概念", "填空", "反向传播使用的核心微积分规则是 ______。", None, "它把局部导数连起来。"),
            ("链路理解", "排序", "排序：`optimizer.step()` / `loss.backward()` / `optimizer.zero_grad()` / `pred = model(x)`。", None, "按一次训练 step 写。"),
            ("代码阅读", "短答", "在最小示例中，为什么梯度最后写到 `w.grad`？", None, "从 `requires_grad=True` 和叶子张量回答。"),
            ("代码阅读", "短答", "`loss = (y_hat - y) ** 2` 为什么能继续反传到 `w`？", None, "说明计算图保存了依赖。"),
            ("错误诊断", "诊断", "训练循环漏掉 `optimizer.step()`，会发生什么？", None, "说清梯度有但参数不更新。"),
            ("错误诊断", "诊断", "训练循环漏掉 `optimizer.zero_grad()`，会发生什么？", None, "说清梯度累积。"),
            ("错误诊断", "诊断", "某个中间张量 `.grad` 是 None，一定是错误吗？", None, "从中间张量默认不保留回答。"),
            ("概念区分", "匹配", "匹配 forward / backward / step：建图、写梯度、改参数。", None, "不要混用概念。"),
            ("概念区分", "短答", "叶子张量和中间张量的区别是什么？", None, "从创建方式和是否优化回答。"),
            ("场景应用", "场景", "如果你想累积 4 个 batch 再更新一次，`zero_grad()` 应该怎样调整？", None, "说明这时梯度累积是有意使用。"),
            ("场景应用", "短答", "为什么评估阶段不需要反向传播？", None, "从不更新参数回答。"),
            ("面试追问", "短答", "用 2-3 句话解释计算图。", None, "说清前向记录和反向使用。"),
            ("面试追问", "短答", "`backward()` 和 `optimizer.step()` 的分工是什么？", None, "分别说。"),
            ("检查清单", "清单", "梯度相关 bug 你会检查哪 5 件事？", None, "覆盖 requires_grad、loss 标量、清零、backward、step。"),
            ("代码修正", "诊断", "有人把 `optimizer.zero_grad()` 放在 `loss.backward()` 后、`step()` 前，会怎样？", None, "说清梯度被清掉，step 读不到。"),
            ("迁移应用", "短答", "为什么复杂网络仍然能用同一个 `backward()`？", None, "从链式法则和计算图回答。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：前向传播、反向传播和参数更新各自做什么。", None, "串联计算图、loss、梯度累积、zero_grad 和 step。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个能检查训练循环的动作。"),
        ],
    ),
    lesson(
        5,
        "用 PyTorch 实现线性回归：Module、Loss 与 Optimizer",
        "P5【05.用PyTorch实现线性回归】",
        "掌握 PyTorch 训练代码的四步结构：准备数据、定义 `nn.Module`、构造损失和优化器、执行训练循环。",
        "把手写线性回归迁移到 PyTorch 框架写法。",
        [
            ("PyTorch 版本的线性回归是在重写流程，不是重写数学", [
                "前几讲已经用手写方式做过线性回归：预测、计算损失、求梯度、更新权重。第五讲换成 PyTorch，不是因为数学变了，而是框架开始接管重复工作。你仍然在做同一件事，只是把参数管理、自动求导和优化步骤交给标准组件。",
                "这种转变很关键。手写版本适合理解机制，PyTorch 版本适合扩展到更复杂网络。`nn.Linear` 可以从一维回归扩到多维输入，`nn.Module` 可以组合很多层，优化器可以管理大量参数。",
                "你现在应该能看出 PyTorch 代码虽然行数多了一点，但结构更能迁移到 CNN、RNN 等后续模型。"
            ]),
            ("第一步：数据必须是张量并且形状对", [
                "PyTorch 模型吃的是 `Tensor`。线性回归例子里，输入 `x_data` 和标签 `y_data` 通常写成形状 `[N, 1]`，其中 `N` 是样本数，`1` 是每个样本的特征数。这个二维形状和 `nn.Linear(1, 1)` 对齐。",
                "很多初学报错不是算法错，而是形状错。`[3]` 和 `[3, 1]` 看起来都装了三个数字，但对线性层来说含义不同。线性层默认把最后一维当作特征维，输入特征数必须等于 `in_features`。",
                "你现在应该能在写模型前先检查 `x.shape`、`y.shape` 和 `nn.Linear(in_features, out_features)` 是否一致。"
            ]),
            ("第二步：Module 管理参数和前向逻辑", [
                "在 PyTorch 中，自定义模型通常继承 `nn.Module`。你在 `__init__` 里定义层，例如 `self.linear = nn.Linear(1, 1)`；在 `forward` 里写数据怎样通过这些层，例如 `return self.linear(x)`。",
                "`nn.Module` 的价值不只是让代码好看。它会登记子模块和参数，`model.parameters()` 才能把这些参数交给优化器。你如果把层写成普通局部变量，优化器可能根本找不到要更新的参数。",
                "你现在应该能解释为什么层要写成 `self.linear`，以及为什么调用 `model(x)` 会自动进入 `forward`。"
            ]),
            ("第三步：Loss 和 Optimizer 接管训练目标与更新", [
                "`nn.MSELoss()` 负责把预测和标签变成标量损失。`torch.optim.SGD(model.parameters(), lr=...)` 负责读取模型参数的梯度并更新参数。损失函数回答“哪里错了”，优化器回答“参数怎么改”。",
                "注意优化器拿到的是 `model.parameters()`，不是模型输出，也不是 loss。它管理的是会被更新的权重和偏置。loss 通过 `backward()` 把梯度写到这些参数上，优化器再读这些 `.grad`。",
                "你现在应该能把 criterion 和 optimizer 的分工说清楚，不会把两者都笼统叫成“训练函数”。"
            ]),
            ("第四步：训练循环仍然是四个动作", [
                "每轮训练的核心动作没有变：前向预测、计算 loss、清梯度并反向传播、参数更新。PyTorch 版本中通常写成 `y_pred = model(x_data)`、`loss = criterion(y_pred, y_data)`、`optimizer.zero_grad()`、`loss.backward()`、`optimizer.step()`。",
                "这里的顺序有含义。你必须先有 loss，才能反向传播；必须先反向传播，优化器才有梯度可读；必须在下一次反向前清掉旧梯度，避免累积干扰。训练循环看似模板，其实每一行都对应状态变化。",
                "你现在应该能盯着一个训练循环，指出每行是在建图、算目标、清梯度、写梯度还是改参数。"
            ]),
            ("预测阶段要和训练阶段分开", [
                "训练完成后，你可能用 `model(torch.tensor([[4.0]]))` 预测 x=4 的结果。预测阶段通常不需要梯度，应放在 `with torch.no_grad()` 里。如果模型含 Dropout 或 BatchNorm，还要先 `model.eval()`。",
                "线性回归例子没有复杂层，训练和评估模式差异不明显，但从现在就养成习惯很重要。后面 CNN 和 RNN 项目中，评估状态写错会直接影响结果。",
                "你现在应该能写出一个最小预测片段，并说明它为什么不需要 `backward()`。"
            ]),
        ],
        [
            ("nn.Module", "PyTorch 中所有神经网络模块的基类，用来组织层、参数和前向计算。", "只把它当成普通 Python 类。"),
            ("forward", "定义输入张量怎样变成输出张量。", "误以为需要手动调用 `forward()`。"),
            ("criterion", "损失函数对象，负责把预测和标签变成标量 loss。", "把它和优化器混淆。"),
            ("optimizer", "读取参数梯度并更新参数的对象。", "以为它会自动计算梯度。"),
        ],
        [
            ("标准 PyTorch 线性回归骨架", """import torch
from torch import nn

x_data = torch.tensor([[1.0], [2.0], [3.0]])
y_data = torch.tensor([[2.0], [4.0], [6.0]])

class LinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

model = LinearModel()
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)"""),
            ("训练循环：每行都有状态变化", """for epoch in range(100):
    y_pred = model(x_data)
    loss = criterion(y_pred, y_data)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()"""),
            ("预测阶段：不建梯度图", """model.eval()
with torch.no_grad():
    x_test = torch.tensor([[4.0]])
    y_test = model(x_test)
    print(y_test.item())"""),
        ],
        [
            ("把层写成局部变量", "优化器可能找不到参数。", "在 `__init__` 中写成 `self.linear = ...`。"),
            ("输入形状和 `nn.Linear` 不匹配", "前向时会报矩阵乘法形状错误。", "检查最后一维是否等于 `in_features`。"),
            ("手动调用 `model.forward(x)`", "会绕开 `Module.__call__` 的一些机制。", "正常使用 `model(x)`。"),
            ("只 backward 不 step", "梯度有了，但参数没有更新。", "每轮反向后调用 `optimizer.step()`。"),
            ("预测时还在建计算图", "浪费内存，也容易混淆训练/评估。", "使用 `model.eval()` 和 `torch.no_grad()`。"),
        ],
        [
            ("Module", "组织模型和参数", "不是损失函数"),
            ("Loss", "计算训练目标", "不更新参数"),
            ("Optimizer", "根据梯度更新参数", "不负责前向预测"),
        ],
        [
            ("基础概念", "选择", "`nn.Module` 中通常在哪里定义层？", ["__init__", "loss.backward()", "optimizer.step()"], "想想参数要被登记在哪里。"),
            ("基础概念", "判断", "调用 `model(x)` 时会间接执行模型的 `forward`。", None, "判断 PyTorch Module 的调用方式。"),
            ("基础概念", "填空", "`nn.Linear(1, 1)` 中第一个 1 表示输入特征数，第二个 1 表示 ______。", None, "填输出维度。"),
            ("代码阅读", "短答", "为什么 `self.linear = nn.Linear(1, 1)` 要带 `self`？", None, "从参数登记和优化器发现参数回答。"),
            ("代码阅读", "短答", "`optimizer = SGD(model.parameters(), lr=0.01)` 中传入的是什么？", None, "不是 loss，也不是数据。"),
            ("代码阅读", "短答", "`loss.item()` 常用来做什么？", None, "从张量标量转 Python 数字回答。"),
            ("排序", "排序", "排序一次训练 step：forward / criterion / zero_grad / backward / step。", None, "按代码执行顺序写。"),
            ("形状判断", "短答", "为什么线性回归输入常写成 `[N, 1]`，而不是只写 `[N]`？", None, "从 batch 维和特征维回答。"),
            ("错误诊断", "诊断", "模型训练后参数没变化，可能漏了哪一步？", None, "至少提 step 或参数没传给优化器。"),
            ("错误诊断", "诊断", "报错提示矩阵形状不能相乘，你会优先检查什么？", None, "从输入最后一维和 Linear 的 in_features 回答。"),
            ("错误诊断", "诊断", "有人把 `criterion = nn.MSELoss` 少写了括号，会怎样？", None, "说明类和实例的区别。"),
            ("场景应用", "场景", "如果输入从 1 个特征变成 8 个特征，`nn.Linear` 应该怎样改？", None, "写出 `in_features` 的变化。"),
            ("场景应用", "短答", "为什么预测阶段通常不需要 `backward()`？", None, "从不更新参数回答。"),
            ("概念区分", "匹配", "匹配 Module / criterion / optimizer 到：组织参数、计算 loss、更新参数。", None, "按分工写。"),
            ("面试追问", "短答", "为什么 PyTorch 训练代码常被拆成四步？", None, "用数据、模型、损失优化、训练回答。"),
            ("面试追问", "短答", "`model.train()` 和 `model.eval()` 为什么要养成习惯？", None, "提 Dropout 或 BatchNorm。"),
            ("检查清单", "清单", "写 PyTorch 线性回归前，列 5 项检查。", None, "覆盖 shape、Module、loss、optimizer、loop。"),
            ("代码修正", "诊断", "有人在 `backward()` 后立刻 `zero_grad()` 再 `step()`，错在哪？", None, "说清梯度被清掉。"),
            ("费曼解释", "费曼", "用 6-9 句话解释：PyTorch 如何把手写线性回归变成标准训练代码。", None, "串联 Tensor、Module、forward、MSELoss、zero_grad、backward、step。"),
            ("自我检查", "短答", "学完本页后，你现在能做什么？", None, "写一个可执行动作。"),
        ],
    ),
])


if __name__ == "__main__":
    main()
