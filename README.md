## LMC project study repo

Use this repo for study and dev

### 250304更新说明：
本次更新中，完成了执行函数中Action的部分，实现内容如下：

| 函数名称 | 实现功能 |
| --- | --- |
| `gen_set_bus_impl` | 设置发电机与母线的关联，可将发电机连接到指定母线或断开发电机 |
| `load_set_bus_impl` | 设置负荷与母线的关联，可将负荷连接到指定母线或断开负荷 |
| `line_or_set_bus_impl` | 设置输电线路的电流输入端与母线的关联 |
| `line_ex_set_bus_impl` | 设置输电线路的电流输出端与母线的关联 |
| `storage_set_bus_impl` | 设置储能设备与母线的关联 |
| `line_set_status_impl` | 设置输电线路的连接状态，可连接或断开指定线路 |
| `redispatch_impl` | 设置发电机的重调度量，调整发电机的发电功率 |
| `cancel_redispatch_impl` | 取消指定发电机的重调度指令，将目标调度值重置为0 |
| `storage_p_impl` | 设置储能单元的充放电功率，正值表示充电，负值表示放电 |
| `curtail_impl` | 设置可再生能源发电机的限电量，控制可再生能源发电机的输出 |

以下是关于Action实现的几点说明：

1. grid2op在bus和line的操作上提供了`change`与`set`两种不同的操作，考虑到组件通常存在两条母线，使用`change`无法精确地设定状态，因此为了统一操作逻辑，bus与line的相关操作将全部通过`set`来进行精确设定。
2. 结合grid2op中对于`redispatch`的说明，本次更新中编写了一个函数`cancel_redispatch_impl`用于取消正处于重调度的发电机组的调度指令。原则上`redispatch`，`storage_p`与`curtail`都是设置一个调控值的setpoint，在不主动取消时，此后的每个时间步都会按照设定值持续生效，但是考虑到三个组件不同的使用方法，此处仅针对`redispatch`编写撤销方法以便后续通过大模型进行控制。
3. 原则上，grid2op环境中的`redispatch`应该作用于非新能源电站，可通过`env.gen_redispatchable`进行验证；`curtail`作用于新能源电站，可通过`env.gen_renewable`进行验证。然而在grid2op中，对新能源电站进行redispatch或对非新能源电站进行`curtail`属于模糊（ambiguous）行为，而非非法(illegal)行为。考虑到方法中本就配置了模糊检测的代码，因此在这两个函数本身的实现中并不对需要操作的电站属性进行验证。后续在编写通过大模型调用的函数时，可酌情添加对约束条件的判定。
